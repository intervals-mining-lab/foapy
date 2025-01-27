from unittest import TestCase

import numpy as np

from foapy.characteristics.arithmetic_mean import arithmetic_mean
from foapy.characteristics.geometric_mean import geometric_mean
from foapy.intervals import intervals
from foapy.intervals_constants import binding, mode
from foapy.order import order


class Test_geometric_mean(TestCase):
    """
    Test list for geometric_mean calculate

    The geometric_mean function computes a geometric mean characteristic for a given
    sequence of intervals based on various configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'geometric_mean' with expected output.

    """

    def test_calculate_start_lossy_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([2.0339])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2.155])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([2.0237])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([2.1182])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_geometric_mean(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([2.3522])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_geometric_mean_1(self):
        X = ["2", "4", "2", "2", "4"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.64375])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_geometric_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([2.139826387867])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_geometric_mean_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([2.513888742864])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_geometric_mean_1(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([2.25869387])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_geometric_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([2.4953181811241978])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_geometric_mean(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([2.843527111557])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_geometric_mean(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_geometric_mean(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_geometric_mean_1(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_geometric_mean_2(self):
        X = ["2", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle(self):
        X = ["10", "87", "10", "87", "10", "87"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_1(self):
        X = ["1", "1", "3", "1", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_2(self):
        X = ["13", "13", "13", "13"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_3(self):
        X = ["A", "B", "A", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_lossy_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_lossy_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_normal_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_normal_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_redundant_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_redundant_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_start_cycle_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)

    def test_geometric_mean_less_than_arithmetic_mean_end_cycle_4(self):
        X = ["B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(delta_g <= delta_a)
