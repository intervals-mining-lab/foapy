from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.depth import depth
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaDepth(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([4, 1.585, 1.585])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([4, 3.1699, 3.9069])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([4, 3.585, 2.585])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([4, 5.1699, 4.9069])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([4, 4.1699, 4.1699])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_different_values_depth(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([0, 0, 0, 0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_depth(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
