from unittest import TestCase

import numpy as np

from foapy import binding, intervals, mode, order
from foapy.characteristics import arithmetic_mean, geometric_mean


class Test_geometric_mean(TestCase):
    """
    Test list for geometric_mean calculate

    The geometric_mean function computes a geometric mean characteristic for a given
    sequence of intervals based on various configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'geometric_mean' with expected output.

    """

    epsilon = np.float_power(10, -100)

    def _test(self, X, binding, mode, expected):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = geometric_mean(intervals_seq)
        diff = 0
        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        self.assertTrue(diff < self.epsilon)

    def test_calculate_start_lossy_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.lossy, np.power(144, 1 / 7))

    def test_calculate_start_normal_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.normal, np.power(2160, 1 / 10))

    def test_calculate_end_normal_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.end, mode.normal, np.power(1152, 1 / 10))

    def test_calculate_start_redunant_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.redundant, np.power(17280, 1 / 13))

    def test_calculate_start_cycle_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.cycle, np.power(5184, 1 / 10))

    def test_calculate_start_normal_geometric_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        self._test(X, binding.start, mode.normal, np.power(12, 1 / 5))

    def test_calculate_start_lossy_geometric_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.lossy, np.power(96, 1 / 6))

    def test_calculate_start_normal_geometric_mean_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.normal, np.power(10080, 1 / 10))

    def test_calculate_end_normal_geometric_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.normal, np.power(3456, 1 / 10))

    def test_calculate_end_redundant_geometric_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.redundant, np.power(362880, 1 / 14))

    def test_calculate_end_cycle_geometric_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.cycle, np.power(34560, 1 / 10))

    def test_calculate_start_lossy_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, np.power(1, 1 / 4))

    def test_calculate_start_normal_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.normal, np.power(1, 1 / 4))

    def test_calculate_end_normal_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.normal, np.power(1, 1 / 4))

    def test_calculate_end_redundant_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, np.power(1, 1 / 5))

    def test_calculate_end_cycle_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.cycle, np.power(1, 1 / 4))

    def test_calculate_end_lossy_different_values_geometric_mean(self):
        X = ["C", "G"]
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_geometric_mean_1(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.lossy, np.power(0, 1 / 4))

    def test_calculate_end_lossy_different_values_geometric_mean_2(self):
        X = ["2", "1"]
        self._test(X, binding.end, mode.lossy, np.power(0, 1 / 2))

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)
