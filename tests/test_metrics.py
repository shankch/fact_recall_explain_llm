from __future__ import annotations

import unittest

import torch

from gemma_interp.metrics import target_margin, token_rank


class MetricsTest(unittest.TestCase):
    def test_token_rank_and_margin(self) -> None:
        logits = torch.tensor([0.1, 0.8, 0.4, 0.2])
        self.assertEqual(token_rank(logits, 1), 1)
        self.assertEqual(token_rank(logits, 2), 2)
        self.assertAlmostEqual(target_margin(logits, 1, 2), 0.4, places=5)


if __name__ == "__main__":
    unittest.main()
