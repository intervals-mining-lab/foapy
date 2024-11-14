from unittest import TestCase

import numpy as np

from foapy.characteristics.uniformity import uniformity
from foapy.constants_intervals import binding, mode


class Test_uniformity(TestCase):
    """
    Test list for uniformity calculate
    """

    def test_calculate_start_lossy_uniformity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.22649821459])
        exists = uniformity(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        print(exists)
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_uniformity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.2632777])
        exists = uniformity(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_uniformity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.2362824857])
        exists = uniformity(np.array(X), binding.end, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_uniformity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.252818955])
        exists = uniformity(np.array(X), binding.start, mode.redundant)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_uniformity(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([0.337])
        exists = uniformity(np.array(X), binding.start, mode.cycle)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_uniformity(self):
        X = []
        expected = np.array([])
        exists = uniformity(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_uniformity_1(self):
        X = ["2", "4", "2", "2", "4"]
        expected = np.array([0.06080123752225])
        exists = uniformity(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
