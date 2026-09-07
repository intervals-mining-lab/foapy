from unittest import TestCase

import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.congenerics import alphabet
from foapy.congenerics import sequences as congenerics_sequences


class TestCongenericsAlphabet(TestCase):
    """
    Test foapy.congenerics.alphabet(CS) -> ndarray.

    CS is the output of foapy.congenerics.sequences(X). Row j's label is its
    single non-masked value — equivalent to foapy.partials.alphabet(X).
    """

    def test_matches_row_order(self):
        X = ["c", "a", "b", "a"]
        CS = congenerics_sequences(X)
        alph = alphabet(CS)
        assert len(alph) == CS.shape[0]
        for j, symbol in enumerate(alph):
            row_values = CS[j].compressed()
            assert all(v == symbol for v in row_values)

    def test_masked_source_values_excluded(self):
        X = ma.masked_array(["a", "x", "b", "a"], mask=[0, 1, 0, 0])
        CS = congenerics_sequences(X)
        assert_equal(alphabet(CS), ["a", "b"])

    def test_empty_or_fully_masked_source(self):
        assert len(alphabet(congenerics_sequences(ma.masked_array([], mask=[])))) == 0
        assert (
            len(alphabet(congenerics_sequences(ma.masked_array(["a"], mask=[1])))) == 0
        )
