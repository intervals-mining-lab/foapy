from unittest import TestCase

import numpy as np

from foapy.characteristics.uniformity import uniformity
from foapy.constants_intervals import binding, mode
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class Test_uniformity(TestCase):
    """
    Test list for uniformity calculate

    The uniformity function computes a uniformity characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup:
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'uniformity' with expected output.

    """

    def test_calculate_start_lossy_uniformity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0.22649821459])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_uniformity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.2632777])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_uniformity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.2362824857])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_uniformity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([0.252818955])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_uniformity(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([0.337])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_uniformity_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.06080123752225])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_uniformity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.2362570097771987])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_uniformity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.18300750037])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_uniformity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0.2102399737463])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_uniformity_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0.25328248774368])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_uniformity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_uniformity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_uniformity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_uniformity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_uniformity(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0])
        exists = uniformity(intervals_seq)
        epsilon = 0.01
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
