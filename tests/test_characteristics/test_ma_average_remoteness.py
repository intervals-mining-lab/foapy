from unittest import TestCase

import numpy as np
import numpy.ma as ma

from foapy import binding as binding_constant
from foapy import mode as mode_constant
from foapy.characteristics.ma import average_remoteness, identifying_information
from foapy.ma import intervals, order


class TestMaAverageRemoteness(TestCase):
    """
    Test list for average remoteness calculate
    """

    def test_calculate_start_normal_average_remoteness(self):
        X = ma.masked_array([2, 4, 2, 2, 4])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0.3333333, 1.29248])
        exists = average_remoteness(intervals_seq)

        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_average_remoteness_2(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([0, 1, 1.5849625])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal_average_remoteness(self):
        X = ma.masked_array([1, 2, 3])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1.5849625, 1, 0])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy_empty_values_average_remoteness(self):
        X = ma.masked_array([])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_lossy(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        expected = np.array([1.3333, 0.79248, 0.79248])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        expected = np.array([1, 1.05664, 1.30229])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_end_normal(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        expected = np.array([1, 1.1949, 0.8616])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_redunant(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        expected = np.array([0.8, 1.2924, 1.2267])
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_start_cycle(self):
        X = ma.masked_array(["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        expected = np.array([1, 1.389975, 1.389975])
        exists = average_remoteness(intervals_seq)
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
        expected = np.array([1.2925])
        exists = average_remoteness(intervals_seq)
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
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
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
        exists = average_remoteness(intervals_seq)
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
        expected = np.array([0])
        exists = average_remoteness(intervals_seq)
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
        exists = average_remoteness(intervals_seq)
        epsilon = 0.0001
        diff = np.absolute(expected - exists)
        self.assertTrue(np.all(diff < epsilon))

    def test_calculate_inequalities_start_lossy(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_lossy(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_normal(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_normal(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_cycle(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_cycle(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_redunant(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_redunant(self):
        X = ma.masked_array([38, 9, 38, 9, 38, 9])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_lossy_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_lossy_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_normal_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_normal_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_cycle_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_cycle_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_redunant_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_redunant_2(self):
        X = ma.masked_array([2, 2, 1, 2, 2])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_lossy_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_lossy_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_normal_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_normal_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_cycle_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_cycle_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_redunant_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_redunant_3(self):
        X = ma.masked_array([1])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_lossy_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_lossy_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_normal_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_normal_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_cycle_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_cycle_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_redunant_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_redunant_4(self):
        X = ma.masked_array(["G", "G", "G", "G"])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_lossy_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.lossy
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_lossy_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.lossy)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_normal_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.normal
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_normal_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.normal)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_cycle_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.cycle
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_cycle_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding_constant.end, mode_constant.cycle)
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_start_redunant_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.start, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))

    def test_calculate_inequalities_end_redunant_5(self):
        X = ma.masked_array([58, 58, 100, 100])
        order_seq = order(X)
        intervals_seq = intervals(
            order_seq, binding_constant.end, mode_constant.redundant
        )
        g = average_remoteness(intervals_seq)
        H = identifying_information(intervals_seq)
        self.assertTrue(np.all(g <= H))
