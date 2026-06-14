from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_experiment_config
from gemma_interp.dataset import load_prepared_dataset
from gemma_interp.interventions import run_causal_interventions
from gemma_interp.modeling import load_model_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Run causal interventions for Gemma factual recall")
    parser.add_argument("--config", default="configs/causal_intervention.yaml")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    examples = [example for example in load_prepared_dataset(args.dataset) if example.split in {"eval", "stress"}]
    bundle = load_model_bundle(
        model_dir=config.model_dir,
        seed=config.seed,
        require_cuda=config.require_cuda,
        dtype=config.dtype,
    )
    outputs = run_causal_interventions(
        bundle=bundle,
        examples=examples,
        output_dir=config.output_root,
        max_examples=config.max_examples,
        max_patch_examples=config.max_patch_examples,
        max_new_tokens=config.max_new_tokens,
    )
    for key, value in outputs.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
