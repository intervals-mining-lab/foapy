from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

from foapy import order as core_order
from foapy.exceptions import Not1DArrayException
from foapy.partials import order


class TestPartialsOrder(TestCase):
    """
    Test foapy.partials.order(X, return_alphabet=False) -> masked_array.

    Returns a 1-D masked array of the same length as the input.
    Non-masked positions hold the element's 0-based alphabet index.
    Masked positions remain masked in the output.
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_array(self):
        X = ma.masked_array([], mask=[])
        result = order(X)
        assert result.shape == (0,)
        assert_equal(result, ma.masked_array([], mask=[]))

    # -------------------------------------------------------------------------
    # Single element
    # -------------------------------------------------------------------------

    def test_single_unmasked_element(self):
        X = ma.masked_array(["a"], mask=[0])
        result = order(X)
        expected = ma.masked_array([0], mask=[0])
        assert_equal(result, expected)

    def test_single_masked_element(self):
        X = ma.masked_array(["a"], mask=[1])
        result = order(X)
        expected = ma.masked_array([0], mask=[1])
        assert_equal(result, expected)

    # -------------------------------------------------------------------------
    # All unique symbols
    # -------------------------------------------------------------------------

    def test_all_unique_strings(self):
        X = ma.masked_array(["a", "b", "c", "d"], mask=[0, 0, 0, 0])
        result = order(X)
        expected = ma.masked_array([0, 1, 2, 3], mask=[0, 0, 0, 0])
        assert_equal(result, expected)

    def test_all_unique_integers(self):
        X = ma.masked_array([10, 20, 30], mask=[0, 0, 0])
        result = order(X)
        expected = ma.masked_array([0, 1, 2], mask=[0, 0, 0])
        assert_equal(result, expected)

    # -------------------------------------------------------------------------
    # All same symbol
    # -------------------------------------------------------------------------

    def test_all_same_symbol(self):
        X = ma.masked_array(["a", "a", "a"], mask=[0, 0, 0])
        result = order(X)
        expected = ma.masked_array([0, 0, 0], mask=[0, 0, 0])
        assert_equal(result, expected)

    # -------------------------------------------------------------------------
    # Realistic dataset
    # -------------------------------------------------------------------------

    def test_realistic_string_dataset(self):
        X = ma.masked_array(["a", "b", "a", "c", "d"], mask=[0, 0, 0, 0, 0])
        result = order(X)
        expected = ma.masked_array([0, 1, 0, 2, 3], mask=[0, 0, 0, 0, 0])
        assert_equal(result, expected)

    def test_realistic_integer_dataset(self):
        X = ma.masked_array([1, 2, 2, 3, 4, 1], mask=[0, 0, 0, 0, 0, 0])
        result = order(X)
        expected = ma.masked_array([0, 1, 1, 2, 3, 0], mask=[0, 0, 0, 0, 0, 0])
        assert_equal(result, expected)

    # -------------------------------------------------------------------------
    # Fully masked
    # -------------------------------------------------------------------------

    def test_fully_masked_returns_full_mask(self):
        X = ma.masked_array(["a", "b", "c"], mask=[1, 1, 1])
        result = order(X)
        assert result.shape == (3,)
        assert np.all(ma.getmaskarray(result))

    # -------------------------------------------------------------------------
    # Partially masked — gap positions preserved
    # -------------------------------------------------------------------------

    def test_partially_masked_preserves_gap_positions(self):
        # X = ['a', --, 'b', 'a', --]
        X = ma.masked_array(["a", "x", "b", "a", "y"], mask=[0, 1, 0, 0, 1])
        result = order(X)
        expected_data_at_non_masked = [0, 1, 0]
        assert result.shape == (5,)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0, 0, 1])
        assert_array_equal(result.compressed(), expected_data_at_non_masked)

    def test_partial_mask_output_same_length_as_input(self):
        X = ma.masked_array(["a", "b", "a"], mask=[0, 1, 0])
        result = order(X)
        assert len(result) == len(X)

    def test_partial_mask_output_mask_identical_to_input(self):
        mask = [0, 1, 0, 1, 0]
        X = ma.masked_array(["a", "b", "c", "d", "a"], mask=mask)
        result = order(X)
        assert_array_equal(ma.getmaskarray(result), mask)

    # -------------------------------------------------------------------------
    # No-mask passthrough — must equal core.order
    # -------------------------------------------------------------------------

    def test_no_mask_matches_core_order(self):
        data = ["a", "b", "a", "c", "d"]
        X = ma.masked_array(data, mask=[0, 0, 0, 0, 0])
        core_result = core_order(data)
        partial_result = order(X)
        assert_array_equal(partial_result.compressed(), core_result)

    # -------------------------------------------------------------------------
    # Plain array auto-wrapping
    # -------------------------------------------------------------------------

    def test_plain_list_accepted(self):
        result = order(["a", "b", "a"])
        assert result.shape == (3,)
        assert_array_equal(result.compressed(), [0, 1, 0])

    def test_plain_ndarray_accepted(self):
        result = order(np.array(["a", "b", "a"]))
        assert result.shape == (3,)
        assert_array_equal(result.compressed(), [0, 1, 0])

    # -------------------------------------------------------------------------
    # return_alphabet=True
    # -------------------------------------------------------------------------

    def test_return_alphabet_unmasked(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"], mask=[0, 0, 0, 0, 0, 0])
        result, alph = order(X, return_alphabet=True)
        assert_array_equal(result.compressed(), [0, 1, 1, 2, 3, 0])
        assert_equal(alph, ["a", "c", "e", "d"])

    def test_return_alphabet_with_mask(self):
        # X = ['a', --, 'b', 'a', --]
        X = ma.masked_array(["a", "x", "b", "a", "y"], mask=[0, 1, 0, 0, 1])
        result, alph = order(X, return_alphabet=True)
        assert_array_equal(result.compressed(), [0, 1, 0])
        assert_equal(alph, ["a", "b"])

    def test_return_alphabet_fully_masked(self):
        X = ma.masked_array(["a", "b"], mask=[1, 1])
        result, alph = order(X, return_alphabet=True)
        assert np.all(ma.getmaskarray(result))
        assert len(alph) == 0

    # -------------------------------------------------------------------------
    # Error handling
    # -------------------------------------------------------------------------

    def test_2d_array_raises_not1d(self):
        X = ma.masked_array([[1, 2], [3, 4]])
        with pytest.raises(Not1DArrayException):
            order(X)
