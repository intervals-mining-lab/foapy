import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import volume


class TestMaVolume(MACharacteristicsTest):
    """
    Test list for volume calculate
    """

    epsilon = np.float_power(10, -100)

    def target(self, X, dtype=None):
        return volume(X)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [16, 3, 3],
                mode_constant.normal: [16, 9, 15],
                mode_constant.redundant: [16, 36, 30],
                mode_constant.cycle: [16, 18, 18],
            },
            binding_constant.end: {
                mode_constant.normal: [16, 12, 6],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        expected = [1, 1, 1, 1]
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def test_calculate_start_lossy_empty_values_volume(self):
        X = ma.masked_array([])
        expected = []
        self.AssertCase(X, binding_constant.start, mode_constant.lossy, expected)

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        expected = [36]
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
