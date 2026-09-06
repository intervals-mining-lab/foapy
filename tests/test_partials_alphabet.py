import inspect
from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

from foapy import alphabet as core_alphabet
from foapy.exceptions import Not1DArrayException
from foapy.partials import alphabet


class TestPartialsAlphabet(TestCase):
    """
    Test foapy.partials.alphabet(X) -> ndarray.

    Returns a plain 1-D array of unique non-masked values in first-appearance
    order. Masked positions are excluded entirely.
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_array(self):
        X = ma.masked_array([], mask=[])
        result = alphabet(X)
        assert len(result) == 0

    # -------------------------------------------------------------------------
    # Single element
    # -------------------------------------------------------------------------

    def test_single_unmasked_element(self):
        X = ma.masked_array(["a"], mask=[0])
        result = alphabet(X)
        assert_equal(result, ["a"])

    def test_single_masked_element_returns_empty(self):
        X = ma.masked_array(["a"], mask=[1])
        result = alphabet(X)
        assert len(result) == 0

    # -------------------------------------------------------------------------
    # All unique symbols
    # -------------------------------------------------------------------------

    def test_all_unique_strings(self):
        X = ma.masked_array(["a", "b", "c", "d"], mask=[0, 0, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a", "b", "c", "d"])

    # -------------------------------------------------------------------------
    # All same symbol
    # -------------------------------------------------------------------------

    def test_all_same_symbol(self):
        X = ma.masked_array(["a", "a", "a"], mask=[0, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a"])

    # -------------------------------------------------------------------------
    # Realistic dataset
    # -------------------------------------------------------------------------

    def test_realistic_string_dataset(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"], mask=[0, 0, 0, 0, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a", "c", "e", "d"])

    def test_realistic_integer_dataset(self):
        X = ma.masked_array([1, 2, 2, 3, 4, 1], mask=[0, 0, 0, 0, 0, 0])
        result = alphabet(X)
        assert_equal(result, [1, 2, 3, 4])

    # -------------------------------------------------------------------------
    # Fully masked
    # -------------------------------------------------------------------------

    def test_fully_masked_returns_empty(self):
        X = ma.masked_array(["a", "b", "c"], mask=[1, 1, 1])
        result = alphabet(X)
        assert len(result) == 0

    # -------------------------------------------------------------------------
    # Partially masked — masked values excluded
    # -------------------------------------------------------------------------

    def test_partially_masked_excludes_masked_values(self):
        X = ma.masked_array(["a", "b", "a", "c"], mask=[0, 1, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a", "c"])

    def test_partially_masked_first_appearance_order(self):
        # 'b' appears in unmasked positions, but 'a' appears first
        X = ma.masked_array(["a", "x", "b", "a", "b"], mask=[0, 1, 0, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a", "b"])

    def test_first_element_masked(self):
        X = ma.masked_array(["x", "b", "a"], mask=[1, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["b", "a"])

    def test_first_occurrence_masked_later_unmasked(self):
        X = ma.masked_array(["a", "a", "b", "a"], mask=[1, 0, 0, 0])
        result = alphabet(X)
        assert_equal(result, ["a", "b"])

    # -------------------------------------------------------------------------
    # No-mask passthrough — must equal core.alphabet
    # -------------------------------------------------------------------------

    def test_no_mask_matches_core_alphabet(self):
        data = ["a", "b", "a", "c", "d"]
        X = ma.masked_array(data, mask=[0, 0, 0, 0, 0])
        core_result = core_alphabet(data)
        partial_result = alphabet(X)
        assert_array_equal(partial_result, core_result)

    # -------------------------------------------------------------------------
    # Plain array auto-wrapping
    # -------------------------------------------------------------------------

    def test_plain_list_accepted(self):
        result = alphabet(["a", "b", "a"])
        assert_equal(result, ["a", "b"])

    def test_plain_ndarray_accepted(self):
        result = alphabet(np.array(["a", "b", "a"]))
        assert_equal(result, ["a", "b"])

    # -------------------------------------------------------------------------
    # Return type is plain ndarray (not masked)
    # -------------------------------------------------------------------------

    def test_returns_plain_ndarray(self):
        X = ma.masked_array(["a", "b"], mask=[0, 1])
        result = alphabet(X)
        assert not isinstance(result, ma.MaskedArray)
        assert isinstance(result, np.ndarray)

    def test_signature_has_input_and_return_annotations(self):
        signature = inspect.signature(alphabet)
        assert signature.parameters["X"].annotation is not inspect.Parameter.empty
        assert signature.return_annotation is not inspect.Signature.empty

    # -------------------------------------------------------------------------
    # Error handling
    # -------------------------------------------------------------------------

    def test_2d_array_raises_not1d(self):
        X = ma.masked_array([[1, 2], [3, 4]])
        with pytest.raises(Not1DArrayException):
            alphabet(X)
