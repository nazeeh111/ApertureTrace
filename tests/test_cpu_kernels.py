"""Small numerical contracts, not a full reconstruction or accuracy benchmark."""
import json
from pathlib import Path
import unittest

import h5py
import numpy as np
import torch

from utils import (Laplacian_and_Hessian, Sample_Lambertian,
                   Sample_Retroreflective, TotalVariation)

ROOT = Path(__file__).resolve().parents[1]
torch.set_num_threads(2)


class ForwardModels(unittest.TestCase):
    # Distances 2 and 5 m; cosines 1 and 4/5. Round-trip bins are 5 and 12
    # at 0.9 m per bin. Values are analytical radiometric weights per unit
    # intensity, independent of an archived implementation's output.
    models = ((Sample_Lambertian, [1 / 16, 256 / 390625]),
              (Sample_Retroreflective, [1 / 4, 16 / 625]))

    def sample(self, model, values, n_t=16):
        return model(values, [[0, 0, -2], [3, 0, -4]],
                     voxel_coordinates=[[0, 0, 0]] * values.numel(),
                     n_t=n_t, bin_resolution_t=0.9 / 3e8,
                     cuda=False, jitter=False, filter=False)

    def test_known_arrival_bins_amplitudes_and_gradients(self):
        for model, weights in self.models:
            with self.subTest(model=model.__name__):
                intensity = torch.tensor([2.0], requires_grad=True)
                actual = self.sample(model, intensity)
                expected = torch.zeros((2, 16))
                expected[0, 5], expected[1, 12] = 2 * weights[0], 2 * weights[1]
                torch.testing.assert_close(actual, expected)
                actual.sum().backward()
                torch.testing.assert_close(intensity.grad, torch.tensor([sum(weights)]))

    def test_colliding_returns_add(self):
        for model, _ in self.models:
            with self.subTest(model=model.__name__):
                actual = self.sample(model, torch.tensor([2.0, 3.0]))
                expected = self.sample(model, torch.tensor([5.0]))
                torch.testing.assert_close(actual, expected)

    def test_returns_outside_time_window_are_discarded(self):
        for model, weights in self.models:
            with self.subTest(model=model.__name__):
                actual = self.sample(model, torch.tensor([2.0]), n_t=8)
                expected = torch.zeros((2, 8))
                expected[0, 5] = 2 * weights[0]
                torch.testing.assert_close(actual, expected)


class Regularizers(unittest.TestCase):
    def test_constant_image_has_no_penalty(self):
        image = torch.ones((8, 8), requires_grad=True)
        laplacian, hessian = Laplacian_and_Hessian(image)
        self.assertEqual(TotalVariation(image).item(), 0)
        self.assertEqual(torch.count_nonzero(laplacian).item(), 0)
        self.assertEqual(torch.count_nonzero(hessian).item(), 0)
        (TotalVariation(image) + laplacian.square().sum() + hessian.square().sum()).backward()
        self.assertTrue(torch.isfinite(image.grad).all())

    def test_affine_ramp(self):
        image = torch.arange(8, dtype=torch.float32)[:, None] + torch.arange(8, dtype=torch.float32)[None, :]
        laplacian, hessian = Laplacian_and_Hessian(image)
        self.assertEqual(TotalVariation(image).item(), 112)
        self.assertEqual(tuple(laplacian.shape), (1, 1, 6, 6))
        self.assertEqual(tuple(hessian.shape), (1, 1, 4, 4))
        self.assertEqual(torch.count_nonzero(laplacian).item(), 0)
        self.assertEqual(torch.count_nonzero(hessian).item(), 0)


class CapturedData(unittest.TestCase):
    def test_included_datasets_match_recorded_shapes_and_are_finite(self):
        # The committed verification record identifies all 25 supplied files.
        recorded = json.loads((ROOT / "verification.json").read_text())["project"]["captured_data"]
        expected_paths = {item["file"] for item in recorded}
        actual_paths = {str(p.relative_to(ROOT)) for p in (ROOT / "captured_data").rglob("*.mat")}
        self.assertEqual(actual_paths, expected_paths)
        self.assertEqual(len(expected_paths), 25)
        for item in recorded:
            with self.subTest(file=item["file"]), h5py.File(ROOT / item["file"], "r") as capture:
                for dataset in item["datasets"]:
                    values = capture[dataset["key"]]
                    self.assertEqual(list(values.shape), dataset["shape"])
                    self.assertTrue(np.isfinite(values[...]).all())


if __name__ == "__main__":
    unittest.main()
