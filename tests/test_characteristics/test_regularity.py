from unittest import TestCase

import numpy as np

from foapy.characteristics.regularity import regularity
from foapy.constants_intervals import binding, mode


class Test_regularity(TestCase):
    """
    Test list for regularity calculate
    """

    def test_calculate_start_lossy_regularity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.8547])
        exists = regularity(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_regularity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.8332])
        exists = regularity(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_regularity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.8489])
        exists = regularity(np.array(X), binding.end, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_regularity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.8393])
        exists = regularity(np.array(X), binding.start, mode.redundant)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_regularity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.7917])
        exists = regularity(np.array(X), binding.start, mode.cycle)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_regularity_1(self):
        X = ["2", "4", "2", "2", "4"]
        expected = np.array([0.9587])
        exists = regularity(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
