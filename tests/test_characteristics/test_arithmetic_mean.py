from unittest import TestCase

import numpy as np

from foapy.characteristics.arithmetic_mean import arithmetic_mean
from foapy.constants_intervals import binding, mode
from foapy.intervals import intervals
from foapy.order import order


class Test_arithmetic_mean(TestCase):
    """
    Test list for arithmetic_mean calculate
    """

    def test_calculate_start_lossy_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([2.4286])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2.6])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([2.4])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([2.5385])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([3.0])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_arithmetic_mean(self):
        X = []
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_arithmetic_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.8])
        exists = arithmetic_mean(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
