from __future__ import annotations

from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from difflib import SequenceMatcher
from math import comb
from pathlib import Path
from typing import Iterator
import gc
import itertools
import json
import re
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch

from .modeling import ModelBundle, load_model_bundle, target_token_id, tokenize_prompt
from .utils import ensure_dir, set_seed, write_json, write_jsonl


PROMPT_FAMILIES = ["raw_question", "declarative", "qa", "chat_template"]


@dataclass(frozen=True)
class RelationSpec:
    label: str
    question: str
    declarative: str
    chat_instruction: str


RELATION_SPECS = {
    "capital": RelationSpec(
        label="capital",
        question="What is the capital of {subject}?",
        declarative="The capital of {subject} is",
        chat_instruction="What is the capital of {subject}? Answer with only the capital city.",
    ),
    "official_language": RelationSpec(
        label="official language",
        question="What is an official language of {subject}?",
        declarative="An official language of {subject} is",
        chat_instruction="What is an official language of {subject}? Answer with only one language.",
    ),
    "currency": RelationSpec(
        label="currency",
        question="What is the currency of {subject}?",
        declarative="The currency of {subject} is",
        chat_instruction="What is the currency of {subject}? Answer with only the currency name.",
    ),
    "headquarters": RelationSpec(
        label="headquarters",
        question="Where is the headquarters of {subject}?",
        declarative="The headquarters of {subject} is in",
        chat_instruction="Where is the headquarters of {subject}? Answer with only the city.",
    ),
    "birth_place": RelationSpec(
        label="birth place",
        question="Where was {subject} born?",
        declarative="{subject} was born in",
        chat_instruction="Where was {subject} born? Answer with only the place name.",
    ),
}


COUNTRY_ALIASES = {
    "United States": "USA",
    "United Kingdom": "UK",
    "Czechia": "Czech Republic",
    "Republic of the Congo": "Congo",
}


@dataclass
class ModelSpec:
    name: str
    path: str
    family: str
    variant: str


def _normalize_text(value: str) -> str:
    text = value.lower().strip()
    text = text.replace("\n", " ")
    text = re.sub(r"<\|[^>]+\|>", " ", text)
    text = re.sub(r"[“”\"`]", "", text)
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _token_f1(prediction: str, target: str) -> float:
    pred_tokens = prediction.split()
    target_tokens = target.split()
    if not pred_tokens or not target_tokens:
        return 0.0
    overlap = 0
    remaining = list(target_tokens)
    for token in pred_tokens:
        if token in remaining:
            overlap += 1
            remaining.remove(token)
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(target_tokens)
    return (2 * precision * recall) / (precision + recall)


def score_answer(generated: str, aliases: list[str]) -> dict[str, float | str]:
    normalized_prediction = _normalize_text(generated)
    normalized_aliases = [_normalize_text(alias) for alias in aliases if alias.strip()]
    exact = float(any(normalized_prediction == alias for alias in normalized_aliases))
    contains = float(any(alias in normalized_prediction for alias in normalized_aliases))
    token_f1 = max((_token_f1(normalized_prediction, alias) for alias in normalized_aliases), default=0.0)
    similarity = max((SequenceMatcher(None, normalized_prediction, alias).ratio() for alias in normalized_aliases), default=0.0)
    return {
        "normalized_generated_text": normalized_prediction,
        "full_exact_match": exact,
        "contains_expected": contains,
        "answer_f1": float(token_f1),
        "answer_similarity": float(similarity),
    }


def _score_answer_or_zero(generated: str, aliases: list[str] | None) -> dict[str, float]:
    if not aliases:
        return {
            "full_exact_match": 0.0,
            "contains_expected": 0.0,
            "answer_f1": 0.0,
            "answer_similarity": 0.0,
        }
    scores = score_answer(generated, list(aliases))
    return {
        "full_exact_match": float(scores["full_exact_match"]),
        "contains_expected": float(scores["contains_expected"]),
        "answer_f1": float(scores["answer_f1"]),
        "answer_similarity": float(scores["answer_similarity"]),
    }


def _strip_leading_answer_prefix(text: str, row: dict) -> str:
    normalized = _normalize_text(text)
    subject = _normalize_text(row["subject"])
    relation = row["relation"]
    prefixes = [
        _normalize_text(RELATION_SPECS[relation].declarative.format(subject=row["subject"])),
        _normalize_text("Q: " + RELATION_SPECS[relation].question.format(subject=row["subject"]) + " A:"),
        _normalize_text("A"),
        _normalize_text("Answer"),
        _normalize_text("Assistant"),
        _normalize_text(f"User {RELATION_SPECS[relation].chat_instruction.format(subject=row['subject'])} Assistant"),
    ]
    if relation == "birth_place":
        prefixes.append(_normalize_text(f"{row['subject']} was born in"))
    for prefix in prefixes:
        if prefix and normalized.startswith(prefix):
            normalized = normalized[len(prefix) :].strip()
    normalized = re.sub(r"^[\-\:\.\s]+", "", normalized).strip()
    return normalized


def _best_target_token_metrics(bundle: ModelBundle, logits: torch.Tensor, aliases: list[str]) -> tuple[int, float]:
    alias_ids = []
    for alias in aliases:
        try:
            alias_ids.append(target_token_id(bundle, alias))
        except ValueError:
            continue
    if not alias_ids:
        raise ValueError("No tokenizable aliases were found for target answer.")
    alias_ids = sorted(set(alias_ids))
    ordered = torch.argsort(logits, descending=True).tolist()
    best_alias_id = max(alias_ids, key=lambda token_id: float(logits[token_id].item()))
    best_rank = min(ordered.index(token_id) + 1 for token_id in alias_ids)
    best_other_id = next(token_id for token_id in ordered if token_id not in alias_ids)
    margin = float(logits[best_alias_id].item() - logits[best_other_id].item())
    return best_rank, margin


def _control_metrics(normalized_prediction: str, row: dict, target_metrics: dict[str, float | str]) -> dict[str, float | str]:
    control_aliases = {
        "same_subject_control": row.get("same_subject_control_aliases", []),
        "same_relation_control": row.get("same_relation_control_aliases", []),
        "lexical_distractor": row.get("lexical_distractor_aliases", []),
    }
    metrics: dict[str, float | str] = {}
    leader = "none"
    leader_tuple = (0.0, 0.0, 0.0)

    for prefix, aliases in control_aliases.items():
        scores = _score_answer_or_zero(normalized_prediction, aliases)
        metrics[f"{prefix}_exact"] = scores["full_exact_match"]
        metrics[f"{prefix}_contains"] = scores["contains_expected"]
        metrics[f"{prefix}_f1"] = scores["answer_f1"]
        metrics[f"{prefix}_similarity"] = scores["answer_similarity"]
        score_tuple = (
            scores["answer_f1"],
            scores["contains_expected"],
            scores["answer_similarity"],
        )
        if score_tuple > leader_tuple:
            leader = prefix
            leader_tuple = score_tuple

    max_control_f1 = max(
        float(metrics["same_subject_control_f1"]),
        float(metrics["same_relation_control_f1"]),
        float(metrics["lexical_distractor_f1"]),
    )
    max_control_contains = max(
        float(metrics["same_subject_control_contains"]),
        float(metrics["same_relation_control_contains"]),
        float(metrics["lexical_distractor_contains"]),
    )
    metrics["max_control_f1"] = max_control_f1
    metrics["max_control_contains"] = max_control_contains
    metrics["target_selectivity"] = float(target_metrics["answer_f1"]) - max_control_f1
    metrics["target_contains_selectivity"] = float(target_metrics["contains_expected"]) - max_control_contains
    metrics["dominant_control"] = leader if leader_tuple[0] > 0.0 else "none"
    return metrics


def _decoder_layers(bundle: ModelBundle):
    return bundle.model.model.layers


def _render_prompt_text(subject: str, relation: str, family: str) -> str:
    spec = RELATION_SPECS[relation]
    if family == "raw_question":
        return spec.question.format(subject=subject)
    if family == "declarative":
        return spec.declarative.format(subject=subject)
    if family == "qa":
        return f"Q: {spec.question.format(subject=subject)}\nA:"
    if family == "chat_template":
        return spec.chat_instruction.format(subject=subject)
    raise ValueError(f"Unknown prompt family: {family}")


def render_model_input(tokenizer, row: dict) -> str:
    prompt = _render_prompt_text(row["subject"], row["relation"], row["prompt_family"])
    if row["prompt_family"] != "chat_template":
        return prompt
    if hasattr(tokenizer, "apply_chat_template"):
        try:
            return tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception:
            pass
    return f"User: {prompt}\nAssistant:"


def _fetch_restcountries_payload() -> list[dict]:
    url = "https://restcountries.com/v3.1/all?fields=name,capital,languages,currencies,independent,unMember"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def _load_seed_facts(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _country_facts(country_payload: list[dict], relation: str) -> list[dict]:
    rows = []
    for item in country_payload:
        common_name = item.get("name", {}).get("common")
        if not common_name or not item.get("independent") or not item.get("unMember"):
            continue
        subject = COUNTRY_ALIASES.get(common_name, common_name)
        if relation == "capital":
            aliases = [value for value in item.get("capital", []) if value]
        elif relation == "official_language":
            aliases = sorted({value for value in (item.get("languages") or {}).values() if value})
        elif relation == "currency":
            aliases = sorted(
                {
                    value.get("name")
                    for value in (item.get("currencies") or {}).values()
                    if isinstance(value, dict) and value.get("name")
                }
            )
        else:
            aliases = []
        if not aliases:
            continue
        rows.append({"subject": subject, "object": aliases[0], "aliases": aliases})
    rows.sort(key=lambda row: row["subject"])
    return rows


def build_multirelation_benchmark(
    output_dir: str | Path,
    limit_per_relation: int = 8,
    families: list[str] | None = None,
    relations: list[str] | None = None,
    country_payload: list[dict] | None = None,
    seed_facts_path: str | Path = "data/factual_seed.json",
) -> Path:
    if families is None:
        families = list(PROMPT_FAMILIES)
    if relations is None:
        relations = list(RELATION_SPECS)

    output_path = ensure_dir(output_dir)
    if country_payload is None:
        country_payload = _fetch_restcountries_payload()
    write_json(output_path / "restcountries_snapshot.json", country_payload)
    seed_facts = _load_seed_facts(seed_facts_path)
    write_json(output_path / "seed_facts_snapshot.json", seed_facts)

    base_facts: list[dict] = []
    for relation in relations:
        if relation in {"capital", "official_language", "currency"}:
            candidates = _country_facts(country_payload, relation)
        else:
            candidates = list(seed_facts[relation])
            candidates.sort(key=lambda row: row["subject"])
        chosen = candidates[:limit_per_relation]
        split_cutoff = max(1, int(len(chosen) * 0.8))
        for idx, row in enumerate(chosen):
            base_facts.append(
                {
                    "fact_id": f"{relation}:{idx}",
                    "relation": relation,
                    "relation_label": RELATION_SPECS[relation].label,
                    "subject": row["subject"],
                    "object": row["object"],
                    "answer_aliases": list(dict.fromkeys(row.get("aliases", [row["object"]]))),
                    "split": "analysis" if idx < split_cutoff else "holdout",
                }
            )

    by_subject: dict[str, list[dict]] = {}
    by_relation: dict[str, list[dict]] = {}
    for fact in base_facts:
        by_subject.setdefault(fact["subject"], []).append(fact)
        by_relation.setdefault(fact["relation"], []).append(fact)
    fact_lookup = {fact["fact_id"]: fact for fact in base_facts}

    expanded_rows = []
    for fact in base_facts:
        same_subject = next(
            (candidate for candidate in by_subject[fact["subject"]] if candidate["relation"] != fact["relation"]),
            None,
        )
        same_relation = next(
            (candidate for candidate in by_relation[fact["relation"]] if candidate["subject"] != fact["subject"]),
            None,
        )
        distractor_fact = next(
            (
                candidate
                for candidate in by_relation[fact["relation"]]
                if candidate["subject"] != fact["subject"] and candidate["object"][0].lower() == fact["object"][0].lower()
            ),
            None,
        )
        if distractor_fact is None:
            distractor_fact = next(
                (candidate for candidate in by_relation[fact["relation"]] if candidate["subject"] != fact["subject"]),
                None,
            )
        if distractor_fact is None and same_relation is not None:
            distractor_fact = fact_lookup.get(same_relation["fact_id"])
        for family in families:
            prompt = _render_prompt_text(fact["subject"], fact["relation"], family)
            expanded = dict(fact)
            expanded["prompt_family"] = family
            expanded["prompt"] = prompt
            expanded["same_subject_control_fact_id"] = same_subject["fact_id"] if same_subject else None
            expanded["same_subject_control_answer"] = same_subject["object"] if same_subject else None
            expanded["same_subject_control_aliases"] = same_subject["answer_aliases"] if same_subject else []
            expanded["same_relation_control_fact_id"] = same_relation["fact_id"] if same_relation else None
            expanded["same_relation_control_answer"] = same_relation["object"] if same_relation else None
            expanded["same_relation_control_aliases"] = same_relation["answer_aliases"] if same_relation else []
            expanded["lexical_distractor"] = distractor_fact["object"] if distractor_fact else None
            expanded["lexical_distractor_aliases"] = distractor_fact["answer_aliases"] if distractor_fact else []
            expanded_rows.append(expanded)

    path = output_path / "multirelation_prompt_benchmark.jsonl"
    write_jsonl(path, expanded_rows)
    return path


def _token_repr(bundle: ModelBundle, token_id: int) -> str:
    decoded = bundle.tokenizer.decode([int(token_id)], clean_up_tokenization_spaces=False)
    if decoded and decoded.strip():
        return decoded.strip()
    raw = bundle.tokenizer.convert_ids_to_tokens(int(token_id))
    return raw if raw is not None else f"<token:{token_id}>"


def _top_tokens(bundle: ModelBundle, logits: torch.Tensor, k: int = 5) -> list[dict]:
    values, ids = torch.topk(logits, k=k)
    rows = []
    for score, token_id in zip(values.tolist(), ids.tolist()):
        rows.append({"token_id": int(token_id), "token": _token_repr(bundle, int(token_id)), "logit": float(score)})
    return rows


def _hook_prompt(bundle: ModelBundle, prompt: str) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], any]:
    attn_outputs: dict[int, np.ndarray] = {}
    mlp_outputs: dict[int, np.ndarray] = {}
    handles = []

    for layer_idx, layer in enumerate(_decoder_layers(bundle)):
        def save_attn(_module, _inputs, output, idx=layer_idx):
            tensor = output[0] if isinstance(output, tuple) else output
            attn_outputs[idx] = tensor[0, -1].detach().float().cpu().numpy()

        def save_mlp(_module, _inputs, output, idx=layer_idx):
            mlp_outputs[idx] = output[0, -1].detach().float().cpu().numpy()

        handles.append(layer.self_attn.register_forward_hook(save_attn))
        handles.append(layer.mlp.act_fn.register_forward_hook(save_mlp))

    inputs = tokenize_prompt(bundle, prompt)
    with torch.no_grad():
        outputs = bundle.model(**inputs, output_hidden_states=True)

    for handle in handles:
        handle.remove()
    return attn_outputs, mlp_outputs, outputs


def analyze_factual_prompt(
    bundle: ModelBundle,
    row: dict,
    max_new_tokens: int = 10,
    top_neurons: int = 24,
) -> dict:
    actual_input = render_model_input(bundle.tokenizer, row)
    attn_outputs, mlp_outputs, outputs = _hook_prompt(bundle, actual_input)
    logits = outputs.logits[0, -1].float().cpu()
    top_prediction_id = int(torch.argmax(logits).item())
    best_rank, margin = _best_target_token_metrics(bundle, logits, row["answer_aliases"])

    hidden_norms = [float(torch.norm(hidden[0, -1].detach().float().cpu()).item()) for hidden in outputs.hidden_states[1:]]
    attn_norms = [float(np.linalg.norm(attn_outputs[layer])) for layer in sorted(attn_outputs)]
    mlp_mean_abs = [float(np.abs(mlp_outputs[layer]).mean()) for layer in sorted(mlp_outputs)]

    flat = []
    for layer_idx, values in mlp_outputs.items():
        for neuron_idx, value in enumerate(values):
            flat.append((layer_idx, neuron_idx, float(value)))
    flat.sort(key=lambda item: abs(item[2]), reverse=True)
    top_neuron_rows = [
        {"layer": layer_idx, "neuron": neuron_idx, "activation": activation}
        for layer_idx, neuron_idx, activation in flat[:top_neurons]
    ]

    prompt_tokens = tokenize_prompt(bundle, actual_input)["input_ids"]
    with torch.no_grad():
        generated_ids = bundle.model.generate(
            **tokenize_prompt(bundle, actual_input),
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    generated_text = bundle.tokenizer.decode(
        generated_ids[0][prompt_tokens.shape[1] :],
        skip_special_tokens=True,
    ).strip()
    normalized_generated = _strip_leading_answer_prefix(generated_text, row)
    answer_metrics = score_answer(normalized_generated, row["answer_aliases"])
    control_metrics = _control_metrics(normalized_generated, row, answer_metrics)

    return {
        "fact_id": row["fact_id"],
        "relation": row["relation"],
        "subject": row["subject"],
        "expected_answer": row["object"],
        "answer_aliases": row["answer_aliases"],
        "prompt_family": row["prompt_family"],
        "prompt": row["prompt"],
        "model_input": actual_input,
        "split": row["split"],
        "same_subject_control_fact_id": row.get("same_subject_control_fact_id"),
        "same_subject_control_answer": row.get("same_subject_control_answer"),
        "same_relation_control_fact_id": row.get("same_relation_control_fact_id"),
        "same_relation_control_answer": row.get("same_relation_control_answer"),
        "lexical_distractor": row.get("lexical_distractor"),
        "target_rank": best_rank,
        "target_margin": margin,
        "top_prediction": _token_repr(bundle, top_prediction_id),
        "top_tokens": _top_tokens(bundle, logits),
        "generated_text": generated_text,
        "layer_hidden_norms": hidden_norms,
        "layer_attention_norms": attn_norms,
        "layer_mlp_mean_abs": mlp_mean_abs,
        "top_neurons": top_neuron_rows,
        "mlp_activations": {str(layer): values.tolist() for layer, values in mlp_outputs.items()},
        **answer_metrics,
        **control_metrics,
    }


def _bootstrap_interval(values: np.ndarray, samples: int, seed: int) -> tuple[float, float, float]:
    if values.size == 0:
        return (0.0, 0.0, 0.0)
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(samples):
        sample = rng.choice(values, size=values.size, replace=True)
        draws.append(float(sample.mean()))
    draws = np.array(draws)
    return (float(values.mean()), float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975)))


def _sign_test_pvalue(diffs: np.ndarray) -> float:
    non_zero = diffs[np.abs(diffs) > 1e-12]
    n = non_zero.size
    if n == 0:
        return 1.0
    positive = int((non_zero > 0).sum())
    cutoff = min(positive, n - positive)
    probability = sum(comb(n, k) for k in range(0, cutoff + 1)) / (2 ** n)
    return float(min(1.0, 2 * probability))


def _paired_family_comparisons(metrics_df: pd.DataFrame, metric: str, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    for relation, relation_df in metrics_df.groupby("relation"):
        pivot = relation_df.pivot_table(index="fact_id", columns="prompt_family", values=metric, aggfunc="mean")
        for family_a, family_b in itertools.combinations(sorted(pivot.columns.tolist()), 2):
            paired = pivot[[family_a, family_b]].dropna()
            if paired.empty:
                continue
            diffs = (paired[family_b] - paired[family_a]).to_numpy(dtype=float)
            mean_diff, ci_low, ci_high = _bootstrap_interval(diffs, bootstrap_samples, seed)
            rows.append(
                {
                    "relation": relation,
                    "metric": metric,
                    "family_a": family_a,
                    "family_b": family_b,
                    "mean_diff": mean_diff,
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                    "sign_test_pvalue": _sign_test_pvalue(diffs),
                    "num_pairs": int(diffs.size),
                }
            )
    return pd.DataFrame(rows)


def _family_bootstrap_rows(metrics_df: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    for (relation, family), frame in metrics_df.groupby(["relation", "prompt_family"]):
        for metric in ["full_exact_match", "contains_expected", "answer_f1", "answer_similarity"]:
            mean, ci_low, ci_high = _bootstrap_interval(frame[metric].to_numpy(dtype=float), bootstrap_samples, seed)
            rows.append(
                {
                    "relation": relation,
                    "prompt_family": family,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                    "count": int(frame.shape[0]),
                }
            )
    return pd.DataFrame(rows)


def _split_family_summary(metrics_df: pd.DataFrame, split: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    subset = metrics_df[metrics_df["split"] == split].copy()
    if subset.empty:
        subset = metrics_df.copy()
    family_summary = (
        subset.groupby(["relation", "prompt_family"])[
            ["target_rank", "target_margin", "full_exact_match", "contains_expected", "answer_f1", "answer_similarity"]
        ]
        .mean()
        .reset_index()
    )
    overall_summary = (
        subset.groupby("prompt_family")[
            ["target_rank", "target_margin", "full_exact_match", "contains_expected", "answer_f1", "answer_similarity"]
        ]
        .mean()
        .reset_index()
    )
    return family_summary, overall_summary


def _split_control_summary(metrics_df: pd.DataFrame, split: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    subset = metrics_df[metrics_df["split"] == split].copy()
    if subset.empty:
        subset = metrics_df.copy()
    family_summary = (
        subset.groupby(["relation", "prompt_family"])[
            [
                "answer_f1",
                "target_selectivity",
                "same_subject_control_f1",
                "same_relation_control_f1",
                "lexical_distractor_f1",
                "max_control_f1",
            ]
        ]
        .mean()
        .reset_index()
    )
    overall_summary = (
        subset.groupby("prompt_family")[
            [
                "answer_f1",
                "target_selectivity",
                "same_subject_control_f1",
                "same_relation_control_f1",
                "lexical_distractor_f1",
                "max_control_f1",
            ]
        ]
        .mean()
        .reset_index()
    )
    return family_summary, overall_summary


def _paired_metric_between_families(
    metrics_df: pd.DataFrame,
    split: str,
    metric: str,
    family_a: str,
    family_b: str,
    bootstrap_samples: int,
    seed: int,
) -> dict[str, float | int | str]:
    subset = metrics_df[metrics_df["split"] == split].copy()
    if subset.empty:
        subset = metrics_df.copy()
    paired = (
        subset.pivot_table(index="fact_id", columns="prompt_family", values=metric, aggfunc="mean")[[family_a, family_b]]
        .dropna()
    )
    diffs = (paired[family_b] - paired[family_a]).to_numpy(dtype=float)
    mean_diff, ci_low, ci_high = _bootstrap_interval(diffs, bootstrap_samples, seed)
    return {
        "split": split,
        "metric": metric,
        "family_a": family_a,
        "family_b": family_b,
        "mean_diff": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "sign_test_pvalue": _sign_test_pvalue(diffs),
        "num_pairs": int(diffs.size),
    }


def _holdout_selection_summary(metrics_df: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    analysis_df = metrics_df[metrics_df["split"] == "analysis"].copy()
    holdout_df = metrics_df[metrics_df["split"] == "holdout"].copy()
    if analysis_df.empty:
        analysis_df = metrics_df.copy()
    if holdout_df.empty:
        holdout_df = metrics_df.copy()

    analysis_means = (
        analysis_df.groupby("prompt_family")[["answer_f1", "target_selectivity"]]
        .mean()
        .sort_values(["answer_f1", "target_selectivity"], ascending=False)
    )
    best_answer_family = str(analysis_means.index[0])
    worst_answer_family = str(analysis_means.sort_values(["answer_f1", "target_selectivity"], ascending=True).index[0])
    best_selectivity_family = str(
        analysis_df.groupby("prompt_family")["target_selectivity"].mean().sort_values(ascending=False).index[0]
    )
    holdout_means = holdout_df.groupby("prompt_family")[["answer_f1", "target_selectivity"]].mean()

    answer_diff = _paired_metric_between_families(
        metrics_df,
        split="holdout",
        metric="answer_f1",
        family_a=worst_answer_family,
        family_b=best_answer_family,
        bootstrap_samples=bootstrap_samples,
        seed=seed,
    )
    selectivity_diff = _paired_metric_between_families(
        metrics_df,
        split="holdout",
        metric="target_selectivity",
        family_a=worst_answer_family,
        family_b=best_answer_family,
        bootstrap_samples=bootstrap_samples,
        seed=seed,
    )
    return pd.DataFrame(
        [
            {
                "analysis_best_answer_family": best_answer_family,
                "analysis_best_selectivity_family": best_selectivity_family,
                "analysis_worst_answer_family": worst_answer_family,
                "selection_agrees": int(best_answer_family == best_selectivity_family),
                "holdout_best_answer_f1": float(holdout_means.loc[best_answer_family, "answer_f1"]),
                "holdout_best_target_selectivity": float(holdout_means.loc[best_answer_family, "target_selectivity"]),
                "holdout_worst_answer_f1": float(holdout_means.loc[worst_answer_family, "answer_f1"]),
                "holdout_worst_target_selectivity": float(holdout_means.loc[worst_answer_family, "target_selectivity"]),
                "holdout_answer_f1_diff": float(answer_diff["mean_diff"]),
                "holdout_answer_f1_ci_low": float(answer_diff["ci_low"]),
                "holdout_answer_f1_ci_high": float(answer_diff["ci_high"]),
                "holdout_answer_f1_sign_test_pvalue": float(answer_diff["sign_test_pvalue"]),
                "holdout_answer_f1_num_pairs": int(answer_diff["num_pairs"]),
                "holdout_target_selectivity_diff": float(selectivity_diff["mean_diff"]),
                "holdout_target_selectivity_ci_low": float(selectivity_diff["ci_low"]),
                "holdout_target_selectivity_ci_high": float(selectivity_diff["ci_high"]),
                "holdout_target_selectivity_sign_test_pvalue": float(selectivity_diff["sign_test_pvalue"]),
                "holdout_target_selectivity_num_pairs": int(selectivity_diff["num_pairs"]),
            }
        ]
    )


@contextmanager
def zero_mlp_neurons(bundle: ModelBundle, selected: list[tuple[int, int]]) -> Iterator[None]:
    grouped: dict[int, list[int]] = {}
    for layer_idx, neuron_idx in selected:
        grouped.setdefault(int(layer_idx), []).append(int(neuron_idx))
    handles = []

    for layer_idx, neuron_indices in grouped.items():
        layer = _decoder_layers(bundle)[layer_idx]

        def hook(_module, _inputs, output, indices=tuple(sorted(set(neuron_indices)))):
            output = output.clone()
            output[..., list(indices)] = 0
            return output

        handles.append(layer.mlp.act_fn.register_forward_hook(hook))
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


def _evaluate_prompt_fast(bundle: ModelBundle, row: dict, max_new_tokens: int, selected_neurons: list[tuple[int, int]] | None = None) -> dict:
    actual_input = render_model_input(bundle.tokenizer, row)
    context = zero_mlp_neurons(bundle, selected_neurons) if selected_neurons else nullcontext()
    with context:
        prompt_tokens = tokenize_prompt(bundle, actual_input)["input_ids"]
        with torch.no_grad():
            outputs = bundle.model(**tokenize_prompt(bundle, actual_input))
            generated_ids = bundle.model.generate(
                **tokenize_prompt(bundle, actual_input),
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )
    logits = outputs.logits[0, -1].float().cpu()
    rank, margin = _best_target_token_metrics(bundle, logits, row["answer_aliases"])
    generated_text = bundle.tokenizer.decode(generated_ids[0][prompt_tokens.shape[1] :], skip_special_tokens=True).strip()
    normalized_generated = _strip_leading_answer_prefix(generated_text, row)
    answer_metrics = score_answer(normalized_generated, row["answer_aliases"])
    return {
        "target_rank": rank,
        "target_margin": margin,
        **answer_metrics,
        **_control_metrics(normalized_generated, row, answer_metrics),
    }


def _neuron_scores(mlp_tensor: np.ndarray, families: list[str], prompt_families: list[str]) -> pd.DataFrame:
    family_means = []
    for family in families:
        family_indices = [idx for idx, prompt_family in enumerate(prompt_families) if prompt_family == family]
        family_means.append(mlp_tensor[family_indices].mean(axis=0))
    family_mean_tensor = np.stack(family_means)
    mean_abs = np.abs(mlp_tensor).mean(axis=0)
    overall_std = mlp_tensor.std(axis=0)
    family_mean_std = family_mean_tensor.std(axis=0)

    rows = []
    for layer_idx in range(mean_abs.shape[0]):
        for neuron_idx in range(mean_abs.shape[1]):
            mean_abs_value = float(mean_abs[layer_idx, neuron_idx])
            overall_std_value = float(overall_std[layer_idx, neuron_idx])
            family_std_value = float(family_mean_std[layer_idx, neuron_idx])
            sharedness = mean_abs_value / (overall_std_value + 1e-6)
            sensitivity = family_std_value / (mean_abs_value + 1e-6)
            rows.append(
                {
                    "layer": layer_idx,
                    "neuron": neuron_idx,
                    "mean_abs_activation": mean_abs_value,
                    "activation_std": overall_std_value,
                    "family_mean_std": family_std_value,
                    "sharedness": float(sharedness),
                    "family_sensitivity": float(sensitivity),
                    "invariance_score": float(sharedness / (1.0 + sensitivity)),
                    "prompt_sensitive_score": float(family_std_value * mean_abs_value),
                }
            )
    return pd.DataFrame(rows)


def _model_report(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    summary = json.loads((output_path / "summary.json").read_text(encoding="utf-8"))
    family_summary = pd.read_csv(output_path / "holdout_family_summary.csv")
    control_summary = pd.read_csv(output_path / "holdout_overall_control_summary.csv")
    selection_summary = pd.read_csv(output_path / "holdout_family_selection_summary.csv")
    ablation_summary = pd.read_csv(output_path / "neuron_ablation_summary.csv")
    selectivity_comparisons = pd.read_csv(output_path / "paired_selectivity_comparisons.csv")
    invariant = pd.read_csv(output_path / "top_invariant_neurons.csv").head(8)
    sensitive = pd.read_csv(output_path / "top_prompt_sensitive_neurons.csv").head(8)

    def markdown_table(frame: pd.DataFrame) -> str:
        columns = list(frame.columns)
        lines = [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |",
        ]
        for row in frame.itertuples(index=False):
            lines.append("| " + " | ".join(str(value) for value in row) + " |")
        return "\n".join(lines)

    lines = [
        f"# Prompt Invariance Report: {summary['model_name']}",
        "",
        f"- Prompts analyzed: {summary['num_prompts']}",
        f"- Mean answer F1: {summary['mean_answer_f1']:.4f}",
        f"- Analysis-selected best family: {selection_summary.iloc[0]['analysis_best_answer_family']}",
        f"- Analysis-selected best selectivity family: {selection_summary.iloc[0]['analysis_best_selectivity_family']}",
        "",
        "## Holdout Family Summary",
        "",
        markdown_table(family_summary.round(4)),
        "",
        "## Control Selectivity Summary",
        "",
        markdown_table(control_summary.round(4)),
        "",
        "## Top Invariant Neurons",
        "",
        markdown_table(invariant.round(4)),
        "",
        "## Top Prompt-Sensitive Neurons",
        "",
        markdown_table(sensitive.round(4)),
        "",
        "## Strongest Selectivity Comparisons",
        "",
        markdown_table(
            selectivity_comparisons.reindex(selectivity_comparisons["mean_diff"].abs().sort_values(ascending=False).index).head(8).round(4)
        ),
        "",
        "## Neuron Ablation Summary",
        "",
        markdown_table(ablation_summary.round(4)),
    ]
    report_path = output_path / "prompt_invariance_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def run_single_model_prompt_invariance(
    model_spec: ModelSpec,
    benchmark_path: str | Path,
    output_dir: str | Path,
    max_new_tokens: int = 10,
    top_neurons: int = 48,
    ablation_neurons: int = 8,
    bootstrap_samples: int = 200,
    seed: int = 13,
) -> dict[str, str]:
    set_seed(seed)
    output_path = ensure_dir(output_dir)
    bundle = load_model_bundle(model_dir=model_spec.path, seed=seed, require_cuda=False, dtype="auto")

    with Path(benchmark_path).open("r", encoding="utf-8") as handle:
        prompts = [json.loads(line) for line in handle if line.strip()]

    profile_rows = []
    norm_rows = []
    all_mlp = []

    for row in prompts:
        profile = analyze_factual_prompt(bundle, row, max_new_tokens=max_new_tokens, top_neurons=top_neurons)
        profile["model_name"] = model_spec.name
        profile["model_family"] = model_spec.family
        profile["model_variant"] = model_spec.variant
        profile_rows.append(profile)

        mlp_matrix = np.stack([np.array(profile["mlp_activations"][str(layer)]) for layer in range(bundle.model.config.num_hidden_layers)])
        all_mlp.append(mlp_matrix)

        for layer_idx, (hidden_norm, attn_norm, mlp_norm) in enumerate(
            zip(profile["layer_hidden_norms"], profile["layer_attention_norms"], profile["layer_mlp_mean_abs"])
        ):
            norm_rows.append(
                {
                    "model_name": model_spec.name,
                    "fact_id": row["fact_id"],
                    "relation": row["relation"],
                    "prompt_family": row["prompt_family"],
                    "layer": layer_idx,
                    "hidden_norm": hidden_norm,
                    "attention_norm": attn_norm,
                    "mlp_mean_abs": mlp_norm,
                }
            )

    mlp_tensor = np.stack(all_mlp)
    metrics_df = pd.DataFrame(
        [
            {
                "model_name": row["model_name"],
                "model_family": row["model_family"],
                "model_variant": row["model_variant"],
                "fact_id": row["fact_id"],
                "relation": row["relation"],
                "subject": row["subject"],
                "expected_answer": row["expected_answer"],
                "prompt_family": row["prompt_family"],
                "split": row["split"],
                "generated_text": row["generated_text"],
                "normalized_generated_text": row["normalized_generated_text"],
                "top_prediction": row["top_prediction"],
                "target_rank": row["target_rank"],
                "target_margin": row["target_margin"],
                "full_exact_match": row["full_exact_match"],
                "contains_expected": row["contains_expected"],
                "answer_f1": row["answer_f1"],
                "answer_similarity": row["answer_similarity"],
                "same_subject_control_fact_id": row["same_subject_control_fact_id"],
                "same_subject_control_answer": row["same_subject_control_answer"],
                "same_subject_control_f1": row["same_subject_control_f1"],
                "same_subject_control_contains": row["same_subject_control_contains"],
                "same_relation_control_answer": row["same_relation_control_answer"],
                "same_relation_control_fact_id": row["same_relation_control_fact_id"],
                "same_relation_control_f1": row["same_relation_control_f1"],
                "same_relation_control_contains": row["same_relation_control_contains"],
                "lexical_distractor": row["lexical_distractor"],
                "lexical_distractor_f1": row["lexical_distractor_f1"],
                "lexical_distractor_contains": row["lexical_distractor_contains"],
                "max_control_f1": row["max_control_f1"],
                "max_control_contains": row["max_control_contains"],
                "target_selectivity": row["target_selectivity"],
                "target_contains_selectivity": row["target_contains_selectivity"],
                "dominant_control": row["dominant_control"],
            }
            for row in profile_rows
        ]
    )
    norm_df = pd.DataFrame(norm_rows)

    family_summary, overall_family_summary = _split_family_summary(metrics_df, split="analysis")
    holdout_family_summary, holdout_overall_family_summary = _split_family_summary(metrics_df, split="holdout")
    control_summary, overall_control_summary = _split_control_summary(metrics_df, split="analysis")
    holdout_control_summary, holdout_overall_control_summary = _split_control_summary(metrics_df, split="holdout")
    bootstrap_df = _family_bootstrap_rows(metrics_df, bootstrap_samples=bootstrap_samples, seed=seed)
    paired_df = _paired_family_comparisons(metrics_df, metric="answer_f1", bootstrap_samples=bootstrap_samples, seed=seed)
    selectivity_paired_df = _paired_family_comparisons(
        metrics_df,
        metric="target_selectivity",
        bootstrap_samples=bootstrap_samples,
        seed=seed,
    )
    holdout_selection_summary = _holdout_selection_summary(metrics_df, bootstrap_samples=bootstrap_samples, seed=seed)

    analysis_indices = [idx for idx, row in enumerate(profile_rows) if row["split"] == "analysis"]
    analysis_prompt_families = [profile_rows[idx]["prompt_family"] for idx in analysis_indices]
    analysis_mlp_tensor = mlp_tensor[analysis_indices]
    neuron_df = _neuron_scores(
        analysis_mlp_tensor,
        families=sorted(metrics_df["prompt_family"].unique().tolist()),
        prompt_families=analysis_prompt_families,
    )
    invariant_df = neuron_df.sort_values("invariance_score", ascending=False).head(top_neurons)
    sensitive_df = neuron_df.sort_values("prompt_sensitive_score", ascending=False).head(top_neurons)

    holdout_rows = [row for row in prompts if row["split"] == "holdout"]
    invariant_neurons = [(int(row["layer"]), int(row["neuron"])) for row in invariant_df.head(ablation_neurons).to_dict("records")]
    sensitive_neurons = [(int(row["layer"]), int(row["neuron"])) for row in sensitive_df.head(ablation_neurons).to_dict("records")]

    baseline_lookup = {
        (row["fact_id"], row["prompt_family"]): row
        for row in metrics_df.to_dict("records")
    }
    ablation_rows = []
    for candidate_type, selected in [("invariant", invariant_neurons), ("prompt_sensitive", sensitive_neurons)]:
        for row in holdout_rows:
            baseline = baseline_lookup[(row["fact_id"], row["prompt_family"])]
            ablated = _evaluate_prompt_fast(bundle, row, max_new_tokens=max_new_tokens, selected_neurons=selected)
            ablation_rows.append(
                {
                    "model_name": model_spec.name,
                    "relation": row["relation"],
                    "prompt_family": row["prompt_family"],
                    "candidate_type": candidate_type,
                    "fact_id": row["fact_id"],
                    "baseline_answer_f1": baseline["answer_f1"],
                    "ablated_answer_f1": ablated["answer_f1"],
                    "answer_f1_drop": baseline["answer_f1"] - ablated["answer_f1"],
                    "baseline_contains_expected": baseline["contains_expected"],
                    "ablated_contains_expected": ablated["contains_expected"],
                    "contains_drop": baseline["contains_expected"] - ablated["contains_expected"],
                    "baseline_rank": baseline["target_rank"],
                    "ablated_rank": ablated["target_rank"],
                    "baseline_target_selectivity": baseline["target_selectivity"],
                    "ablated_target_selectivity": ablated["target_selectivity"],
                    "target_selectivity_drop": baseline["target_selectivity"] - ablated["target_selectivity"],
                    "same_subject_control_f1_increase": ablated["same_subject_control_f1"] - baseline["same_subject_control_f1"],
                    "same_relation_control_f1_increase": ablated["same_relation_control_f1"] - baseline["same_relation_control_f1"],
                    "lexical_distractor_f1_increase": ablated["lexical_distractor_f1"] - baseline["lexical_distractor_f1"],
                    "max_control_f1_increase": ablated["max_control_f1"] - baseline["max_control_f1"],
                }
            )
    ablation_df = pd.DataFrame(ablation_rows)
    ablation_summary = (
        ablation_df.groupby(["candidate_type", "prompt_family"])[
            [
                "answer_f1_drop",
                "contains_drop",
                "target_selectivity_drop",
                "same_subject_control_f1_increase",
                "same_relation_control_f1_increase",
                "lexical_distractor_f1_increase",
                "max_control_f1_increase",
            ]
        ]
        .mean()
        .reset_index()
        if not ablation_df.empty
        else pd.DataFrame(
            columns=[
                "candidate_type",
                "prompt_family",
                "answer_f1_drop",
                "contains_drop",
                "target_selectivity_drop",
                "same_subject_control_f1_increase",
                "same_relation_control_f1_increase",
                "lexical_distractor_f1_increase",
                "max_control_f1_increase",
            ]
        )
    )

    metrics_path = output_path / "prompt_metrics.csv"
    norms_path = output_path / "layer_component_norms.csv"
    family_summary_path = output_path / "family_summary.csv"
    overall_family_path = output_path / "overall_family_summary.csv"
    holdout_family_summary_path = output_path / "holdout_family_summary.csv"
    holdout_overall_family_path = output_path / "holdout_overall_family_summary.csv"
    control_summary_path = output_path / "control_summary.csv"
    overall_control_path = output_path / "overall_control_summary.csv"
    holdout_control_summary_path = output_path / "holdout_control_summary.csv"
    holdout_overall_control_path = output_path / "holdout_overall_control_summary.csv"
    bootstrap_path = output_path / "bootstrap_summary.csv"
    paired_path = output_path / "paired_family_comparisons.csv"
    selectivity_paired_path = output_path / "paired_selectivity_comparisons.csv"
    holdout_selection_summary_path = output_path / "holdout_family_selection_summary.csv"
    neuron_path = output_path / "neuron_scores.csv"
    invariant_path = output_path / "top_invariant_neurons.csv"
    sensitive_path = output_path / "top_prompt_sensitive_neurons.csv"
    ablation_path = output_path / "neuron_ablation.csv"
    ablation_summary_path = output_path / "neuron_ablation_summary.csv"
    activations_path = output_path / "mlp_activations.npz"
    profiles_path = output_path / "prompt_profiles.jsonl"

    metrics_df.to_csv(metrics_path, index=False)
    norm_df.to_csv(norms_path, index=False)
    family_summary.to_csv(family_summary_path, index=False)
    overall_family_summary.to_csv(overall_family_path, index=False)
    holdout_family_summary.to_csv(holdout_family_summary_path, index=False)
    holdout_overall_family_summary.to_csv(holdout_overall_family_path, index=False)
    control_summary.to_csv(control_summary_path, index=False)
    overall_control_summary.to_csv(overall_control_path, index=False)
    holdout_control_summary.to_csv(holdout_control_summary_path, index=False)
    holdout_overall_control_summary.to_csv(holdout_overall_control_path, index=False)
    bootstrap_df.to_csv(bootstrap_path, index=False)
    paired_df.to_csv(paired_path, index=False)
    selectivity_paired_df.to_csv(selectivity_paired_path, index=False)
    holdout_selection_summary.to_csv(holdout_selection_summary_path, index=False)
    neuron_df.to_csv(neuron_path, index=False)
    invariant_df.to_csv(invariant_path, index=False)
    sensitive_df.to_csv(sensitive_path, index=False)
    ablation_df.to_csv(ablation_path, index=False)
    ablation_summary.to_csv(ablation_summary_path, index=False)
    np.savez_compressed(activations_path, mlp_activations=mlp_tensor)
    write_jsonl(
        profiles_path,
        [{key: value for key, value in row.items() if key != "mlp_activations"} for row in profile_rows],
    )

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 4))
    sns.barplot(data=holdout_overall_family_summary, x="prompt_family", y="answer_f1", color="#bf4d28")
    plt.title(f"{model_spec.name}: holdout answer F1 by prompt family")
    plt.xticks(rotation=20)
    plt.tight_layout()
    family_plot_path = output_path / "answer_f1_by_family.png"
    plt.savefig(family_plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    sns.barplot(data=holdout_overall_control_summary, x="prompt_family", y="target_selectivity", color="#2e6f95")
    plt.title(f"{model_spec.name}: holdout target selectivity by prompt family")
    plt.xticks(rotation=20)
    plt.tight_layout()
    selectivity_plot_path = output_path / "target_selectivity_by_family.png"
    plt.savefig(selectivity_plot_path, dpi=200)
    plt.close()

    relation_pivot = holdout_family_summary.pivot(index="relation", columns="prompt_family", values="answer_f1")
    plt.figure(figsize=(8, 4))
    sns.heatmap(relation_pivot, annot=True, fmt=".2f", cmap="viridis")
    plt.title(f"{model_spec.name}: holdout answer F1 by relation and family")
    plt.tight_layout()
    relation_plot_path = output_path / "answer_f1_relation_heatmap.png"
    plt.savefig(relation_plot_path, dpi=200)
    plt.close()

    if not ablation_summary.empty:
        plt.figure(figsize=(8, 4))
        sns.barplot(data=ablation_summary, x="prompt_family", y="answer_f1_drop", hue="candidate_type")
        plt.title(f"{model_spec.name}: neuron ablation effect")
        plt.xticks(rotation=20)
        plt.tight_layout()
        ablation_plot_path = output_path / "ablation_effects.png"
        plt.savefig(ablation_plot_path, dpi=200)
        plt.close()
    else:
        ablation_plot_path = output_path / "ablation_effects.png"

    summary = {
        "model_name": model_spec.name,
        "model_family": model_spec.family,
        "model_variant": model_spec.variant,
        "num_prompts": int(metrics_df.shape[0]),
        "mean_answer_f1": float(metrics_df["answer_f1"].mean()),
        "mean_contains_expected": float(metrics_df["contains_expected"].mean()),
        "mean_full_exact_match": float(metrics_df["full_exact_match"].mean()),
        "best_prompt_family_by_answer_f1": holdout_selection_summary.iloc[0]["analysis_best_answer_family"],
        "artifacts": {
            "metrics": str(metrics_path),
            "norms": str(norms_path),
            "family_summary": str(family_summary_path),
            "overall_family_summary": str(overall_family_path),
            "holdout_family_summary": str(holdout_family_summary_path),
            "holdout_overall_family_summary": str(holdout_overall_family_path),
            "control_summary": str(control_summary_path),
            "overall_control_summary": str(overall_control_path),
            "holdout_control_summary": str(holdout_control_summary_path),
            "holdout_overall_control_summary": str(holdout_overall_control_path),
            "bootstrap_summary": str(bootstrap_path),
            "paired_family_comparisons": str(paired_path),
            "paired_selectivity_comparisons": str(selectivity_paired_path),
            "holdout_family_selection_summary": str(holdout_selection_summary_path),
            "neuron_scores": str(neuron_path),
            "top_invariant_neurons": str(invariant_path),
            "top_prompt_sensitive_neurons": str(sensitive_path),
            "neuron_ablation": str(ablation_path),
            "neuron_ablation_summary": str(ablation_summary_path),
            "mlp_activations": str(activations_path),
            "profiles": str(profiles_path),
            "answer_f1_by_family_png": str(family_plot_path),
            "target_selectivity_by_family_png": str(selectivity_plot_path),
            "answer_f1_relation_heatmap_png": str(relation_plot_path),
            "ablation_effects_png": str(ablation_plot_path),
        },
    }
    write_json(output_path / "summary.json", summary)
    report_path = _model_report(output_path)
    summary["artifacts"]["report"] = str(report_path)
    write_json(output_path / "summary.json", summary)

    del bundle.model
    del bundle.tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return summary["artifacts"]


def run_multimodel_prompt_invariance(
    model_specs: list[ModelSpec],
    benchmark_path: str | Path,
    output_dir: str | Path,
    max_new_tokens: int = 10,
    top_neurons: int = 48,
    ablation_neurons: int = 8,
    bootstrap_samples: int = 200,
    seed: int = 13,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    model_summaries = []
    for model_spec in model_specs:
        model_output_dir = output_path / model_spec.name
        artifacts = run_single_model_prompt_invariance(
            model_spec=model_spec,
            benchmark_path=benchmark_path,
            output_dir=model_output_dir,
            max_new_tokens=max_new_tokens,
            top_neurons=top_neurons,
            ablation_neurons=ablation_neurons,
            bootstrap_samples=bootstrap_samples,
            seed=seed,
        )
        summary = json.loads((model_output_dir / "summary.json").read_text(encoding="utf-8"))
        model_summaries.append(summary)

    overall_rows = []
    descriptive_rows = []
    control_rows = []
    descriptive_control_rows = []
    selection_rows = []
    paired_rows = []
    selectivity_rows = []
    ablation_rows = []
    for summary in model_summaries:
        overall = pd.read_csv(summary["artifacts"]["holdout_overall_family_summary"])
        overall["model_name"] = summary["model_name"]
        overall["model_family"] = summary["model_family"]
        overall["model_variant"] = summary["model_variant"]
        overall_rows.append(overall)

        descriptive = pd.read_csv(summary["artifacts"]["overall_family_summary"])
        descriptive["model_name"] = summary["model_name"]
        descriptive["model_family"] = summary["model_family"]
        descriptive["model_variant"] = summary["model_variant"]
        descriptive_rows.append(descriptive)

        control = pd.read_csv(summary["artifacts"]["holdout_overall_control_summary"])
        control["model_name"] = summary["model_name"]
        control["model_family"] = summary["model_family"]
        control["model_variant"] = summary["model_variant"]
        control_rows.append(control)

        descriptive_control = pd.read_csv(summary["artifacts"]["overall_control_summary"])
        descriptive_control["model_name"] = summary["model_name"]
        descriptive_control["model_family"] = summary["model_family"]
        descriptive_control["model_variant"] = summary["model_variant"]
        descriptive_control_rows.append(descriptive_control)

        selection = pd.read_csv(summary["artifacts"]["holdout_family_selection_summary"])
        selection["model_name"] = summary["model_name"]
        selection["model_family"] = summary["model_family"]
        selection["model_variant"] = summary["model_variant"]
        selection_rows.append(selection)

        paired = pd.read_csv(summary["artifacts"]["paired_family_comparisons"])
        paired["model_name"] = summary["model_name"]
        paired_rows.append(paired)

        selectivity = pd.read_csv(summary["artifacts"]["paired_selectivity_comparisons"])
        selectivity["model_name"] = summary["model_name"]
        selectivity_rows.append(selectivity)

        ablation = pd.read_csv(summary["artifacts"]["neuron_ablation_summary"])
        ablation["model_name"] = summary["model_name"]
        ablation_rows.append(ablation)

    overall_df = pd.concat(overall_rows, ignore_index=True)
    descriptive_df = pd.concat(descriptive_rows, ignore_index=True)
    control_df = pd.concat(control_rows, ignore_index=True)
    descriptive_control_df = pd.concat(descriptive_control_rows, ignore_index=True)
    selection_df = pd.concat(selection_rows, ignore_index=True)
    paired_df = pd.concat(paired_rows, ignore_index=True)
    selectivity_df = pd.concat(selectivity_rows, ignore_index=True)
    ablation_df = pd.concat(ablation_rows, ignore_index=True)

    overall_path = output_path / "multimodel_family_summary.csv"
    descriptive_path = output_path / "multimodel_descriptive_family_summary.csv"
    control_path = output_path / "multimodel_control_summary.csv"
    descriptive_control_path = output_path / "multimodel_descriptive_control_summary.csv"
    selection_path = output_path / "multimodel_family_selection_summary.csv"
    paired_path = output_path / "multimodel_paired_family_comparisons.csv"
    selectivity_path = output_path / "multimodel_paired_selectivity_comparisons.csv"
    ablation_path = output_path / "multimodel_ablation_summary.csv"
    overall_df.to_csv(overall_path, index=False)
    descriptive_df.to_csv(descriptive_path, index=False)
    control_df.to_csv(control_path, index=False)
    descriptive_control_df.to_csv(descriptive_control_path, index=False)
    selection_df.to_csv(selection_path, index=False)
    paired_df.to_csv(paired_path, index=False)
    selectivity_df.to_csv(selectivity_path, index=False)
    ablation_df.to_csv(ablation_path, index=False)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 5))
    sns.barplot(data=overall_df, x="model_name", y="answer_f1", hue="prompt_family")
    plt.xticks(rotation=20)
    plt.title("Holdout answer F1 across local models")
    plt.tight_layout()
    family_plot_path = output_path / "multimodel_family_answer_f1.png"
    plt.savefig(family_plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.barplot(data=control_df, x="model_name", y="target_selectivity", hue="prompt_family")
    plt.xticks(rotation=20)
    plt.title("Holdout target selectivity across local models")
    plt.tight_layout()
    selectivity_plot_path = output_path / "multimodel_target_selectivity.png"
    plt.savefig(selectivity_plot_path, dpi=200)
    plt.close()

    heatmap_df = overall_df.pivot(index="model_name", columns="prompt_family", values="answer_f1")
    plt.figure(figsize=(8, 4))
    sns.heatmap(heatmap_df, annot=True, fmt=".2f", cmap="magma")
    plt.title("Holdout answer F1 by model and prompt family")
    plt.tight_layout()
    heatmap_path = output_path / "multimodel_family_heatmap.png"
    plt.savefig(heatmap_path, dpi=200)
    plt.close()

    control_heatmap_df = control_df.pivot(index="model_name", columns="prompt_family", values="target_selectivity")
    plt.figure(figsize=(8, 4))
    sns.heatmap(control_heatmap_df, annot=True, fmt=".2f", cmap="crest")
    plt.title("Holdout target selectivity by model and prompt family")
    plt.tight_layout()
    control_heatmap_path = output_path / "multimodel_selectivity_heatmap.png"
    plt.savefig(control_heatmap_path, dpi=200)
    plt.close()

    if not ablation_df.empty:
        plt.figure(figsize=(10, 4))
        sns.barplot(data=ablation_df, x="model_name", y="answer_f1_drop", hue="candidate_type")
        plt.xticks(rotation=20)
        plt.title("Invariant vs prompt-sensitive neuron ablation drop")
        plt.tight_layout()
        ablation_plot_path = output_path / "multimodel_ablation_effects.png"
        plt.savefig(ablation_plot_path, dpi=200)
        plt.close()
    else:
        ablation_plot_path = output_path / "multimodel_ablation_effects.png"

    best_rows = selection_df.copy()
    report_lines = [
        "# Multi-Model Prompt Invariance Study",
        "",
        f"- Models evaluated: {len(model_specs)}",
        f"- Total prompts per model: {model_summaries[0]['num_prompts'] if model_summaries else 0}",
        "",
        "## Held-out family selection summary",
        "",
    ]
    report_lines.append("| model_name | model_family | model_variant | analysis_best_answer_family | analysis_best_selectivity_family | holdout_best_answer_f1 | holdout_answer_f1_diff | holdout_target_selectivity_diff |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in best_rows.itertuples(index=False):
        report_lines.append(
            f"| {row.model_name} | {row.model_family} | {row.model_variant} | {row.analysis_best_answer_family} | {row.analysis_best_selectivity_family} | {row.holdout_best_answer_f1:.4f} | {row.holdout_answer_f1_diff:.4f} | {row.holdout_target_selectivity_diff:.4f} |"
        )
    report_lines.extend(["", "## Strongest family comparisons by answer F1 difference", ""])
    top_paired = paired_df.reindex(paired_df["mean_diff"].abs().sort_values(ascending=False).index).head(12)
    report_lines.append("| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in top_paired.itertuples(index=False):
        report_lines.append(
            f"| {row.model_name} | {row.relation} | {row.family_a} | {row.family_b} | {row.mean_diff:.4f} | {row.ci_low:.4f} | {row.ci_high:.4f} | {row.sign_test_pvalue:.4f} |"
        )
    report_lines.extend(["", "## Strongest family comparisons by target selectivity", ""])
    top_selectivity = selectivity_df.reindex(selectivity_df["mean_diff"].abs().sort_values(ascending=False).index).head(12)
    report_lines.append("| model_name | relation | family_a | family_b | mean_diff | ci_low | ci_high | pvalue |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in top_selectivity.itertuples(index=False):
        report_lines.append(
            f"| {row.model_name} | {row.relation} | {row.family_a} | {row.family_b} | {row.mean_diff:.4f} | {row.ci_low:.4f} | {row.ci_high:.4f} | {row.sign_test_pvalue:.4f} |"
        )
    report_path = output_path / "multimodel_prompt_invariance_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    summary = {
        "models": [summary["model_name"] for summary in model_summaries],
        "num_models": len(model_summaries),
        "artifacts": {
            "multimodel_family_summary": str(overall_path),
            "multimodel_descriptive_family_summary": str(descriptive_path),
            "multimodel_control_summary": str(control_path),
            "multimodel_descriptive_control_summary": str(descriptive_control_path),
            "multimodel_family_selection_summary": str(selection_path),
            "multimodel_paired_family_comparisons": str(paired_path),
            "multimodel_paired_selectivity_comparisons": str(selectivity_path),
            "multimodel_ablation_summary": str(ablation_path),
            "multimodel_family_answer_f1_png": str(family_plot_path),
            "multimodel_target_selectivity_png": str(selectivity_plot_path),
            "multimodel_family_heatmap_png": str(heatmap_path),
            "multimodel_selectivity_heatmap_png": str(control_heatmap_path),
            "multimodel_ablation_effects_png": str(ablation_plot_path),
            "report": str(report_path),
        },
    }
    write_json(output_path / "summary.json", summary)
    return summary["artifacts"]
