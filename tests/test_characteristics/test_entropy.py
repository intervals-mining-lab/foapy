from unittest import TestCase

import numpy as np

from foapy.characteristics.entropy import entropy
from foapy.constants_intervals import binding, mode


class Test_entropy(TestCase):
    """
    Test list for entropy calculate
    """

    def test_calculate_start_lossy_entropy(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1.25069821459])
        exists = entropy(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_entropy(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1.3709777])
        exists = entropy(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_entropy(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1.2532824857])
        exists = entropy(np.array(X), binding.end, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_entropy(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1.335618955])
        exists = entropy(np.array(X), binding.start, mode.redundant)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_entropy(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1.571])
        exists = entropy(np.array(X), binding.start, mode.cycle)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_entropy(self):
        X = []
        expected = np.array([])
        exists = entropy(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_entropy_1(self):
        X = ["2", "4", "2", "2", "4"]
        expected = np.array([0.77779373752225])
        exists = entropy(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
