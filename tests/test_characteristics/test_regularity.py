from unittest import TestCase

import numpy as np

from foapy.characteristics.regularity import regularity
from foapy.intervals_constants import binding, mode
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class Test_regularity(TestCase):
    """
    Test list for regularity calculate

    The regularity function computes a regularity characteristic
    for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'regularity' with expected output.

    """

    def test_calculate_start_lossy_regularity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0.8547])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_regularity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.8332])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_regularity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.8489])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_regularity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([0.8393])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_regularity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([0.7917])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_regularity_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.9587])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_regularity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.848944998])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_regularity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.88086479457968535])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_regularity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0.86439343863])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_regularity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0.838985343])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_regularity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_regularity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_regularity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_regularity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_regularity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information_1(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information_2(self):
        X = np.array(["2", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = regularity(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_descriptive_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0.924481699264])
        exists = regularity(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_regularity_start_lossy_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_end_lossy_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_start_normal_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_end_normal_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_start_redundant_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_end_redundant_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_start_cycle_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_end_cycle_returns_value_between_0_and_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_start_lossy_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_end_lossy_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_start_normal_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_end_normal_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_start_redundant_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_end_redundant_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_start_cycle_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_2_end_cycle_returns_value_between_0_and_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_start_lossy_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_end_lossy_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_start_normal_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_end_normal_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_start_redundant_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_end_redundant_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_start_cycle_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_3_end_cycle_returns_value_between_0_and_1(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_start_lossy_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_end_lossy_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_start_normal_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_end_normal_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_start_redundant_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_end_redundant_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_start_cycle_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_4_end_cycle_returns_value_between_0_and_1(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_start_lossy_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_end_lossy_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_start_normal_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_end_normal_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_start_redundant_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_end_redundant_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_start_cycle_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)

    def test_regularity_5_end_cycle_returns_value_between_0_and_1(self):
        X = np.array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        r = regularity(intervals_seq)
        self.assertTrue(0 <= r <= 1)
