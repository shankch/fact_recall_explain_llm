from __future__ import annotations

import unittest

import numpy as np
import torch

from gemma_interp.subspace_interventions import (
    _random_component_like,
    _relation_control_fact_ids,
    _rescale_component,
    add_component,
    project_out_component,
)


class SubspaceInterventionTest(unittest.TestCase):
    def test_project_out_component_removes_parallel_part(self) -> None:
        vector = torch.tensor([3.0, 4.0])
        component = torch.tensor([3.0, 0.0])
        projected = project_out_component(vector, component)
        self.assertAlmostEqual(float(projected[0].item()), 0.0, places=6)
        self.assertAlmostEqual(float(projected[1].item()), 4.0, places=6)

    def test_add_component_shifts_vector(self) -> None:
        vector = torch.tensor([1.0, 2.0])
        component = torch.tensor([0.5, -1.0])
        shifted = add_component(vector, component, scale=2.0)
        self.assertAlmostEqual(float(shifted[0].item()), 2.0, places=6)
        self.assertAlmostEqual(float(shifted[1].item()), 0.0, places=6)

    def test_rescale_component_matches_template_norm(self) -> None:
        component = np.array([1.0, 0.0], dtype=np.float32)
        template = np.array([0.0, 3.0, 4.0], dtype=np.float32)
        scaled = _rescale_component(component=np.pad(component, (0, 1)), template=template)
        self.assertAlmostEqual(float(np.linalg.norm(scaled)), 5.0, places=6)

    def test_random_component_like_matches_norm(self) -> None:
        rng = np.random.default_rng(13)
        template = np.array([3.0, 4.0], dtype=np.float32)
        sample = _random_component_like(template=template, rng=rng)
        self.assertEqual(sample.shape, template.shape)
        self.assertAlmostEqual(float(np.linalg.norm(sample)), 5.0, places=6)

    def test_relation_control_fact_ids_stays_within_relation(self) -> None:
        mapping = _relation_control_fact_ids(
            {
                "capital:0": {"relation": "capital"},
                "capital:1": {"relation": "capital"},
                "currency:0": {"relation": "currency"},
                "currency:1": {"relation": "currency"},
            }
        )
        self.assertEqual(mapping["capital:0"], "capital:1")
        self.assertEqual(mapping["capital:1"], "capital:0")
        self.assertEqual(mapping["currency:0"], "currency:1")
        self.assertEqual(mapping["currency:1"], "currency:0")


if __name__ == "__main__":
    unittest.main()
