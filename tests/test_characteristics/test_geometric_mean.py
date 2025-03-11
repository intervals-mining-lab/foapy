import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsTest

from foapy import binding, intervals, mode, order
from foapy.characteristics import arithmetic_mean, geometric_mean


class Test_geometric_mean(CharacteristicsTest):
    """
    Test list for geometric_mean calculate

    The geometric_mean function computes a geometric mean characteristic for a given
    sequence of intervals based on various configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'geometric_mean' with expected output.

    """

    epsilon = np.float_power(10, -100)

    def target(self, X, dtype=None):
        return geometric_mean(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: np.power(
                    144,
                    1 / 7,
                ),
                mode.normal: np.power(2160, 1 / 10),
                mode.redundant: np.power(17280, 1 / 13),
                mode.cycle: np.power(5184, 1 / 10),
            },
            binding.end: {
                mode.lossy: np.power(144, 1 / 7),
                mode.normal: np.power(1152, 1 / 10),
                mode.redundant: np.power(17280, 1 / 13),
                mode.cycle: np.power(5184, 1 / 10),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: np.power(96, 1 / 6),
                mode.normal: np.power(10080, 1 / 10),
                mode.redundant: np.power(362880, 1 / 14),
                mode.cycle: np.power(34560, 1 / 10),
            },
            binding.end: {
                mode.lossy: np.power(96, 1 / 6),
                mode.normal: np.power(3456, 1 / 10),
                mode.redundant: np.power(362880, 1 / 14),
                mode.cycle: np.power(34560, 1 / 10),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: np.power(1, 1 / 2),
                mode.normal: np.power(1, 1 / 4),
                mode.redundant: np.power(1, 1 / 5),
                mode.cycle: np.power(1, 1 / 4),
            },
            binding.end: {
                mode.lossy: np.power(1, 1 / 2),
                mode.normal: np.power(1, 1 / 4),
                mode.redundant: np.power(1, 1 / 5),
                mode.cycle: np.power(1, 1 / 4),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_geometric_mean(self):
        X = ["C", "G"]
        self.AssertCase(X, binding.start, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_geometric_mean_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, np.power(0, 1 / 4))

    def test_calculate_end_lossy_different_values_geometric_mean_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, np.power(0, 1 / 2))

    def test_calculate_start_normal_geometric_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, np.power(12, 1 / 5))

    def AssertInEquality(self, X):
        order_seq = order(X)

        for b in [binding.start, binding.end]:
            for m in [mode.lossy, mode.normal, mode.redundant, mode.cycle]:
                intervals_seq = intervals(order_seq, b, m)
                delta_g = geometric_mean(intervals_seq)
                delta_a = arithmetic_mean(intervals_seq)
                err_msg = (
                    f"delta_g <= delta_a | Binding {b}, mode {m}: "
                    f"delta_g={delta_g}, delta_a={delta_a}"
                )
                self.assertTrue(delta_g <= delta_a, err_msg)

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
