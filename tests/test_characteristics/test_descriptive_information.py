from unittest import TestCase

import numpy as np

from foapy import binding, intervals, mode, order
from foapy.characteristics import descriptive_information, geometric_mean
from foapy.ma import intervals as intervals_ma
from foapy.ma import order as order_ma


class Test_descriptive_information(TestCase):
    """
    Test list for descriptive_information calculate

    The descriptive_information function computes a descriptive information
    characteristic for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'descriptive_information' with expected output.

    """

    def test_calculate_start_lossy_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.lossy)
        expected = np.array([2.37956557896877])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.normal)
        expected = np.array([2.58645791024])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.normal)
        expected = np.array([2.383831871])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.redundant)
        expected = np.array([2.52382717296366])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_descriptive_information(self):
        X = np.array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.cycle)
        expected = np.array([2.971])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.normal)
        expected = np.array([1.71450693])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.normal)
        expected = np.array([2.9611915354687])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.normal)
        expected = np.array([2.56417770797363])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.redundant)
        expected = np.array([2.8867851948])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_descriptive_information_2(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.cycle)
        expected = np.array([3.389245277])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.normal)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.normal)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.redundant)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_descriptive_information(self):
        X = np.array(["C", "C", "C", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information(self):
        X = np.array(["C", "G"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information_1(self):
        X = np.array(["A", "C", "G", "T"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_descriptive_information_2(self):
        X = np.array(["2", "1"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.end, mode.lossy)
        expected = np.array([1])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_descriptive_information_3(self):
        X = np.array(["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"])
        order_seq = order_ma(X)
        intervals_seq = intervals_ma(order_seq, binding.start, mode.lossy)
        expected = np.array([2.314622766])
        exists = descriptive_information(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_geometric_mean_less_than_descriptive_information_start_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_redundant_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_redundant_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_redundant_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_redundant_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_redundant_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_redundant_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_redundant_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_redundant_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_start_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)

    def test_geometric_mean_less_than_descriptive_information_end_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        D = descriptive_information(ma_intervals_seq)
        self.assertTrue(delta_g <= D)
