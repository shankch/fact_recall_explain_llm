from __future__ import annotations

from contextlib import contextmanager, nullcontext
from pathlib import Path
import gc
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch

from .modeling import load_model_bundle, subject_span, tokenize_prompt
from .prompt_invariance import (
    ModelSpec,
    _control_metrics,
    _strip_leading_answer_prefix,
    build_multirelation_benchmark,
    render_model_input,
    score_answer,
)
from .utils import ensure_dir, read_jsonl, set_seed, write_json


def project_out_component(vector: torch.Tensor, component: torch.Tensor) -> torch.Tensor:
    denominator = torch.dot(component, component)
    if float(denominator.item()) == 0.0:
        return vector
    coefficient = torch.dot(vector, component) / denominator
    return vector - coefficient * component


def add_component(vector: torch.Tensor, component: torch.Tensor, scale: float = 1.0) -> torch.Tensor:
    return vector + (scale * component)


def _rescale_component(component: np.ndarray, template: np.ndarray) -> np.ndarray:
    component_norm = float(np.linalg.norm(component))
    template_norm = float(np.linalg.norm(template))
    if component_norm == 0.0 or template_norm == 0.0:
        return np.zeros_like(template, dtype=np.float32)
    scaled = component.astype(np.float32) * (template_norm / component_norm)
    return scaled.astype(np.float32)


def _random_component_like(template: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    sample = rng.standard_normal(size=template.shape).astype(np.float32)
    return _rescale_component(sample, template)


@contextmanager
def edit_layer_token_component(
    bundle,
    layer_idx: int,
    token_idx: int,
    component: np.ndarray,
    mode: str,
    scale: float = 1.0,
):
    layer = bundle.model.model.layers[int(layer_idx)]
    base_component = torch.tensor(component, device=bundle.device, dtype=bundle.dtype)

    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if token_idx >= hidden.shape[1]:
            return output
        hidden = hidden.clone()
        token_vec = hidden[:, token_idx, :]
        component_vec = base_component.to(device=hidden.device, dtype=hidden.dtype)
        if mode == "project_out":
            edited = torch.stack([project_out_component(row, component_vec) for row in token_vec], dim=0)
        elif mode == "add":
            edited = torch.stack([add_component(row, component_vec, scale=scale) for row in token_vec], dim=0)
        else:
            raise ValueError(f"Unknown edit mode: {mode}")
        hidden[:, token_idx, :] = edited
        if isinstance(output, tuple):
            return (hidden, *output[1:])
        return hidden

    handle = layer.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


def _cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0.0:
        return 0.0
    return float(np.dot(left, right) / denominator)


def _load_family_preferences(prompt_invariance_dir: str | Path, model_name: str) -> tuple[str, str]:
    selection_path = Path(prompt_invariance_dir) / "multimodel_family_selection_summary.csv"
    if selection_path.exists():
        summary = pd.read_csv(selection_path)
        row = summary[summary["model_name"] == model_name].iloc[0]
        return str(row["analysis_best_answer_family"]), str(row["analysis_worst_answer_family"])

    summary = pd.read_csv(Path(prompt_invariance_dir) / "multimodel_family_summary.csv")
    frame = summary[summary["model_name"] == model_name].sort_values("answer_f1", ascending=False)
    best_family = str(frame.iloc[0]["prompt_family"])
    worst_family = str(frame.iloc[-1]["prompt_family"])
    return best_family, worst_family


def _load_layer_choices(storage_access_dir: str | Path, model_name: str) -> tuple[int, int]:
    summary_path = Path(storage_access_dir) / "multimodel_summary.csv"
    if summary_path.exists():
        summary = pd.read_csv(summary_path)
        row = summary[summary["model_name"] == model_name].iloc[0]
        early_layer = int(round(float(row["subject_invariance_depth_mean"])))
        late_layer = int(round(float(row["preanswer_invariance_depth_mean"])))
        return early_layer, late_layer

    model_summary = json.loads((Path(storage_access_dir) / model_name / "summary.json").read_text(encoding="utf-8"))
    early_layer = int(round(float(model_summary["subject_invariance_depth_mean"])))
    late_layer = int(round(float(model_summary["preanswer_invariance_depth_mean"])))
    return early_layer, late_layer


def _load_activation_profiles(storage_access_dir: str | Path, model_name: str) -> list[dict]:
    path = Path(storage_access_dir) / model_name / "activation_profiles.jsonl"
    rows = read_jsonl(path)
    for row in rows:
        row["subject_vectors"] = np.asarray(row["subject_vectors"], dtype=np.float32)
        row["preanswer_vectors"] = np.asarray(row["preanswer_vectors"], dtype=np.float32)
    return rows


def _build_fact_components(profile_rows: list[dict], early_layer: int, late_layer: int) -> dict[str, dict]:
    by_fact: dict[str, list[dict]] = {}
    by_relation: dict[str, list[dict]] = {}
    for row in profile_rows:
        by_fact.setdefault(row["fact_id"], []).append(row)
        by_relation.setdefault(row["relation"], []).append(row)

    fact_components = {}
    for fact_id, fact_rows in by_fact.items():
        relation = fact_rows[0]["relation"]
        relation_rows = [row for row in by_relation[relation] if row["fact_id"] != fact_id]
        subject_fact_centroid = np.mean([row["subject_vectors"][early_layer] for row in fact_rows], axis=0)
        if relation_rows:
            subject_relation_centroid = np.mean([row["subject_vectors"][early_layer] for row in relation_rows], axis=0)
            late_relation_centroid = np.mean([row["preanswer_vectors"][late_layer] for row in relation_rows], axis=0)
        else:
            subject_relation_centroid = np.zeros_like(subject_fact_centroid)
            late_relation_centroid = np.zeros_like(fact_rows[0]["preanswer_vectors"][late_layer])
        component = subject_fact_centroid - subject_relation_centroid
        late_fact_centroid = np.mean([row["preanswer_vectors"][late_layer] for row in fact_rows], axis=0)
        fact_components[fact_id] = {
            "relation": relation,
            "subject_component": component,
            "late_fact_centroid": late_fact_centroid,
            "late_relation_centroid": late_relation_centroid,
        }
    return fact_components


def _relation_control_fact_ids(fact_components: dict[str, dict]) -> dict[str, str]:
    by_relation: dict[str, list[str]] = {}
    for fact_id, payload in fact_components.items():
        by_relation.setdefault(str(payload["relation"]), []).append(fact_id)

    mapping: dict[str, str] = {}
    for relation, fact_ids in by_relation.items():
        ordered = sorted(fact_ids)
        if len(ordered) == 1:
            mapping[ordered[0]] = ordered[0]
            continue
        for idx, fact_id in enumerate(ordered):
            mapping[fact_id] = ordered[(idx + 1) % len(ordered)]
    return mapping


def _evaluate_prompt(
    bundle,
    row: dict,
    early_layer: int,
    late_layer: int,
    late_fact_centroid: np.ndarray,
    late_relation_centroid: np.ndarray,
    component: np.ndarray | None = None,
    mode: str | None = None,
    scale: float = 1.0,
    max_new_tokens: int = 10,
) -> dict:
    actual_input = render_model_input(bundle.tokenizer, row)
    encoded = tokenize_prompt(bundle, actual_input)
    prompt_tokens = encoded["input_ids"]
    _, subject_end = subject_span(bundle, actual_input, row["subject"])
    if subject_end < 0:
        subject_end = prompt_tokens.shape[1] - 1

    context = (
        edit_layer_token_component(bundle, early_layer, subject_end, component, mode=mode, scale=scale)
        if component is not None and mode is not None
        else nullcontext()
    )
    with context:
        with torch.no_grad():
            outputs = bundle.model(**encoded, output_hidden_states=True)
            generated_ids = bundle.model.generate(
                **encoded,
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
    late_vector = outputs.hidden_states[late_layer + 1][0, -1].detach().float().cpu().numpy()
    late_alignment = _cosine_similarity(late_vector, late_fact_centroid) - _cosine_similarity(late_vector, late_relation_centroid)
    return {
        "generated_text": generated_text,
        "normalized_generated_text": normalized_generated,
        "late_alignment": late_alignment,
        **answer_metrics,
        **control_metrics,
    }


def _intervention_rows_for_strategy(
    bundle,
    benchmark_lookup: dict[tuple[str, str], dict],
    fact_components: dict[str, dict],
    control_fact_ids: dict[str, str],
    best_family: str,
    worst_family: str,
    early_layer: int,
    late_layer: int,
    rng: np.random.Generator,
    model_spec: ModelSpec,
    layer_strategy: str,
    max_new_tokens: int,
    add_scale: float,
) -> list[dict]:
    rows = []
    for fact_id, components in fact_components.items():
        best_row = benchmark_lookup.get((fact_id, best_family))
        worst_row = benchmark_lookup.get((fact_id, worst_family))
        if best_row is None or worst_row is None:
            continue
        if best_row.get("split") != "holdout" or worst_row.get("split") != "holdout":
            continue

        control_fact_id = control_fact_ids[fact_id]
        control_component = _rescale_component(
            fact_components[control_fact_id]["subject_component"],
            components["subject_component"],
        )
        random_component = _random_component_like(components["subject_component"], rng)
        baseline_best = _evaluate_prompt(
            bundle,
            best_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            max_new_tokens=max_new_tokens,
        )
        projected_best = _evaluate_prompt(
            bundle,
            best_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=components["subject_component"],
            mode="project_out",
            max_new_tokens=max_new_tokens,
        )
        projected_best_control = _evaluate_prompt(
            bundle,
            best_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=control_component,
            mode="project_out",
            max_new_tokens=max_new_tokens,
        )
        projected_best_random = _evaluate_prompt(
            bundle,
            best_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=random_component,
            mode="project_out",
            max_new_tokens=max_new_tokens,
        )
        baseline_worst = _evaluate_prompt(
            bundle,
            worst_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            max_new_tokens=max_new_tokens,
        )
        patched_worst = _evaluate_prompt(
            bundle,
            worst_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=components["subject_component"],
            mode="add",
            scale=add_scale,
            max_new_tokens=max_new_tokens,
        )
        patched_worst_control = _evaluate_prompt(
            bundle,
            worst_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=control_component,
            mode="add",
            scale=add_scale,
            max_new_tokens=max_new_tokens,
        )
        patched_worst_random = _evaluate_prompt(
            bundle,
            worst_row,
            early_layer=early_layer,
            late_layer=late_layer,
            late_fact_centroid=components["late_fact_centroid"],
            late_relation_centroid=components["late_relation_centroid"],
            component=random_component,
            mode="add",
            scale=add_scale,
            max_new_tokens=max_new_tokens,
        )
        rows.append(
            {
                "model_name": model_spec.name,
                "model_variant": model_spec.variant,
                "relation": best_row["relation"],
                "fact_id": fact_id,
                "relation_control_fact_id": control_fact_id,
                "best_family": best_family,
                "worst_family": worst_family,
                "layer_strategy": layer_strategy,
                "early_layer": early_layer,
                "late_layer": late_layer,
                "baseline_best_answer_f1": baseline_best["answer_f1"],
                "projected_best_answer_f1": projected_best["answer_f1"],
                "project_best_answer_f1_delta": projected_best["answer_f1"] - baseline_best["answer_f1"],
                "baseline_best_selectivity": baseline_best["target_selectivity"],
                "projected_best_selectivity": projected_best["target_selectivity"],
                "project_best_selectivity_delta": projected_best["target_selectivity"] - baseline_best["target_selectivity"],
                "baseline_best_alignment": baseline_best["late_alignment"],
                "projected_best_alignment": projected_best["late_alignment"],
                "project_best_alignment_delta": projected_best["late_alignment"] - baseline_best["late_alignment"],
                "projected_best_control_answer_f1": projected_best_control["answer_f1"],
                "project_best_control_answer_f1_delta": projected_best_control["answer_f1"] - baseline_best["answer_f1"],
                "projected_best_control_selectivity": projected_best_control["target_selectivity"],
                "project_best_control_selectivity_delta": projected_best_control["target_selectivity"] - baseline_best["target_selectivity"],
                "projected_best_control_alignment": projected_best_control["late_alignment"],
                "project_best_control_alignment_delta": projected_best_control["late_alignment"] - baseline_best["late_alignment"],
                "projected_best_random_answer_f1": projected_best_random["answer_f1"],
                "project_best_random_answer_f1_delta": projected_best_random["answer_f1"] - baseline_best["answer_f1"],
                "projected_best_random_selectivity": projected_best_random["target_selectivity"],
                "project_best_random_selectivity_delta": projected_best_random["target_selectivity"] - baseline_best["target_selectivity"],
                "projected_best_random_alignment": projected_best_random["late_alignment"],
                "project_best_random_alignment_delta": projected_best_random["late_alignment"] - baseline_best["late_alignment"],
                "baseline_worst_answer_f1": baseline_worst["answer_f1"],
                "patched_worst_answer_f1": patched_worst["answer_f1"],
                "patch_worst_answer_f1_delta": patched_worst["answer_f1"] - baseline_worst["answer_f1"],
                "baseline_worst_selectivity": baseline_worst["target_selectivity"],
                "patched_worst_selectivity": patched_worst["target_selectivity"],
                "patch_worst_selectivity_delta": patched_worst["target_selectivity"] - baseline_worst["target_selectivity"],
                "baseline_worst_alignment": baseline_worst["late_alignment"],
                "patched_worst_alignment": patched_worst["late_alignment"],
                "patch_worst_alignment_delta": patched_worst["late_alignment"] - baseline_worst["late_alignment"],
                "patched_worst_control_answer_f1": patched_worst_control["answer_f1"],
                "patch_worst_control_answer_f1_delta": patched_worst_control["answer_f1"] - baseline_worst["answer_f1"],
                "patched_worst_control_selectivity": patched_worst_control["target_selectivity"],
                "patch_worst_control_selectivity_delta": patched_worst_control["target_selectivity"] - baseline_worst["target_selectivity"],
                "patched_worst_control_alignment": patched_worst_control["late_alignment"],
                "patch_worst_control_alignment_delta": patched_worst_control["late_alignment"] - baseline_worst["late_alignment"],
                "patched_worst_random_answer_f1": patched_worst_random["answer_f1"],
                "patch_worst_random_answer_f1_delta": patched_worst_random["answer_f1"] - baseline_worst["answer_f1"],
                "patched_worst_random_selectivity": patched_worst_random["target_selectivity"],
                "patch_worst_random_selectivity_delta": patched_worst_random["target_selectivity"] - baseline_worst["target_selectivity"],
                "patched_worst_random_alignment": patched_worst_random["late_alignment"],
                "patch_worst_random_alignment_delta": patched_worst_random["late_alignment"] - baseline_worst["late_alignment"],
            }
        )
    return rows


def run_subspace_intervention_model(
    model_spec: ModelSpec,
    benchmark_path: str | Path,
    output_dir: str | Path,
    prompt_invariance_dir: str | Path,
    storage_access_dir: str | Path,
    seed: int = 13,
    max_new_tokens: int = 10,
    add_scale: float = 1.0,
) -> dict[str, str]:
    set_seed(seed)
    output_path = ensure_dir(output_dir)
    best_family, worst_family = _load_family_preferences(prompt_invariance_dir, model_spec.name)
    early_layer, late_layer = _load_layer_choices(storage_access_dir, model_spec.name)
    profile_rows = _load_activation_profiles(storage_access_dir, model_spec.name)
    rng = np.random.default_rng(seed)
    bundle = load_model_bundle(model_dir=model_spec.path, seed=seed, require_cuda=False, dtype="auto")

    benchmark_rows = read_jsonl(benchmark_path)
    lookup = {(row["fact_id"], row["prompt_family"]): row for row in benchmark_rows}
    intervention_rows = []
    layer_plan = [("primary", early_layer)]
    if early_layer + 1 < int(bundle.model.config.num_hidden_layers):
        layer_plan.append(("plus_one", early_layer + 1))

    for layer_strategy, current_early_layer in layer_plan:
        fact_components = _build_fact_components(profile_rows, early_layer=current_early_layer, late_layer=late_layer)
        control_fact_ids = _relation_control_fact_ids(fact_components)
        intervention_rows.extend(
            _intervention_rows_for_strategy(
                bundle=bundle,
                benchmark_lookup=lookup,
                fact_components=fact_components,
                control_fact_ids=control_fact_ids,
                best_family=best_family,
                worst_family=worst_family,
                early_layer=current_early_layer,
                late_layer=late_layer,
                rng=rng,
                model_spec=model_spec,
                layer_strategy=layer_strategy,
                max_new_tokens=max_new_tokens,
                add_scale=add_scale,
            )
        )

    intervention_df = pd.DataFrame(intervention_rows)
    summary_rows = []
    for layer_strategy, frame in intervention_df.groupby("layer_strategy"):
        summary_rows.append(
            {
                "model_name": model_spec.name,
                "model_variant": model_spec.variant,
                "best_family": best_family,
                "worst_family": worst_family,
                "layer_strategy": layer_strategy,
                "early_layer": int(frame["early_layer"].iloc[0]),
                "late_layer": late_layer,
                "num_holdout_facts": int(frame["fact_id"].nunique()),
                "project_best_answer_f1_delta_mean": float(frame["project_best_answer_f1_delta"].mean()),
                "project_best_selectivity_delta_mean": float(frame["project_best_selectivity_delta"].mean()),
                "project_best_alignment_delta_mean": float(frame["project_best_alignment_delta"].mean()),
                "project_best_control_answer_f1_delta_mean": float(frame["project_best_control_answer_f1_delta"].mean()),
                "project_best_control_selectivity_delta_mean": float(frame["project_best_control_selectivity_delta"].mean()),
                "project_best_control_alignment_delta_mean": float(frame["project_best_control_alignment_delta"].mean()),
                "project_best_random_answer_f1_delta_mean": float(frame["project_best_random_answer_f1_delta"].mean()),
                "project_best_random_selectivity_delta_mean": float(frame["project_best_random_selectivity_delta"].mean()),
                "project_best_random_alignment_delta_mean": float(frame["project_best_random_alignment_delta"].mean()),
                "patch_worst_answer_f1_delta_mean": float(frame["patch_worst_answer_f1_delta"].mean()),
                "patch_worst_selectivity_delta_mean": float(frame["patch_worst_selectivity_delta"].mean()),
                "patch_worst_alignment_delta_mean": float(frame["patch_worst_alignment_delta"].mean()),
                "patch_worst_control_answer_f1_delta_mean": float(frame["patch_worst_control_answer_f1_delta"].mean()),
                "patch_worst_control_selectivity_delta_mean": float(frame["patch_worst_control_selectivity_delta"].mean()),
                "patch_worst_control_alignment_delta_mean": float(frame["patch_worst_control_alignment_delta"].mean()),
                "patch_worst_random_answer_f1_delta_mean": float(frame["patch_worst_random_answer_f1_delta"].mean()),
                "patch_worst_random_selectivity_delta_mean": float(frame["patch_worst_random_selectivity_delta"].mean()),
                "patch_worst_random_alignment_delta_mean": float(frame["patch_worst_random_alignment_delta"].mean()),
                "patch_worst_answer_f1_improve_rate": float((frame["patch_worst_answer_f1_delta"] > 0).mean()),
                "patch_worst_alignment_improve_rate": float((frame["patch_worst_alignment_delta"] > 0).mean()),
                "project_best_alignment_drop_rate": float((frame["project_best_alignment_delta"] < 0).mean()),
                "project_target_stronger_than_control_rate": float(
                    (frame["project_best_alignment_delta"] < frame["project_best_control_alignment_delta"]).mean()
                ),
                "project_target_stronger_than_random_rate": float(
                    (frame["project_best_alignment_delta"] < frame["project_best_random_alignment_delta"]).mean()
                ),
                "patch_target_stronger_than_control_rate": float(
                    (frame["patch_worst_alignment_delta"] > frame["patch_worst_control_alignment_delta"]).mean()
                ),
                "patch_target_stronger_than_random_rate": float(
                    (frame["patch_worst_alignment_delta"] > frame["patch_worst_random_alignment_delta"]).mean()
                ),
            }
        )
    summary_df = pd.DataFrame(summary_rows)

    intervention_path = output_path / "subspace_interventions.csv"
    summary_path = output_path / "summary.csv"
    intervention_df.to_csv(intervention_path, index=False)
    summary_df.to_csv(summary_path, index=False)

    sns.set_theme(style="whitegrid")
    primary_frame = intervention_df[intervention_df["layer_strategy"] == "primary"].copy()
    if primary_frame.empty:
        primary_frame = intervention_df.copy()
    plot_df = pd.DataFrame(
        [
            {"metric": "project_fact_alignment_delta", "value": float(value)}
            for value in primary_frame["project_best_alignment_delta"]
        ]
        + [
            {"metric": "project_control_alignment_delta", "value": float(value)}
            for value in primary_frame["project_best_control_alignment_delta"]
        ]
        + [
            {"metric": "project_random_alignment_delta", "value": float(value)}
            for value in primary_frame["project_best_random_alignment_delta"]
        ]
        + [
            {"metric": "patch_fact_alignment_delta", "value": float(value)}
            for value in primary_frame["patch_worst_alignment_delta"]
        ]
        + [
            {"metric": "patch_control_alignment_delta", "value": float(value)}
            for value in primary_frame["patch_worst_control_alignment_delta"]
        ]
        + [
            {"metric": "patch_random_alignment_delta", "value": float(value)}
            for value in primary_frame["patch_worst_random_alignment_delta"]
        ]
    )
    plt.figure(figsize=(8, 4))
    sns.barplot(data=plot_df, x="metric", y="value", color="#c05621")
    plt.axhline(0.0, color="#666666", linestyle="--", linewidth=0.8)
    plt.xticks(rotation=10)
    plt.title(f"{model_spec.name}: subspace intervention alignment deltas")
    plt.tight_layout()
    plot_path = output_path / "alignment_delta_bar.png"
    plt.savefig(plot_path, dpi=200)
    plt.close()

    summary = {
        "model_name": model_spec.name,
        "model_variant": model_spec.variant,
        "artifacts": {
            "interventions": str(intervention_path),
            "summary": str(summary_path),
            "alignment_delta_bar_png": str(plot_path),
        },
    }
    write_json(output_path / "summary.json", summary)

    del bundle.model
    del bundle.tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return summary["artifacts"]


def run_subspace_intervention_suite(
    model_specs: list[ModelSpec],
    benchmark_path: str | Path,
    output_dir: str | Path,
    prompt_invariance_dir: str | Path,
    storage_access_dir: str | Path,
    seed: int = 13,
    max_new_tokens: int = 10,
    add_scale: float = 1.0,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    summary_rows = []
    intervention_frames = []
    for model_spec in model_specs:
        model_output_dir = output_path / model_spec.name
        run_subspace_intervention_model(
            model_spec=model_spec,
            benchmark_path=benchmark_path,
            output_dir=model_output_dir,
            prompt_invariance_dir=prompt_invariance_dir,
            storage_access_dir=storage_access_dir,
            seed=seed,
            max_new_tokens=max_new_tokens,
            add_scale=add_scale,
        )
        summary_rows.append(pd.read_csv(model_output_dir / "summary.csv"))
        intervention_frames.append(pd.read_csv(model_output_dir / "subspace_interventions.csv"))

    summary_df = pd.concat(summary_rows, ignore_index=True)
    summary_path = output_path / "multimodel_subspace_intervention_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    intervention_df = pd.concat(intervention_frames, ignore_index=True)
    intervention_path = output_path / "multimodel_subspace_interventions.csv"
    intervention_df.to_csv(intervention_path, index=False)
    primary_summary_df = summary_df[summary_df["layer_strategy"] == "primary"].copy()
    if primary_summary_df.empty:
        primary_summary_df = summary_df.copy()
    robustness_df = (
        summary_df.pivot(index="model_name", columns="layer_strategy", values="project_best_alignment_delta_mean")
        .reset_index()
        if not summary_df.empty
        else pd.DataFrame()
    )
    robustness_path = output_path / "multimodel_layer_strategy_robustness.csv"
    robustness_df.to_csv(robustness_path, index=False)

    plt.figure(figsize=(10, 4))
    sns.barplot(data=primary_summary_df, x="model_name", y="patch_worst_alignment_delta_mean", color="#15616d")
    plt.axhline(0.0, color="#666666", linestyle="--", linewidth=0.8)
    plt.xticks(rotation=20)
    plt.title("Mean late-alignment gain after patching worst-family prompts")
    plt.tight_layout()
    patch_plot_path = output_path / "multimodel_patch_alignment_gain.png"
    plt.savefig(patch_plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    sns.barplot(data=primary_summary_df, x="model_name", y="project_best_alignment_delta_mean", color="#8a3b12")
    plt.axhline(0.0, color="#666666", linestyle="--", linewidth=0.8)
    plt.xticks(rotation=20)
    plt.title("Mean late-alignment change after projecting out best-family components")
    plt.tight_layout()
    project_plot_path = output_path / "multimodel_project_alignment_delta.png"
    plt.savefig(project_plot_path, dpi=200)
    plt.close()

    report_lines = [
        "# Subspace Intervention Summary",
        "",
        "| model_name | layer_strategy | best_family | worst_family | patch_fact_align | patch_ctrl_align | project_fact_align | project_ctrl_align | patch_fact_f1 | patch_ctrl_f1 | project_fact_f1 | project_ctrl_f1 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_df.itertuples(index=False):
        report_lines.append(
            f"| {row.model_name} | {row.layer_strategy} | {row.best_family} | {row.worst_family} | {row.patch_worst_alignment_delta_mean:.4f} | {row.patch_worst_control_alignment_delta_mean:.4f} | {row.project_best_alignment_delta_mean:.4f} | {row.project_best_control_alignment_delta_mean:.4f} | {row.patch_worst_answer_f1_delta_mean:.4f} | {row.patch_worst_control_answer_f1_delta_mean:.4f} | {row.project_best_answer_f1_delta_mean:.4f} | {row.project_best_control_answer_f1_delta_mean:.4f} |"
        )
    report_path = output_path / "multimodel_subspace_intervention_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    summary = {
        "num_models": len(model_specs),
        "artifacts": {
            "multimodel_subspace_intervention_summary": str(summary_path),
            "multimodel_subspace_interventions": str(intervention_path),
            "multimodel_layer_strategy_robustness": str(robustness_path),
            "multimodel_patch_alignment_gain_png": str(patch_plot_path),
            "multimodel_project_alignment_delta_png": str(project_plot_path),
            "report": str(report_path),
        },
    }
    write_json(output_path / "summary.json", summary)
    return summary["artifacts"]


def build_subspace_benchmark(
    output_dir: str | Path,
    limit_per_relation: int = 12,
    families: list[str] | None = None,
    relations: list[str] | None = None,
    seed_facts_path: str | Path = "data/factual_seed.json",
) -> Path:
    return build_multirelation_benchmark(
        output_dir=output_dir,
        limit_per_relation=limit_per_relation,
        families=families,
        relations=relations,
        seed_facts_path=seed_facts_path,
    )
