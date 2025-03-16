import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import average_remoteness, identifying_information
from foapy.ma import intervals, order


class TestMaAverageRemoteness(MACharacteristicsTest):
    """
    Test list for average remoteness calculate
    """

    epsilon = np.float_power(10, -15)

    def target(self, X, dtype=None):
        return average_remoteness(X)

    def test_calculate_start_lossy_average_remoteness(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [
            np.mean(np.log2([1, 2, 1])),
            np.mean(np.log2([2, 3])),
        ]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [
                    np.mean(np.log2([1])),
                    np.mean(np.log2([2])),
                    np.mean(np.log2([3])),
                ],
            },
            binding_constant.end: {
                mode_constant.normal: [
                    np.mean(np.log2([3])),
                    np.mean(np.log2([2])),
                    np.mean(np.log2([1])),
                ],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = ma.masked_array([])
        expected = []
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def test_dataset_2(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [
                    np.mean(np.log2([1, 4, 4])),
                    np.mean(np.log2([1, 3])),
                    np.mean(np.log2([3, 1])),
                ],
                mode_constant.normal: [
                    np.mean(np.log2([1, 1, 4, 4])),
                    np.mean(np.log2([3, 1, 3])),
                    np.mean(np.log2([5, 3, 1])),
                ],
                mode_constant.redundant: [
                    np.mean(np.log2([1, 1, 4, 4, 1])),
                    np.mean(np.log2([3, 1, 3, 4])),
                    np.mean(np.log2([5, 3, 1, 2])),
                ],
                mode_constant.cycle: [
                    np.mean(np.log2([1, 1, 4, 4])),
                    np.mean(np.log2([6, 1, 3])),
                    np.mean(np.log2([6, 3, 1])),
                ],
            },
            binding_constant.end: {
                mode_constant.normal: [
                    np.mean(np.log2([1, 4, 4, 1])),
                    np.mean(np.log2([1, 3, 4])),
                    np.mean(np.log2([3, 1, 2])),
                ],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        expected = [np.mean(np.log2([4, 1, 3, 3]))]
        self.AssertCase(
            masked_X, binding_constant.start, mode_constant.redundant, expected
        )

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        expected = [0]
        self.AssertCase(
            masked_X, binding_constant.start, mode_constant.normal, expected
        )

    def test_calculate_start_cycle_with_masked_single_value(self):
        X = ["A"]
        mask = [1]
        masked_X = ma.masked_array(X, mask)
        expected = []
        self.AssertCase(masked_X, binding_constant.start, mode_constant.cycle, expected)

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        expected = [0]
        self.AssertCase(masked_X, binding_constant.start, mode_constant.cycle, expected)

    def test_calculate_start_lossy_different_values(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        expected = [0, 0, 0, 0]
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def AssertInEquality(self, X):
        order_seq = order(X)

        modes = [
            mode_constant.lossy,
            mode_constant.normal,
            mode_constant.redundant,
            mode_constant.cycle,
        ]
        for b in [binding_constant.start, binding_constant.end]:
            for m in modes:
                intervals_seq = intervals(order_seq, b, m)
                g = average_remoteness(intervals_seq)
                H = identifying_information(intervals_seq)
                err_msg = f"g <= H | Binding {b}, mode {m}: " f"g={g}, H={H}"
                self.assertTrue(np.all(g <= H), err_msg)

    def test_inequality_1(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        self.AssertInEquality(X)

    def test_inequality_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        self.AssertInEquality(X)

    def test_inequality_3(self):
        X = ma.masked_array([1])
        self.AssertInEquality(X)

    def test_inequality_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        self.AssertInEquality(X)

    def test_inequality_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        self.AssertInEquality(X)
