from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.uniformity import uniformity
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaUniformity(TestCase):
    """
    Test list for uniformity calculate
    """

    def test_calculate_start_normal_uniformity(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.081704199, 0.029448094887])
        exists = uniformity(intervals_seq)

        epsilon = 0.01
        diff = np.absolute(expected - exists)
        print(exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_uniformity_2(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0, 0, 0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_uniformity(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([0, 0, 0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_uniformity(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
