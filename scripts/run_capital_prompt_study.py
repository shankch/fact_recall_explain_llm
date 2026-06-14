from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gemma_interp.capital_study import build_capital_benchmark, run_capital_prompt_study
from gemma_interp.modeling import load_model_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a capital-city prompt activation study")
    parser.add_argument("--model-dir", default="models/gemma-3-270m-it")
    parser.add_argument("--benchmark-dir", default="artifacts/datasets/capital_prompts")
    parser.add_argument("--output-dir", default="artifacts/results/capital_study")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument(
        "--families",
        default="raw_question",
        help="Comma-separated prompt families: raw_question,declarative,qa,chat_template",
    )
    args = parser.parse_args()

    bundle = load_model_bundle(model_dir=args.model_dir, dtype="auto", require_cuda=False)
    families = [family.strip() for family in args.families.split(",") if family.strip()]
    benchmark_path = build_capital_benchmark(
        args.benchmark_dir,
        limit=args.limit,
        families=families,
        tokenizer=bundle.tokenizer,
    )
    artifacts = run_capital_prompt_study(bundle, benchmark_path, args.output_dir)
    for key, value in artifacts.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
