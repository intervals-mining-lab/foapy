import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsTest

from foapy import binding, mode
from foapy.characteristics import arithmetic_mean


class Test_arithmetic_mean(CharacteristicsTest):
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

    def target(self, X, dtype=None):
        return arithmetic_mean(X)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = {
            binding.start: {
                mode.lossy: 17 / 7,
                mode.normal: 26 / 10,
                mode.redundant: 33 / 13,
                mode.cycle: 30 / 10,
            },
            binding.end: {
                mode.lossy: 17 / 7,
                mode.normal: 24 / 10,
                mode.redundant: 33 / 13,
                mode.cycle: 30 / 10,
            },
        }
        self.AssertBatch(X, expected)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        expected = {
            binding.start: {
                mode.lossy: 16 / 6,
                mode.normal: 32 / 10,
                mode.redundant: 44 / 14,
                mode.cycle: 40 / 10,
            },
            binding.end: {
                mode.lossy: 16 / 6,
                mode.normal: 28 / 10,
                mode.redundant: 44 / 14,
                mode.cycle: 40 / 10,
            },
        }

        self.AssertBatch(X, expected)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        expected = {
            binding.start: {
                mode.lossy: 3 / 3,
                mode.normal: 4 / 4,
                mode.redundant: 5 / 5,
                mode.cycle: 4 / 4,
            },
            binding.end: {
                mode.lossy: 3 / 3,
                mode.normal: 4 / 4,
                mode.redundant: 5 / 5,
                mode.cycle: 4 / 4,
            },
        }

        self.AssertBatch(X, expected)

    def test_calculate_start_lossy_empty_values_arithmetic_mean(self):
        X = []
        self.AssertCase(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_arithmetic_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, 9 / 5)

    def test_calculate_end_lossy_different_values_arithmetic_mean(self):
        X = np.array(["C", "G"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_arithmetic_mean_1(self):
        X = np.array(["A", "C", "G", "T"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_arithmetic_mean_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 0)
