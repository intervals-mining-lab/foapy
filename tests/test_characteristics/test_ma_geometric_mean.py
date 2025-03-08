from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import arithmetic_mean, geometric_mean
from foapy.ma import intervals, order


class TestGeometricMean(TestCase):
    """
    Test list for geometric_mean calculate
    """

    def test_calculate_start_normal_geometric_mean(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1.259921, 2.44948974])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal_geometric_mean_2(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1, 2, 3])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_geometric_mean(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([3, 2, 1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_geometric_mean(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([2.5198, 1.73205, 1.73205])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([2, 2.08008382, 2.46621207])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([2, 2.28942, 1.8171])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([1.74110, 2.44948, 2.34034])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([2, 2.6207, 2.6207])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
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
        expected = np.array([2.449489])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calulate_normal_with_the_same_values(self):
        X = ["A", "A", "A", "A", "A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
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
        expected = np.array([0])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle_with_single_value(self):
        X = ["A"]
        masked_X = ma.masked_array(X)
        order_seq = order(masked_X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([1])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_different_values(self):
        X = ma.masked_array(["B", "A", "C", "D"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([0, 0, 0, 0])
        exists = geometric_mean(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_inequalities_start_lossy(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_lossy(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_normal(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_normal(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_cycle(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_cycle(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_redunant(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_redunant(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_lossy_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_lossy_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_normal_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_normal_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_cycle_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_cycle_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_redunant_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_redunant_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_lossy_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_lossy_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_normal_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_normal_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_cycle_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_cycle_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_redunant_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_redunant_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_lossy_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_lossy_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_normal_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_normal_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_cycle_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_cycle_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_redunant_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_redunant_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_lossy_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_lossy_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_normal_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_normal_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_cycle_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_cycle_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_start_redunant_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))

    def test_calculate_inequalities_end_redunant_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        delta_g = geometric_mean(intervals_seq)
        delta_a = arithmetic_mean(intervals_seq)
        self.assertTrue(np.all(delta_g <= delta_a))
