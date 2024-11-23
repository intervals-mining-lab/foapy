from unittest import TestCase

import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.exceptions import Not1DArrayException
from foapy.ma import order


class TestMaOrder(TestCase):
    """
    Test list of masked_array sequence
    """

    def test_string_values(self):
        X = ma.masked_array(["a", "b", "a", "c", "d"])
        expected = ma.masked_array(
            [
                [0, None, 0, None, None],
                [None, 1, None, None, None],
                [None, None, None, 2, None],
                [None, None, None, None, 3],
            ],
            mask=[
                [0, 1, 0, 1, 1],
                [1, 0, 1, 1, 1],
                [1, 1, 1, 0, 1],
                [1, 1, 1, 1, 0],
            ],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_string_values_with_mask(self):
        X = ma.masked_array(["a", "b", "a", "c", "d"], mask=[0, 1, 0, 0, 0])
        expected = ma.masked_array(
            [
                [0, None, 0, None, None],
                [None, None, None, 2, None],
                [None, None, None, None, 3],
            ],
            mask=[[0, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_with_return_alphabet(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"])
        expected_alphabet = ma.masked_array(["a", "c", "e", "d"])
        expected_array = ma.masked_array(
            [
                [0, None, None, None, None, 0],
                [None, 1, 1, None, None, None],
                [None, None, None, 2, None, None],
                [None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 1],
            ],
        )
        exists_array, exists_alphabet = order(X, True)
        assert_equal(expected_alphabet, exists_alphabet)
        assert_equal(expected_array, exists_array)

    def test_int_values(self):
        X = ma.masked_array([1, 4, 1000, 4, 15])
        expected = ma.masked_array(
            [
                [0, None, None, None, None],
                [None, 1, None, 1, None],
                [None, None, 2, None, None],
                [None, None, None, None, 3],
            ],
            mask=[
                [0, 1, 1, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0],
            ],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_two_pairs_string_values(self):
        X = ma.masked_array(["a", "c", "c", "e", "d", "a"])
        expected = ma.masked_array(
            [
                [0, None, None, None, None, 0],
                [None, 1, 1, None, None, None],
                [None, None, None, 2, None, None],
                [None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 1],
            ],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_two_pairs_int_values(self):
        X = ma.masked_array([1, 2, 2, 3, 4, 1])
        expected = ma.masked_array(
            [
                [0, None, None, None, None, 0],
                [None, 1, 1, None, None, None],
                [None, None, None, 2, None, None],
                [None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0],
                [1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 1],
            ],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_with_no_values(self):
        X = ma.masked_array([])
        expected = ma.masked_array([]).ravel
        exists = order(X)
        assert_equal(expected, exists)

    def test_with_single_string_value(self):
        X = ma.masked_array(["E"])
        expected = ma.masked_array([[0]])
        exists = order(X)
        assert_equal(expected, exists)

    def test_with_several_characters_in_value(self):
        X = ma.masked_array(["ATC", "CGT", "ATC"])
        expected = ma.masked_array(
            [[0, None, 0], [None, 1, None]], mask=[[0, 1, 0], [1, 0, 1]]
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_with_d2_array_exception(self):
        X = ma.masked_array([[2, 2, 2], [2, 2, 2]])
        with pytest.raises(Not1DArrayException) as e_info:
            order(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 2",
                e_info.message,
            )

    def test_with_d3_array_exception(self):
        X = ma.masked_array(
            [[[1], [3]], [[6], [9]], [[6], [3]]],
        )
        with pytest.raises(Not1DArrayException) as e_info:
            order(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 3",
                e_info.message,
            )

    def test_with_exception(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "b", "a"], mask=[0, 1, 0, 0, 0, 0, 1, 0]
        )
        expected = ma.masked_array(
            [
                [0, None, None, 0, None, None, None, 0],
                [None, None, 1, None, None, 1, None, None],
                [None, None, None, None, 2, None, None, None],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 0, 1, 1, 1],
            ],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_int_values_with_mask(self):
        X = ma.masked_array([1, 2, 1, 1, 4], mask=[0, 1, 0, 0, 0])
        expected = ma.masked_array(
            [
                [0, None, 0, 0, None],
                [None, None, None, None, 2],
            ],
            mask=[[0, 1, 0, 0, 1], [1, 1, 1, 1, 0]],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_void_int_values_with_mask(self):
        X = ma.masked_array([1], mask=[1])
        expected = ma.masked_array(
            [],
            mask=[],
        )
        exists = order(X)
        assert_equal(expected, exists)

    def test_int_values_with_middle_mask(self):
        X = ma.masked_array([1, 2, 3, 3, 4, 2], mask=[0, 0, 1, 1, 0, 0])
        expected = ma.masked_array(
            [
                [0, None, None, None, None, None],
                [None, 1, None, None, None, 1],
                [None, None, None, None, 3, None],
            ],
            mask=[[0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1]],
        )
        exists = order(X)
        assert_equal(expected, exists)
