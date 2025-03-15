import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import arithmetic_mean


class TestMaArigthmeticMean(MACharacteristicsTest):
    """
    Test list for volume calculate
    """

    epsilon = np.float_power(10, -4)

    def target(self, X, dtype=None):
        return arithmetic_mean(X)

    def test_calculate_start_lossy_arigthmetic_mean(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [1.3333, 2.5]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [1, 2, 3],
            },
            binding_constant.end: {
                mode_constant.normal: [3, 2, 1],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)

        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [2],
                mode_constant.redundant: [2.75],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)

        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [3, 2, 2],
                mode_constant.normal: [2.5, 2.3333333, 3],
                mode_constant.redundant: [2.2, 2.75, 2.75],
                mode_constant.cycle: [2.5, 3.333333, 3.3333333],
            },
            binding_constant.end: {
                mode_constant.normal: [2.5, 2.66666667, 2],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        self.AssertCase(masked_X, binding_constant.start, mode_constant.normal, [1])

    def test_calculate_start_cycle_with_masked_single_value(self):
        X = ["A"]
        mask = [1]
        masked_X = ma.masked_array(X, mask)
        self.AssertCase(masked_X, binding_constant.start, mode_constant.normal, [])

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        self.AssertCase(masked_X, binding_constant.start, mode_constant.cycle, [1])

    def test_calculate_start_lossy_different_values(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, [0, 0, 0, 0])
