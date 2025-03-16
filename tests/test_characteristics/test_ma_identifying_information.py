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

    epsilon = np.float_power(10, -100)

    def target(self, X, dtype=None):
        return identifying_information(X)

    def test_calculate_start_normal_entropy(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        expected = [
            np.log2(np.mean([1, 2, 1])),
            np.log2(np.mean([2, 3])),
        ]
        self.AssertCase(X, binding_constant.start, mode_constant.normal, expected)

    def test_dataset_1(self):
        X = [1, 2, 3]
        masked_X = ma.masked_array(X)
        dtype = np.longdouble
        expected = {
            binding_constant.start: {
                mode_constant.normal: [
                    np.log2(np.mean([1])),
                    np.log2(np.mean([2])),
                    np.log2(np.mean([3])),
                ],
            },
            binding_constant.end: {
                mode_constant.normal: [
                    np.log2(np.mean([3])),
                    np.log2(np.mean([2])),
                    np.log2(np.mean([1])),
                ],
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
                mode_constant.lossy: [
                    np.log2(np.mean([1, 4, 4])),
                    np.log2(np.mean([1, 3])),
                    np.log2(np.mean([3, 1])),
                ],
                mode_constant.normal: [
                    np.log2(np.mean([1, 1, 4, 4])),
                    np.log2(np.mean([3, 1, 3])),
                    np.log2(np.mean([5, 3, 1])),
                ],
                mode_constant.redundant: [
                    np.log2(np.mean([1, 1, 4, 4, 1])),
                    np.log2(np.mean([3, 1, 3, 4])),
                    np.log2(np.mean([5, 3, 1, 2])),
                ],
                mode_constant.cycle: [
                    np.log2(np.mean([1, 1, 4, 4])),
                    np.log2(np.mean([6, 1, 3])),
                    np.log2(np.mean([6, 3, 1])),
                ],
            },
            binding_constant.end: {
                mode_constant.normal: [
                    np.log2(np.mean([1, 4, 4, 1])),
                    np.log2(np.mean([1, 3, 4])),
                    np.log2(np.mean([3, 1, 2])),
                ],
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
        expected = [np.log2(np.mean([4, 1, 3, 3]))]
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
