from unittest import TestCase

import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.exceptions import InconsistentOrderException, Not1DArrayException
from foapy.ma.alphabet import alphabet


class TestMaAlphabet(TestCase):
    """
    Test list of unique masked_array elements
    """

    def test_string_values_with_mask(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"], mask=[0, 0, 0, 1, 0, 0])
        expected = ma.masked_array(["a", "c", "e", "d"], mask=[0, 0, 1, 0])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_string_values_with_no_mask(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"], mask=[0, 0, 0, 0, 0, 0])
        expected = ma.masked_array(["a", "c", "e", "d"], mask=[0, 0, 0, 0])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_integer_values_with_no_mask(self):
        X = ma.masked_array([1, 2, 2, 3, 4, 1], mask=[0, 0, 0, 0, 0, 0])
        expected = ma.masked_array([1, 2, 3, 4], mask=[0, 0, 0, 0])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_integer_values_with_mask(self):
        X = ma.masked_array([1, 2, 2, 3, 4, 1], mask=[1, 0, 0, 0, 0, 1])
        expected = ma.masked_array([1, 2, 3, 4], mask=[1, 0, 0, 0])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_with_single_integer_value(self):
        X = ma.masked_array([1], mask=[0])
        expected = ma.masked_array([1], mask=[0])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_with_single_string_value_with_mask(self):
        X = ma.masked_array(["a"], mask=[1])
        expected = ma.masked_array(["a"], mask=[1])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_with_no_values(self):
        X = ma.masked_array([], mask=[])
        expected = ma.masked_array([], mask=[])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_several_mask_obj(self):
        X = ma.masked_array(["a", "b", "c", "c", "b", "a"], mask=[0, 1, 1, 1, 1, 0])
        expected = ma.masked_array(["a", "b", "c"], mask=[0, 1, 1])
        exists = alphabet(X)
        assert_equal(expected, exists)

    def test_with_exception(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "b", "a"], mask=[0, 1, 0, 0, 0, 0, 1, 0]
        )

        with pytest.raises(InconsistentOrderException) as e_info:
            alphabet(X)
            self.assertEqual(
                "Element b have mask and unmasked appearance",
                e_info.message,
            )

    def test_with_d2_array_exception(self):
        X = ma.masked_array([[2, 2, 2], [2, 2, 2]], mask=[[0, 0, 0], [0, 0, 0]])
        with pytest.raises(Not1DArrayException) as e_info:
            alphabet(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 2",
                e_info.message,
            )

    def test_with_d3_array_exception(self):
        X = ma.masked_array(
            [[[1], [3]], [[6], [9]], [[6], [3]]],
            mask=[[[1], [0]], [[0], [0]], [[0], [0]]],
        )
        with pytest.raises(Not1DArrayException) as e_info:
            alphabet(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 3",
                e_info.message,
            )
