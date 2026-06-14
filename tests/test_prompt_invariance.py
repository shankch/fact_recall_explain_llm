from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from gemma_interp.prompt_invariance import (
    _holdout_selection_summary,
    build_multirelation_benchmark,
    score_answer,
)


class PromptInvarianceTest(unittest.TestCase):
    def test_score_answer_handles_multi_token_aliases(self) -> None:
        scores = score_answer("new delhi", ["New Delhi", "Delhi"])
        self.assertEqual(scores["full_exact_match"], 1.0)
        self.assertEqual(scores["contains_expected"], 1.0)
        self.assertGreaterEqual(scores["answer_f1"], 0.99)

    def test_build_multirelation_benchmark_creates_controls(self) -> None:
        country_payload = [
            {
                "name": {"common": "India"},
                "capital": ["New Delhi"],
                "languages": {"hin": "Hindi", "eng": "English"},
                "currencies": {"INR": {"name": "Indian rupee"}},
                "independent": True,
                "unMember": True,
            },
            {
                "name": {"common": "Japan"},
                "capital": ["Tokyo"],
                "languages": {"jpn": "Japanese"},
                "currencies": {"JPY": {"name": "Japanese yen"}},
                "independent": True,
                "unMember": True,
            },
        ]
        seed_payload = {
            "headquarters": [
                {"subject": "Apple", "object": "Cupertino", "aliases": ["Cupertino"]},
                {"subject": "Sony", "object": "Tokyo", "aliases": ["Tokyo"]},
            ],
            "birth_place": [
                {"subject": "Barack Obama", "object": "Honolulu", "aliases": ["Honolulu"]},
                {"subject": "Adele", "object": "London", "aliases": ["London"]},
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            seed_path = Path(temp_dir) / "seed.json"
            seed_path.write_text(json.dumps(seed_payload), encoding="utf-8")
            benchmark_path = build_multirelation_benchmark(
                output_dir=temp_dir,
                limit_per_relation=2,
                families=["raw_question", "declarative"],
                relations=["capital", "official_language", "currency", "headquarters", "birth_place"],
                country_payload=country_payload,
                seed_facts_path=seed_path,
            )
            rows = [json.loads(line) for line in benchmark_path.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(len(rows), 20)
        capital_row = next(row for row in rows if row["relation"] == "capital" and row["subject"] == "India")
        self.assertEqual(capital_row["same_subject_control_fact_id"], "official_language:0")
        self.assertEqual(capital_row["same_relation_control_fact_id"], "capital:1")
        self.assertTrue(capital_row["lexical_distractor"])
        self.assertEqual(capital_row["same_subject_control_answer"], "English")
        self.assertIn("English", capital_row["same_subject_control_aliases"])
        self.assertEqual(capital_row["same_relation_control_answer"], "Tokyo")
        self.assertIn("Tokyo", capital_row["same_relation_control_aliases"])
        self.assertIn("Tokyo", capital_row["lexical_distractor_aliases"])

    def test_holdout_selection_summary_uses_analysis_for_choice_and_holdout_for_eval(self) -> None:
        metrics = pd.DataFrame(
            [
                {"fact_id": "capital:0", "prompt_family": "qa", "split": "analysis", "answer_f1": 0.9, "target_selectivity": 0.8},
                {"fact_id": "capital:0", "prompt_family": "raw_question", "split": "analysis", "answer_f1": 0.1, "target_selectivity": 0.2},
                {"fact_id": "capital:1", "prompt_family": "qa", "split": "analysis", "answer_f1": 0.8, "target_selectivity": 0.7},
                {"fact_id": "capital:1", "prompt_family": "raw_question", "split": "analysis", "answer_f1": 0.2, "target_selectivity": 0.1},
                {"fact_id": "capital:2", "prompt_family": "qa", "split": "holdout", "answer_f1": 0.4, "target_selectivity": 0.3},
                {"fact_id": "capital:2", "prompt_family": "raw_question", "split": "holdout", "answer_f1": 0.1, "target_selectivity": 0.0},
                {"fact_id": "capital:3", "prompt_family": "qa", "split": "holdout", "answer_f1": 0.5, "target_selectivity": 0.4},
                {"fact_id": "capital:3", "prompt_family": "raw_question", "split": "holdout", "answer_f1": 0.2, "target_selectivity": 0.1},
            ]
        )
        summary = _holdout_selection_summary(metrics, bootstrap_samples=50, seed=13)
        self.assertEqual(summary.iloc[0]["analysis_best_answer_family"], "qa")
        self.assertEqual(summary.iloc[0]["analysis_worst_answer_family"], "raw_question")
        self.assertAlmostEqual(float(summary.iloc[0]["holdout_best_answer_f1"]), 0.45, places=6)
        self.assertAlmostEqual(float(summary.iloc[0]["holdout_worst_answer_f1"]), 0.15, places=6)


if __name__ == "__main__":
    unittest.main()
