import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, intervals, mode, order
from foapy.characteristics import descriptive_information, geometric_mean
from foapy.ma import intervals as intervals_ma
from foapy.ma import order as order_ma


class Test_descriptive_information(CharacteristicsInfromationalTest):
    """
    Test list for descriptive_information calculate

    The descriptive_information function computes a descriptive information
    characteristic for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'descriptive_information' with expected output.

    """

    epsilon = np.float_power(10, -4)

    def target(self, X, dtype=None):
        return descriptive_information(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 2.37956557896877,
                mode.normal: 2.58645791024,
                mode.redundant: 2.52382717296366,
                mode.cycle: 2.971,
            },
            binding.end: {
                mode.lossy: 2.37956557896877,
                mode.normal: 2.383831871,
                mode.redundant: 2.52382717296366,
                mode.cycle: 2.971,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 2.314622766,
                mode.normal: 2.9611915354687,
                mode.redundant: 2.8867851948,
                mode.cycle: 3.389245277,
            },
            binding.end: {
                mode.lossy: 2.314622766,
                mode.normal: 2.56417770797363,
                mode.redundant: 2.8867851948,
                mode.cycle: 3.389245277,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = np.longdouble
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
        X = np.array(["C", "G"])
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_descriptive_information_1(self):
        X = np.array(["A", "C", "G", "T"])
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_descriptive_information_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def AssertInEquality(self, X):
        X = np.array(X)
        order_seq = order(X)
        ma_order_seq = order_ma(X)

        for b in [binding.start, binding.end]:
            for m in [mode.lossy, mode.normal, mode.redundant, mode.cycle]:
                intervals_seq = intervals(order_seq, b, m)
                ma_intervals_seq = intervals_ma(ma_order_seq, b, m)
                delta_g = geometric_mean(intervals_seq)
                D = descriptive_information(ma_intervals_seq)
                err_msg = (
                    f"delta_g <= D | Binding {b}, mode {m}: "
                    f"delta_g={delta_g}, D={D}"
                )
                self.assertTrue(delta_g <= D, err_msg)

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

    def test_inequality_6(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertInEquality(X)
