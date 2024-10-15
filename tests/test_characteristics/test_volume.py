from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy.characteristics.volume import volume
from foapy.constants_intervals import binding, mode
from foapy.intervals import intervals
from foapy.order import order


class TestVolume(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([144])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2160])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1152])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_redunant_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([17280])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_cycle_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([5184])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ["B", "A", "C", "D"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = []
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)
