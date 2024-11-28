from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.arigthmetic_mean import arigthmetic_mean
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaArigthmeticMean(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_arigthmetic_mean(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1.3333, 2.5])
        exists = arigthmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_arigthmetic_mean(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1, 2, 3])
        exists = arigthmetic_mean(intervals_seq)

        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_arigthmetic_mean(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([3, 2, 1])
        exists = arigthmetic_mean(intervals_seq)

        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_depth(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([2])
        exists = arigthmetic_mean(intervals_seq)
        epsilon = 0.01
        print(exists)
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
