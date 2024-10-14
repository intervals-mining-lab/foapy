from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy.characteristics.volume import volume

class TestVolume(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([144])
        exists = volume(X, 1, 1)
        assert_array_equal(expected, exists)

    def test_calculate_start_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([2160])
        exists = volume(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_calculate_end_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([1152])
        exists = volume(X, 2, 2)
        assert_array_equal(expected, exists)

    def test_calculate_start_redunant_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([17280])
        exists = volume(X, 1, 4)
        assert_array_equal(expected, exists)

    def test_calculate_start_cycle_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = np.array([5184])
        exists = volume(X, 1, 3)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ["B", "A", "C", "D"]
        expected = np.array([1])
        exists = volume(X, 1, 1)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = []
        expected = np.array([])
        exists = volume(X, 1, 1)
        assert_array_equal(expected, exists)