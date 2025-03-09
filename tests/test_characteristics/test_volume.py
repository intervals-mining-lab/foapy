from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy import binding, intervals, mode, order
from foapy.characteristics import volume


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

    def _test(self, X, binding, mode, expected):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = volume(intervals_seq)
        assert_array_equal(expected, exists)

    def test_calculate_start_lossy_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.lossy, 144)

    def test_calculate_start_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.normal, 2160)

    def test_calculate_end_normal_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.end, mode.normal, 1152)

    def test_calculate_start_redunant_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.redundant, 17280)

    def test_calculate_start_cycle_volume(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        self._test(X, binding.start, mode.cycle, 5184)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ["B", "A", "C", "D"]
        self._test(X, binding.start, mode.lossy, 1)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = []
        self._test(X, binding.start, mode.lossy, [])

    def test_calculate_start_normal_volume_1(self):
        X = ["2", "4", "2", "2", "4"]
        self._test(X, binding.start, mode.normal, 12)

    def test_calculate_start_lossy_volume_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.lossy, 96)

    def test_calculate_start_normal_volume_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.start, mode.normal, 10080)

    def test_calculate_end_normal_volume_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.normal, 3456)

    def test_calculate_end_redundant_volume(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.redundant, 362880)

    def test_calculate_end_cycle_volume(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        self._test(X, binding.end, mode.cycle, 34560)

    def test_calculate_start_lossy_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.lossy, 1)

    def test_calculate_start_normal_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.start, mode.normal, 1)

    def test_calculate_end_normal_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.normal, 1)

    def test_calculate_end_redundant_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.redundant, 1)

    def test_calculate_end_cycle_same_values_volume(self):
        X = ["C", "C", "C", "C"]
        self._test(X, binding.end, mode.cycle, 1)

    def test_calculate_end_lossy_different_values_volume(self):
        X = ["C", "G"]
        self._test(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_volume_1(self):
        X = ["A", "C", "G", "T"]
        self._test(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_volume_2(self):
        X = ["2", "1"]
        self._test(X, binding.end, mode.lossy, 1)

    def test_overflow_volume(self):
        length = 100
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        result = volume(intervals_seq)
        self.assertEqual(result, 0)
