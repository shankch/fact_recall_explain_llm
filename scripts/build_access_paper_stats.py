from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from math import comb, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


MODEL_LABELS = {
    "gemma_270m_base": "Gemma-3-270M",
    "gemma_270m_it": "Gemma-3-270M-IT",
    "qwen2_5_0_5b_base": "Qwen2.5-0.5B",
    "qwen2_5_0_5b_instruct": "Qwen2.5-0.5B-Instruct",
    "smollm2_360m_base": "SmolLM2-360M",
    "smollm2_360m_instruct": "SmolLM2-360M-Instruct",
}

FAMILY_LABELS = {
    "raw_question": "Raw question",
    "declarative": "Declarative",
    "qa": "Q/A",
    "chat_template": "Chat template",
}


@dataclass
class CIResult:
    mean: float
    ci_low: float
    ci_high: float
    pvalue: float | None = None
    n: int | None = None


def bootstrap_mean_ci(values: np.ndarray, samples: int = 400, seed: int = 13) -> CIResult:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return CIResult(mean=0.0, ci_low=0.0, ci_high=0.0, pvalue=None, n=0)
    rng = np.random.default_rng(seed)
    draws = [float(rng.choice(values, size=values.size, replace=True).mean()) for _ in range(samples)]
    return CIResult(
        mean=float(values.mean()),
        ci_low=float(np.quantile(draws, 0.025)),
        ci_high=float(np.quantile(draws, 0.975)),
        pvalue=None,
        n=int(values.size),
    )


def sign_test_pvalue(diffs: np.ndarray) -> float:
    values = np.asarray(diffs, dtype=float)
    non_zero = values[np.abs(values) > 1e-12]
    n = int(non_zero.size)
    if n == 0:
        return 1.0
    positive = int((non_zero > 0).sum())
    cutoff = min(positive, n - positive)
    probability = sum(comb(n, k) for k in range(cutoff + 1)) / (2 ** n)
    return float(min(1.0, 2 * probability))


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    phat = successes / total
    denom = 1 + z**2 / total
    center = (phat + z**2 / (2 * total)) / denom
    margin = z * sqrt((phat * (1 - phat) / total) + (z**2 / (4 * total**2))) / denom
    return (float(max(0.0, center - margin)), float(min(1.0, center + margin)))


def prompt_access_summary(prompt_dir: Path) -> dict:
    selection_df = pd.read_csv(prompt_dir / "multimodel_family_selection_summary.csv")
    holdout_df = pd.read_csv(prompt_dir / "multimodel_family_summary.csv")
    control_holdout_df = pd.read_csv(prompt_dir / "multimodel_control_summary.csv")
    rows = []
    for row in selection_df.to_dict("records"):
        model_name = str(row["model_name"])
        best_family = str(row["analysis_best_answer_family"])
        worst_family = str(row["analysis_worst_answer_family"])
        family_frame = holdout_df[holdout_df["model_name"] == model_name].set_index("prompt_family")
        control_frame = control_holdout_df[control_holdout_df["model_name"] == model_name].set_index("prompt_family")
        rows.append(
            {
                "model_name": model_name,
                "model_label": MODEL_LABELS.get(model_name, model_name),
                "best_family": best_family,
                "best_family_label": FAMILY_LABELS.get(best_family, best_family),
                "worst_family": worst_family,
                "worst_family_label": FAMILY_LABELS.get(worst_family, worst_family),
                "best_selectivity_family": str(row["analysis_best_selectivity_family"]),
                "selection_agrees": int(row["selection_agrees"]),
                "best_answer_f1": float(row["holdout_best_answer_f1"]),
                "best_selectivity": float(row["holdout_best_target_selectivity"]),
                "worst_answer_f1": float(row["holdout_worst_answer_f1"]),
                "worst_selectivity": float(row["holdout_worst_target_selectivity"]),
                "f1_diff": {
                    "mean": float(row["holdout_answer_f1_diff"]),
                    "ci_low": float(row["holdout_answer_f1_ci_low"]),
                    "ci_high": float(row["holdout_answer_f1_ci_high"]),
                    "pvalue": float(row["holdout_answer_f1_sign_test_pvalue"]),
                    "n": int(row["holdout_answer_f1_num_pairs"]),
                },
                "selectivity_diff": {
                    "mean": float(row["holdout_target_selectivity_diff"]),
                    "ci_low": float(row["holdout_target_selectivity_ci_low"]),
                    "ci_high": float(row["holdout_target_selectivity_ci_high"]),
                    "pvalue": float(row["holdout_target_selectivity_sign_test_pvalue"]),
                    "n": int(row["holdout_target_selectivity_num_pairs"]),
                },
                "holdout_family_means": {
                    family: {
                        "answer_f1": float(family_frame.loc[family, "answer_f1"]),
                        "target_selectivity": float(control_frame.loc[family, "target_selectivity"]),
                    }
                    for family in family_frame.index
                },
            }
        )
    return {
        "models": rows,
        "total_prompts": int(sum(row["f1_diff"]["n"] for row in rows) * len(FAMILY_LABELS)),
        "families_tested": sorted(FAMILY_LABELS.keys()),
    }


def competition_summary(prompt_dir: Path) -> dict:
    frames = []
    for model_dir in sorted(path for path in prompt_dir.iterdir() if path.is_dir()):
        metrics = pd.read_csv(model_dir / "prompt_metrics.csv")
        metrics = metrics[metrics["split"] == "holdout"].copy()
        metrics["model_name"] = model_dir.name
        frames.append(metrics)
    metrics_df = pd.concat(frames, ignore_index=True)
    failures = metrics_df[(metrics_df["answer_f1"] <= 0.0) & (metrics_df["max_control_f1"] > 0.0)]
    control_counts = failures["dominant_control"].value_counts().to_dict()
    return {
        "failure_with_control_count": int(failures.shape[0]),
        "failure_with_control_rate": float(failures.shape[0] / metrics_df.shape[0]),
        "dominant_control_counts": {str(key): int(value) for key, value in control_counts.items()},
        "dominant_control_rates": {
            str(key): float(value / failures.shape[0]) for key, value in control_counts.items()
        }
        if failures.shape[0]
        else {},
    }


def invariance_summary(storage_dir: Path) -> dict:
    fact_df = pd.read_csv(storage_dir / "multimodel_fact_invariance_summary.csv")
    model_df = pd.read_csv(storage_dir / "multimodel_summary.csv")
    control_df = pd.read_csv(storage_dir / "multimodel_control_variant_summary.csv")
    position_summary = {}
    for position in ["subject", "preanswer"]:
        subset = fact_df[fact_df["position"] == position]
        successes = int((subset["invariance_depth"] >= 0).sum())
        total = int(subset.shape[0])
        low, high = wilson_interval(successes, total)
        depth_vals = subset[subset["invariance_depth"] >= 0]["invariance_depth"].to_numpy(dtype=float)
        depth_ci = bootstrap_mean_ci(depth_vals)
        gap_vals = subset["mean_invariance_gap"].to_numpy(dtype=float)
        gap_ci = bootstrap_mean_ci(gap_vals)
        position_summary[position] = {
            "found_count": successes,
            "total_count": total,
            "found_rate": float(successes / total),
            "found_rate_ci_low": low,
            "found_rate_ci_high": high,
            "depth": asdict(depth_ci),
            "mean_gap": asdict(gap_ci),
        }
    relation_rows = (
        fact_df[fact_df["position"] == "subject"]
        .groupby("relation")[["mean_invariance_gap", "peak_invariance_gap"]]
        .agg({"mean_invariance_gap": "mean", "peak_invariance_gap": "max"})
        .reset_index()
        .to_dict("records")
    )
    relation_found = (
        fact_df[fact_df["position"] == "subject"]
        .assign(found=lambda df: (df["invariance_depth"] >= 0).astype(float))
        .groupby("relation")["found"]
        .mean()
        .to_dict()
    )
    for row in relation_rows:
        row["found_rate"] = float(relation_found[row["relation"]])
    variant_rows = []
    for (split_eval, variant, position), subset in control_df.groupby(["split_eval", "analysis_variant", "position"]):
        total = int(subset["num_facts"].sum())
        successes = int(round(float((subset["found_rate"] * subset["num_facts"]).sum())))
        low, high = wilson_interval(successes, total)
        weighted_gap = (
            float((subset["mean_invariance_gap"] * subset["num_facts"]).sum()) / total if total else 0.0
        )
        weighted_peak_gap = (
            float((subset["peak_invariance_gap"] * subset["num_facts"]).sum()) / total if total else 0.0
        )
        depth_num = float(
            (
                subset["invariance_depth_mean"].clip(lower=0.0)
                * subset["found_rate"]
                * subset["num_facts"]
            ).sum()
        )
        depth_mean = (depth_num / successes) if successes else -1.0
        variant_rows.append(
            {
                "split_eval": str(split_eval),
                "analysis_variant": str(variant),
                "position": str(position),
                "found_count": successes,
                "total_count": total,
                "found_rate": float(successes / total) if total else 0.0,
                "found_rate_ci_low": low,
                "found_rate_ci_high": high,
                "depth": {
                    "mean": float(depth_mean),
                    "ci_low": float(depth_mean),
                    "ci_high": float(depth_mean),
                    "pvalue": None,
                    "n": successes,
                },
                "mean_gap": {
                    "mean": float(weighted_gap),
                    "ci_low": float(weighted_gap),
                    "ci_high": float(weighted_gap),
                    "pvalue": None,
                    "n": total,
                },
                "peak_gap_weighted_mean": float(weighted_peak_gap),
            }
        )
    return {
        "overall": position_summary,
        "per_model": model_df.to_dict("records"),
        "subject_relation_summary": relation_rows,
        "variant_summary": variant_rows,
        "controls": control_df.to_dict("records"),
    }


def ablation_summary(prompt_dir: Path) -> dict:
    frames = []
    for model_dir in sorted(path for path in prompt_dir.iterdir() if path.is_dir()):
        ablation_path = model_dir / "neuron_ablation.csv"
        if not ablation_path.exists():
            continue
        ablation = pd.read_csv(ablation_path)
        ablation["model_name"] = model_dir.name
        frames.append(ablation)
    ablation_df = pd.concat(frames, ignore_index=True)
    overall = (
        ablation_df.groupby("candidate_type")[["answer_f1_drop", "target_selectivity_drop"]]
        .mean()
        .reset_index()
        .to_dict("records")
    )
    return {"overall": overall}


def subspace_summary(subspace_dir: Path) -> dict:
    summary_df = pd.read_csv(subspace_dir / "multimodel_subspace_intervention_summary.csv")
    detail_df = pd.read_csv(subspace_dir / "multimodel_subspace_interventions.csv")
    primary_summary_df = summary_df[summary_df["layer_strategy"] == "primary"].copy()
    if primary_summary_df.empty:
        primary_summary_df = summary_df.copy()
    aggregate = {
        "project_fact_alignment_delta_mean": float(primary_summary_df["project_best_alignment_delta_mean"].mean()),
        "project_control_alignment_delta_mean": float(primary_summary_df["project_best_control_alignment_delta_mean"].mean()),
        "project_random_alignment_delta_mean": float(primary_summary_df["project_best_random_alignment_delta_mean"].mean()),
        "project_fact_answer_f1_delta_mean": float(primary_summary_df["project_best_answer_f1_delta_mean"].mean()),
        "project_control_answer_f1_delta_mean": float(primary_summary_df["project_best_control_answer_f1_delta_mean"].mean()),
        "project_random_answer_f1_delta_mean": float(primary_summary_df["project_best_random_answer_f1_delta_mean"].mean()),
        "patch_fact_alignment_delta_mean": float(primary_summary_df["patch_worst_alignment_delta_mean"].mean()),
        "patch_control_alignment_delta_mean": float(primary_summary_df["patch_worst_control_alignment_delta_mean"].mean()),
        "patch_random_alignment_delta_mean": float(primary_summary_df["patch_worst_random_alignment_delta_mean"].mean()),
        "patch_fact_answer_f1_delta_mean": float(primary_summary_df["patch_worst_answer_f1_delta_mean"].mean()),
        "patch_control_answer_f1_delta_mean": float(primary_summary_df["patch_worst_control_answer_f1_delta_mean"].mean()),
        "patch_random_answer_f1_delta_mean": float(primary_summary_df["patch_worst_random_answer_f1_delta_mean"].mean()),
    }
    comparisons = {}
    for key, lhs, rhs in [
        (
            "project_alignment_target_vs_control",
            detail_df["project_best_control_alignment_delta"] - detail_df["project_best_alignment_delta"],
            "fact projection causes more alignment loss than matched-control projection",
        ),
        (
            "project_alignment_target_vs_random",
            detail_df["project_best_random_alignment_delta"] - detail_df["project_best_alignment_delta"],
            "fact projection causes more alignment loss than random projection",
        ),
        (
            "project_f1_target_vs_control",
            detail_df["project_best_control_answer_f1_delta"] - detail_df["project_best_answer_f1_delta"],
            "fact projection causes more F1 loss than matched-control projection",
        ),
        (
            "project_f1_target_vs_random",
            detail_df["project_best_random_answer_f1_delta"] - detail_df["project_best_answer_f1_delta"],
            "fact projection causes more F1 loss than random projection",
        ),
        (
            "patch_alignment_target_vs_control",
            detail_df["patch_worst_alignment_delta"] - detail_df["patch_worst_control_alignment_delta"],
            "fact patching causes more alignment gain than matched-control patching",
        ),
        (
            "patch_alignment_target_vs_random",
            detail_df["patch_worst_alignment_delta"] - detail_df["patch_worst_random_alignment_delta"],
            "fact patching causes more alignment gain than random patching",
        ),
        (
            "patch_f1_target_vs_control",
            detail_df["patch_worst_answer_f1_delta"] - detail_df["patch_worst_control_answer_f1_delta"],
            "fact patching causes more F1 gain than matched-control patching",
        ),
        (
            "patch_f1_target_vs_random",
            detail_df["patch_worst_answer_f1_delta"] - detail_df["patch_worst_random_answer_f1_delta"],
            "fact patching causes more F1 gain than random patching",
        ),
    ]:
        diff = np.asarray(lhs, dtype=float)
        ci = bootstrap_mean_ci(diff)
        ci.pvalue = sign_test_pvalue(diff)
        comparisons[key] = {
            "description": rhs,
            **asdict(ci),
        }
    layer_robustness_df = pd.read_csv(subspace_dir / "multimodel_layer_strategy_robustness.csv")
    layer_robustness = {
        "per_model": layer_robustness_df.to_dict("records"),
    }
    if {"primary", "plus_one"}.issubset(layer_robustness_df.columns):
        delta = layer_robustness_df["plus_one"] - layer_robustness_df["primary"]
        layer_robustness["primary_vs_plus_one_alignment_delta"] = asdict(bootstrap_mean_ci(delta.to_numpy(dtype=float)))
        same_sign = (
            np.sign(layer_robustness_df["primary"].to_numpy(dtype=float))
            == np.sign(layer_robustness_df["plus_one"].to_numpy(dtype=float))
        )
        layer_robustness["same_sign_rate"] = float(same_sign.mean()) if same_sign.size else 0.0
    return {
        "per_model": primary_summary_df.to_dict("records"),
        "per_model_all_layers": summary_df.to_dict("records"),
        "aggregate": aggregate,
        "comparisons": comparisons,
        "layer_robustness": layer_robustness,
    }


def build_markdown(summary: dict) -> str:
    lines = ["# Paper Stats Summary", ""]
    lines.append("## Prompt Access")
    lines.append("")
    lines.append("| Model | Best family | Worst family | Best F1 | F1 diff [95% CI] | p-value | Selectivity diff [95% CI] | p-value |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary["prompt_access"]["models"]:
        lines.append(
            f"| {row['model_label']} | {row['best_family_label']} | {row['worst_family_label']} | "
            f"{row['best_answer_f1']:.4f} | "
            f"{row['f1_diff']['mean']:.4f} [{row['f1_diff']['ci_low']:.4f}, {row['f1_diff']['ci_high']:.4f}] | "
            f"{row['f1_diff']['pvalue']:.4g} | "
            f"{row['selectivity_diff']['mean']:.4f} [{row['selectivity_diff']['ci_low']:.4f}, {row['selectivity_diff']['ci_high']:.4f}] | "
            f"{row['selectivity_diff']['pvalue']:.4g} |"
        )
    lines.append("")
    lines.append("## Invariance")
    for position, payload in summary["invariance"]["overall"].items():
        lines.append(
            f"- {position}: {payload['found_count']}/{payload['total_count']} "
            f"({payload['found_rate']:.4f}; 95% CI {payload['found_rate_ci_low']:.4f} to {payload['found_rate_ci_high']:.4f}), "
            f"depth {payload['depth']['mean']:.4f} [{payload['depth']['ci_low']:.4f}, {payload['depth']['ci_high']:.4f}]"
        )
    lines.append("")
    lines.append("## Competition")
    comp = summary["competition"]
    lines.append(
        f"- failure-with-control count: {comp['failure_with_control_count']} "
        f"({comp['failure_with_control_rate']:.4f} of prompts)"
    )
    for key, value in sorted(comp["dominant_control_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Subspace")
    for key, payload in summary["subspace"]["comparisons"].items():
        lines.append(
            f"- {key}: {payload['mean']:.4f} [{payload['ci_low']:.4f}, {payload['ci_high']:.4f}], p={payload['pvalue']:.4g}"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build aligned statistics for the IEEE Access manuscript.")
    parser.add_argument("--prompt-dir", default="artifacts/results/prompt_invariance_access_r2")
    parser.add_argument("--storage-dir", default="artifacts/results/storage_access_competition_access_r2")
    parser.add_argument("--subspace-dir", default="artifacts/results/subspace_intervention_access_r2")
    parser.add_argument("--output-json", default="paper/paper_stats_access.json")
    parser.add_argument("--output-md", default="paper/paper_stats_access.md")
    args = parser.parse_args()

    summary = {
        "prompt_access": prompt_access_summary(Path(args.prompt_dir)),
        "competition": competition_summary(Path(args.prompt_dir)),
        "invariance": invariance_summary(Path(args.storage_dir)),
        "ablation": ablation_summary(Path(args.prompt_dir)),
        "subspace": subspace_summary(Path(args.subspace_dir)),
    }
    output_json = Path(args.output_json)
    output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    output_md = Path(args.output_md)
    output_md.write_text(build_markdown(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
