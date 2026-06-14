from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch

from .modeling import ModelBundle, target_token_id, tokenize_prompt
from .utils import ensure_dir, write_json, write_jsonl


COUNTRY_ALIASES = {
    "United States": "USA",
    "United Kingdom": "UK",
    "Czechia": "Czech Republic",
    "Republic of the Congo": "Congo",
}

PROMPT_FAMILIES = [
    "raw_question",
    "declarative",
    "qa",
    "chat_template",
]


@dataclass
class CapitalPrompt:
    country: str
    prompt_country: str
    capital: str
    prompt: str
    model_input: str
    prompt_family: str
    split: str


def _base_question(prompt_country: str) -> str:
    return f"What is the capital of {prompt_country}?"


def _render_prompt(tokenizer, prompt_country: str, family: str) -> tuple[str, str]:
    question = _base_question(prompt_country)
    if family == "raw_question":
        return question, question
    if family == "declarative":
        prompt = f"The capital of {prompt_country} is"
        return prompt, prompt
    if family == "qa":
        prompt = f"Q: {question}\nA:"
        return prompt, prompt
    if family == "chat_template":
        user_prompt = f"{question} Answer with only the capital city."
        model_input = tokenizer.apply_chat_template(
            [{"role": "user", "content": user_prompt}],
            tokenize=False,
            add_generation_prompt=True,
        )
        return user_prompt, model_input
    raise ValueError(f"Unknown prompt family: {family}")


def build_capital_benchmark(
    output_dir: str | Path,
    limit: int = 100,
    seed: int = 13,
    families: list[str] | None = None,
    tokenizer=None,
) -> Path:
    del seed
    if families is None:
        families = ["raw_question"]
    if tokenizer is None:
        raise ValueError("A tokenizer is required to build the capital benchmark.")
    output_path = ensure_dir(output_dir)
    raw_path = output_path / "restcountries_capitals_raw.json"
    processed_path = output_path / "capital_prompts.jsonl"

    url = "https://restcountries.com/v3.1/all?fields=name,capital,cca2,cca3,independent,unMember"
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.load(response)
    write_json(raw_path, payload)

    rows: list[CapitalPrompt] = []
    filtered = [
        item
        for item in payload
        if item.get("independent")
        and item.get("unMember")
        and item.get("capital")
        and item["capital"]
        and item.get("name", {}).get("common")
    ]
    filtered.sort(key=lambda item: item["name"]["common"])
    chosen = filtered[:limit]

    for idx, item in enumerate(chosen):
        country = item["name"]["common"]
        prompt_country = COUNTRY_ALIASES.get(country, country)
        split = "analysis" if idx < int(limit * 0.8) else "holdout"
        for family in families:
            prompt, model_input = _render_prompt(tokenizer, prompt_country, family)
            rows.append(
                CapitalPrompt(
                    country=country,
                    prompt_country=prompt_country,
                    capital=item["capital"][0],
                    prompt=prompt,
                    model_input=model_input,
                    prompt_family=family,
                    split=split,
                )
            )

    write_jsonl(processed_path, [row.__dict__ for row in rows])
    return processed_path


def _hook_prompt(bundle: ModelBundle, prompt: str) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray], any]:
    attn_outputs: dict[int, np.ndarray] = {}
    mlp_outputs: dict[int, np.ndarray] = {}
    handles = []

    for layer_idx, layer in enumerate(bundle.model.model.layers):
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


def _normalize_generation(generated: str, prompt: str, prompt_country: str) -> str:
    text = generated.strip()
    patterns = [
        rf"^the capital of {re.escape(prompt_country.lower())} is",
        rf"^q:\s*what is the capital of {re.escape(prompt_country.lower())}\?\s*a:\s*",
        r"^a[:)\].-]*\s*",
        r"^answer[:)\].-]*\s*",
    ]
    lowered = text.lower()
    for pattern in patterns:
        lowered = re.sub(pattern, "", lowered).strip()
    lowered = re.sub(r"^[\s:,\-\.\)\(]+", "", lowered).strip()
    lowered = lowered.split("\n")[0].strip()
    return lowered


def _answer_metrics(normalized_generated: str, expected_capital: str) -> tuple[float, float]:
    expected = expected_capital.lower().strip()
    prefix_match = float(normalized_generated.startswith(expected))
    contains_match = float(expected in normalized_generated)
    return prefix_match, contains_match


def analyze_single_capital_prompt(
    bundle: ModelBundle,
    prompt: str,
    expected_capital: str,
    top_k: int = 24,
    model_input: str | None = None,
    prompt_country: str | None = None,
) -> dict:
    actual_input = model_input or prompt
    actual_country = prompt_country or ""
    attn_outputs, mlp_outputs, outputs = _hook_prompt(bundle, actual_input)
    logits = outputs.logits[0, -1].float().cpu()
    target_id = target_token_id(bundle, expected_capital)
    top_prediction = int(torch.argmax(logits).item())

    hidden_norms = [float(torch.norm(hidden[0, -1].detach().float().cpu()).item()) for hidden in outputs.hidden_states[1:]]
    attn_norms = [float(np.linalg.norm(attn_outputs[layer])) for layer in sorted(attn_outputs)]
    mlp_mean_abs = [float(np.abs(mlp_outputs[layer]).mean()) for layer in sorted(mlp_outputs)]

    flat = []
    for layer, values in mlp_outputs.items():
        for neuron_idx, value in enumerate(values):
            flat.append((layer, neuron_idx, float(value)))
    flat.sort(key=lambda item: abs(item[2]), reverse=True)
    top_neurons = [
        {"layer": layer, "neuron": neuron, "activation": activation}
        for layer, neuron, activation in flat[:top_k]
    ]

    generated_ids = bundle.model.generate(**tokenize_prompt(bundle, actual_input), max_new_tokens=8, do_sample=False)
    prompt_ids = tokenize_prompt(bundle, actual_input)["input_ids"]
    generated = bundle.tokenizer.decode(generated_ids[0][prompt_ids.shape[1] :], skip_special_tokens=True).strip()
    normalized_generated = _normalize_generation(generated, prompt, actual_country)
    exact_match, contains_expected = _answer_metrics(normalized_generated, expected_capital)

    return {
        "prompt": prompt,
        "model_input": actual_input,
        "expected_capital": expected_capital,
        "target_token_id": target_id,
        "target_rank": int((torch.argsort(logits, descending=True) == target_id).nonzero(as_tuple=False)[0].item() + 1),
        "target_margin": float(logits[target_id].item() - torch.topk(logits, k=2).values[1].item()),
        "exact_match": exact_match,
        "contains_expected": contains_expected,
        "top_prediction": _token_repr(bundle, top_prediction),
        "top_tokens": _top_tokens(bundle, logits),
        "generated_text": generated,
        "normalized_generated_text": normalized_generated,
        "layer_hidden_norms": hidden_norms,
        "layer_attention_norms": attn_norms,
        "layer_mlp_mean_abs": mlp_mean_abs,
        "top_neurons": top_neurons,
        "mlp_activations": {str(layer): values.tolist() for layer, values in mlp_outputs.items()},
    }


def _markdown_table(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in df.itertuples(index=False):
        values = [str(value) for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_capital_report(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    summary = json.loads((output_path / "summary.json").read_text(encoding="utf-8"))
    neuron_summary = pd.read_csv(output_path / "capital_neuron_summary.csv")
    metrics = pd.read_csv(output_path / "capital_prompt_metrics.csv")
    family_summary_path = output_path / "capital_prompt_family_summary.csv"
    family_summary = pd.read_csv(family_summary_path) if family_summary_path.exists() else None

    top_shared = neuron_summary.sort_values("sharedness", ascending=False).head(12)
    top_country_hits = metrics.sort_values(["exact_match", "target_rank"], ascending=[False, True]).head(10)[
        ["country", "prompt_family", "expected_capital", "top_prediction", "target_rank", "exact_match", "contains_expected"]
    ]

    lines = [
        "# Capital Prompt Study",
        "",
        f"- Prompts analyzed: {summary['num_prompts']}",
        f"- Mean exact match: {summary['mean_exact_match']:.4f}",
        f"- Mean contains-expected: {summary['mean_contains_expected']:.4f}",
        f"- Mean target rank: {summary['mean_target_rank']:.2f}",
        f"- Mean target margin: {summary['mean_target_margin']:.4f}",
        f"- Strongest shared layer by mean MLP activity: {summary['strongest_shared_layer']}",
        f"- Best prompt family by target rank: {summary.get('best_prompt_family_by_rank', 'n/a')}",
        "",
    ]
    if family_summary is not None:
        lines.extend(
            [
                "## Prompt family comparison",
                "",
                _markdown_table(family_summary.round(4)),
                "",
            ]
        )
    lines.extend(
        [
        "## Shared neuron candidates",
        "",
        _markdown_table(top_shared),
        "",
        "## Best prompt outcomes",
        "",
        _markdown_table(top_country_hits),
        ]
    )
    report_path = output_path / "capital_study_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def run_capital_prompt_study(
    bundle: ModelBundle,
    benchmark_path: str | Path,
    output_dir: str | Path,
    top_neurons: int = 128,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    with Path(benchmark_path).open("r", encoding="utf-8") as handle:
        prompts = [json.loads(line) for line in handle if line.strip()]

    profile_rows = []
    norm_rows = []
    all_mlp = []

    for row in prompts:
        profile = analyze_single_capital_prompt(
            bundle,
            row["prompt"],
            row["capital"],
            model_input=row.get("model_input"),
            prompt_country=row["prompt_country"],
        )
        profile.update(
            {
                "country": row["country"],
                "prompt_country": row["prompt_country"],
                "prompt_family": row.get("prompt_family", "raw_question"),
                "split": row["split"],
            }
        )
        profile_rows.append(profile)

        mlp_matrix = np.stack([np.array(profile["mlp_activations"][str(layer)]) for layer in range(bundle.model.config.num_hidden_layers)])
        all_mlp.append(mlp_matrix)

        for layer_idx, (hidden_norm, attn_norm, mlp_norm) in enumerate(
            zip(profile["layer_hidden_norms"], profile["layer_attention_norms"], profile["layer_mlp_mean_abs"])
        ):
            norm_rows.append(
                {
                    "country": row["country"],
                    "prompt": row["prompt"],
                    "prompt_family": row.get("prompt_family", "raw_question"),
                    "layer": layer_idx,
                    "hidden_norm": hidden_norm,
                    "attention_norm": attn_norm,
                    "mlp_mean_abs": mlp_norm,
                }
            )

    mlp_tensor = np.stack(all_mlp)
    mean_abs = np.abs(mlp_tensor).mean(axis=0)
    flat_scores = []
    for layer in range(mean_abs.shape[0]):
        for neuron in range(mean_abs.shape[1]):
            flat_scores.append((layer, neuron, float(mean_abs[layer, neuron]), float(mlp_tensor[:, layer, neuron].std())))
    flat_scores.sort(key=lambda item: item[2], reverse=True)
    top_selected = flat_scores[:top_neurons]

    heatmap_matrix = []
    heatmap_columns = []
    for layer, neuron, _mean_abs, _std in top_selected:
        heatmap_columns.append(f"L{layer}:N{neuron}")
    for prompt_idx in range(mlp_tensor.shape[0]):
        heatmap_matrix.append([float(mlp_tensor[prompt_idx, layer, neuron]) for layer, neuron, _, _ in top_selected])

    heatmap_df = pd.DataFrame(heatmap_matrix, columns=heatmap_columns)
    heatmap_df.insert(0, "prompt", [row["prompt"] for row in profile_rows])
    heatmap_df.insert(0, "country", [row["country"] for row in profile_rows])

    neuron_summary = pd.DataFrame(
        [
            {
                "layer": layer,
                "neuron": neuron,
                "mean_abs_activation": mean_abs_value,
                "activation_std": std_value,
                "sharedness": float(mean_abs_value / (std_value + 1e-6)),
            }
            for layer, neuron, mean_abs_value, std_value in top_selected
        ]
    )

    profile_jsonl = output_path / "capital_prompt_profiles.jsonl"
    metrics_csv = output_path / "capital_prompt_metrics.csv"
    norms_csv = output_path / "capital_layer_component_norms.csv"
    heatmap_csv = output_path / "capital_top_neuron_heatmap.csv"
    neuron_csv = output_path / "capital_neuron_summary.csv"
    npz_path = output_path / "capital_mlp_activations.npz"

    write_jsonl(
        profile_jsonl,
        [
            {key: value for key, value in row.items() if key != "mlp_activations"}
            for row in profile_rows
        ],
    )
    pd.DataFrame(
        [
            {
                "country": row["country"],
                "prompt": row["prompt"],
                "prompt_family": row.get("prompt_family", "raw_question"),
                "expected_capital": row["expected_capital"],
                "top_prediction": row["top_prediction"],
                "generated_text": row["generated_text"],
                "normalized_generated_text": row["normalized_generated_text"],
                "target_rank": row["target_rank"],
                "target_margin": row["target_margin"],
                "exact_match": row["exact_match"],
                "contains_expected": row["contains_expected"],
            }
            for row in profile_rows
        ]
    ).to_csv(metrics_csv, index=False)
    pd.DataFrame(norm_rows).to_csv(norms_csv, index=False)
    heatmap_df.to_csv(heatmap_csv, index=False)
    neuron_summary.to_csv(neuron_csv, index=False)
    np.savez_compressed(npz_path, mlp_activations=mlp_tensor)

    metrics_df = pd.read_csv(metrics_csv)
    family_summary = (
        metrics_df.groupby("prompt_family")[["target_rank", "target_margin", "exact_match", "contains_expected"]]
        .agg(["mean", "median"])
        .reset_index()
    )
    family_summary.columns = [
        "prompt_family",
        "target_rank_mean",
        "target_rank_median",
        "target_margin_mean",
        "target_margin_median",
        "exact_match_mean",
        "exact_match_median",
        "contains_expected_mean",
        "contains_expected_median",
    ]
    family_summary_path = output_path / "capital_prompt_family_summary.csv"
    family_summary.to_csv(family_summary_path, index=False)

    sns.set_theme(style="whitegrid")
    prompt_order = [f"{row['country']} [{row['prompt_family']}]" for row in profile_rows]
    prompt_heatmap = heatmap_df.drop(columns=["country", "prompt"]).to_numpy()
    plt.figure(figsize=(16, 14))
    sns.heatmap(prompt_heatmap, cmap="magma", yticklabels=prompt_order, xticklabels=heatmap_columns)
    plt.xlabel("Top globally active MLP neurons")
    plt.ylabel("Capital prompts")
    plt.xticks(rotation=90)
    plt.tight_layout()
    prompt_heatmap_path = output_path / "capital_prompt_neuron_heatmap.png"
    plt.savefig(prompt_heatmap_path, dpi=200)
    plt.close()

    norm_df = pd.DataFrame(norm_rows)
    layer_heatmap = (
        norm_df.assign(country_family=lambda frame: frame["country"] + " [" + frame["prompt_family"] + "]")
        .pivot(index="country_family", columns="layer", values="hidden_norm")
        .reindex(prompt_order)
    )
    plt.figure(figsize=(12, 14))
    sns.heatmap(layer_heatmap, cmap="viridis")
    plt.xlabel("Layer")
    plt.ylabel("Capital prompts")
    plt.tight_layout()
    layer_heatmap_path = output_path / "capital_layer_hidden_heatmap.png"
    plt.savefig(layer_heatmap_path, dpi=200)
    plt.close()

    component_summary = norm_df.groupby("layer")[["hidden_norm", "attention_norm", "mlp_mean_abs"]].mean().reset_index()
    plt.figure(figsize=(12, 4))
    component_melt = component_summary.melt(id_vars="layer", var_name="component", value_name="value")
    sns.barplot(data=component_melt, x="layer", y="value", hue="component")
    plt.tight_layout()
    component_path = output_path / "capital_architecture_component_profile.png"
    plt.savefig(component_path, dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.barplot(data=family_summary, x="prompt_family", y="contains_expected_mean", color="#bf4d28")
    plt.xticks(rotation=20)
    plt.tight_layout()
    family_contains_path = output_path / "capital_prompt_family_contains_expected.png"
    plt.savefig(family_contains_path, dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.barplot(data=family_summary, x="prompt_family", y="target_rank_median", color="#1d7f73")
    plt.xticks(rotation=20)
    plt.tight_layout()
    family_rank_path = output_path / "capital_prompt_family_rank_median.png"
    plt.savefig(family_rank_path, dpi=200)
    plt.close()

    family_layer_summary = norm_df.groupby(["prompt_family", "layer"])[["hidden_norm", "attention_norm", "mlp_mean_abs"]].mean().reset_index()
    family_layer_summary_path = output_path / "capital_prompt_family_layer_summary.csv"
    family_layer_summary.to_csv(family_layer_summary_path, index=False)

    summary = {
        "num_prompts": len(profile_rows),
        "mean_exact_match": float(np.mean([row["exact_match"] for row in profile_rows])),
        "mean_contains_expected": float(np.mean([row["contains_expected"] for row in profile_rows])),
        "mean_target_rank": float(np.mean([row["target_rank"] for row in profile_rows])),
        "mean_target_margin": float(np.mean([row["target_margin"] for row in profile_rows])),
        "strongest_shared_layer": int(component_summary.sort_values("mlp_mean_abs", ascending=False).iloc[0]["layer"]),
        "best_prompt_family_by_rank": family_summary.sort_values("target_rank_mean").iloc[0]["prompt_family"],
        "artifacts": {
            "profiles": str(profile_jsonl),
            "metrics": str(metrics_csv),
            "norms": str(norms_csv),
            "heatmap_csv": str(heatmap_csv),
            "neuron_summary": str(neuron_csv),
            "family_summary": str(family_summary_path),
            "family_layer_summary": str(family_layer_summary_path),
            "prompt_heatmap_png": str(prompt_heatmap_path),
            "layer_heatmap_png": str(layer_heatmap_path),
            "component_profile_png": str(component_path),
            "family_contains_png": str(family_contains_path),
            "family_rank_png": str(family_rank_path),
        },
    }
    write_json(output_path / "summary.json", summary)

    report_path = write_capital_report(output_path)
    return {key: value for key, value in summary["artifacts"].items()}
