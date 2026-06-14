from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_experiment_config
from gemma_interp.dataset import load_prepared_dataset
from gemma_interp.modeling import load_model_bundle
from gemma_interp.passive import run_passive_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Run passive factual-knowledge analyses")
    parser.add_argument("--config", default="configs/passive_analysis.yaml")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    examples = load_prepared_dataset(args.dataset)
    bundle = load_model_bundle(
        model_dir=config.model_dir,
        seed=config.seed,
        require_cuda=config.require_cuda,
        dtype=config.dtype,
    )
    outputs = run_passive_analysis(
        bundle=bundle,
        examples=examples,
        output_dir=config.output_root,
        max_examples=config.max_examples,
        max_paraphrases=config.max_paraphrases,
        max_salience_examples=config.max_salience_examples,
        max_new_tokens=config.max_new_tokens,
    )
    for key, value in outputs.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
