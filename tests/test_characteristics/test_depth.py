from unittest import TestCase

import numpy as np

from foapy import binding, intervals, mode, order
from foapy.characteristics import depth


class TestDepth(TestCase):
    """
    Test list for depth calculate

    The depth function computes a depth characteristic for a given sequence
    of intervals based on various configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'depth' with expected output.

    """

    epsilon = np.float_power(10, -100)

    def _test(self, X, binding, mode, expected):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = depth(intervals_seq)
        diff = 0
        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        self.assertTrue(diff < self.epsilon)

    def test_calculate_start_lossy_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.lossy, np.log2(144))

    def test_calculate_start_normal_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.normal, np.log2(2160))

    def test_calculate_end_normal_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.end, mode.normal, np.log2(1152))

    def test_calculate_start_redunant_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.redundant, np.log2(17280))

    def test_calculate_start_cycle_depth(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.cycle, np.log2(5184))

    def test_calculate_start_lossy_different_values_depth(self):
        X = ["B", "A", "C", "D"]
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_lossy_empty_values_depth(self):
        X = []
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_depth_1(self):
        X = ["2", "4", "2", "2", "4"]
        self._test(X, binding.start, mode.normal, np.log2(12))

    def test_calculate_start_lossy_depth_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.lossy, np.log2(96))

    def test_calculate_start_normal_depth_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.normal, np.log2(10080))

    def test_calculate_end_normal_depth_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.normal, np.log2(3456))

    def test_calculate_end_redundant_depth(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.redundant, np.log2(362880))

    def test_calculate_end_cycle_depth(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.cycle, np.log2(34560))

    def test_calculate_start_lossy_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.normal, 0)

    def test_calculate_end_normal_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.normal, 0)

    def test_calculate_end_redundant_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.redundant, 0)

    def test_calculate_end_cycle_same_values_depth(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.cycle, 0)

    def test_calculate_end_lossy_different_values_depth(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_depth_1(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_depth_2(self):
        X = ["2", "1"]
        self._test(X, binding.end, mode.lossy, 0)
