from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class DatasetConfig:
    fact_source: str = "counterfact"
    raw_url: str = "https://rome.baulab.info/data/dsets/counterfact.json"
    output_dir: str = "artifacts/datasets/counterfact"
    raw_file: str = "raw_counterfact.json"
    prepared_file: str = "prepared_facts.jsonl"
    limit: int = 300
    paraphrases_per_fact: int = 3
    neighborhood_controls_per_fact: int = 3
    attribute_controls_per_fact: int = 3
    min_prompt_words: int = 3
    split_ratios: dict[str, float] = field(
        default_factory=lambda: {"dev": 0.6, "eval": 0.25, "stress": 0.15}
    )
    seed: int = 13


@dataclass
class ExperimentConfig:
    model_dir: str = "models/gemma-3-270m-it"
    output_root: str = "artifacts/results"
    seed: int = 13
    batch_size: int = 1
    max_examples: int = 48
    max_paraphrases: int = 2
    max_salience_examples: int = 12
    max_patch_examples: int = 12
    max_new_tokens: int = 8
    metric_set: list[str] = field(
        default_factory=lambda: ["target_rank", "target_margin", "exact_match"]
    )
    component_granularity: list[str] = field(
        default_factory=lambda: ["layer", "attention", "mlp", "head"]
    )
    intervention_types: list[str] = field(
        default_factory=lambda: ["ablation", "activation_patching", "weight_zeroing"]
    )
    dtype: str = "auto"
    require_cuda: bool = False


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_dataset_config(path: str | Path) -> DatasetConfig:
    return DatasetConfig(**load_yaml_config(path))


def load_experiment_config(path: str | Path) -> ExperimentConfig:
    return ExperimentConfig(**load_yaml_config(path))


def dump_config(path: str | Path, obj: DatasetConfig | ExperimentConfig) -> None:
    with Path(path).open("w", encoding="utf-8") as handle:
        yaml.safe_dump(asdict(obj), handle, sort_keys=False)
