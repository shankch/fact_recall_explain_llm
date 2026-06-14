#!/usr/bin/env python3
"""Upload the large, regenerable experiment artifacts to a Hugging Face dataset.

These files are excluded from git (see ../.gitignore) because they are big and
deterministically regenerable. Hosting them on the Hub gives reviewers the exact
artifacts behind the paper without bloating the code repo. The dataset mirrors
this repo's ``artifacts/`` directory (so the heavy files live under ``results/``).

Prerequisites:
    pip install huggingface_hub
    huggingface-cli login        # use a token with WRITE access

Usage:
    python scripts/upload_artifacts_hf.py --repo-id <user>/fact-recall-explain-llm-artifacts
    python scripts/upload_artifacts_hf.py --repo-id <user>/... --private
"""
from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import HfApi

# Paths are relative to the repo's artifacts/ directory.
HEAVY_PATTERNS = [
    "results/**/*.npz",
    "results/**/*.jsonl",
    "results/**/neuron_scores.csv",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Hugging Face dataset id, e.g. username/fact-recall-explain-llm-artifacts",
    )
    parser.add_argument(
        "--private", action="store_true", help="create the dataset as private"
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    artifacts = root / "artifacts"

    api = HfApi()
    api.create_repo(
        repo_id=args.repo_id,
        repo_type="dataset",
        private=args.private,
        exist_ok=True,
    )

    # Dataset card -> the dataset's README.md.
    card = artifacts / "hf_dataset_card.md"
    if card.exists():
        api.upload_file(
            path_or_fileobj=str(card),
            path_in_repo="README.md",
            repo_id=args.repo_id,
            repo_type="dataset",
            commit_message="Add dataset card",
        )

    # Heavy artifacts, preserving the results/** structure.
    upload_large = getattr(api, "upload_large_folder", None)
    if upload_large is not None:
        upload_large(
            repo_id=args.repo_id,
            repo_type="dataset",
            folder_path=str(artifacts),
            allow_patterns=HEAVY_PATTERNS,
        )
    else:  # older huggingface_hub
        api.upload_folder(
            repo_id=args.repo_id,
            repo_type="dataset",
            folder_path=str(artifacts),
            allow_patterns=HEAVY_PATTERNS,
            commit_message="Upload heavy experiment artifacts",
        )

    print(f"Done: https://huggingface.co/datasets/{args.repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
