import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import uniformity


class Test_uniformity(CharacteristicsInfromationalTest):
    """
    Test list for uniformity calculate

    The uniformity function computes a uniformity characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'uniformity' with expected output.

    """

    epsilon = np.float_power(10, -3)

    def target(self, X, dtype=None):
        return uniformity(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 0.22649821459,
                mode.normal: 0.2632777,
                mode.redundant: 0.252818955,
                mode.cycle: 0.337,
            },
            binding.end: {
                mode.lossy: 0.22649821459,
                mode.normal: 0.2362824857,
                mode.redundant: 0.252818955,
                mode.cycle: 0.337,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 0.113283334415,
                mode.normal: 0.2362570097771987,
                mode.redundant: 0.2102399737463,
                mode.cycle: 0.25328248774368,
            },
            binding.end: {
                mode.lossy: 0.113283334415,
                mode.normal: 0.18300750037,
                mode.redundant: 0.2102399737463,
                mode.cycle: 0.25328248774368,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = None
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

    def test_calculate_end_lossy_different_values_uniformity(self):
        X = np.array(["C", "G"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_uniformity_1(self):
        X = np.array(["A", "C", "G", "T"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_uniformity_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_uniformity_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        self.AssertCase(X, binding.start, mode.normal, 0.06080123752225)
