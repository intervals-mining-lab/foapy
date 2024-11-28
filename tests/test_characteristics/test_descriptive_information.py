from unittest import TestCase

import numpy as np

from foapy.characteristics.descriptive_information import descriptive_information
from foapy.constants_intervals import binding, mode
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class Test_descriptive_information(TestCase):
    """
    Test list for descriptive_information calculate

    The descriptive_information function computes a descriptive information
    characteristic for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup:
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'descriptive_information' with expected output.

    """

    def test_calculate_start_lossy_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([2.37956557896877])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2.58645791024])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([2.383831871])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([2.52382717296366])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([2.971])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.71450693])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2.9611915354687])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([2.56417770797363])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([2.8867851948])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([3.389245277])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
