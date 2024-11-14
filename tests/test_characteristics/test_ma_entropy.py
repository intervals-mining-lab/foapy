from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy.characteristics.ma.entropy import entropy
from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class TestMaEntropy(TestCase):
    """
    Test list for entropy calculate
    """

    def test_calculate_start_normalf_entropy(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.415037499, 1.321928094887])
        exists = entropy(intervals_seq)
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
        exists = entropy(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_single_elements_normal_entropy(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1.5849625, 1, 0])
        exists = entropy(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_single_element_lossy_entropy(self):
        X = ma.masked_array(["B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([0])
        exists = entropy(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_void_lossy_entropy(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        expected = np.array([])
        exists = entropy(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
