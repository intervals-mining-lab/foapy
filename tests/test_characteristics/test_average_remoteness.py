from unittest import TestCase

import numpy as np

from foapy.characteristics.average_remoteness import average_remoteness
from foapy.characteristics.identifying_information import identifying_information
from foapy.intervals import intervals
from foapy.intervals_constants import binding, mode
from foapy.ma.intervals import intervals as intervals_ma
from foapy.ma.order import order as order_ma
from foapy.order import order


class Test_average_remoteness(TestCase):
    """
    Test list for average_remoteness calculate

    The average_remoteness function computes a average remoteness characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'average_remoteness' with expected output.

    """

    def test_calculate_start_lossy_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.0242])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.1077])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.017])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        expected = np.array([1.0828])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_average_remoteness(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        expected = np.array([1.234])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = []
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness_1(self):
        X = ["2", "4", "2", "2", "4"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.7169925])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_same_values_average_remoteness(self):
        X = ["C", "C", "C", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness_4(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.1462406252])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.1462406252])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.1462406252])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_average_remoteness_2(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([2])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_average_remoteness_3(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_average_remoteness_3(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([0.5])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_3(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.5])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_5(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([0.5])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.09749375])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.3299208])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.17548874963])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.31922378713])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_average_remoteness_6(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.5076815597])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([1.6726956021])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.4943064208])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([1.4621136113])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.3948590506])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_average_remoteness_7(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.8112989210])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        expected = np.array([1.102035074])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        expected = np.array([0.654994643])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_redundant_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        expected = np.array([1.1181098199])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_cycle_average_remoteness_8(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        expected = np.array([1.4888663952])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_average_remoteness(self):
        X = ["C", "G"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_average_remoteness_1(self):
        X = ["A", "C", "G", "T"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_lossy_different_values_average_remoteness_2(self):
        X = ["2", "1"]
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.00001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_average_remoteness_less_than_identifying_information_start_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle(self):
        X = np.array(["10", "87", "10", "87", "10", "87"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_1(
        self,
    ):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_1(self):
        X = np.array(["1", "1", "3", "1", "1"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_2(
        self,
    ):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_2(self):
        X = np.array(["13", "13", "13", "13"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_3(
        self,
    ):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_3(self):
        X = np.array(["A", "B", "A", "B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_lossy_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.lossy)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_normal_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.normal)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_redundant_4(
        self,
    ):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_redundant_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.redundant)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.redundant)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_start_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.start, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.start, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)

    def test_average_remoteness_less_than_identifying_information_end_cycle_4(self):
        X = np.array(["B"])
        order_seq = order(X)
        ma_order_seq = order_ma(X)
        intervals_seq = intervals(order_seq, binding.end, mode.cycle)
        ma_intervals_seq = intervals_ma(ma_order_seq, binding.end, mode.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(ma_intervals_seq)
        self.assertTrue(g <= H)
