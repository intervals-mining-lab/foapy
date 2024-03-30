from unittest import TestCase

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy.order import order
from foapy.exceptions import Not1DArrayException

class TestMaOrder(TestCase):
    """
    Test list of array sequence
    """
    def test_string_values(self):
        X = ['a', 'b', 'a', 'c', 'd']
        expected = np.array([0, 1, 0, 2, 3])
        exists = order(X)
        assert_array_equal(expected, exists)
    
    def test_int_values(self):
        X =[1, 2, 2, 3, 4, 1]
        expected = np.array([0, 1, 1, 2, 3,0])
        exists = order(X)
        assert_array_equal(expected, exists)
        
    def test_void(self):
        X = []
        expected = np.array([])
        exists = order(X)
        assert_array_equal(expected, exists)
        
    def test_single_value(self):
        X = ['E']
        expected = np.array([0])
        exists = order(X)
        assert_array_equal(expected, exists)
    
    def test_with_d2_array_exception(self):
        X = [[[2, 2, 2], [2, 2, 2]]]
        with pytest.raises(Not1DArrayException) as e_info:
            order(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 2",
                e_info.message,
            )

    def test_with_d3_array_exception(self):
        X = [[[1], [3]], [[6], [9]], [[6], [3]]]
        with pytest.raises(Not1DArrayException) as e_info:
            order(X)
            self.assertEqual(
                "Incorrect array form. Excpected d1 array, exists 3",
                e_info.message,
            )