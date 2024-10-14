from unittest import TestCase

import numpy as np
import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.characteristics.ma.depth import depth


class TestMaDepth(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([4, 1.585, 1.585])
        exists = depth(X, 1, 1)
        assert_equal(expected, exists)

    def test_calculate_start_normal_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([4, 3.1699, 3.9069])
        exists = depth(X, 1, 2)
        assert_equal(expected, exists)

    def test_calculate_end_normal_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([4, 3.585, 2.585])
        exists = depth(X, 2, 2)
        assert_equal(expected, exists)

    def test_calculate_start_redunant_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([4, 5.1699, 4.9069])
        exists = depth(X, 1, 4)
        assert_equal(expected, exists)

    def test_calculate_start_cycle_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        expected = np.array([4, 4.1699, 4.1699])
        exists = depth(X, 1, 3)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_different_values_depth(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        expected = np.array([0, 0, 0, 0])
        exists = depth(X, 1, 1)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_empty_values_depth(self):
        X = ma.masked_array([])
        expected = np.array([])
        exists = depth(X, 1, 1)
        assert_equal(expected, exists)
