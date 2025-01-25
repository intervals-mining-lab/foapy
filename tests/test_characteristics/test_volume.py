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

    The 'volume' function calculates a characteristic volume based
    on the intervals provided.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'volume' with expected output.

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

    def test_calculate_start_normal_volume_1(self):
        X = ["2", "4", "2", "2", "4"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([12])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_volume_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([96])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_normal_volume_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([10080])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_normal_volume_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([3456])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_redundant_volume(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([362880])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_cycle_volume(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([34560])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_normal_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_normal_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_redundant_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_cycle_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_lossy_different_values_volume(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_lossy_different_values_volume_1(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_end_lossy_different_values_volume_2(self):
        X = ["2", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)
