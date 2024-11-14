from unittest import TestCase

import numpy as np

from foapy.characteristics.descriptive_information import descriptive_information
from foapy.constants_intervals import binding, mode


class Test_descriptive_information(TestCase):
    """
    Test list for descriptive_information calculate
    """

    def test_calculate_start_lossy_descriptive_information(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2.37956557896877])
        exists = descriptive_information(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2.58645791024])
        exists = descriptive_information(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_descriptive_information(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2.383831871])
        exists = descriptive_information(np.array(X), binding.end, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_descriptive_information(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2.52382717296366])
        exists = descriptive_information(np.array(X), binding.start, mode.redundant)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_descriptive_information(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2.971])
        exists = descriptive_information(np.array(X), binding.start, mode.cycle)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_descriptive_information(self):
        X = []
        expected = np.array([])
        exists = descriptive_information(np.array(X), binding.start, mode.lossy)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information_1(self):
        X = ["2", "4", "2", "2", "4"]
        expected = np.array([1.71450693])
        exists = descriptive_information(np.array(X), binding.start, mode.normal)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
