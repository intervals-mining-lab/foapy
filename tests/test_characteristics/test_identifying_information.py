import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import identifying_information


class Test_identifying_information(CharacteristicsInfromationalTest):
    """
    Test list for identifying_information calculate

    The identifying_information function computes a identifying_information
    characteristic for a given sequence of intervals based on various
    configurations of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'identifying_information' with expected output.
    """

    epsilon = np.float_power(10, -10)

    def target(self, X, dtype=None):
        return identifying_information(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 1.25069821459,
                mode.lossy: 1
                / 7
                * np.sum(
                    [
                        3 * np.log2(np.sum([1, 4, 4]) / 3),
                        2 * np.log2(np.sum([1, 3]) / 2),
                        2 * np.log2(np.sum([3, 1]) / 2),
                    ],
                ),
                # mode.normal: 1.3709777,
                mode.normal: 1
                / 10
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 1, 4, 4]) / 4),
                        3 * np.log2(np.sum([3, 1, 3]) / 3),
                        3 * np.log2(np.sum([5, 3, 1]) / 3),
                    ],
                ),
                # mode.redundant: 1.335618955,
                mode.redundant: 1
                / 13
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 1, 4, 4, 1]) / 5),
                        4 * np.log2(np.sum([3, 1, 3, 4]) / 4),
                        4 * np.log2(np.sum([5, 3, 1, 2]) / 4),
                    ]
                ),
                # mode.cycle: 1.571
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 1, 4, 4]) / 4),
                        3 * np.log2(np.sum([6, 1, 3]) / 3),
                        3 * np.log2(np.sum([6, 3, 1]) / 3),
                    ]
                ),
            },
            binding.end: {
                # mode.lossy: 1.25069821459,
                mode.lossy: 1
                / 7
                * np.sum(
                    [
                        3 * np.log2(np.sum([1, 4, 4]) / 3),
                        2 * np.log2(np.sum([1, 3]) / 2),
                        2 * np.log2(np.sum([3, 1]) / 2),
                    ]
                ),
                # mode.redundant: 1.335618955,
                mode.redundant: 1
                / 13
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 1, 4, 4, 1]) / 5),
                        4 * np.log2(np.sum([3, 1, 3, 4]) / 4),
                        4 * np.log2(np.sum([5, 3, 1, 2]) / 4),
                    ]
                ),
                # mode.cycle: 1.571
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 4, 4, 1]) / 4),
                        3 * np.log2(np.sum([1, 3, 6]) / 3),
                        3 * np.log2(np.sum([3, 1, 6]) / 3),
                    ]
                ),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["A", "C", "T", "T", "G", "A", "T", "A", "C", "G"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 1.7906654768,
                mode.lossy: 1
                / 6
                * np.sum(
                    [
                        2 * np.log2(np.sum([5, 2]) / 2),
                        1 * np.log2(np.sum([7]) / 1),
                        2 * np.log2(np.sum([1, 3]) / 2),
                        1 * np.log2(np.sum([5]) / 1),
                    ]
                ),
                # mode.normal: 1.6895995955,
                mode.normal: 1
                / 10
                * np.sum(
                    [
                        3 * np.log2(np.sum([1, 5, 2]) / 3),
                        2 * np.log2(np.sum([2, 7]) / 2),
                        3 * np.log2(np.sum([3, 1, 3]) / 3),
                        2 * np.log2(np.sum([5, 5]) / 2),
                    ]
                ),
                # mode.redundant: 1.6373048326,
                mode.redundant: 1
                / 14
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 5, 2, 3]) / 4),
                        3 * np.log2(np.sum([2, 7, 2]) / 3),
                        4 * np.log2(np.sum([3, 1, 3, 4]) / 4),
                        3 * np.log2(np.sum([5, 5, 1]) / 3),
                    ]
                ),
                # mode.cycle: 1.9709505945,
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        3 * np.log2(np.sum([3, 5, 2]) / 3),
                        2 * np.log2(np.sum([3, 7]) / 2),
                        3 * np.log2(np.sum([6, 1, 3]) / 3),
                        2 * np.log2(np.sum([5, 5]) / 2),
                    ]
                ),
            },
            binding.end: {
                # mode.lossy: 1.7906654768,
                mode.lossy: 1
                / 6
                * np.sum(
                    [
                        2 * np.log2(np.sum([5, 2]) / 2),
                        1 * np.log2(np.sum([7]) / 1),
                        2 * np.log2(np.sum([1, 3]) / 2),
                        1 * np.log2(np.sum([5]) / 1),
                    ]
                ),
                # mode.normal: 1.6965784285,
                mode.normal: 1
                / 10
                * np.sum(
                    [
                        3 * np.log2(np.sum([5, 2, 3]) / 3),
                        2 * np.log2(np.sum([7, 2]) / 2),
                        3 * np.log2(np.sum([1, 3, 4]) / 3),
                        2 * np.log2(np.sum([5, 1]) / 2),
                    ]
                ),
                # mode.redundant: 1.6373048326,
                mode.redundant: 1
                / 14
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 5, 2, 3]) / 4),
                        3 * np.log2(np.sum([2, 7, 2]) / 3),
                        4 * np.log2(np.sum([3, 1, 3, 4]) / 4),
                        3 * np.log2(np.sum([5, 5, 1]) / 3),
                    ]
                ),
                # mode.cycle: 1.9709505945,
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        3 * np.log2(np.sum([5, 2, 3]) / 3),
                        2 * np.log2(np.sum([7, 3]) / 2),
                        3 * np.log2(np.sum([1, 3, 6]) / 3),
                        2 * np.log2(np.sum([5, 5]) / 2),
                    ]
                ),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 1.210777084415,
                mode.lossy: 1
                / 6
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 2, 2, 4]) / 4),
                        1 * np.log2(np.sum([6]) / 1),
                        1 * np.log2(np.sum([1]) / 1),
                    ]
                ),
                # mode.normal: 1.5661778097771987,
                mode.normal: 1
                / 10
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 1, 2, 2, 4]) / 5),
                        2 * np.log2(np.sum([3, 6]) / 2),
                        1 * np.log2(np.sum([5]) / 1),
                        2 * np.log2(np.sum([7, 1]) / 2),
                    ]
                ),
                # mode.redundant: 1.5294637608763,
                mode.redundant: 1
                / 14
                * np.sum(
                    [
                        6 * np.log2(np.sum([1, 1, 2, 2, 4, 1]) / 6),
                        3 * np.log2(np.sum([3, 6, 2]) / 3),
                        2 * np.log2(np.sum([5, 6]) / 2),
                        3 * np.log2(np.sum([7, 1, 3]) / 3),
                    ]
                ),
                # mode.cycle: 1.76096404744368,
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 1, 2, 2, 4]) / 5),
                        2 * np.log2(np.sum([4, 6]) / 2),
                        1 * np.log2(np.sum([10]) / 1),
                        2 * np.log2(np.sum([9, 1]) / 2),
                    ]
                ),
            },
            binding.end: {
                # mode.lossy: 1.210777084415,
                mode.lossy: 1
                / 6
                * np.sum(
                    [
                        4 * np.log2(np.sum([1, 2, 2, 4]) / 4),
                        1 * np.log2(np.sum([6]) / 1),
                        1 * np.log2(np.sum([1]) / 1),
                    ]
                ),
                # mode.normal: 1.35849625,
                mode.normal: 1
                / 10
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 2, 2, 4, 1]) / 5),
                        2 * np.log2(np.sum([6, 2]) / 2),
                        1 * np.log2(np.sum([6]) / 1),
                        2 * np.log2(np.sum([1, 3]) / 2),
                    ]
                ),
                # mode.redundant: 1.5294637608763,
                mode.redundant: 1
                / 14
                * np.sum(
                    [
                        6 * np.log2(np.sum([1, 1, 2, 2, 4, 1]) / 6),
                        3 * np.log2(np.sum([3, 6, 2]) / 3),
                        2 * np.log2(np.sum([5, 6]) / 2),
                        3 * np.log2(np.sum([7, 1, 3]) / 3),
                    ]
                ),
                # mode.cycle: 1.76096404744368,
                mode.cycle: 1
                / 10
                * np.sum(
                    [
                        5 * np.log2(np.sum([1, 2, 2, 4, 1]) / 5),
                        2 * np.log2(np.sum([6, 4]) / 2),
                        1 * np.log2(np.sum([10]) / 1),
                        2 * np.log2(np.sum([1, 9]) / 2),
                    ]
                ),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_4(self):
        X = ["C", "G"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5849625007,
                mode.cycle: 1,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0.5,
                mode.redundant: 0.5849625007,
                mode.cycle: 1,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_5(self):
        X = ["C", "C", "C", "C"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 0,
                mode.redundant: 0,
                mode.cycle: 0,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0,
                mode.redundant: 0,
                mode.cycle: 0,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_6(self):
        X = ["A", "C", "G", "T"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 1.1462406252,
                mode.redundant: 1.3219280949,
                mode.cycle: 2,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 1.1462406252,
                mode.redundant: 1.3219280949,
                mode.cycle: 2,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_7(self):
        X = ["A", "A", "A", "A", "C", "G", "T"]
        dtype = np.longdouble
        expected = {
            binding.start: {
                mode.lossy: 0,
                mode.normal: 1.102035074,
                mode.redundant: 1.3991235932,
                mode.cycle: 1.6644977792,
            },
            binding.end: {
                mode.lossy: 0,
                mode.normal: 0.830626027,
                mode.redundant: 1.3991235932,
                mode.cycle: 1.6644977792,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_identifying_information_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_identifying_information_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        self.AssertCase(X, binding.start, mode.normal, 0.77779373752225)
