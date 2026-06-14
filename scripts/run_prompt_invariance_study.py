from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_yaml_config
from gemma_interp.prompt_invariance import (
    ModelSpec,
    build_multirelation_benchmark,
    run_multimodel_prompt_invariance,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a multi-model prompt-family invariance study")
    parser.add_argument("--config", default="configs/prompt_invariance_smoke.yaml")
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    benchmark_path = build_multirelation_benchmark(
        output_dir=config["benchmark_dir"],
        limit_per_relation=int(config.get("limit_per_relation", 4)),
        families=list(config.get("prompt_families", [])),
        relations=list(config.get("relations", [])),
        seed_facts_path=config.get("seed_facts_path", "data/factual_seed.json"),
    )
    model_specs = [ModelSpec(**row) for row in config["models"]]
    artifacts = run_multimodel_prompt_invariance(
        model_specs=model_specs,
        benchmark_path=benchmark_path,
        output_dir=config["output_dir"],
        max_new_tokens=int(config.get("max_new_tokens", 10)),
        top_neurons=int(config.get("top_neurons", 32)),
        ablation_neurons=int(config.get("ablation_neurons", 6)),
        bootstrap_samples=int(config.get("bootstrap_samples", 100)),
        seed=int(config.get("seed", 13)),
    )
    for key, value in artifacts.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
