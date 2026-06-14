from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pandas as pd
import torch

from .dataset import FactExample
from .metrics import greedy_exact_match, target_margin, token_rank
from .modeling import ModelBundle, target_token_id, tokenize_prompt
from .utils import ensure_dir, write_json


def _restore_like(output, replacement):
    if isinstance(output, tuple):
        return (replacement,) + tuple(output[1:])
    return replacement


@contextmanager
def zero_module_output(module) -> Iterator[None]:
    def hook(_module, _inputs, output):
        tensor = output[0] if isinstance(output, tuple) else output
        return _restore_like(output, torch.zeros_like(tensor))

    handle = module.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


@contextmanager
def patch_module_output(module, cached_tensor: torch.Tensor) -> Iterator[None]:
    def hook(_module, _inputs, output):
        target = output[0] if isinstance(output, tuple) else output
        if tuple(target.shape) != tuple(cached_tensor.shape):
            return output
        return _restore_like(output, cached_tensor.to(target.device))

    handle = module.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


@contextmanager
def zero_attention_heads(attn_module, heads: list[int], head_dim: int) -> Iterator[None]:
    def pre_hook(_module, inputs):
        hidden = inputs[0].clone()
        for head in heads:
            start = head * head_dim
            end = min(hidden.shape[-1], start + head_dim)
            if start < hidden.shape[-1]:
                hidden[..., start:end] = 0
        return (hidden,)

    handle = attn_module.o_proj.register_forward_pre_hook(pre_hook)
    try:
        yield
    finally:
        handle.remove()


@contextmanager
def zero_module_weights(module) -> Iterator[None]:
    state = {name: param.detach().clone() for name, param in module.named_parameters(recurse=False)}
    try:
        for _, param in module.named_parameters(recurse=False):
            param.data.zero_()
        yield
    finally:
        for name, param in module.named_parameters(recurse=False):
            param.data.copy_(state[name])


def evaluate_prompt(
    bundle: ModelBundle,
    prompt: str,
    target_true: str,
    target_new: str,
    max_new_tokens: int,
    use_generation: bool = False,
) -> dict:
    inputs = tokenize_prompt(bundle, prompt)
    with torch.no_grad():
        outputs = bundle.model(**inputs)
    logits = outputs.logits[0, -1].float().cpu()
    true_id = target_token_id(bundle, target_true)
    new_id = target_token_id(bundle, target_new)
    rank = token_rank(logits, true_id)
    return {
        "target_rank": rank,
        "target_margin": target_margin(logits, true_id, new_id),
        "exact_match": greedy_exact_match(bundle, prompt, target_true, max_new_tokens=max_new_tokens)
        if use_generation
        else float(rank == 1),
    }


def _matched_control(example: FactExample, examples: list[FactExample]) -> FactExample | None:
    for candidate in examples:
        if candidate.case_id == example.case_id:
            continue
        if candidate.relation_id == example.relation_id:
            return candidate
    return examples[0] if examples else None


def run_causal_interventions(
    bundle: ModelBundle,
    examples: list[FactExample],
    output_dir: str | Path,
    max_examples: int,
    max_patch_examples: int,
    max_new_tokens: int,
) -> dict[str, str]:
    output_path = ensure_dir(output_dir)
    layer_rows: list[dict] = []
    component_rows: list[dict] = []
    patch_rows: list[dict] = []
    weight_rows: list[dict] = []

    selected = examples[:max_examples]
    head_dim = bundle.model.config.head_dim

    for example in selected:
        baseline = evaluate_prompt(bundle, example.canonical_prompt, example.target_true, example.target_new, max_new_tokens)
        control_example = _matched_control(example, selected)
        control_baseline = None
        if control_example is not None:
            control_baseline = evaluate_prompt(
                bundle,
                control_example.canonical_prompt,
                control_example.target_true,
                control_example.target_new,
                max_new_tokens,
            )

        for layer_idx, layer in enumerate(bundle.model.model.layers):
            for component_name, module in [
                ("layer", layer),
                ("attention", layer.self_attn),
                ("mlp", layer.mlp),
            ]:
                with zero_module_output(module):
                    perturbed = evaluate_prompt(
                        bundle,
                        example.canonical_prompt,
                        example.target_true,
                        example.target_new,
                        max_new_tokens,
                    )
                    control_metrics = None
                    if control_example is not None:
                        control_metrics = evaluate_prompt(
                            bundle,
                            control_example.canonical_prompt,
                            control_example.target_true,
                            control_example.target_new,
                            max_new_tokens,
                        )
                row = {
                    "case_id": example.case_id,
                    "relation_id": example.relation_id,
                    "layer": layer_idx,
                    "component": component_name,
                    "baseline_margin": baseline["target_margin"],
                    "ablated_margin": perturbed["target_margin"],
                    "margin_drop": baseline["target_margin"] - perturbed["target_margin"],
                    "baseline_rank": baseline["target_rank"],
                    "ablated_rank": perturbed["target_rank"],
                    "exact_match_drop": baseline["exact_match"] - perturbed["exact_match"],
                }
                if control_baseline and control_metrics:
                    row["collateral_margin_drop"] = control_baseline["target_margin"] - control_metrics["target_margin"]
                component_rows.append(row)

            for head in range(bundle.model.config.num_attention_heads):
                with zero_attention_heads(layer.self_attn, [head], head_dim):
                    perturbed = evaluate_prompt(
                        bundle,
                        example.canonical_prompt,
                        example.target_true,
                        example.target_new,
                        max_new_tokens,
                    )
                layer_rows.append(
                    {
                        "case_id": example.case_id,
                        "relation_id": example.relation_id,
                        "layer": layer_idx,
                        "head": head,
                        "baseline_margin": baseline["target_margin"],
                        "ablated_margin": perturbed["target_margin"],
                        "margin_drop": baseline["target_margin"] - perturbed["target_margin"],
                    }
                )

        if control_example is not None and example.case_id != control_example.case_id and len(patch_rows) < max_patch_examples * bundle.model.config.num_hidden_layers:
            for layer_idx, layer in enumerate(bundle.model.model.layers):
                cached = {}

                def save_output(_module, _inputs, output):
                    cached["value"] = (output[0] if isinstance(output, tuple) else output).detach().clone()

                handle = layer.self_attn.register_forward_hook(save_output)
                with torch.no_grad():
                    _ = bundle.model(**tokenize_prompt(bundle, example.canonical_prompt))
                handle.remove()

                if "value" not in cached:
                    continue
                with patch_module_output(layer.self_attn, cached["value"]):
                    patched = evaluate_prompt(
                        bundle,
                        control_example.canonical_prompt,
                        example.target_true,
                        example.target_new,
                        max_new_tokens,
                    )
                patch_rows.append(
                    {
                        "source_case_id": example.case_id,
                        "target_case_id": control_example.case_id,
                        "relation_id": example.relation_id,
                        "layer": layer_idx,
                        "patched_margin": patched["target_margin"],
                        "patched_rank": patched["target_rank"],
                    }
                )

        top_layer = max(
            [row for row in component_rows if row["case_id"] == example.case_id and row["component"] == "layer"],
            key=lambda row: row["margin_drop"],
        )
        chosen_layer = bundle.model.model.layers[top_layer["layer"]]
        for name, module in [("attn_o_proj", chosen_layer.self_attn.o_proj), ("mlp_down_proj", chosen_layer.mlp.down_proj)]:
            with zero_module_weights(module):
                zeroed = evaluate_prompt(
                    bundle,
                    example.canonical_prompt,
                    example.target_true,
                    example.target_new,
                    max_new_tokens,
                )
            weight_rows.append(
                {
                    "case_id": example.case_id,
                    "relation_id": example.relation_id,
                    "layer": top_layer["layer"],
                    "parameter_group": name,
                    "margin_drop": baseline["target_margin"] - zeroed["target_margin"],
                    "rank_change": zeroed["target_rank"] - baseline["target_rank"],
                }
            )

    component_df = pd.DataFrame(component_rows)
    head_df = pd.DataFrame(layer_rows)
    patch_df = pd.DataFrame(patch_rows)
    weight_df = pd.DataFrame(weight_rows)

    component_path = output_path / "component_ablation.csv"
    head_path = output_path / "head_ablation.csv"
    patch_path = output_path / "activation_patching.csv"
    weight_path = output_path / "weight_zeroing.csv"
    component_df.to_csv(component_path, index=False)
    head_df.to_csv(head_path, index=False)
    patch_df.to_csv(patch_path, index=False)
    weight_df.to_csv(weight_path, index=False)

    ranked_layers = (
        component_df[component_df["component"] == "layer"]
        .groupby("layer")["margin_drop"]
        .mean()
        .sort_values(ascending=False)
    )
    topk_rows = []
    ordered = ranked_layers.index.tolist()
    for k in range(1, len(ordered) + 1):
        subset = ordered[:k]
        drops = component_df[(component_df["component"] == "layer") & (component_df["layer"].isin(subset))]["margin_drop"]
        topk_rows.append({"k": k, "mean_margin_drop": float(drops.mean()) if not drops.empty else 0.0})
    topk_df = pd.DataFrame(topk_rows)
    topk_path = output_path / "topk_localization_curve.csv"
    topk_df.to_csv(topk_path, index=False)

    summary = {
        "component_ablation_path": str(component_path),
        "head_ablation_path": str(head_path),
        "activation_patching_path": str(patch_path),
        "weight_zeroing_path": str(weight_path),
        "topk_curve_path": str(topk_path),
    }
    write_json(output_path / "summary.json", summary)
    return summary
