from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy import alphabet
from foapy.exceptions import Not1DArrayException


class TestAlphabet(TestCase):
    """Test list of unique array elements"""

    def test_string_values(self):
        X = ["a", "c", "c", "e", "d", "a"]
        expected = np.array(["a", "c", "e", "d"])
        exists = alphabet(X)
        assert_array_equal(expected, exists)

    def test_int_values(self):
        X = [0, 1, 2, 3, 4]
        expected = np.array([0, 1, 2, 3, 4])
        exists = alphabet(X)
        assert_array_equal(expected, exists)

    def test_void(self):
        X = []
        expected = np.array([])
        exists = alphabet(X)
        assert_array_equal(expected, exists)

    def test_with_d2_array_exception(self):
        X = [[[2, 2, 2], [2, 2, 2]]]
        with pytest.raises(Not1DArrayException) as e_info:
            alphabet(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 2",
                e_info.message,
            )

    def test_with_d3_array_exception(self):
        X = [[[1], [3]], [[6], [9]], [[6], [3]]]
        with pytest.raises(Not1DArrayException) as e_info:
            alphabet(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 3",
                e_info.message,
            )

    def test_single_int_value(self):
        X = [1]
        expected = np.array([1])
        exists = alphabet(X)
        assert_array_equal(expected, exists)

    def test_single_str_value(self):
        X = ["m"]
        expected = np.array(["m"])
        exists = alphabet(X)
        assert_array_equal(expected, exists)
