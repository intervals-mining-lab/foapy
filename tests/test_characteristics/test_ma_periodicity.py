import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import periodicity


class TestMaPeriodicity(MACharacteristicsTest):
    """
    Test list for uniformity calculate
    """

    epsilon = np.float_power(10, -4)

    def target(self, X, dtype=None):
        return periodicity(X)

    def test_calculate_start_normal_periodicity(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [0.94494079, 0.9797959]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [1, 1, 1],
            },
            binding_constant.end: {
                mode_constant.normal: [1, 1, 1],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_lossy_empty_values_periodicity(self):
        X = ma.masked_array([])
        expected = []
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def test_dataset_2(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [0.83994, 0.86602, 0.86602],
                mode_constant.normal: [0.8, 0.8914645, 0.82207069],
                mode_constant.redundant: [0.7914, 0.8907, 0.85103],
                mode_constant.cycle: [0.8, 0.78622, 0.78622242],
            },
            binding_constant.end: {
                mode_constant.normal: [0.8, 0.8585, 0.9085],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        expected = [0.8907]
        self.AssertCase(
            masked_X, binding_constant.start, mode_constant.redundant, expected
        )

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        expected = [1]
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
        expected = [1]
        self.AssertCase(masked_X, binding_constant.start, mode_constant.cycle, expected)

    def test_calculate_start_lossy_different_values(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        expected = [0, 0, 0, 0]
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)
