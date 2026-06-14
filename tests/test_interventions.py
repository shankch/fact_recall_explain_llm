from __future__ import annotations

import unittest

import torch
from torch import nn

from gemma_interp.interventions import zero_module_output, zero_module_weights


class InterventionTest(unittest.TestCase):
    def test_zero_module_output_restores_behavior(self) -> None:
        layer = nn.Linear(4, 4, bias=False)
        x = torch.ones(1, 4)
        baseline = layer(x)
        with zero_module_output(layer):
            zeroed = layer(x)
        restored = layer(x)
        self.assertTrue(torch.allclose(zeroed, torch.zeros_like(zeroed)))
        self.assertTrue(torch.allclose(baseline, restored))

    def test_zero_module_weights_restores_parameters(self) -> None:
        layer = nn.Linear(4, 4, bias=False)
        original = layer.weight.detach().clone()
        with zero_module_weights(layer):
            self.assertTrue(torch.allclose(layer.weight, torch.zeros_like(layer.weight)))
        self.assertTrue(torch.allclose(layer.weight, original))


if __name__ == "__main__":
    unittest.main()
