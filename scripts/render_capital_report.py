from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.capital_study import write_capital_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the markdown report for the capital activation study")
    parser.add_argument("--output-dir", default="artifacts/results/capital_study")
    args = parser.parse_args()
    path = write_capital_report(args.output_dir)
    print(path)


if __name__ == "__main__":
    main()
