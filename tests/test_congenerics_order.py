from unittest import TestCase

import numpy.ma as ma
from numpy.testing import assert_array_equal

from foapy.congenerics import order
from foapy.congenerics import sequences as congenerics_sequences


class TestCongenericsOrder(TestCase):
    """
    Test foapy.congenerics.order(CS) -> masked_array, shape (m, l).

    CS is the output of foapy.congenerics.sequences(X). Every non-masked
    value MUST be 0 (Congeneric Order), and the mask MUST match CS exactly.
    """

    def test_every_non_masked_value_is_zero(self):
        X = ["a", "b", "a", "c"]
        CS = congenerics_sequences(X)
        result = order(CS)
        assert result.shape == (3, 4)
        assert (result.compressed() == 0).all()

    def test_mask_matches_sequences_row_for_row(self):
        X = ma.masked_array(["a", "x", "b", "a"], mask=[0, 1, 0, 0])
        CS = congenerics_sequences(X)
        result = order(CS)
        assert_array_equal(ma.getmaskarray(result), ma.getmaskarray(CS))

    def test_empty_input(self):
        CS = congenerics_sequences([])
        result = order(CS)
        assert result.shape == (0, 0)
