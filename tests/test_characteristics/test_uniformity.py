import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import uniformity


class Test_uniformity(CharacteristicsInfromationalTest):
    """
    Test list for uniformity calculate

    The uniformity function computes a uniformity characteristic for
    a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'uniformity' with expected output.

    """

    epsilon = np.float_power(10, -15)

    def target(self, X, dtype=None):
        return uniformity(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 0.22649821459,
                mode.lossy: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 4, 4]) / 3, 3) / np.prod([1, 4, 4])
                        ),
                        np.log2(np.power(np.sum([1, 3]) / 2, 2) / np.prod([1, 3])),
                        np.log2(np.power(np.sum([3, 1]) / 2, 2) / np.prod([3, 1])),
                    ]
                )
                / 7,
                # mode.normal: 0.2632777,
                mode.normal: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 4, 4]) / 4, 4)
                            / np.prod([1, 1, 4, 4])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([3, 1, 3]) / 3, 3) / np.prod([3, 1, 3])
                        ),
                        np.log2(
                            np.power(np.sum([5, 3, 1]) / 3, 3) / np.prod([5, 3, 1])
                        ),
                    ]
                )
                / 10,
                # mode.redundant: 0.252818955,
                mode.redundant: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 4, 4, 1]) / 5, 5)
                            / np.prod([1, 1, 4, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([3, 1, 3, 4]) / 4, 4)
                            / np.prod([3, 1, 3, 4])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([5, 3, 1, 2]) / 4, 4)
                            / np.prod([5, 3, 1, 2])
                        ),  # noqa: E261 E501
                    ]
                )
                / 13,
                # mode.cycle: 0.337,
                mode.cycle: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 4, 4]) / 4, 4)
                            / np.prod([1, 1, 4, 4])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([6, 1, 3]) / 3, 3) / np.prod([6, 1, 3])
                        ),
                        np.log2(
                            np.power(np.sum([6, 3, 1]) / 3, 3) / np.prod([6, 3, 1])
                        ),
                    ]
                )
                / 10,
            },
            binding.end: {
                # mode.lossy: 0.22649821459,
                mode.lossy: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 4, 4]) / 3, 3) / np.prod([1, 4, 4])
                        ),
                        np.log2(np.power(np.sum([1, 3]) / 2, 2) / np.prod([1, 3])),
                        np.log2(np.power(np.sum([3, 1]) / 2, 2) / np.prod([3, 1])),
                    ]
                )
                / 7,
                # mode.normal: 0.2362824857,
                mode.normal: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 4, 4, 1]) / 4, 4)
                            / np.prod([1, 4, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([1, 3, 4]) / 3, 3) / np.prod([1, 3, 4])
                        ),
                        np.log2(
                            np.power(np.sum([3, 1, 2]) / 3, 3) / np.prod([3, 1, 2])
                        ),
                    ]
                )
                / 10,
                # mode.redundant: 0.252818955,
                mode.redundant: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 4, 4, 1]) / 5, 5)
                            / np.prod([1, 1, 4, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([3, 1, 3, 4]) / 4, 4)
                            / np.prod([3, 1, 3, 4])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([5, 3, 1, 2]) / 4, 4)
                            / np.prod([5, 3, 1, 2])
                        ),  # noqa: E261 E501
                    ]
                )
                / 13,
                # mode.cycle: 0.337,
                mode.cycle: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 4, 4, 1]) / 4, 4)
                            / np.prod([1, 4, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([1, 3, 6]) / 3, 3) / np.prod([1, 3, 6])
                        ),
                        np.log2(
                            np.power(np.sum([3, 1, 6]) / 3, 3) / np.prod([3, 1, 6])
                        ),
                    ]
                )
                / 10,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 0.113283334415,
                mode.lossy: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 2, 2, 4]) / 4, 4)
                            / np.prod([1, 2, 2, 4])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([6]) / 1, 1) / np.prod([6])),
                        np.log2(np.power(np.sum([1]) / 1, 1) / np.prod([1])),
                    ]
                )
                / 6,
                # mode.normal: 0.2362570097771987,
                mode.normal: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 2, 2, 4]) / 5, 5)
                            / np.prod([1, 1, 2, 2, 4])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([3, 6]) / 2, 2) / np.prod([3, 6])),
                        np.log2(np.power(np.sum([5]) / 1, 1) / np.prod([5])),
                        np.log2(np.power(np.sum([7, 1]) / 2, 2) / np.prod([7, 1])),
                    ]
                )
                / 10,
                # mode.redundant: 0.2102399737463,
                mode.redundant: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 2, 2, 4, 1]) / 6, 6)
                            / np.prod([1, 1, 2, 2, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([3, 6, 2]) / 3, 3) / np.prod([3, 6, 2])
                        ),
                        np.log2(np.power(np.sum([5, 6]) / 2, 2) / np.prod([5, 6])),
                        np.log2(
                            np.power(np.sum([7, 1, 3]) / 3, 3) / np.prod([7, 1, 3])
                        ),
                    ]
                )
                / 14,
                # mode.cycle: 0.25328248774368,
                mode.cycle: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 2, 2, 4]) / 5, 5)
                            / np.prod([1, 1, 2, 2, 4])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([4, 6]) / 2, 2) / np.prod([4, 6])),
                        np.log2(np.power(np.sum([10]) / 1, 1) / np.prod([10])),
                        np.log2(np.power(np.sum([9, 1]) / 2, 2) / np.prod([9, 1])),
                    ]
                )
                / 10,
            },
            binding.end: {
                # mode.lossy: 0.113283334415,
                mode.lossy: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 2, 2, 4]) / 4, 4)
                            / np.prod([1, 2, 2, 4])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([6]) / 1, 1) / np.prod([6])),
                        np.log2(np.power(np.sum([1]) / 1, 1) / np.prod([1])),
                    ]
                )
                / 6,
                # mode.normal: 0.18300750037,
                mode.normal: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 2, 2, 4, 1]) / 5, 5)
                            / np.prod([1, 2, 2, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([6, 2]) / 2, 2) / np.prod([6, 2])),
                        np.log2(np.power(np.sum([6]) / 1, 1) / np.prod([6])),
                        np.log2(np.power(np.sum([1, 3]) / 2, 2) / np.prod([1, 3])),
                    ]
                )
                / 10,
                # mode.redundant: 0.2102399737463,
                mode.redundant: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 1, 2, 2, 4, 1]) / 6, 6)
                            / np.prod([1, 1, 2, 2, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(
                            np.power(np.sum([3, 6, 2]) / 3, 3) / np.prod([3, 6, 2])
                        ),
                        np.log2(np.power(np.sum([5, 6]) / 2, 2) / np.prod([5, 6])),
                        np.log2(
                            np.power(np.sum([7, 1, 3]) / 3, 3) / np.prod([7, 1, 3])
                        ),
                    ]
                )
                / 14,
                # mode.cycle: 0.25328248774368,
                mode.cycle: np.sum(
                    [
                        np.log2(
                            np.power(np.sum([1, 2, 2, 4, 1]) / 5, 5)
                            / np.prod([1, 2, 2, 4, 1])
                        ),  # noqa: E261 E501
                        np.log2(np.power(np.sum([6, 4]) / 2, 2) / np.prod([6, 4])),
                        np.log2(np.power(np.sum([10]) / 1, 1) / np.prod([10])),
                        np.log2(np.power(np.sum([1, 9]) / 2, 2) / np.prod([1, 9])),
                    ]
                )
                / 10,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = None
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

    def test_calculate_end_lossy_different_values_uniformity(self):
        X = np.array(["C", "G"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_uniformity_1(self):
        X = np.array(["A", "C", "G", "T"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_uniformity_2(self):
        X = np.array(["2", "1"])
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_uniformity_1(self):
        X = np.array(["2", "4", "2", "2", "4"])
        expected = (
            np.sum(
                [
                    np.log2(np.power(np.sum([1, 2, 1]) / 3, 3) / np.prod([1, 2, 1])),
                    np.log2(np.power(np.sum([2, 3]) / 2, 2) / np.prod([2, 3])),
                ]
            )
            / 5
        )
        self.AssertCase(X, binding.start, mode.normal, expected)
