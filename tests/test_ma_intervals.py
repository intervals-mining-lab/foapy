from unittest import TestCase

import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.exceptions import InconsistentOrderException, Not1DArrayException
from foapy.ma.intervals import intervals


class TestMaIntervals(TestCase):
    """
    Test list of masked_array sequence
    """

    # Start-none
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

    def test_int_values_start_None(self):
        X = ma.masked_array([2, 4, 2, 2, 4], mask=[0, 0, 0, 0, 0])
        expected = [[2, 1], [3]]
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    def test_int_values_with_not_all_mask_start_None(self):
        X = ma.masked_array([4, 250, 8, 250], mask=[1, 0, 1, 0])
        expected = [[2]]
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    def test_int_values_start_None_all_mask(self):
        X = ma.masked_array([2, 250, 8], mask=[0, 0, 0])
        expected = [[], [], []]
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    # End-None
    def test_empty_end_None(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    def test_int_values_with_not_all_mask_end_None(self):
        X = ma.masked_array([4, 250, 8, 250], mask=[1, 0, 1, 0])
        expected = [[2]]
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    def test_str_values_end_None(self):
        X = ma.masked_array(
            ["a", "c", "c", "e", "d", "a", "c"], mask=[0, 0, 0, 0, 0, 0, 0]
        )
        expected = [[5], [1, 4], [], []]
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    def test_int_values_end_None(self):
        X = ma.masked_array([2, 4, 2, 2, 4], mask=[0, 0, 0, 0, 0])
        expected = [[2, 1], [3]]
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    def test_int_values_end_None_all_mask(self):
        X = ma.masked_array([2, 250, 8], mask=[0, 0, 0])
        expected = [[], [], []]
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    # Start Normal
    def test_int_values_start_normal(self):
        X = ma.masked_array([2, 4, 2, 2, 4], mask=[0, 0, 0, 0, 0])
        expected = [[1, 2, 1], [2, 3]]
        exists = intervals(X, 1, 2)
        assert_equal(expected, exists)

    def test_str_values_start_normal(self):
        X = ma.masked_array(
            ["a", "c", "c", "e", "d", "a", "c"], mask=[0, 0, 0, 0, 0, 0, 0]
        )
        expected = [[1, 5], [2, 1, 4], [4], [5]]
        exists = intervals(X, 1, 2)
        assert_equal(expected, exists)

    def test_empty_start_Normal_with_mask(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
            mask=[0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
        )
        expected = [[1, 3, 6], [3, 3, 1, 1, 3, 2]]
        exists = intervals(X, 1, 2)
        assert_equal(expected, exists)

    def test_empty_start_Normal(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 1, 2)
        assert_equal(expected, exists)

    def test_same_values_start_Normal(self):
        X = ma.masked_array(["c", "c", "c"], mask=[0, 0, 0])
        expected = [[1, 1, 1]]
        exists = intervals(X, 1, 2)
        assert_equal(expected, exists)

    # Exceptions
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

    def test_with_exception(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "b", "a"], mask=[0, 1, 0, 0, 0, 0, 1, 0]
        )

        with pytest.raises(InconsistentOrderException) as e_info:
            intervals(X, 1, 2)
            self.assertEqual(
                "Element b have mask and unmasked appearance",
                e_info.message,
            )
