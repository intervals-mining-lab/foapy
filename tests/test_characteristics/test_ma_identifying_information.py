from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.identifying_information import identifying_information
from foapy.intervals_constants import binding as binding_constant
from foapy.intervals_constants import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaIdentifyingInformation(TestCase):
    """
    Test list for identifying information calculate
    """

    def test_calculate_start_normal_entropy(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.415037499, 1.321928094887])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_single_elements_normal_entropy(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0, 1, 1.5849625])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_single_elements_normal_entropy(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1.5849625, 1, 0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_single_element_lossy_entropy(self):
        X = ma.masked_array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_void_lossy_entropy(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        expected = np.array([])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([1.5849, 1, 1])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1.3219, 1.22239, 1.5849])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1.3210, 1.4150, 1])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([1.1375, 1.45943, 1.4594])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([1.3219, 1.7369, 1.73696])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_uniformity(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_values_with_mask(self):
        X = ["B", "B", "B", "A", "A", "B", "B", "A", "B", "B"]
        mask = [1, 1, 1, 0, 0, 1, 1, 0, 1, 1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([1.4594])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_with_masked_single_value(self):
        X = ["A"]
        mask = [1]
        masked_X = ma.masked_array(X, mask)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_different_values(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([0, 0, 0, 0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
