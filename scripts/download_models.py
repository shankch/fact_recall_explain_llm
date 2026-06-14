#!/usr/bin/env python3
"""Download the six local checkpoints used by the paper from Hugging Face.

Model weights are intentionally NOT committed to this repository: together they
are ~7.8 GB, and several vendor licenses (notably Google Gemma) restrict
redistribution. Run this script once to populate the local ``models/``
directory that the experiment configs expect.

Usage:
    python scripts/download_models.py                       # all six models
    python scripts/download_models.py gemma-3-270m Qwen2.5-0.5B

Gemma checkpoints require Hugging Face authentication and acceptance of the
Gemma license on the model page first:
    huggingface-cli login
"""
from __future__ import annotations

import sys
from pathlib import Path

from huggingface_hub import snapshot_download

# local directory name -> Hugging Face repo id
MODELS = {
    "gemma-3-270m": "google/gemma-3-270m",
    "gemma-3-270m-it": "google/gemma-3-270m-it",
    "Qwen2.5-0.5B": "Qwen/Qwen2.5-0.5B",
    "Qwen2.5-0.5B-Instruct": "Qwen/Qwen2.5-0.5B-Instruct",
    "SmolLM2-360M": "HuggingFaceTB/SmolLM2-360M",
    "SmolLM2-360M-Instruct": "HuggingFaceTB/SmolLM2-360M-Instruct",
}


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    models_dir = root / "models"

    requested = argv or list(MODELS)
    unknown = [m for m in requested if m not in MODELS]
    if unknown:
        print(f"Unknown model(s): {', '.join(unknown)}")
        print(f"Available: {', '.join(MODELS)}")
        return 2

    for name in requested:
        repo_id = MODELS[name]
        target = models_dir / name
        print(f"Downloading {repo_id} -> {target}")
        snapshot_download(repo_id=repo_id, local_dir=str(target))

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
