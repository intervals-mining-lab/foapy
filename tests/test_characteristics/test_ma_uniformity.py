import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import uniformity


class TestMaUniformity(MACharacteristicsTest):
    """
    Test list for uniformity calculate
    """

    epsilon = np.float_power(10, -4)

    def target(self, X, dtype=None):
        return uniformity(X)

    def test_calculate_start_normal_uniformity(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [0.081704199, 0.029448094887]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [0, 0, 0],
            },
            binding_constant.end: {
                mode_constant.normal: [0, 0, 0],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [0.2516, 0.2075, 0.2075],
                mode_constant.normal: [0.3219, 0.1657, 0.2826],
                mode_constant.redundant: [0.3375, 0.16695, 0.2327],
                mode_constant.cycle: [0.32192, 0.34699, 0.34699],
            },
            binding_constant.end: {
                mode_constant.normal: [0.3219, 0.22005, 0.13834],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_lossy_empty_values_uniformity(self):
        X = ma.masked_array([])
        expected = []
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        expected = [0.16695037]
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
