from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_yaml_config
from gemma_interp.prompt_invariance import ModelSpec
from gemma_interp.storage_access_competition import (
    build_storage_access_benchmark,
    run_storage_access_competition_suite,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the storage/access/competition activation study")
    parser.add_argument("--config", default="configs/storage_access_competition_smoke.yaml")
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    benchmark_path = build_storage_access_benchmark(
        output_dir=config["benchmark_dir"],
        limit_per_relation=int(config.get("limit_per_relation", 4)),
        families=list(config.get("prompt_families", [])),
        relations=list(config.get("relations", [])),
        seed_facts_path=config.get("seed_facts_path", "data/factual_seed.json"),
    )
    model_specs = [ModelSpec(**row) for row in config["models"]]
    artifacts = run_storage_access_competition_suite(
        model_specs=model_specs,
        benchmark_path=benchmark_path,
        output_dir=config["output_dir"],
        seed=int(config.get("seed", 13)),
    )
    for key, value in artifacts.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
