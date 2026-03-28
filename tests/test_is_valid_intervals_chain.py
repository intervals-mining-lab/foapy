from unittest import TestCase

import numpy as np

from foapy.core import is_valid_intervals_chain


class TestIsValidIntervalsChain(TestCase):
    """
    Test is_valid_intervals_chain(chain) -> bool.

    Never raises; returns True only for 1-D integer arrays of strictly
    positive values all <= len(chain).
    """

    # -------------------------------------------------------------------------
    # Valid inputs — should return True
    # -------------------------------------------------------------------------

    def test_valid_boundary_start(self):
        self.assertTrue(
            is_valid_intervals_chain(np.array([1, 2, 2, 4, 2], dtype=np.intp))
        )

    def test_valid_boundary_end(self):
        self.assertTrue(
            is_valid_intervals_chain(np.array([2, 4, 2, 2, 1], dtype=np.intp))
        )

    def test_valid_cycle_start(self):
        self.assertTrue(
            is_valid_intervals_chain(np.array([1, 5, 2, 5, 2], dtype=np.intp))
        )

    def test_valid_single_element(self):
        self.assertTrue(is_valid_intervals_chain(np.array([1], dtype=np.intp)))

    def test_valid_all_ones(self):
        self.assertTrue(is_valid_intervals_chain(np.array([1, 1, 1], dtype=np.intp)))

    def test_valid_max_value_equals_n(self):
        # value == n is valid
        self.assertTrue(
            is_valid_intervals_chain(np.array([5, 1, 2, 3, 4], dtype=np.intp))
        )

    # -------------------------------------------------------------------------
    # Empty array — should return True
    # -------------------------------------------------------------------------

    def test_empty_array_returns_true(self):
        self.assertTrue(is_valid_intervals_chain(np.array([], dtype=np.intp)))

    def test_empty_list_returns_true(self):
        self.assertTrue(is_valid_intervals_chain([]))

    # -------------------------------------------------------------------------
    # Invalid values — should return False
    # -------------------------------------------------------------------------

    def test_zero_value_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(np.array([0, 1, 2], dtype=np.intp)))

    def test_all_zeros_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(np.array([0, 0, 0], dtype=np.intp)))

    def test_negative_value_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(np.array([-1, 2, 2], dtype=np.intp)))

    def test_value_exceeds_length_returns_false(self):
        # n=3, value 4 > 3
        self.assertFalse(is_valid_intervals_chain(np.array([1, 4, 2], dtype=np.intp)))

    def test_value_equals_n_plus_one_returns_false(self):
        # n=3, value 4 = n+1
        self.assertFalse(is_valid_intervals_chain(np.array([4, 1, 2], dtype=np.intp)))

    # -------------------------------------------------------------------------
    # Non-1D arrays — should return False, no exception
    # -------------------------------------------------------------------------

    def test_2d_array_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(np.array([[1, 2], [3, 4]])))

    def test_0d_array_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(np.array(42)))

    # -------------------------------------------------------------------------
    # Non-array input — should return False, no exception
    # -------------------------------------------------------------------------

    def test_string_returns_false(self):
        self.assertFalse(is_valid_intervals_chain("not_a_chain"))

    def test_none_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(None))

    def test_int_returns_false(self):
        self.assertFalse(is_valid_intervals_chain(42))
