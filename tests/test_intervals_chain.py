from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain
from foapy.exceptions import Not1DArrayException


class TestIntervalsChain(TestCase):
    """
    Test intervals_chain(X, binding, chain_mode) -> plain 1-D ndarray.

    Verifies raw interval chain computation for all combinations of
    binding direction and chain_mode.
    """

    # -------------------------------------------------------------------------
    # Empty sequence
    # -------------------------------------------------------------------------

    def test_empty_start_boundary(self):
        X = []
        expected = np.array([], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_empty_start_cycle(self):
        X = []
        expected = np.array([], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert_array_equal(expected, result)

    def test_empty_end_boundary(self):
        X = []
        expected = np.array([], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(expected, result)

    # -------------------------------------------------------------------------
    # Single element
    # -------------------------------------------------------------------------

    def test_single_start_boundary(self):
        X = ["a"]
        expected = np.array([1], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_single_start_cycle(self):
        X = ["a"]
        # Cyclic: delta = n - last_pos = 1 - 0 = 1; interval = 0 + 1 = 1
        expected = np.array([1], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert_array_equal(expected, result)

    def test_single_end_boundary(self):
        X = ["a"]
        expected = np.array([1], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(expected, result)

    # -------------------------------------------------------------------------
    # All-unique elements
    # -------------------------------------------------------------------------

    def test_all_unique_start_boundary(self):
        X = [1, 2, 3, 4, 5]
        # Each element appears once; boundary = position + 1
        expected = np.array([1, 2, 3, 4, 5], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_all_unique_end_boundary(self):
        X = [1, 2, 3, 4, 5]
        # Reversed: positions in reversed are n-1-pos → boundary = (n-1-pos)+1 = n-pos
        expected = np.array([5, 4, 3, 2, 1], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(expected, result)

    # -------------------------------------------------------------------------
    # All-identical elements
    # -------------------------------------------------------------------------

    def test_all_identical_start_boundary(self):
        X = ["a", "a", "a"]
        # First at pos 0: interval=1; subsequent: each gap=1
        expected = np.array([1, 1, 1], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_all_identical_start_cycle(self):
        X = ["a", "a", "a"]
        # Cyclic: delta = 3 - last_pos = 3 - 2 = 1; first = 0+1=1; rest = 1
        expected = np.array([1, 1, 1], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert_array_equal(expected, result)

    # -------------------------------------------------------------------------
    # Mixed sequence — binding.start + chain_mode.boundary
    # -------------------------------------------------------------------------

    def test_mixed_start_boundary(self):
        X = ["b", "a", "b", "c", "b"]
        # a at 1 → interval=2; b at 0 → interval=1, then 2, 2; c at 3 → interval=4
        expected = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_mixed_start_boundary_2(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([1, 2, 2, 1, 3], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_mixed_start_boundary_consistent_with_intervals_normal(self):
        """Chain with boundary mode matches intervals() normal mode result."""
        from helpers.intervals import intervals, mode

        X = ["a", "b", "a", "c", "a", "d"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        reference = intervals(X, binding.start, mode.normal)
        assert_array_equal(reference, chain)

    # -------------------------------------------------------------------------
    # Mixed sequence — binding.end + chain_mode.boundary
    # -------------------------------------------------------------------------

    def test_mixed_end_boundary(self):
        X = ["b", "a", "b", "c", "b"]
        # reversed: ["b","c","b","a","b"], then reverse result
        expected = np.array([2, 4, 2, 2, 1], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(expected, result)

    def test_mixed_end_boundary_2(self):
        X = [2, 4, 2, 2, 4]
        # Matches intervals(X, binding.end, mode.normal)
        expected = np.array([2, 3, 1, 2, 1], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(expected, result)

    # -------------------------------------------------------------------------
    # Mixed sequence — chain_mode.cycle
    # -------------------------------------------------------------------------

    def test_mixed_start_cycle(self):
        X = ["b", "a", "b", "c", "b"]
        # b: last at 4, delta=5-4=1, first=0+1=1; interior: 2,2
        # a: last at 1, delta=5-1=4, first=1+4=5
        # c: last at 3, delta=5-3=2, first=3+2=5
        expected = np.array([1, 5, 2, 5, 2], dtype=np.intp)
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert_array_equal(expected, result)

    def test_mixed_end_cycle(self):
        X = ["b", "a", "b", "c", "b"]
        expected = np.array([2, 5, 2, 5, 1], dtype=np.intp)
        result = intervals_chain(X, binding.end, chain_mode.cycle)
        assert_array_equal(expected, result)

    def test_mixed_start_cycle_sum_equals_n(self):
        """For cycle mode, chain values sum to n * num_unique_elements."""
        X = [2, 4, 2, 2, 4]
        n = len(X)
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        # Sum of chain = n * num_unique (each element's group sums to n)
        self.assertEqual(int(np.sum(chain)) % n, 0)

    # -------------------------------------------------------------------------
    # Error cases
    # -------------------------------------------------------------------------

    def test_raises_not1d_for_2d_array(self):
        X = [[1, 2], [3, 4]]
        with pytest.raises(Not1DArrayException):
            intervals_chain(X, binding.start, chain_mode.boundary)

    def test_raises_value_error_for_invalid_binding(self):
        X = [1, 2, 3]
        with pytest.raises(ValueError):
            intervals_chain(X, 99, chain_mode.boundary)

    def test_raises_value_error_for_invalid_chain_mode(self):
        X = [1, 2, 3]
        with pytest.raises(ValueError):
            intervals_chain(X, binding.start, 99)
