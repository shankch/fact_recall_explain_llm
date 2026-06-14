from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import gc
import json
import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch

from .modeling import load_model_bundle, subject_span, tokenize_prompt
from .prompt_invariance import ModelSpec, build_multirelation_benchmark, render_model_input
from .utils import ensure_dir, read_jsonl, set_seed, write_json, write_jsonl


POSITIONS = ("subject", "preanswer")
ANALYSIS_VARIANTS = {
    "all_families": {},
    "no_chat": {"exclude_families": {"chat_template"}},
    "length_matched_delta4": {"max_length_delta": 4},
}


@dataclass(frozen=True)
class ActivationProfile:
    fact_id: str
    relation: str
    subject: str
    prompt_family: str
    split: str
    model_name: str
    model_family: str
    model_variant: str
    prompt: str
    model_input: str
    prompt_length: int
    subject_vectors: np.ndarray
    preanswer_vectors: np.ndarray


def _cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0.0:
        return 0.0
    return float(np.dot(left, right) / denominator)


def _mean_pairwise_similarity(vectors: list[np.ndarray]) -> float:
    if len(vectors) < 2:
        return 0.0
    values = [
        _cosine_similarity(left, right)
        for left, right in itertools.combinations(vectors, 2)
    ]
    return float(np.mean(values)) if values else 0.0


def first_sustained_layer(values: list[float], threshold: float = 0.0, sustain: int = 2) -> int:
    if sustain <= 0:
        raise ValueError("sustain must be positive")
    for start in range(0, max(0, len(values) - sustain + 1)):
        window = values[start : start + sustain]
        if all(value > threshold for value in window):
            return start
    return -1


def _collect_activation_profile(bundle, row: dict, model_spec: ModelSpec) -> ActivationProfile:
    actual_input = render_model_input(bundle.tokenizer, row)
    encoded = tokenize_prompt(bundle, actual_input)
    input_ids = encoded["input_ids"]
    prompt_len = int(input_ids.shape[1])
    subject_start, subject_end = subject_span(bundle, actual_input, row["subject"])

    with torch.no_grad():
        outputs = bundle.model(**encoded, output_hidden_states=True)

    subject_vectors = []
    preanswer_vectors = []
    for hidden in outputs.hidden_states[1:]:
        layer_state = hidden[0].detach().float().cpu()
        preanswer_vectors.append(layer_state[prompt_len - 1].numpy())
        if subject_end >= 0 and subject_end < layer_state.shape[0]:
            subject_vectors.append(layer_state[subject_end].numpy())
        else:
            subject_vectors.append(layer_state[prompt_len - 1].numpy())

    return ActivationProfile(
        fact_id=row["fact_id"],
        relation=row["relation"],
        subject=row["subject"],
        prompt_family=row["prompt_family"],
        split=row["split"],
        model_name=model_spec.name,
        model_family=model_spec.family,
        model_variant=model_spec.variant,
        prompt=row["prompt"],
        model_input=actual_input,
        prompt_length=prompt_len,
        subject_vectors=np.stack(subject_vectors),
        preanswer_vectors=np.stack(preanswer_vectors),
    )


def _profile_to_row(profile: ActivationProfile) -> dict:
    return {
        "fact_id": profile.fact_id,
        "relation": profile.relation,
        "subject": profile.subject,
        "prompt_family": profile.prompt_family,
        "split": profile.split,
        "model_name": profile.model_name,
        "model_family": profile.model_family,
        "model_variant": profile.model_variant,
        "prompt": profile.prompt,
        "model_input": profile.model_input,
        "prompt_length": profile.prompt_length,
        "subject_vectors": profile.subject_vectors.tolist(),
        "preanswer_vectors": profile.preanswer_vectors.tolist(),
    }


def _profiles_from_rows(rows: list[dict]) -> list[ActivationProfile]:
    profiles = []
    for row in rows:
        profiles.append(
            ActivationProfile(
                fact_id=row["fact_id"],
                relation=row["relation"],
                subject=row["subject"],
                prompt_family=row["prompt_family"],
                split=row["split"],
                model_name=row["model_name"],
                model_family=row["model_family"],
                model_variant=row["model_variant"],
                prompt=row["prompt"],
                model_input=row["model_input"],
                prompt_length=int(row["prompt_length"]),
                subject_vectors=np.asarray(row["subject_vectors"], dtype=np.float32),
                preanswer_vectors=np.asarray(row["preanswer_vectors"], dtype=np.float32),
            )
        )
    return profiles


def _filtered_profiles(
    profiles: list[ActivationProfile],
    split: str = "all",
    exclude_families: set[str] | None = None,
) -> list[ActivationProfile]:
    filtered = profiles
    if split != "all":
        filtered = [profile for profile in filtered if profile.split == split]
    if exclude_families:
        filtered = [profile for profile in filtered if profile.prompt_family not in exclude_families]
    return filtered


def _compute_layer_metrics(profiles: list[ActivationProfile]) -> pd.DataFrame:
    if not profiles:
        return pd.DataFrame()

    num_layers = profiles[0].subject_vectors.shape[0]
    layer_rows = []
    for position in POSITIONS:
        vectors_by_profile = [
            profile.subject_vectors if position == "subject" else profile.preanswer_vectors
            for profile in profiles
        ]
        for layer_idx in range(num_layers):
            same_fact_scores = []
            same_relation_scores = []
            global_other_scores = []
            family_centroids: dict[str, list[np.ndarray]] = {}

            for idx, profile in enumerate(profiles):
                family_centroids.setdefault(profile.prompt_family, []).append(vectors_by_profile[idx][layer_idx])

            for family, vectors in family_centroids.items():
                family_centroids[family] = [np.mean(vectors, axis=0)]

            for left_idx, right_idx in itertools.combinations(range(len(profiles)), 2):
                left = profiles[left_idx]
                right = profiles[right_idx]
                score = _cosine_similarity(vectors_by_profile[left_idx][layer_idx], vectors_by_profile[right_idx][layer_idx])
                if left.fact_id == right.fact_id and left.prompt_family != right.prompt_family:
                    same_fact_scores.append(score)
                elif left.relation == right.relation and left.fact_id != right.fact_id:
                    same_relation_scores.append(score)
                elif left.fact_id != right.fact_id:
                    global_other_scores.append(score)

            centroid_vectors = [vectors[0] for vectors in family_centroids.values()]
            centroid_separation = 0.0
            if len(centroid_vectors) >= 2:
                centroid_separation = float(
                    np.mean(
                        [
                            1.0 - _cosine_similarity(left, right)
                            for left, right in itertools.combinations(centroid_vectors, 2)
                        ]
                    )
                )

            within_fact = float(np.mean(same_fact_scores)) if same_fact_scores else 0.0
            same_relation = float(np.mean(same_relation_scores)) if same_relation_scores else 0.0
            global_other = float(np.mean(global_other_scores)) if global_other_scores else 0.0
            layer_rows.append(
                {
                    "position": position,
                    "layer": layer_idx,
                    "within_fact_similarity": within_fact,
                    "same_relation_similarity": same_relation,
                    "global_other_similarity": global_other,
                    "invariance_gap": within_fact - same_relation,
                    "family_centroid_separation": centroid_separation,
                }
            )
    return pd.DataFrame(layer_rows)


def _compute_fact_layer_scores(
    profiles: list[ActivationProfile],
    max_length_delta: int | None = None,
) -> pd.DataFrame:
    if not profiles:
        return pd.DataFrame()

    num_layers = profiles[0].subject_vectors.shape[0]
    rows = []
    by_fact: dict[str, list[ActivationProfile]] = {}
    by_relation: dict[str, list[ActivationProfile]] = {}
    for profile in profiles:
        by_fact.setdefault(profile.fact_id, []).append(profile)
        by_relation.setdefault(profile.relation, []).append(profile)

    for fact_id, fact_profiles in by_fact.items():
        relation = fact_profiles[0].relation
        relation_profiles = [profile for profile in by_relation[relation] if profile.fact_id != fact_id]
        for position in POSITIONS:
            for layer_idx in range(num_layers):
                within_fact_scores = []
                relation_scores = []
                for left, right in itertools.combinations(fact_profiles, 2):
                    if left.prompt_family == right.prompt_family:
                        continue
                    if max_length_delta is not None and abs(left.prompt_length - right.prompt_length) > max_length_delta:
                        continue
                    left_vec = left.subject_vectors[layer_idx] if position == "subject" else left.preanswer_vectors[layer_idx]
                    right_vec = right.subject_vectors[layer_idx] if position == "subject" else right.preanswer_vectors[layer_idx]
                    within_fact_scores.append(_cosine_similarity(left_vec, right_vec))

                for left in fact_profiles:
                    for right in relation_profiles:
                        if max_length_delta is not None and abs(left.prompt_length - right.prompt_length) > max_length_delta:
                            continue
                        left_vec = left.subject_vectors[layer_idx] if position == "subject" else left.preanswer_vectors[layer_idx]
                        right_vec = right.subject_vectors[layer_idx] if position == "subject" else right.preanswer_vectors[layer_idx]
                        relation_scores.append(_cosine_similarity(left_vec, right_vec))

                within_fact = float(np.mean(within_fact_scores)) if within_fact_scores else 0.0
                relation_similarity = float(np.mean(relation_scores)) if relation_scores else 0.0
                rows.append(
                    {
                        "fact_id": fact_id,
                        "relation": relation,
                        "position": position,
                        "layer": layer_idx,
                        "within_fact_similarity": within_fact,
                        "same_relation_similarity": relation_similarity,
                        "invariance_gap": within_fact - relation_similarity,
                    }
                )
    return pd.DataFrame(rows)


def _fact_summary(fact_layer_df: pd.DataFrame) -> pd.DataFrame:
    if fact_layer_df.empty:
        return pd.DataFrame()

    summary_rows = []
    for (fact_id, relation, position), frame in fact_layer_df.groupby(["fact_id", "relation", "position"]):
        ordered = frame.sort_values("layer")
        gaps = ordered["invariance_gap"].tolist()
        summary_rows.append(
            {
                "fact_id": fact_id,
                "relation": relation,
                "position": position,
                "mean_invariance_gap": float(np.mean(gaps)),
                "peak_invariance_gap": float(np.max(gaps)),
                "invariance_depth": first_sustained_layer(gaps, threshold=0.0, sustain=2),
            }
        )
    return pd.DataFrame(summary_rows)


def _safe_depth_mean(frame: pd.DataFrame, position: str) -> float:
    values = frame[frame["position"] == position]["invariance_depth"].to_numpy(dtype=float)
    values = values[values >= 0]
    if values.size == 0:
        return -1.0
    return float(values.mean())


def run_storage_access_competition_model(
    model_spec: ModelSpec,
    benchmark_path: str | Path,
    output_dir: str | Path,
    seed: int = 13,
) -> dict[str, str]:
    set_seed(seed)
    output_path = ensure_dir(output_dir)
    bundle = load_model_bundle(model_dir=model_spec.path, seed=seed, require_cuda=False, dtype="auto")
    benchmark_rows = read_jsonl(benchmark_path)

    profiles = [
        _collect_activation_profile(bundle, row, model_spec)
        for row in benchmark_rows
    ]
    main_profiles = _filtered_profiles(profiles, split="holdout")
    if not main_profiles:
        main_profiles = profiles
    layer_df = _compute_layer_metrics(main_profiles)

    fact_layer_frames = []
    fact_summary_frames = []
    control_rows = []
    for split_name in ["all", "holdout"]:
        split_profiles = _filtered_profiles(profiles, split=split_name)
        if not split_profiles:
            continue
        for variant_name, options in ANALYSIS_VARIANTS.items():
            variant_profiles = _filtered_profiles(
                split_profiles,
                exclude_families=set(options.get("exclude_families", set())),
            )
            if not variant_profiles:
                continue
            fact_layer_variant = _compute_fact_layer_scores(
                variant_profiles,
                max_length_delta=options.get("max_length_delta"),
            )
            if fact_layer_variant.empty:
                continue
            fact_layer_variant["split_eval"] = split_name
            fact_layer_variant["analysis_variant"] = variant_name
            fact_summary_variant = _fact_summary(fact_layer_variant)
            fact_summary_variant["split_eval"] = split_name
            fact_summary_variant["analysis_variant"] = variant_name
            fact_layer_frames.append(fact_layer_variant)
            fact_summary_frames.append(fact_summary_variant)

            for position in POSITIONS:
                frame = fact_summary_variant[fact_summary_variant["position"] == position]
                depths = frame["invariance_depth"].to_numpy(dtype=float)
                found_mask = depths >= 0
                valid_depths = depths[found_mask]
                control_rows.append(
                    {
                        "model_name": model_spec.name,
                        "model_family": model_spec.family,
                        "model_variant": model_spec.variant,
                        "split_eval": split_name,
                        "analysis_variant": variant_name,
                        "position": position,
                        "num_facts": int(frame.shape[0]),
                        "found_rate": float(found_mask.mean()) if depths.size else 0.0,
                        "invariance_depth_mean": float(valid_depths.mean()) if valid_depths.size else -1.0,
                        "mean_invariance_gap": float(frame["mean_invariance_gap"].mean()) if not frame.empty else 0.0,
                        "peak_invariance_gap": float(frame["peak_invariance_gap"].max()) if not frame.empty else 0.0,
                    }
                )

    fact_layer_df = pd.concat(fact_layer_frames, ignore_index=True)
    fact_summary_df = pd.concat(fact_summary_frames, ignore_index=True)
    control_summary_df = pd.DataFrame(control_rows)
    main_summary_frame = control_summary_df[
        (control_summary_df["split_eval"] == "all") & (control_summary_df["analysis_variant"] == "all_families")
    ]
    if main_summary_frame.empty:
        main_summary_frame = control_summary_df[
            (control_summary_df["split_eval"] == "holdout") & (control_summary_df["analysis_variant"] == "all_families")
        ]

    profiles_path = output_path / "activation_profiles.jsonl"
    layer_path = output_path / "layer_similarity_summary.csv"
    fact_layer_path = output_path / "fact_layer_similarity.csv"
    fact_summary_path = output_path / "fact_invariance_summary.csv"
    control_summary_path = output_path / "control_variant_summary.csv"
    write_jsonl(profiles_path, [_profile_to_row(profile) for profile in profiles])
    layer_df.to_csv(layer_path, index=False)
    fact_layer_df.to_csv(fact_layer_path, index=False)
    fact_summary_df.to_csv(fact_summary_path, index=False)
    control_summary_df.to_csv(control_summary_path, index=False)

    sns.set_theme(style="whitegrid")
    for position in POSITIONS:
        frame = layer_df[layer_df["position"] == position].copy()
        plt.figure(figsize=(9, 4))
        sns.lineplot(data=frame, x="layer", y="invariance_gap", marker="o", color="#15616d", label="Invariance gap")
        sns.lineplot(
            data=frame,
            x="layer",
            y="family_centroid_separation",
            marker="o",
            color="#c05621",
            label="Family separation",
        )
        plt.axhline(0.0, color="#666666", linewidth=0.8, linestyle="--")
        plt.title(f"{model_spec.name}: {position} position dynamics")
        plt.tight_layout()
        plt.savefig(output_path / f"{position}_dynamics.png", dpi=200)
        plt.close()

    summary = {
        "model_name": model_spec.name,
        "model_family": model_spec.family,
        "model_variant": model_spec.variant,
        "num_prompts": len(profiles),
        "subject_invariance_depth_mean": float(
            main_summary_frame[main_summary_frame["position"] == "subject"]["invariance_depth_mean"].iloc[0]
        ),
        "preanswer_invariance_depth_mean": float(
            main_summary_frame[main_summary_frame["position"] == "preanswer"]["invariance_depth_mean"].iloc[0]
        ),
        "artifacts": {
            "profiles": str(profiles_path),
            "layer_similarity_summary": str(layer_path),
            "fact_layer_similarity": str(fact_layer_path),
            "fact_invariance_summary": str(fact_summary_path),
            "control_variant_summary": str(control_summary_path),
            "subject_dynamics_png": str(output_path / "subject_dynamics.png"),
            "preanswer_dynamics_png": str(output_path / "preanswer_dynamics.png"),
        },
    }
    write_json(output_path / "summary.json", summary)

    del bundle.model
    del bundle.tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return summary["artifacts"]


def run_storage_access_competition_suite(
    model_specs: list[ModelSpec],
    benchmark_path: str | Path,
    output_dir: str | Path,
    seed: int = 13,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    model_rows = []
    fact_rows = []
    summary_rows = []
    control_rows = []

    for model_spec in model_specs:
        model_output_dir = output_path / model_spec.name
        run_storage_access_competition_model(
            model_spec=model_spec,
            benchmark_path=benchmark_path,
            output_dir=model_output_dir,
            seed=seed,
        )
        summary = json.loads((model_output_dir / "summary.json").read_text(encoding="utf-8"))
        fact_df = pd.read_csv(summary["artifacts"]["fact_invariance_summary"])
        main_fact_df = fact_df[
            (fact_df["split_eval"] == "all") & (fact_df["analysis_variant"] == "all_families")
        ].copy()
        if main_fact_df.empty:
            main_fact_df = fact_df[
                (fact_df["split_eval"] == "holdout") & (fact_df["analysis_variant"] == "all_families")
            ].copy()
        subject_frame = main_fact_df[main_fact_df["position"] == "subject"]
        preanswer_frame = main_fact_df[main_fact_df["position"] == "preanswer"]
        summary_rows.append(
            {
                "model_name": summary["model_name"],
                "model_family": summary["model_family"],
                "model_variant": summary["model_variant"],
                "num_prompts": summary["num_prompts"],
                "subject_invariance_depth_mean": summary["subject_invariance_depth_mean"],
                "preanswer_invariance_depth_mean": summary["preanswer_invariance_depth_mean"],
                "subject_found_rate": float((subject_frame["invariance_depth"] >= 0).mean()),
                "preanswer_found_rate": float((preanswer_frame["invariance_depth"] >= 0).mean()),
                "subject_mean_invariance_gap": float(subject_frame["mean_invariance_gap"].mean()),
                "preanswer_mean_invariance_gap": float(preanswer_frame["mean_invariance_gap"].mean()),
            }
        )
        layer_df = pd.read_csv(summary["artifacts"]["layer_similarity_summary"])
        layer_df["model_name"] = model_spec.name
        layer_df["model_variant"] = model_spec.variant
        model_rows.append(layer_df)
        main_fact_df["model_name"] = model_spec.name
        main_fact_df["model_variant"] = model_spec.variant
        fact_rows.append(main_fact_df)
        control_df = pd.read_csv(summary["artifacts"]["control_variant_summary"])
        control_rows.append(control_df)

    combined_layers = pd.concat(model_rows, ignore_index=True)
    combined_facts = pd.concat(fact_rows, ignore_index=True)
    summary_df = pd.DataFrame(summary_rows)
    combined_controls = pd.concat(control_rows, ignore_index=True)
    combined_layers_path = output_path / "multimodel_layer_similarity_summary.csv"
    combined_facts_path = output_path / "multimodel_fact_invariance_summary.csv"
    summary_path = output_path / "multimodel_summary.csv"
    control_path = output_path / "multimodel_control_variant_summary.csv"
    combined_layers.to_csv(combined_layers_path, index=False)
    combined_facts.to_csv(combined_facts_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    combined_controls.to_csv(control_path, index=False)

    heatmap_paths = {}
    for position in POSITIONS:
        heatmap_rows = (
            combined_layers[combined_layers["position"] == position]
            .pivot(index="model_name", columns="layer", values="invariance_gap")
        )
        plt.figure(figsize=(10, 4))
        sns.heatmap(heatmap_rows, cmap="crest", center=0.0)
        plt.title(f"{position.capitalize()} invariance gap by model and layer")
        plt.tight_layout()
        heatmap_path = output_path / f"multimodel_{position}_invariance_heatmap.png"
        plt.savefig(heatmap_path, dpi=200)
        plt.close()
        heatmap_paths[position] = str(heatmap_path)

    report_lines = [
        "# Storage / Access / Competition Summary",
        "",
        "| model_name | variant | subject_depth_mean | preanswer_depth_mean | subject_found | preanswer_found |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in summary_df.itertuples(index=False):
        report_lines.append(
            f"| {row.model_name} | {row.model_variant} | {row.subject_invariance_depth_mean:.2f} | {row.preanswer_invariance_depth_mean:.2f} | {row.subject_found_rate:.3f} | {row.preanswer_found_rate:.3f} |"
        )
    report_path = output_path / "multimodel_storage_access_report.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    summary = {
        "num_models": len(model_specs),
        "artifacts": {
            "multimodel_layer_similarity_summary": str(combined_layers_path),
            "multimodel_fact_invariance_summary": str(combined_facts_path),
            "multimodel_summary": str(summary_path),
            "multimodel_control_variant_summary": str(control_path),
            "multimodel_subject_invariance_heatmap_png": heatmap_paths["subject"],
            "multimodel_preanswer_invariance_heatmap_png": heatmap_paths["preanswer"],
            "report": str(report_path),
        },
    }
    write_json(output_path / "summary.json", summary)
    return summary["artifacts"]


def build_storage_access_benchmark(
    output_dir: str | Path,
    limit_per_relation: int = 4,
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
