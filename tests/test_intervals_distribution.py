from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import (
    intervals_chain,
    intervals_distribution,
    intervals_tuple,
    tuple_mode,
)


class TestIntervalsDistribution(TestCase):
    """
    Test intervals_distribution(tuple_result) -> ndarray.

    Result[i] = count of interval value (i+1) in tuple_result.
    Length = max(tuple_result).
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_returns_empty(self):
        result = intervals_distribution(np.array([], dtype=np.intp))
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_empty_list_returns_empty(self):
        result = intervals_distribution([])
        assert_array_equal(result, np.array([], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Single-element tuple
    # -------------------------------------------------------------------------

    def test_single_value_one(self):
        # [1] → one interval of length 1 → distribution = [1]
        result = intervals_distribution(np.array([1], dtype=np.intp))
        assert_array_equal(result, np.array([1], dtype=np.intp))

    def test_single_value_three(self):
        # [3] → distribution = [0, 0, 1]
        result = intervals_distribution(np.array([3], dtype=np.intp))
        assert_array_equal(result, np.array([0, 0, 1], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Known tuple with expected counts
    # -------------------------------------------------------------------------

    def test_all_ones(self):
        # [1, 1, 1] → three intervals of length 1 → [3]
        result = intervals_distribution(np.array([1, 1, 1], dtype=np.intp))
        assert_array_equal(result, np.array([3], dtype=np.intp))

    def test_mixed_values(self):
        # [1, 2, 2, 4, 2] → 1 one, 3 twos, 0 threes, 1 four → [1, 3, 0, 1]
        result = intervals_distribution(np.array([1, 2, 2, 4, 2], dtype=np.intp))
        assert_array_equal(result, np.array([1, 3, 0, 1], dtype=np.intp))

    def test_max_value_determines_length(self):
        # max value = 5 → length 5
        result = intervals_distribution(np.array([1, 5, 2, 5, 2], dtype=np.intp))
        self.assertEqual(len(result), 5)

    # -------------------------------------------------------------------------
    # All-equal tuple — single non-zero position
    # -------------------------------------------------------------------------

    def test_all_equal_values(self):
        # [3, 3, 3] → distribution = [0, 0, 3]
        result = intervals_distribution(np.array([3, 3, 3], dtype=np.intp))
        assert_array_equal(result, np.array([0, 0, 3], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Integration with intervals_chain + intervals_tuple
    # -------------------------------------------------------------------------

    def test_pipeline_distribution_sum_equals_input_length(self):
        # The sum of distribution counts must equal the number of intervals
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        normal_result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        dist = intervals_distribution(normal_result)
        self.assertEqual(int(np.sum(dist)), len(normal_result))

    def test_pipeline_lossy_distribution(self):
        # Lossy intervals [2, 2] for X=["b","a","b","c","b"] → distribution = [0, 2]
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        lossy = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        dist = intervals_distribution(lossy)
        assert_array_equal(dist, np.array([0, 2], dtype=np.intp))
