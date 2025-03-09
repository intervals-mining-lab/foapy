from unittest import TestCase

import numpy as np

from foapy import binding, intervals, mode, order
from foapy.characteristics import average_remoteness, identifying_information
from foapy.ma import intervals as intervals_ma
from foapy.ma import order as order_ma


class Test_average_remoteness(TestCase):
    """
    Test list for average_remoteness calculate

    The average_remoteness function computes a average remoteness characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'average_remoteness' with expected output.

    """

    epsilon = np.float_power(10, -18)

    def _test(self, X, binding, mode, expected, dtype=None):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = average_remoteness(intervals_seq, dtype=dtype)
        diff = 0
        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        self.assertTrue(diff < self.epsilon, f"Difference: {diff} > {self.epsilon}")

    def test_calculate_start_lossy_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.lossy, np.log2(144) / 7)

    def test_calculate_start_normal_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.normal, np.log2(2160) / 10)

    def test_calculate_end_normal_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.end, mode.normal, np.log2(1152) / 10)

    def test_calculate_start_redunant_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.redundant, np.log2(17280) / 13)

    def test_calculate_start_cycle_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.cycle, np.log2(5184) / 10)

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = []
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_average_remoteness_1(self):
        X = ["2", "4", "2", "2", "4"]
        self._test(X, binding.start, mode.normal, np.log2(12) / 5)

    def test_calculate_start_lossy_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.normal, 0)

    def test_calculate_end_normal_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.normal, 0)

    def test_calculate_end_redundant_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.redundant, 0)

    def test_calculate_end_cycle_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.cycle, 0)

    def test_calculate_start_normal_average_remoteness_4(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.start, mode.normal, np.log2(24) / 4)

    def test_calculate_end_normal_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.normal, np.log2(24) / 4)

    def test_calculate_end_redundant_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.redundant, np.log2(576) / 8)

    def test_calculate_end_cycle_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.cycle, 2)

    def test_calculate_end_cycle_average_remoteness_3(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.cycle, 1)

    def test_calculate_end_redundant_average_remoteness_3(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.redundant, 0.5)

    def test_calculate_end_normal_average_remoteness_3(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.normal, 0.5)

    def test_calculate_end_normal_average_remoteness_5(self):
        X = ["C", "G"]
        self._test(X, binding.start, mode.normal, 0.5)

    def test_calculate_start_lossy_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.lossy, np.log2(96) / 6)

    def test_calculate_start_normal_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.normal, np.log2(10080) / 10)

    def test_calculate_end_normal_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.normal, np.log2(3456) / 10)

    def test_calculate_end_redundant_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.redundant, np.log2(362880) / 14)

    def test_calculate_end_cycle_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        expected = np.log2(34560, dtype=np.longdouble) / 10
        self._test(X, binding.end, mode.cycle, expected, dtype=np.longdouble)

    def test_calculate_start_lossy_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        expected = np.log2(1050, dtype=np.longdouble) / 6
        self._test(X, binding.start, mode.lossy, expected, dtype=np.longdouble)

    def test_calculate_start_normal_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        expected = np.log2(31500, dtype=np.longdouble) / 10
        self._test(X, binding.start, mode.normal, expected, dtype=np.longdouble)

    def test_calculate_end_normal_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        self._test(X, binding.end, mode.normal, np.log2(25200) / 10)

    def test_calculate_end_redundant_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        self._test(X, binding.end, mode.redundant, np.log2(756000) / 14)

    def test_calculate_end_cycle_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        self._test(X, binding.end, mode.cycle, np.log2(283500) / 10)

    def test_calculate_start_lossy_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        expected = np.log2(210, dtype=np.longdouble) / 7
        self._test(X, binding.start, mode.normal, expected, dtype=np.longdouble)

    def test_calculate_end_normal_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        self._test(X, binding.end, mode.normal, np.log2(24) / 7)

    def test_calculate_end_redundant_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        self._test(X, binding.end, mode.redundant, np.log2(5040) / 11)

    def test_calculate_end_cycle_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        expected = np.log2(1372, dtype=np.longdouble) / 7
        self._test(X, binding.end, mode.cycle, expected, dtype=np.longdouble)

    def test_calculate_end_lossy_different_values_average_remoteness(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_average_remoteness_1(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_average_remoteness_2(self):
        X = ["2", "1"]
        self._test(X, binding.end, mode.lossy, 0)

    def test_average_remoteness_less_than_identifying_information_start_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_1(
        self,
    ):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_2(
        self,
    ):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_3(
        self,
    ):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_4(
        self,
    ):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)
