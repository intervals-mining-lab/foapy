from unittest import TestCase

import numpy as np
import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.characteristics.ma.volume import volume


class TestMaVolume(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([16, 3, 3])
        exists = volume(X, 1, 1)
        assert_equal(expected, exists)

    def test_calculate_start_normal_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([16, 9, 15])
        exists = volume(X, 1, 2)
        assert_equal(expected, exists)

    def test_calculate_end_normal_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([16, 12, 6])
        exists = volume(X, 2, 2)
        assert_equal(expected, exists)

    def test_calculate_start_redunant_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([16, 36, 30])
        exists = volume(X, 1, 4)
        assert_equal(expected, exists)

    def test_calculate_start_cycle_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([16, 18, 18])
        exists = volume(X, 1, 3)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        expected = np.array([1, 1, 1, 1])
        exists = volume(X, 1, 1)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = ma.masked_array([])
        expected = np.array([])
        exists = volume(X, 1, 1)
        assert_equal(expected, exists)
