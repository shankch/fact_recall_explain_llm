from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.reporting import generate_figures


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate figures and tables for the Gemma study")
    parser.add_argument("--passive-dir", required=True)
    parser.add_argument("--causal-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    figures = generate_figures(args.passive_dir, args.causal_dir, args.output_dir)
    for name, path in figures.items():
        print(f"{name}={path}")


if __name__ == "__main__":
    main()
