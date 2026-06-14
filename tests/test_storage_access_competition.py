from __future__ import annotations

import unittest

from gemma_interp.storage_access_competition import first_sustained_layer


class StorageAccessCompetitionTest(unittest.TestCase):
    def test_first_sustained_layer_finds_first_valid_window(self) -> None:
        values = [-0.2, -0.1, 0.05, 0.12, 0.08]
        self.assertEqual(first_sustained_layer(values, threshold=0.0, sustain=2), 2)

    def test_first_sustained_layer_returns_negative_one_when_not_found(self) -> None:
        values = [-0.2, 0.1, -0.05, 0.02]
        self.assertEqual(first_sustained_layer(values, threshold=0.0, sustain=2), -1)


if __name__ == "__main__":
    unittest.main()
