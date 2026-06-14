#!/usr/bin/env python3
"""Download the large experiment artifacts from the companion Hugging Face
dataset back into this repo's ``artifacts/`` directory.

This restores the raw activation tensors, per-record dumps, and per-neuron score
dumps that are excluded from git, giving you a complete local copy without
re-running the studies.

Prerequisites:
    pip install huggingface_hub

Usage:
    python scripts/download_artifacts_hf.py --repo-id <user>/fact-recall-explain-llm-artifacts
"""
from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import snapshot_download


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Hugging Face dataset id, e.g. username/fact-recall-explain-llm-artifacts",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    artifacts = root / "artifacts"

    # Only fetch the heavy results/** payload; do not overwrite the repo's own
    # artifacts/README.md with the dataset card.
    snapshot_download(
        repo_id=args.repo_id,
        repo_type="dataset",
        local_dir=str(artifacts),
        allow_patterns=["results/**"],
    )
    print(f"Done. Artifacts restored under {artifacts / 'results'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
