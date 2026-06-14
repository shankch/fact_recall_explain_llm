from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from gemma_interp.config import DatasetConfig
from gemma_interp.dataset import load_prepared_dataset, prepare_counterfact


class DatasetPreparationTest(unittest.TestCase):
    def test_prepare_counterfact_creates_disjoint_splits(self) -> None:
        fixture_path = Path("tests/fixtures/mini_counterfact.json")
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_copy = Path(temp_dir) / "raw_counterfact.json"
            raw_copy.write_text(fixture_path.read_text(encoding="utf-8"), encoding="utf-8")
            config = DatasetConfig(
                raw_url="file://" + str(raw_copy.resolve()),
                output_dir=temp_dir,
                limit=3,
                paraphrases_per_fact=2,
                neighborhood_controls_per_fact=2,
                attribute_controls_per_fact=2,
            )
            prepared_path = prepare_counterfact(config)
            examples = load_prepared_dataset(prepared_path)

            self.assertEqual(len(examples), 3)
            splits = {example.case_id: example.split for example in examples}
            self.assertEqual(len(splits), len(set(splits)))
            self.assertIn("dev", splits.values())
            self.assertTrue(all(example.canonical_prompt for example in examples))


if __name__ == "__main__":
    unittest.main()
