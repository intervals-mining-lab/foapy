from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain, intervals_tuple, tuple_mode


class TestIntervalsTuple(TestCase):
    """
    Test intervals_tuple(chain, tuple_mode) -> ndarray.

    Verifies that boundary handling (lossy / normal / redundant) is applied
    correctly to chains produced by intervals_chain.
    """

    # -------------------------------------------------------------------------
    # Empty chain — all modes return empty array
    # -------------------------------------------------------------------------

    def test_empty_normal(self):
        chain = np.array([], dtype=np.intp)
        assert_array_equal(
            intervals_tuple(chain, tuple_mode.normal), np.array([], dtype=np.intp)
        )

    def test_empty_lossy(self):
        chain = np.array([], dtype=np.intp)
        assert_array_equal(
            intervals_tuple(chain, tuple_mode.lossy), np.array([], dtype=np.intp)
        )

    def test_empty_redundant(self):
        chain = np.array([], dtype=np.intp)
        assert_array_equal(
            intervals_tuple(chain, tuple_mode.redundant), np.array([], dtype=np.intp)
        )

    # -------------------------------------------------------------------------
    # Invalid tuple_mode raises ValueError
    # -------------------------------------------------------------------------

    def test_invalid_tuple_mode_raises(self):
        chain = np.array([1, 2, 2], dtype=np.intp)
        with pytest.raises(ValueError):
            intervals_tuple(chain, 99)

    # -------------------------------------------------------------------------
    # tuple_mode.normal — returns chain unchanged
    # -------------------------------------------------------------------------

    def test_normal_boundary_start(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.normal)
        assert_array_equal(result, chain)

    def test_normal_boundary_end(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.normal)
        assert_array_equal(result, chain)

    def test_normal_cycle_start(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        result = intervals_tuple(chain, tuple_mode.normal)
        assert_array_equal(result, chain)

    def test_normal_cycle_end(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        result = intervals_tuple(chain, tuple_mode.normal)
        assert_array_equal(result, chain)

    # -------------------------------------------------------------------------
    # tuple_mode.lossy — removes boundary (first/last occurrence) intervals
    # -------------------------------------------------------------------------

    def test_lossy_boundary_start_mixed(self):
        # chain = [1, 2, 2, 4, 2]; boundary at positions {0,1,3}; non-boundary = [2, 2]
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.lossy)
        # Only interior intervals: b's second interval (2) and b's third interval (2)
        assert_array_equal(result, np.array([2, 2], dtype=np.intp))

    def test_lossy_boundary_start_integers(self):
        # X = [2, 4, 2, 2, 4]; chain = [1, 2, 2, 1, 3]
        # boundary at positions {0, 1} (chain[i] > i)
        # Wait: boundary = chain[i] > i:
        # i=0: 1>0 T, i=1: 2>1 T, i=2: 2>2 F, i=3: 1>3 F, i=4: 3>4 F
        # boundary at {0, 1}; non-boundary = [2, 1, 3] at positions {2, 3, 4}
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.lossy)
        assert_array_equal(result, np.array([2, 1, 3], dtype=np.intp))

    def test_lossy_boundary_end_mixed(self):
        # chain = [2, 4, 2, 2, 1]; boundary (chain[i] > n-1-i = 4,3,2,1,0):
        # i=0: 2>4 F, i=1: 4>3 T, i=2: 2>2 F, i=3: 2>1 T, i=4: 1>0 T
        # boundary at {1,3,4}; non-boundary at {0,2} → values [2, 2]
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.lossy)
        assert_array_equal(result, np.array([2, 2], dtype=np.intp))

    def test_lossy_all_unique_start(self):
        # All elements unique — all intervals are boundary intervals → lossy = empty
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.lossy)
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_lossy_all_identical_start(self):
        # X = ["a","a","a"]; chain = [1,1,1]; boundary at {0}; non-boundary = [1,1]
        X = ["a", "a", "a"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.lossy)
        assert_array_equal(result, np.array([1, 1], dtype=np.intp))

    # -------------------------------------------------------------------------
    # tuple_mode.redundant — both boundary intervals included
    # -------------------------------------------------------------------------

    def test_redundant_boundary_start_mixed(self):
        # chain = [1, 2, 2, 4, 2]
        # boundary at {0,1,3}; non-boundary at {2,4}: prev_pos = [2-2, 4-2] = [0, 2]
        # is_prev = [T, F, T, F, F]; last_mask = [F, T, F, T, T]; last_pos = [1, 3, 4]
        # trailing = 5 - [1, 3, 4] = [4, 2, 1]
        # result = [1, 2, 2, 4, 2, 4, 2, 1]
        # [1, 2, 2, 4, 2] -> [1, 2, 2, 4, 2, 1, 4, 2]
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(np.sort(result), np.sort(np.array([1, 2, 2, 4, 2, 1, 4, 2])))

    def test_redundant_boundary_end_mixed(self):
        # chain = [2, 4, 2, 2, 1]
        # boundary_end at {1,3,4}; non-boundary at {0,2}: next_pos = [0+2, 2+2] = [2, 4]
        # is_next = [F, F, T, F, T]; first_mask = [T, T, F, T, F]; first_pos = [0, 1, 3]
        # leading = [1, 2, 4]
        # result = [2, 4, 2, 2, 1, 1, 2, 4]
        # [2, 4, 2, 2, 1] -> [2, 4, 1, 2, 4, 2, 2, 1]
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(np.sort(result), np.sort(np.array([2, 4, 1, 2, 4, 2, 2, 1])))

    def test_redundant_all_unique_start(self):
        # X = [1,2,3,4,5]; chain = [1,2,3,4,5]; all boundary; no non-boundary
        # last_mask = all True (no position is pointed to)
        # last_pos = [0,1,2,3,4]; trailing = [5,4,3,2,1]
        # result = [1,2,3,4,5, 5,4,3,2,1]
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(
            result, np.array([1, 2, 3, 4, 5, 5, 4, 3, 2, 1], dtype=np.intp)
        )

    def test_redundant_all_identical_start(self):
        # X = ["a","a","a"]; chain = [1,1,1]; boundary at {0}; non-boundary at {1,2}
        # prev_pos = [1-1, 2-1] = [0, 1]; is_prev = [T, T, F]
        # last_mask = [F, F, T]; last_pos = [2]; trailing = [1]
        # result = [1,1,1, 1]
        X = ["a", "a", "a"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(result, np.array([1, 1, 1, 1], dtype=np.intp))

    def test_redundant_single_element(self):
        # Single-element: only one occurrence — it's both first and last
        # X = ["a"]; chain = [1]; boundary at {0} (1>0); non-boundary = empty
        # last_mask: is_prev all False → last_mask all True → trailing = [1]
        # result = [1, 1]
        X = ["a"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(result, np.array([1, 1], dtype=np.intp))

    def test_redundant_single_element_end(self):
        # X = ["a"]; chain = [1] (same); binding.end → same chain
        X = ["a"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        assert_array_equal(result, np.array([1, 1], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Single-element sequence produces correct size
    # -------------------------------------------------------------------------

    def test_length_normal_equals_n(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.normal)
        self.assertEqual(len(result), len(X))

    def test_length_redundant_equals_n_plus_k(self):
        X = [2, 4, 2, 2, 4]  # 2 unique elements
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, tuple_mode.redundant)
        self.assertEqual(len(result), len(X) + 2)
