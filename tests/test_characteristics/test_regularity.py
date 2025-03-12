import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import regularity
from foapy.ma import intervals, order


class Test_regularity(CharacteristicsInfromationalTest):
    """
    Test list for regularity calculate

    The regularity function computes a regularity characteristic
    for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'regularity' with expected output.

    """

    epsilon = np.float_power(10, -3)

    def target(self, X, dtype=None):
        return regularity(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 0.8547,
                mode.normal: 0.8332,
                mode.redundant: 0.8393,
                mode.cycle: 0.7917,
            },
            binding.end: {
                mode.lossy: 0.8547,
                mode.normal: 0.8489,
                mode.redundant: 0.8393,
                mode.cycle: 0.7917,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 0.924481699264,
                mode.normal: 0.848944998,
                mode.redundant: 0.86439343863,
                mode.cycle: 0.838985343,
            },
            binding.end: {
                mode.lossy: 0.924481699264,
                mode.normal: 0.88086479457968535,
                mode.redundant: 0.86439343863,
                mode.cycle: 0.838985343,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 1,
                mode.normal: 1,
                mode.redundant: 1,
                mode.cycle: 1,
            },
            binding.end: {
                mode.lossy: 1,
                mode.normal: 1,
                mode.redundant: 1,
                mode.cycle: 1,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_descriptive_information(self):
        X = ["C", "G"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_descriptive_information_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_descriptive_information_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_regularity_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, 0.9587)

    def AssertInEquality(self, X):
        X = np.asanyarray(X)
        order_seq = order(X)

        for b in [binding.start, binding.end]:
            for m in [mode.lossy, mode.normal, mode.redundant, mode.cycle]:
                intervals_seq = intervals(order_seq, b, m)
                r = regularity(intervals_seq)
                err_msg = f"0 <= r <= 1 | Binding {b}, mode {m}: " f"r={r}"
                self.assertTrue(0 <= r <= 1, err_msg)

    def test_inequality_1(self):
        X = ["10", "87", "10", "87", "10", "87"]
        self.AssertInEquality(X)

    def test_inequality_2(self):
        X = ["1", "1", "3", "1", "1"]
        self.AssertInEquality(X)

    def test_inequality_3(self):
        X = ["13", "13", "13", "13"]
        self.AssertInEquality(X)

    def test_inequality_4(self):
        X = ["A", "B", "A", "B"]
        self.AssertInEquality(X)

    def test_inequality_5(self):
        X = ["B"]
        self.AssertInEquality(X)
