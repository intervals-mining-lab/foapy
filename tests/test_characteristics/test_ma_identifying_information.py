import numpy as np
import numpy.ma as ma
from test_characteristics.characterisitcs_test import MACharacteristicsTest

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import identifying_information


class TestMaIdentifyingInformation(MACharacteristicsTest):
    """
    Test list for identifying information calculate
    """

    epsilon = np.float_power(10, -2)

    def target(self, X, dtype=None):
        return identifying_information(X)

    def test_calculate_start_normal_entropy(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [0.415037499, 1.321928094887]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [0, 1, 1.5849625],
            },
            binding_constant.end: {
                mode_constant.normal: [1.5849625, 1, 0],
            },
        }
        self.AssertBatch(masked_X, expected, dtype=dtype)

    def test_calculate_end_single_element_lossy_entropy(self):
        X = ma.masked_array(["B"])
        expected = [0]
        self.AssertCase(X, binding_constant.end, mode_constant.lossy, expected)

    def test_calculate_end_void_lossy_entropy(self):
        X = ma.masked_array([])
        expected = []
        self.AssertCase(X, binding_constant.end, mode_constant.lossy, expected)

    def test_dataset_2(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.lossy: [1.5849, 1, 1],
                mode_constant.normal: [1.3219, 1.22239, 1.5849],
                mode_constant.redundant: [1.1375, 1.45943, 1.4594],
                mode_constant.cycle: [1.3219, 1.7369, 1.73696],
            },
            binding_constant.end: {
                mode_constant.normal: [1.3210, 1.4150, 1],
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
        expected = [1.4594]
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
