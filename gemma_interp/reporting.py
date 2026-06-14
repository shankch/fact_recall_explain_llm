from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .utils import ensure_dir


def _savefig(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def generate_figures(passive_dir: str | Path, causal_dir: str | Path, output_dir: str | Path) -> dict[str, str]:
    sns.set_theme(style="whitegrid")
    output_path = ensure_dir(output_dir)
    figures: dict[str, str] = {}

    prompt_df = pd.read_csv(Path(passive_dir) / "prompt_metrics.csv")
    salience_df = pd.read_csv(Path(passive_dir) / "salience.csv")
    similarity_df = pd.read_csv(Path(passive_dir) / "paraphrase_similarity.csv")
    component_df = pd.read_csv(Path(causal_dir) / "component_ablation.csv")
    head_df = pd.read_csv(Path(causal_dir) / "head_ablation.csv")
    topk_df = pd.read_csv(Path(causal_dir) / "topk_localization_curve.csv")

    heatmap_df = salience_df.groupby(["relation_id", "layer"])["salience_norm"].mean().reset_index()
    heatmap_pivot = heatmap_df.pivot(index="relation_id", columns="layer", values="salience_norm").fillna(0.0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_pivot, cmap="magma")
    heatmap_path = output_path / "layerwise_factual_sensitivity_heatmap.png"
    _savefig(heatmap_path)
    figures["layerwise_factual_sensitivity_heatmap"] = str(heatmap_path)

    component_map = component_df.groupby(["layer", "component"])["margin_drop"].mean().reset_index()
    block_pivot = component_map.pivot(index="component", columns="layer", values="margin_drop").fillna(0.0)
    plt.figure(figsize=(10, 4))
    sns.heatmap(block_pivot, cmap="viridis")
    block_path = output_path / "block_contribution_map.png"
    _savefig(block_path)
    figures["block_contribution_map"] = str(block_path)

    plt.figure(figsize=(7, 4))
    sns.lineplot(data=topk_df, x="k", y="mean_margin_drop", marker="o")
    topk_path = output_path / "topk_ablation_curve.png"
    _savefig(topk_path)
    figures["topk_ablation_curve"] = str(topk_path)

    localization = component_df[component_df["component"] == "layer"].groupby("case_id")["margin_drop"].max()
    robustness = similarity_df.groupby("case_id")["cosine_similarity"].mean()
    merged = pd.DataFrame({"localization": localization, "robustness": robustness}).dropna()
    if not merged.empty:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=merged, x="robustness", y="localization")
        robustness_path = output_path / "paraphrase_robustness_vs_localization.png"
        _savefig(robustness_path)
        figures["paraphrase_robustness_vs_localization"] = str(robustness_path)

    collateral = component_df.dropna(subset=["collateral_margin_drop"]).copy()
    if not collateral.empty:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=collateral, x="collateral_margin_drop", y="margin_drop", hue="component")
        collateral_path = output_path / "collateral_damage_vs_factual_suppression.png"
        _savefig(collateral_path)
        figures["collateral_damage_vs_factual_suppression"] = str(collateral_path)

    if not head_df.empty:
        plt.figure(figsize=(8, 4))
        sns.barplot(data=head_df.groupby(["layer", "head"], as_index=False)["margin_drop"].mean(), x="layer", y="margin_drop", hue="head")
        head_path = output_path / "head_ablation_summary.png"
        _savefig(head_path)
        figures["head_ablation_summary"] = str(head_path)

    prompt_summary = (
        prompt_df.groupby(["split", "prompt_kind"])[["target_rank", "target_margin", "exact_match"]]
        .mean()
        .reset_index()
    )
    prompt_summary.to_csv(output_path / "benchmark_statistics.csv", index=False)
    component_df.groupby(["component", "layer"])[["margin_drop", "exact_match_drop"]].mean().reset_index().to_csv(
        output_path / "main_intervention_results.csv",
        index=False,
    )
    component_df.groupby("relation_id")[["margin_drop"]].mean().reset_index().to_csv(
        output_path / "robustness_by_relation.csv",
        index=False,
    )
    return figures
