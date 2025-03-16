import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsTest

from foapy import binding, intervals, mode, order
from foapy.characteristics import average_remoteness, identifying_information
from foapy.ma import intervals as intervals_ma
from foapy.ma import order as order_ma


class Test_average_remoteness(CharacteristicsTest):
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

    epsilon = np.float_power(10, -15)

    def target(self, X, dtype=None):
        return average_remoteness(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        expected = {
            binding.start: {
                mode.lossy: np.log2(144) / 7,
                mode.normal: np.log2(2160) / 10,
                mode.redundant: np.log2(17280) / 13,
                mode.cycle: np.log2(5184) / 10,
            },
            binding.end: {
                mode.lossy: np.log2(144) / 7,
                mode.normal: np.log2(1152) / 10,
                mode.redundant: np.log2(17280) / 13,
                mode.cycle: np.log2(5184) / 10,
            },
        }
        self.AssertBatch(X, expected)

    def test_dataset_2(self):
        X = ["C", "C", "C", "C"]
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
        self.AssertBatch(X, expected)

    def test_dataset_3(self):
        X = ["A", "C", "G", "T"]
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: np.log2(24) / 4,
                mode.redundant: np.log2(576) / 8,
                mode.cycle: 2,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: np.log2(24) / 4,
                mode.redundant: np.log2(576) / 8,
                mode.cycle: 2,
            },
        }
        self.AssertBatch(X, expected)

    def test_dataset_4(self):
        X = ["C", "G"]
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5,
                mode.cycle: 1,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5,
                mode.cycle: 1,
            },
        }
        self.AssertBatch(X, expected)

    def test_dataset_5(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: np.log2(96, dtype=dtype) / 6,
                mode.normal: np.log2(10080, dtype=dtype) / 10,
                mode.redundant: np.log2(362880, dtype=dtype) / 14,
                mode.cycle: np.log2(34560, dtype=dtype) / 10,
            },
            binding.end: {
                mode.lossy: np.log2(96, dtype=dtype) / 6,
                mode.normal: np.log2(3456, dtype=dtype) / 10,
                mode.redundant: np.log2(362880, dtype=dtype) / 14,
                mode.cycle: np.log2(34560, dtype=dtype) / 10,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_6(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: np.log2(1050, dtype=dtype) / 6,
                mode.normal: np.log2(31500, dtype=dtype) / 10,
                mode.redundant: np.log2(756000, dtype=dtype) / 14,
                mode.cycle: np.log2(283500, dtype=dtype) / 10,
            },
            binding.end: {
                mode.lossy: np.log2(1050, dtype=dtype) / 6,
                mode.normal: np.log2(25200, dtype=dtype) / 10,
                mode.redundant: np.log2(756000, dtype=dtype) / 14,
                mode.cycle: np.log2(283500, dtype=dtype) / 10,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_7(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: np.log2(210, dtype=dtype) / 7,
                mode.redundant: np.log2(5040, dtype=dtype) / 11,
                mode.cycle: np.log2(1372, dtype=dtype) / 7,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: np.log2(24, dtype=dtype) / 7,
                mode.redundant: np.log2(5040, dtype=dtype) / 11,
                mode.cycle: np.log2(1372, dtype=dtype) / 7,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_average_remoteness_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_average_remoteness_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = []
        self.AssertCase(X, binding.start, mode.lossy, 0)

    def test_calculate_start_normal_average_remoteness_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, np.log2(12) / 5)

    def AssertInEquality(self, X):
        order_seq = order(X)
        ma_order_seq = order_ma(X)

        for b in [binding.start, binding.end]:
            for m in [mode.lossy, mode.normal, mode.redundant, mode.cycle]:
                intervals_seq = intervals(order_seq, b, m)
                ma_intervals_seq = intervals_ma(ma_order_seq, b, m)
                g = average_remoteness(intervals_seq)
                H = identifying_information(ma_intervals_seq)
                err_msg = f"g <= H | Binding {b}, mode {m}: g={g}, H={H}"
                self.assertTrue(g <= H, err_msg)

    def test_inequality_1(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        self.AssertInEquality(X)

    def test_inequality_2(self):
        X = np.array(["1", "1", "3", "1", "1"])
        self.AssertInEquality(X)

    def test_inequality_3(self):
        X = np.array(["13", "13", "13", "13"])
        self.AssertInEquality(X)

    def test_inequality_4(self):
        X = np.array(["A", "B", "A", "B"])
        self.AssertInEquality(X)

    def test_inequality_5(self):
        X = np.array(["B"])
        self.AssertInEquality(X)
