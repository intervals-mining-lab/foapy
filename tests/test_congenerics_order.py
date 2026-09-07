from unittest import TestCase

import numpy.ma as ma
from numpy.testing import assert_array_equal

from foapy.congenerics import order
from foapy.congenerics import sequences as congenerics_sequences


class TestCongenericsOrder(TestCase):
    """
    Test foapy.congenerics.order(X) -> masked_array, shape (m, l).

    Every non-masked value MUST be 0 (Congeneric Order), and the mask MUST
    match foapy.congenerics.sequences(X) row-for-row.
    """

    def test_every_non_masked_value_is_zero(self):
        X = ["a", "b", "a", "c"]
        result = order(X)
        assert result.shape == (3, 4)
        assert (result.compressed() == 0).all()

    def test_mask_matches_sequences_row_for_row(self):
        X = ma.masked_array(["a", "x", "b", "a"], mask=[0, 1, 0, 0])
        result = order(X)
        CS = congenerics_sequences(X)
        for j in range(CS.shape[0]):
            assert_array_equal(ma.getmaskarray(result[j]), ma.getmaskarray(CS[j]))

    def test_empty_input(self):
        result = order([])
        assert result.shape == (0, 0)
