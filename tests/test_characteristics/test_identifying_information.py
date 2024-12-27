from unittest import TestCase

import numpy as np

from foapy.characteristics.identifying_information import identifying_information
from foapy.constants_intervals import binding, mode
from foapy.ma.intervals import intervals
from foapy.ma.order import order


class Test_identifying_information(TestCase):
    """
    Test list for identifying_information calculate

    The identifying_information function computes a identifying_information characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup:
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'identifying_information' with expected output.

    """

    def test_calculate_start_lossy_identifying_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.25069821459])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.3709777])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.2532824857])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_identifying_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([1.335618955])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_identifying_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([1.571])
        exists = identifying_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.77779373752225])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_identifying_information_2(self):
        X = np.array(["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.7906654768])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_2(self):
        X = np.array(["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.6895995955])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information_2(self):
        X = np.array(["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.6965784285])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_identifying_information_2(self):
        X = np.array(["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.6373048326])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_identifying_information_2(self):
        X = np.array(["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.9709505945])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.5661778097771987])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.35849625])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_identifying_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.5294637608763])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_identifying_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.76096404744368])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_identifying_information_4(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_identifying_information_4(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0.5849625007])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information_4(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.5])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_4(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.5])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_identifying_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_identifying_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_identifying_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_identifying_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_identifying_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_5(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.1462406252])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information_5(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.1462406252])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_identifying_information_5(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.3219280949])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_identifying_information_5(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([2])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_identifying_information_6(self):
        X = np.array(["A", "A", "A", "A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.102035074])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_identifying_information_6(self):
        X = np.array(["A", "A", "A", "A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.830626027])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_identifying_information_6(self):
        X = np.array(["A", "A", "A", "A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.3991235932])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_identifying_information_6(self):
        X = np.array(["A", "A", "A", "A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.6644977792])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_identifying_information(self):
        X = np.array(["C", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_identifying_information_1(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_identifying_information_2(self):
        X = np.array(["2", "1"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_identifying_information_6(self):
        X = np.array(["A", "A", "A", "A", "C", "G", "T"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        print(exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_identifying_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.210777084415])
        exists = identifying_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))
