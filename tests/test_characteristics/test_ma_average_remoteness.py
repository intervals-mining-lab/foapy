from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.average_remoteness import average_remoteness
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaAverageRemoteness(TestCase):
    """
    Test list for average remoteness calculate
    """

    def test_calculate_start_normal_average_remoteness(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.3333333, 1.29248])
        exists = average_remoteness(intervals_seq)

        epsilon = 0.01
        diff = np.absolute(expected - exists)
        print(exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_average_remoteness_2(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0, 1, 1.5849625])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1.5849625, 1, 0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
