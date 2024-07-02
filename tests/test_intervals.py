from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy.intervals import intervals


class TestIntervals(TestCase):
    """
    Test list of array intervals
    """

    def test_int_start_none(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1])
        exists = intervals(X, 1, 1)
        assert_array_equal(expected, exists)

    def test_void(self):
        X = []
        expected = np.array([])
        exists = intervals(X, 1, 1)
        assert_array_equal(expected, exists)

    def test_int_end_none(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 1, 3])
        exists = intervals(X, 2, 1)
        assert_array_equal(expected, exists)

    def test_int_start_normal_1(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([1, 2, 2, 1, 3])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_string_start_normal_1(self):
        X = ["a", "b", "a", "c", "d"]
        expected = np.array([1, 2, 2, 4, 5])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_string_start_normal_2(self):
        X = ["a", "c", "c", "e", "d", "a"]
        expected = np.array([1, 2, 1, 4, 5, 5])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_int_start_normal_2(self):
        X = [0, 1, 2, 3, 4]
        expected = np.array([1, 2, 3, 4, 5])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_single_value_1(self):
        X = ["E"]
        expected = np.array([1])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_string_start_normal_3(self):
        X = ["E", "E", "E"]
        expected = np.array([1, 1, 1])
        exists = intervals(X, 1, 2)
        assert_array_equal(expected, exists)

    def test_int_end_normal_1(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1, 2, 1])
        exists = intervals(X, 2, 2)
        assert_array_equal(expected, exists)

    def test_int_end_normal_2(self):
        X = [0, 1, 2, 3, 4]
        expected = np.array([5, 4, 3, 2, 1])
        exists = intervals(X, 2, 2)
        assert_array_equal(expected, exists)
