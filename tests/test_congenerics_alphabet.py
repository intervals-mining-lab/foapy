from unittest import TestCase

import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.congenerics import alphabet
from foapy.congenerics import sequences as congenerics_sequences
from foapy.exceptions import Not1DArrayException


class TestCongenericsAlphabet(TestCase):
    """
    Test foapy.congenerics.alphabet(X) -> ndarray.

    Returns the row labels of foapy.congenerics.sequences(X), in
    first-appearance order — equivalent to foapy.partials.alphabet(X).
    """

    def test_matches_row_order(self):
        X = ["c", "a", "b", "a"]
        alph = alphabet(X)
        CS = congenerics_sequences(X)
        assert len(alph) == CS.shape[0]
        for j, symbol in enumerate(alph):
            row_values = CS[j].compressed()
            assert all(v == symbol for v in row_values)

    def test_masked_values_excluded(self):
        X = ma.masked_array(["a", "x", "b", "a"], mask=[0, 1, 0, 0])
        assert_equal(alphabet(X), ["a", "b"])

    def test_empty_or_fully_masked(self):
        assert len(alphabet(ma.masked_array([], mask=[]))) == 0
        assert len(alphabet(ma.masked_array(["a"], mask=[1]))) == 0

    def test_2d_array_raises_not1d(self):
        with pytest.raises(Not1DArrayException):
            alphabet([[1, 2], [3, 4]])
