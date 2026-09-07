from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.testing import assert_array_equal

from foapy.congenerics import alphabet as congenerics_alphabet
from foapy.congenerics import sequences
from foapy.exceptions import Not1DArrayException


class TestCongenericsSequences(TestCase):
    """
    Test foapy.congenerics.sequences(X) -> masked_array, shape (m, l).

    Row j holds the j-th alphabet symbol (first-appearance order) at its
    original positions and is masked everywhere else.
    """

    # -------------------------------------------------------------------------
    # Occurrence-per-row correctness
    # -------------------------------------------------------------------------

    def test_decomposition_rows_match_occurrences(self):
        X = ["a", "b", "a", "c"]
        result = sequences(X)
        assert result.shape == (3, 4)
        assert_array_equal(ma.getmaskarray(result[0]), [0, 1, 0, 1])
        assert_array_equal(ma.getmaskarray(result[1]), [1, 0, 1, 1])
        assert_array_equal(ma.getmaskarray(result[2]), [1, 1, 1, 0])
        assert result[0, 0] == "a"
        assert result[0, 2] == "a"
        assert result[1, 1] == "b"
        assert result[2, 3] == "c"

    def test_rows_ordered_by_first_appearance(self):
        X = ["c", "a", "b", "a"]
        result = sequences(X)
        alph = congenerics_alphabet(X)
        assert_array_equal(alph, ["c", "a", "b"])
        assert result.shape == (3, 4)

    def test_single_element(self):
        result = sequences(["a"])
        assert result.shape == (1, 1)
        assert result[0, 0] == "a"

    def test_all_same_symbol(self):
        result = sequences(["a", "a", "a"])
        assert result.shape == (1, 3)
        assert_array_equal(ma.getmaskarray(result[0]), [0, 0, 0])

    # -------------------------------------------------------------------------
    # Gap propagation
    # -------------------------------------------------------------------------

    def test_source_gaps_remain_masked_in_every_row(self):
        # X = ['a', --, 'b', 'a']
        X = ma.masked_array(["a", "x", "b", "a"], mask=[0, 1, 0, 0])
        result = sequences(X)
        assert result.shape == (2, 4)
        # Row 0 ('a'): positions 0 and 3 are 'a', position 1 is a source gap.
        assert_array_equal(ma.getmaskarray(result[0]), [0, 1, 1, 0])
        # Row 1 ('b'): position 2 is 'b', position 1 is a source gap.
        assert_array_equal(ma.getmaskarray(result[1]), [1, 1, 0, 1])

    # -------------------------------------------------------------------------
    # Empty / fully masked input
    # -------------------------------------------------------------------------

    def test_empty_array(self):
        result = sequences(ma.masked_array([], mask=[]))
        assert result.shape == (0, 0)

    def test_fully_masked_input(self):
        X = ma.masked_array(["a", "b"], mask=[1, 1])
        result = sequences(X)
        assert result.shape == (0, 2)

    # -------------------------------------------------------------------------
    # Errors
    # -------------------------------------------------------------------------

    def test_2d_array_raises_not1d(self):
        X = np.array([[1, 2], [3, 4]])
        with pytest.raises(Not1DArrayException):
            sequences(X)
