from unittest import TestCase

import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.exceptions import Not1DArrayException
from foapy.ma.intervals import intervals


class TestMaIntervals(TestCase):
    """
    Test list of masked_array sequence
    """

    def test_str_values_start_None(self):
        X = ma.masked_array(
            ["a", "c", "c", "e", "d", "a", "c"], mask=[0, 0, 0, 0, 0, 0, 0]
        )
        expected = [[5], [1, 4], [], []]
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    def test_empty_start_None(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    def test_with_d3_array_exception(self):
        X = ma.masked_array(
            [[[1], [3]], [[6], [9]], [[6], [3]]],
        )
        with pytest.raises(Not1DArrayException) as e_info:
            intervals(X, 1, 1)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 3",
                e_info.message,
            )

    def test_with_d2_array_exception(self):
        X = ma.masked_array([[2, 2, 2], [2, 2, 2]])
        with pytest.raises(Not1DArrayException) as e_info:
            intervals(X, 1, 1)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 2",
                e_info.message,
            )
