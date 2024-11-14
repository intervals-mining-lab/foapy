from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.periodicity import periodicity
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaPeriodicity(TestCase):
    """
    Test list for uniformity calculate
    """

    def test_calculate_start_normal_periodicity(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.944925, 0.97996])
        exists = periodicity(intervals_seq)
        print(exists)
        epsilon = 0.01
        diff = np.absolute(expected - exists)

        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_periodicity_2(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1, 1, 1])
        exists = periodicity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_periodicity(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1, 1, 1])
        exists = periodicity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_periodicity(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = periodicity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
