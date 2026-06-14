from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.config import load_dataset_config
from gemma_interp.dataset import prepare_counterfact


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare CounterFact-style benchmark for Gemma research")
    parser.add_argument("--config", default="configs/dataset_counterfact.yaml")
    args = parser.parse_args()

    config = load_dataset_config(args.config)
    path = prepare_counterfact(config)
    print(path)


if __name__ == "__main__":
    main()
