from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy.intervals import intervals


class TestIntervals(TestCase):
    """
    Test list of array intervals
    """

    def test_int_start_none(self):
        X = [2, 4, 2, 2, 4]
        expected = np.array([2, 3, 1])
        exists = intervals(X, 1, 1)
        assert_array_equal(expected, exists)

    def test_void(self):
        X = []
        expected = np.array([])
        exists = intervals(X, 1, 1)
        assert_array_equal(expected, exists)
