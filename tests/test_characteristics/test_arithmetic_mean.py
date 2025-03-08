from unittest import TestCase

import numpy as np

from foapy import binding, intervals, mode, order
from foapy.characteristics import arithmetic_mean


class Test_arithmetic_mean(TestCase):
    """
    Test list for arithmetic_mean calculate

    The arithmetic_mean function computes a arithmetic mean characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'arithmetic_mean' with expected output.

    """

    epsilon = np.float_power(10, -100)

    def _test(self, X, binding, mode, expected):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = arithmetic_mean(intervals_seq)

        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        self.assertTrue(diff < self.epsilon)

    def test_calculate_start_lossy_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.lossy, 17 / 7)

    def test_calculate_start_normal_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.normal, 26 / 10)

    def test_calculate_end_normal_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.end, mode.normal, 24 / 10)

    def test_calculate_start_redunant_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.redundant, 33 / 13)

    def test_calculate_start_cycle_arithmetic_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.cycle, 30 / 10)

    def test_calculate_start_lossy_empty_values_arithmetic_mean(self):
        X = []
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_arithmetic_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        self._test(X, binding.start, mode.normal, 9 / 5)

    def test_calculate_start_lossy_arithmetic_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.lossy, 16 / 6)

    def test_calculate_start_normal_arithmetic_mean_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.normal, 32 / 10)

    def test_calculate_end_normal_arithmetic_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.normal, 28 / 10)

    def test_calculate_end_redundant_arithmetic_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.redundant, 44 / 14)

    def test_calculate_end_cycle_arithmetic_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.cycle, 40 / 10)

    def test_calculate_start_lossy_same_values_arithmetic_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, 3 / 3)

    def test_calculate_start_normal_same_values_arithmetic_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.normal, 4 / 4)

    def test_calculate_end_normal_same_values_arithmetic_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.normal, 4 / 4)

    def test_calculate_end_redundant_same_values_arithmetic_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.redundant, 5 / 5)

    def test_calculate_end_cycle_same_values_arithmetic_mean(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.cycle, 4 / 4)

    def test_calculate_end_lossy_different_values_arithmetic_mean(self):
        X = np.array(["C", "G"])
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_arithmetic_mean_1(self):
        X = np.array(["A", "C", "G", "T"])
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_arithmetic_mean_2(self):
        X = np.array(["2", "1"])
        self._test(X, binding.end, mode.lossy, 0)
