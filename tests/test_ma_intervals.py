from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal

from foapy.exceptions import InconsistentOrderException, Not1DArrayException
from foapy.ma import intervals


class TestMaIntervals(TestCase):
    """
    Test list of masked_array sequence
    """

    # Start-lossy
    def test_str_values_start_None(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [
            np.array([5]),
            np.array([1, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 1, 1))
        assert_equal(expected, exists)

    def test_empty_start_None(self):
        X = ma.masked_array([], mask=[])
        expected = np.array([])
        exists = intervals(X, 1, 1)
        assert_equal(expected, exists)

    def test_empty_start_None_with_mask(self):
        X = ma.masked_array(
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [np.array([3, 6]), np.array([], dtype=int), np.array([], dtype=int)]
        exists = list(intervals(X, 1, 1))
        assert_equal(expected, exists)

    def test_int_values_start_None(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([2, 1]), np.array([3])]
        exists = list(intervals(X, 1, 1))
        assert_equal(expected, exists)

    def test_int_values_with_not_all_mask_start_None(self):
        X = ma.masked_array(
            [[None, None, None, None], [None, 1, None, 1], [None, None, None, None]],
            mask=[[1, 1, 1, 1], [1, 0, 1, 0], [1, 1, 1, 1]],
        )
        expected = [np.array([], dtype=int), np.array([2]), np.array([], dtype=int)]
        exists = list(intervals(X, 1, 1))
        assert_equal(expected, exists)

    def test_int_values_start_None_all_mask(self):
        X = ma.masked_array(
            [[0, None, None], [None, 1, None], [None, None, 2]],
            mask=[[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        )
        expected = [
            np.array([], dtype=int),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 1, 1))
        assert_equal(expected, exists)

    # End-None
    def test_empty_end_None(self):
        X = ma.masked_array([], mask=[])
        expected = np.array([])
        exists = intervals(X, 2, 1)
        assert_equal(expected, exists)

    def test_int_values_with_not_all_mask_end_None(self):
        X = ma.masked_array(
            [[None, None, None, None], [None, 1, None, 1], [None, None, None, None]],
            mask=[[1, 1, 1, 1], [1, 0, 1, 0], [1, 1, 1, 1]],
        )
        expected = [np.array([], dtype=int), np.array([2]), np.array([], dtype=int)]
        exists = list(intervals(X, 2, 1))
        assert_equal(expected, exists)

    def test_str_values_end_None(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [
            np.array([5]),
            np.array([1, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 2, 1))
        assert_equal(expected, exists)

    def test_int_values_end_None(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([2, 1]), np.array([3])]
        exists = list(intervals(X, 2, 1))
        assert_equal(expected, exists)

    def test_int_values_end_None_no_all_mask(self):
        X = ma.masked_array(
            [[0, None, None], [None, 1, None], [None, None, 2]],
            mask=[[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        )
        expected = [
            np.array([], dtype=int),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 2, 1))
        assert_equal(expected, exists)

    # Start Normal
    def test_int_values_start_normal(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([1, 2, 1]), np.array([2, 3])]
        exists = list(intervals(X, 1, 2))
        assert_equal(expected, exists)

    def test_str_values_start_normal(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [np.array([1, 5]), np.array([2, 1, 4]), np.array([4]), np.array([6])]
        exists = list(intervals(X, 1, 2))
        assert_equal(expected, exists)

    def test_empty_start_Normal(self):
        X = ma.masked_array([], mask=[])
        expected = np.array([])
        exists = list(intervals(X, 1, 2))
        assert_equal(expected, exists)

    def test_same_values_start_Normal(self):
        X = ma.masked_array([[0, 0, 0]], mask=[[0, 0, 0]])
        expected = [np.array([1, 1, 1])]
        exists = list(intervals(X, 1, 2))
        assert_equal(expected, exists)

    # End Normal
    def test_int_values_end_normal(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([2, 1, 2]), np.array([3, 1])]
        exists = list(intervals(X, 2, 2))
        assert_equal(expected, exists)

    def test_str_values_end_normal(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [np.array([5, 2]), np.array([1, 4, 1]), np.array([4]), np.array([2])]
        exists = intervals(X, 2, 2)
        assert_equal(expected, exists)

    def test_empty_End_Normal_with_mask(self):
        X = ma.masked_array(
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [
            np.array([3, 6, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 2, 2))
        assert_equal(expected, exists)

    def test_int_values_end_Normal_no_all_mask(self):
        X = ma.masked_array(
            [[0, None, None], [None, 1, None], [None, None, 2]],
            mask=[[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        )
        expected = [
            np.array([3], dtype=int),
            np.array([2], dtype=int),
            np.array([1], dtype=int),
        ]
        exists = list(intervals(X, 2, 2))
        assert_equal(expected, exists)

    def test_empty_end_Normal(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 2, 2)
        assert_equal(expected, exists)

    # Start Cycle

    def test_int_values_start_cycle(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([2, 2, 1]), np.array([2, 3])]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_str_values_start_Cycle(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [np.array([2, 5]), np.array([2, 1, 4]), np.array([7]), np.array([7])]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_empty_start_Cycle_with_mask(self):
        X = ma.masked_array(
            # ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
            # mask=[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [
            np.array([4, 3, 6]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_int_values_start_Cycle_no_all_mask(self):
        X = ma.masked_array(
            [[0, None, None], [None, 1, None], [None, None, 2]],
            mask=[[0, 1, 1], [1, 0, 1], [1, 1, 0]],
        )
        expected = [np.array([3]), np.array([3]), np.array([3])]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_empty_start_Cycle(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 1, 3)
        assert_equal(expected, exists)

    def test_single_value_start_Cycle(self):
        X = ma.masked_array([[0]], mask=[[0]])
        expected = [np.array([1])]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_many_values_start_Cycle(self):
        X = ma.masked_array([[1, 1, 1]], mask=[[0, 0, 0]])
        expected = [np.array([1, 1, 1])]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    # End Cycle
    def test_int_values_end_cycle(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([2, 1, 2]), np.array([3, 2])]
        exists = list(intervals(X, 2, 3))
        assert_equal(expected, exists)

    def test_str_values_end_Cycle(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [np.array([5, 2]), np.array([1, 4, 2]), np.array([7]), np.array([7])]
        exists = list(intervals(X, 2, 3))
        assert_equal(expected, exists)

    def test_empty_end_Cycle_with_mask(self):
        X = ma.masked_array(
            # ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
            # mask=[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [
            np.array([3, 6, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 2, 3))
        assert_equal(expected, exists)

    def test_empty_end_Cycle(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 1, 3)
        assert_equal(expected, exists)

    def test_single_value_end_Cycle(self):
        X = ma.masked_array([[0]], mask=[[0]])
        expected = [[1]]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    def test_many_values_end_Cycle(self):
        X = ma.masked_array([["c", "c", "c"]], mask=[[0, 0, 0]])
        expected = [[1, 1, 1]]
        exists = list(intervals(X, 1, 3))
        assert_equal(expected, exists)

    # Start Redunant
    def test_int_values_start_redunant(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([1, 2, 1, 2]), np.array([2, 3, 1])]
        exists = list(intervals(X, 1, 4))
        assert_equal(expected, exists)

    def test_str_values_start_redunant(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [
            np.array([1, 5, 2]),
            np.array([2, 1, 4, 1]),
            np.array([4, 4]),
            np.array([6, 2]),
        ]
        exists = list(intervals(X, 1, 4))
        assert_equal(expected, exists)

    def test_empty_start_redunant_with_mask(self):
        X = ma.masked_array(
            # ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
            # mask=[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [
            np.array([1, 3, 6, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 1, 4))
        assert_equal(expected, exists)

    def test_empty_start_redunant(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 1, 4)
        assert_equal(expected, exists)

    def test_single_value_start_redunant(self):
        X = ma.masked_array([[0]], mask=[[0]])
        expected = [np.array([1, 1])]
        exists = list(intervals(X, 1, 4))
        assert_equal(expected, exists)

    def test_many_values_start_redunant(self):
        X = ma.masked_array([[0, 0, 0]], mask=[[0, 0, 0]])
        expected = [np.array([1, 1, 1, 1])]
        exists = list(intervals(X, 1, 4))
        assert_equal(expected, exists)

    # End Redunant
    def test_int_values_end_redunant(self):
        X = ma.masked_array(
            [[0, None, 0, 0, None], [None, 1, None, None, 1]],
            mask=[[0, 1, 0, 0, 1], [1, 0, 1, 1, 0]],
        )
        expected = [np.array([1, 2, 1, 2]), np.array([2, 3, 1])]
        exists = list(intervals(X, 2, 4))
        assert_equal(expected, exists)

    def test_str_values_end_redunant(self):
        X = ma.masked_array(
            [
                [0, None, None, None, None, 0, None],
                [None, 1, 1, None, None, None, 1],
                [None, None, None, 2, None, None, None],
                [None, None, None, None, None, 3, None],
            ],
            mask=[
                [0, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 1],
            ],
        )
        expected = [
            np.array([1, 5, 2]),
            np.array([2, 1, 4, 1]),
            np.array([4, 4]),
            np.array([6, 2]),
        ]
        exists = list(intervals(X, 2, 4))
        assert_equal(expected, exists)

    def test_empty_end_redunant_with_mask(self):
        X = ma.masked_array(
            # ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
            # mask=[0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [
                [0, None, None, 0, None, None, None, None, None, 0, None, None, None],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
            ],
            mask=[
                [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ],
        )
        expected = [
            np.array([1, 3, 6, 4]),
            np.array([], dtype=int),
            np.array([], dtype=int),
        ]
        exists = list(intervals(X, 2, 4))
        assert_equal(expected, exists)

    def test_empty_end_redunant(self):
        X = ma.masked_array([], mask=[])
        expected = []
        exists = intervals(X, 2, 4)
        assert_equal(expected, exists)

    def test_single_value_end_redunant(self):
        X = ma.masked_array([[0]], mask=[[0]])
        expected = [np.array([1, 1])]
        exists = list(intervals(X, 2, 4))
        assert_equal(expected, exists)

    def test_many_values_end_redunant(self):
        X = ma.masked_array([[0, 0, 0]], mask=[[0, 0, 0]])
        expected = [np.array([1, 1, 1, 1])]
        exists = list(intervals(X, 2, 4))
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

    def test_with_d1_array_exception(self):
        X = ma.masked_array([2, 2, 2])
        with pytest.raises(Not1DArrayException) as e_info:
            intervals(X, 1, 1)
            self.assertEqual(
                "Incorrect array form. Expected d2 array, exists 1",
                e_info.message,
            )

    def test_with_exception(self):
        X = ma.masked_array([[1, 1, 2], [3, 1, 1]], mask=[[0, 1, 0], [1, 0, 0]])

        with pytest.raises(InconsistentOrderException) as e_info:
            intervals(X, 1, 2)
            self.assertEqual(
                "Elements [1 -- 2] have wrong appearance",
                e_info.message,
            )

    def test_with_binding_exception(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "b", "a"], mask=[0, 0, 0, 0, 0, 0, 0, 0]
        )

        with pytest.raises(ValueError) as e_info:
            intervals(X, 5, 1)
            self.assertEqual(
                "Invalid binding value. Use binding.start or binding.end.",
                e_info.message,
            )

    def test_with_mode_exception(self):
        X = ma.masked_array(
            ["a", "b", "c", "a", "b", "c", "b", "a"], mask=[0, 0, 0, 0, 0, 0, 0, 0]
        )

        with pytest.raises(ValueError) as e_info:
            intervals(X, 1, 6)
            self.assertEqual(
                "Invalid binding value. Use binding.start or binding.end.",
                e_info.message,
            )
