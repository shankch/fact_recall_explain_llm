from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_yaml_config
from gemma_interp.prompt_invariance import ModelSpec
from gemma_interp.subspace_interventions import (
    build_subspace_benchmark,
    run_subspace_intervention_suite,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the fact-subspace intervention study")
    parser.add_argument("--config", default="configs/subspace_intervention_smoke.yaml")
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    benchmark_path = build_subspace_benchmark(
        output_dir=config["benchmark_dir"],
        limit_per_relation=int(config.get("limit_per_relation", 4)),
        families=list(config.get("prompt_families", [])),
        relations=list(config.get("relations", [])),
        seed_facts_path=config.get("seed_facts_path", "data/factual_seed.json"),
    )
    model_specs = [ModelSpec(**row) for row in config["models"]]
    artifacts = run_subspace_intervention_suite(
        model_specs=model_specs,
        benchmark_path=benchmark_path,
        output_dir=config["output_dir"],
        prompt_invariance_dir=config["prompt_invariance_dir"],
        storage_access_dir=config["storage_access_dir"],
        seed=int(config.get("seed", 13)),
        max_new_tokens=int(config.get("max_new_tokens", 10)),
        add_scale=float(config.get("add_scale", 1.0)),
    )
    for key, value in artifacts.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
