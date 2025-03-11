import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import identifying_information


class Test_identifying_information(CharacteristicsInfromationalTest):
    """
    Test list for identifying_information calculate

    The identifying_information function computes a identifying_information
    characteristic for a given sequence of intervals based on various
    configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'identifying_information' with expected output.
    """

    epsilon = np.float_power(10, -4)

    def target(self, X, dtype=None):
        return identifying_information(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 1.25069821459,
                mode.normal: 1.3709777,
                mode.redundant: 1.335618955,
                mode.cycle: 1.571,
            },
            binding.end: {
                mode.lossy: 1.25069821459,
                mode.normal: 1.2532824857,
                mode.redundant: 1.335618955,
                mode.cycle: 1.571,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 1.7906654768,
                mode.normal: 1.6895995955,
                mode.redundant: 1.6373048326,
                mode.cycle: 1.9709505945,
            },
            binding.end: {
                mode.lossy: 1.7906654768,
                mode.normal: 1.6965784285,
                mode.redundant: 1.6373048326,
                mode.cycle: 1.9709505945,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 1.210777084415,
                mode.normal: 1.5661778097771987,
                mode.redundant: 1.5294637608763,
                mode.cycle: 1.76096404744368,
            },
            binding.end: {
                mode.lossy: 1.210777084415,
                mode.normal: 1.35849625,
                mode.redundant: 1.5294637608763,
                mode.cycle: 1.76096404744368,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_4(self):
        X = ["C", "G"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5849625007,
                mode.cycle: 1,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5849625007,
                mode.cycle: 1,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_5(self):
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

    def test_dataset_6(self):
        X = ["A", "C", "G", "T"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 1.1462406252,
                mode.redundant: 1.3219280949,
                mode.cycle: 2,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 1.1462406252,
                mode.redundant: 1.3219280949,
                mode.cycle: 2,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_7(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 1.102035074,
                mode.redundant: 1.3991235932,
                mode.cycle: 1.6644977792,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0.830626027,
                mode.redundant: 1.3991235932,
                mode.cycle: 1.6644977792,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_identifying_information_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_identifying_information_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        self.AssertCase(X, binding.start, mode.normal, 0.77779373752225)
