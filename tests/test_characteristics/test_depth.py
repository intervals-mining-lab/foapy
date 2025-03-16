import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsTest

from foapy import binding, mode
from foapy.characteristics import depth


class TestDepth(CharacteristicsTest):
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

    epsilon = np.float_power(10, -14)

    def target(self, X, dtype=None):
        return depth(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: np.log2(144, dtype=dtype),
                mode.normal: np.log2(2160, dtype=dtype),
                mode.redundant: np.log2(17280, dtype=dtype),
                mode.cycle: np.log2(5184, dtype=dtype),
            },
            binding.end: {
                mode.lossy: np.log2(144, dtype=dtype),
                mode.normal: np.log2(1152, dtype=dtype),
                mode.redundant: np.log2(17280, dtype=dtype),
                mode.cycle: np.log2(5184, dtype=dtype),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: np.log2(96, dtype=dtype),
                mode.normal: np.log2(10080, dtype=dtype),
                mode.redundant: np.log2(362880, dtype=dtype),
                mode.cycle: np.log2(34560, dtype=dtype),
            },
            binding.end: {
                mode.lossy: np.log2(96, dtype=dtype),
                mode.normal: np.log2(3456, dtype=dtype),
                mode.redundant: np.log2(362880, dtype=dtype),
                mode.cycle: np.log2(34560, dtype=dtype),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 0,
                mode.redundant: 0,
                mode.cycle: 0,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0,
                mode.redundant: 0,
                mode.cycle: 0,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_start_lossy_different_values_depth(self):
        X = ["B", "A", "C", "D"]
        self.AssertCase(X, binding.start, mode.lossy, 0)

    def test_calculate_start_lossy_empty_values_depth(self):
        X = []
        self.AssertCase(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_depth_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, np.log2(12))

    def test_calculate_end_lossy_different_values_depth(self):
        X = ["C", "G"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_depth_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_depth_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_overflow_float64_depth(self):
        result = self.GetPrecision(10)
        self.assertNotEqual(result, 0)

        result = self.GetPrecision(10000)
        self.assertNotEqual(result, 0)

    def test_overflow_longdouble_depth(self):
        result = self.GetPrecision(10000, dtype=np.longdouble)
        self.assertNotEqual(result, 0)

        result = self.GetPrecision(1000000, dtype=np.longdouble)
        self.assertNotEqual(result, np.longdouble("-inf"))
        self.assertNotEqual(result, np.longdouble("inf"))
