from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma.depth import depth
from foapy.ma import intervals, order


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
        epsilon = 0.0001
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
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_depth(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([4, 3.585, 2.585])
        exists = depth(intervals_seq)
        epsilon = 0.0001
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
        epsilon = 0.0001
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
        epsilon = 0.0001
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
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = depth(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([5.1699])
        exists = depth(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_with_masked_single_value(self):
        X = ["A"]
        mask = [1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([])
        exists = depth(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
