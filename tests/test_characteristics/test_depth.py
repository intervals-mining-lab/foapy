from unittest import TestCase

import numpy as np

from foapy.characteristics.depth import depth
from foapy.constants_intervals import binding, mode
from foapy.intervals import intervals
from foapy.order import order


class TestDepth(TestCase):
    """
    Test list for depth calculate

    The depth function computes a depth characteristic for a given sequence
    of intervals based on various configurations of `binding` and `mode`.

    Test setup:
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'depth' with expected output.

    """

    def test_calculate_start_lossy_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([7.1699])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([11.0768])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([10.1699])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([14.0768])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([12.3399])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_different_values_depth(self):
        X = ["B", "A", "C", "D"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_depth(self):
        X = []
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_depth_1(self):
        X = ["2", "4", "2", "2", "4"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([3.5849625])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_depth_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([6.5849625])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_depth_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([13.299208])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_depth_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([11.7548875])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_depth(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([18.469133])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_depth(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([15.076815597])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_depth(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_depth_1(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_depth_2(self):
        X = ["2", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = depth(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
