from unittest import TestCase

import numpy as np
import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.characteristics.ma.volume import volume
from foapy.intervals_constants import binding as binding_constant
from foapy.intervals_constants import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaVolume(TestCase):
    """
    Test list for volume calculate
    """

    def test_calculate_start_lossy_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([16, 3, 3])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_normal_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([16, 9, 15])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_end_normal_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([16, 12, 6])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_redunant_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([16, 36, 30])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_cycle_volume(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([16, 18, 18])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([1, 1, 1, 1])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([36])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_cycle_with_masked_single_value(self):
        X = ["A"]
        mask = [1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([1])
        exists = volume(intervals_seq)
        assert_equal(expected, exists)
