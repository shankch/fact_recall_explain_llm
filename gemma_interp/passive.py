from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from .dataset import FactExample, split_examples
from .metrics import greedy_exact_match, target_margin, token_rank
from .modeling import ModelBundle, run_forward, subject_span, target_token_id, tokenize_prompt
from .utils import ensure_dir, write_json


def _prompt_variants(example: FactExample, max_paraphrases: int) -> list[tuple[str, str]]:
    variants = [("canonical", example.canonical_prompt)]
    variants.extend(("paraphrase", prompt) for prompt in example.paraphrase_prompts[:max_paraphrases])
    variants.extend(("generation", prompt) for prompt in example.generation_prompts[:1])
    return variants


def collect_hidden_state_rows(
    bundle: ModelBundle,
    examples: list[FactExample],
    max_paraphrases: int,
    max_examples: int,
    max_new_tokens: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    prompt_rows: list[dict] = []
    feature_rows: list[dict] = []

    for example in examples[:max_examples]:
        for prompt_kind, prompt in _prompt_variants(example, max_paraphrases):
            outputs = run_forward(bundle, prompt, output_hidden_states=True)
            logits = outputs.logits[0, -1].float().cpu()
            true_id = target_token_id(bundle, example.target_true)
            new_id = target_token_id(bundle, example.target_new)
            subject_start, subject_end = subject_span(bundle, prompt, example.subject)
            prompt_rows.append(
                {
                    "case_id": example.case_id,
                    "split": example.split,
                    "relation_id": example.relation_id,
                    "subject": example.subject,
                    "prompt_kind": prompt_kind,
                    "prompt": prompt,
                    "target_true": example.target_true,
                    "target_new": example.target_new,
                    "target_token_id": true_id,
                    "target_rank": token_rank(logits, true_id),
                    "target_margin": target_margin(logits, true_id, new_id),
                    "exact_match": greedy_exact_match(bundle, prompt, example.target_true, max_new_tokens=max_new_tokens),
                    "subject_start": subject_start,
                    "subject_end": subject_end,
                    "top_prediction": bundle.tokenizer.decode([int(torch.argmax(logits).item())]).strip(),
                }
            )

            for layer_idx, hidden in enumerate(outputs.hidden_states[1:]):
                hidden_cpu = hidden[0].detach().float().cpu()
                final_vec = hidden_cpu[-1]
                subject_vec = hidden_cpu[subject_end] if subject_end >= 0 else hidden_cpu[-1]
                feature_rows.append(
                    {
                        "case_id": example.case_id,
                        "relation_id": example.relation_id,
                        "split": example.split,
                        "prompt_kind": prompt_kind,
                        "target_token_id": true_id,
                        "layer": layer_idx,
                        "position": "final",
                        "vector": final_vec.numpy().tolist(),
                    }
                )
                feature_rows.append(
                    {
                        "case_id": example.case_id,
                        "relation_id": example.relation_id,
                        "split": example.split,
                        "prompt_kind": prompt_kind,
                        "target_token_id": true_id,
                        "layer": layer_idx,
                        "position": "subject",
                        "vector": subject_vec.numpy().tolist(),
                    }
                )

    return pd.DataFrame(prompt_rows), pd.DataFrame(feature_rows)


def _probe_accuracy(feature_df: pd.DataFrame, label_key: str) -> pd.DataFrame:
    rows: list[dict] = []
    train_df = feature_df[(feature_df["split"] == "dev") & (feature_df["prompt_kind"] == "canonical") & (feature_df["position"] == "final")]
    eval_df = feature_df[(feature_df["split"] == "eval") & (feature_df["prompt_kind"] == "canonical") & (feature_df["position"] == "final")]
    if train_df.empty or eval_df.empty:
        return pd.DataFrame(rows)

    for layer, layer_train in train_df.groupby("layer"):
        layer_eval = eval_df[eval_df["layer"] == layer]
        if layer_eval.empty:
            continue
        y_train = layer_train[label_key]
        y_eval = layer_eval[label_key]
        if len(set(y_train)) < 2 or len(set(y_eval)) < 2:
            continue
        x_train = np.stack(layer_train["vector"].map(np.array))
        x_eval = np.stack(layer_eval["vector"].map(np.array))
        clf = LogisticRegression(max_iter=500, multi_class="auto")
        clf.fit(x_train, y_train)
        preds = clf.predict(x_eval)
        rows.append({"layer": layer, "label": label_key, "accuracy": accuracy_score(y_eval, preds)})
    return pd.DataFrame(rows)


def _salience_rows(bundle: ModelBundle, examples: list[FactExample], max_examples: int) -> pd.DataFrame:
    rows: list[dict] = []
    for example in examples[:max_examples]:
        handles = []
        captures: dict[int, torch.Tensor] = {}

        for layer_idx, layer in enumerate(bundle.model.model.layers):
            def save_output(_module, _inputs, output, idx=layer_idx):
                tensor = output[0] if isinstance(output, tuple) else output
                tensor.retain_grad()
                captures[idx] = tensor

            handles.append(layer.register_forward_hook(save_output))

        inputs = tokenize_prompt(bundle, example.canonical_prompt)
        outputs = bundle.model(**inputs)
        target_id = target_token_id(bundle, example.target_true)
        loss = outputs.logits[0, -1, target_id]
        bundle.model.zero_grad(set_to_none=True)
        loss.backward()

        for layer_idx, tensor in captures.items():
            grad = tensor.grad[0, -1].detach().float().cpu()
            rows.append(
                {
                    "case_id": example.case_id,
                    "relation_id": example.relation_id,
                    "layer": layer_idx,
                    "salience_norm": float(torch.norm(grad).item()),
                }
            )

        for handle in handles:
            handle.remove()

    return pd.DataFrame(rows)


def _similarity_rows(feature_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    canonical = feature_df[(feature_df["prompt_kind"] == "canonical") & (feature_df["position"] == "final")]
    paraphrase = feature_df[(feature_df["prompt_kind"] == "paraphrase") & (feature_df["position"] == "final")]
    for (case_id, layer), base_row in canonical.groupby(["case_id", "layer"]):
        para_rows = paraphrase[(paraphrase["case_id"] == case_id) & (paraphrase["layer"] == layer)]
        if para_rows.empty:
            continue
        base_vec = np.stack(base_row["vector"].map(np.array)).mean(axis=0)
        base_norm = np.linalg.norm(base_vec)
        for _, para_row in para_rows.iterrows():
            para_vec = np.array(para_row["vector"])
            similarity = float(np.dot(base_vec, para_vec) / ((base_norm * np.linalg.norm(para_vec)) + 1e-8))
            rows.append({"case_id": case_id, "layer": layer, "cosine_similarity": similarity})
    return pd.DataFrame(rows)


def run_passive_analysis(
    bundle: ModelBundle,
    examples: list[FactExample],
    output_dir: str | Path,
    max_examples: int,
    max_paraphrases: int,
    max_salience_examples: int,
    max_new_tokens: int,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    prompt_df, feature_df = collect_hidden_state_rows(
        bundle=bundle,
        examples=examples,
        max_paraphrases=max_paraphrases,
        max_examples=max_examples,
        max_new_tokens=max_new_tokens,
    )

    probe_relation_df = _probe_accuracy(feature_df, "relation_id")
    probe_target_df = _probe_accuracy(feature_df, "target_token_id")
    probe_df = pd.concat([probe_relation_df, probe_target_df], ignore_index=True)
    salience_df = _salience_rows(bundle, examples, max_salience_examples)
    similarity_df = _similarity_rows(feature_df)

    prompt_csv = output_path / "prompt_metrics.csv"
    feature_jsonl = output_path / "hidden_features.jsonl"
    probe_csv = output_path / "probe_results.csv"
    salience_csv = output_path / "salience.csv"
    similarity_csv = output_path / "paraphrase_similarity.csv"

    prompt_df.to_csv(prompt_csv, index=False)
    feature_df.to_json(feature_jsonl, orient="records", lines=True)
    probe_df.to_csv(probe_csv, index=False)
    salience_df.to_csv(salience_csv, index=False)
    similarity_df.to_csv(similarity_csv, index=False)

    summary = {
        "prompt_metrics_path": str(prompt_csv),
        "hidden_features_path": str(feature_jsonl),
        "probe_results_path": str(probe_csv),
        "salience_path": str(salience_csv),
        "similarity_path": str(similarity_csv),
        "mean_target_rank": float(prompt_df["target_rank"].mean()) if not prompt_df.empty else None,
        "mean_exact_match": float(prompt_df["exact_match"].mean()) if not prompt_df.empty else None,
    }
    write_json(output_path / "summary.json", summary)
    return {key: str(value) for key, value in summary.items() if key.endswith("_path")}
