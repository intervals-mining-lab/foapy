from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy import binding, intervals, mode


class TestIntervals(TestCase):
    """
    Test list of array intervals
    """

    def test_int_start_none(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 1, 3])
        exists = intervals(X, binding.start, mode.lossy)
        assert_array_equal(expected, exists)

    def test_void(self):
        X = []
        expected = np.array([])
        exists = intervals(X, binding.start, mode.lossy)
        assert_array_equal(expected, exists)

    def test_int_end_none(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1])
        exists = intervals(X, binding.end, mode.lossy)
        assert_array_equal(expected, exists)

    def test_int_start_normal_1(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([1, 2, 2, 1, 3])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_string_start_normal_1(self):
        X = ["a", "b", "a", "c", "d"]
        expected = np.array([1, 2, 2, 4, 5])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_string_start_normal_2(self):
        X = ["a", "c", "c", "e", "d", "a"]
        expected = np.array([1, 2, 1, 4, 5, 5])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_int_start_normal_2(self):
        X = [0, 1, 2, 3, 4]
        expected = np.array([1, 2, 3, 4, 5])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_single_value_1(self):
        X = ["E"]
        expected = np.array([1])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_string_start_normal_3(self):
        X = ["E", "E", "E"]
        expected = np.array([1, 1, 1])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_int_end_normal_1(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1, 2, 1])
        exists = intervals(X, binding.end, mode.normal)
        assert_array_equal(expected, exists)

    def test_int_end_normal_2(self):
        X = [0, 1, 2, 3, 4]
        expected = np.array([5, 4, 3, 2, 1])
        exists = intervals(X, binding.end, mode.normal)
        assert_array_equal(expected, exists)

    def test_int_start_cycle(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 2, 2, 1, 3])
        exists = intervals(X, binding.start, mode.cycle)
        assert_array_equal(expected, exists)

    def test_int_end_cycle(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1, 2, 2])
        exists = intervals(X, binding.end, mode.cycle)
        assert_array_equal(expected, exists)

    def test_dna_start_normal(self):
        X = ["ATC", "CTG", "ATC"]
        expected = np.array([1, 2, 2])
        exists = intervals(X, binding.start, mode.normal)
        assert_array_equal(expected, exists)

    def test_int_start_redundant(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([1, 2, 2, 1, 2, 3, 1])
        exists = intervals(X, binding.start, mode.redundant)
        assert_array_equal(expected, exists)

    def test_int_end_redundant(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([1, 2, 2, 3, 1, 2, 1])
        exists = intervals(X, binding.end, mode.redundant)
        assert_array_equal(expected, exists)

    def test_single_redundant(self):
        X = ["E"]
        expected = np.array([1, 1])
        exists = intervals(X, binding.start, mode.redundant)
        assert_array_equal(expected, exists)

    def test_string_start_redundant(self):
        X = ["E", "E", "E"]
        expected = np.array([1, 1, 1, 1])
        exists = intervals(X, binding.start, mode.redundant)
        assert_array_equal(expected, exists)

    def test_dna_start_redundant(self):
        X = ["ATC", "CTG", "ATC"]
        expected = np.array([1, 2, 2, 2, 1])
        exists = intervals(X, binding.start, mode.redundant)
        assert_array_equal(expected, exists)

    def test_ValueError_mode_1(self):
        X = [2, 4, 2, 2, 4]
        with pytest.raises(ValueError) as e_info:
            intervals(X, 2, 5)
            self.assertEqual(
                "Invalid mode value. Use mode.lossy,normal,cycle or redundant.",
                e_info.message,
            )

    def test_ValueError_mode_2(self):
        X = [2, 4, 2, 2, 4]
        with pytest.raises(ValueError) as e_info:
            intervals(X, binding.start, 10)
            self.assertEqual(
                "Invalid mode value. Use mode.lossy,normal,cycle or redundant.",
                e_info.message,
            )

    def test_ValueError_binding_1(self):
        X = [2, 4, 2, 2, 4]
        with pytest.raises(ValueError) as e_info:
            intervals(X, 3, 4)
            self.assertEqual(
                "Invalid binding value. Use binding.start or binding.end.",
                e_info.message,
            )

    def test_ValueError_binding_2(self):
        X = [2, 4, 2, 2, 4]
        with pytest.raises(ValueError) as e_info:
            intervals(X, 3, mode.redundant)
            self.assertEqual(
                "Invalid binding value. Use binding.start or binding.end.",
                e_info.message,
            )
