import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsInfromationalTest

from foapy import binding, mode
from foapy.characteristics import regularity
from foapy.ma import intervals, order


class Test_regularity(CharacteristicsInfromationalTest):
    """
    Test list for regularity calculate

    The regularity function computes a regularity characteristic
    for a given sequence of intervals based on various configurations
    of `binding` and `mode`.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'regularity' with expected output.

    """

    epsilon = np.float_power(10, -15)

    def target(self, X, dtype=None):
        return regularity(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 0.8547,
                mode.lossy: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 4, 4]) / np.power(np.sum([1, 4, 4]) / 3, 3),
                            np.prod([1, 3]) / np.power(np.sum([1, 3]) / 2, 2),
                            np.prod([3, 1]) / np.power(np.sum([3, 1]) / 2, 2),
                        ]
                    ),
                    1 / 7,
                ),
                # mode.normal: 0.8332,
                mode.normal: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 4, 4])
                            / np.power(np.sum([1, 1, 4, 4]) / 4, 4),
                            np.prod([3, 1, 3]) / np.power(np.sum([3, 1, 3]) / 3, 3),
                            np.prod([5, 3, 1]) / np.power(np.sum([5, 3, 1]) / 3, 3),
                        ]
                    ),
                    1 / 10,
                ),
                # mode.redundant: 0.8393,
                mode.redundant: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 4, 4, 1])
                            / np.power(
                                np.sum([1, 1, 4, 4, 1]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([3, 1, 3, 4])
                            / np.power(np.sum([3, 1, 3, 4]) / 4, 4),
                            np.prod([5, 3, 1, 2])
                            / np.power(np.sum([5, 3, 1, 2]) / 4, 4),
                        ]
                    ),
                    1 / 13,
                ),
                # mode.cycle: 0.7917,
                mode.cycle: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 4, 4])
                            / np.power(np.sum([1, 1, 4, 4]) / 4, 4),  # noqa: E261 E501
                            np.prod([6, 1, 3]) / np.power(np.sum([6, 1, 3]) / 3, 3),
                            np.prod([6, 3, 1]) / np.power(np.sum([6, 3, 1]) / 3, 3),
                        ]
                    ),
                    1 / 10,
                ),
            },
            binding.end: {
                # mode.lossy: 0.8547,
                mode.lossy: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 4, 4]) / np.power(np.sum([1, 4, 4]) / 3, 3),
                            np.prod([1, 3]) / np.power(np.sum([1, 3]) / 2, 2),
                            np.prod([3, 1]) / np.power(np.sum([3, 1]) / 2, 2),
                        ]
                    ),
                    1 / 7,
                ),
                # mode.normal: 0.8489,
                mode.normal: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 4, 4, 1])
                            / np.power(np.sum([1, 4, 4, 1]) / 4, 4),
                            np.prod([1, 3, 4]) / np.power(np.sum([1, 3, 4]) / 3, 3),
                            np.prod([3, 1, 2]) / np.power(np.sum([3, 1, 2]) / 3, 3),
                        ]
                    ),
                    1 / 10,
                ),
                # mode.redundant: 0.8393,
                mode.redundant: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 4, 4, 1])
                            / np.power(
                                np.sum([1, 1, 4, 4, 1]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([3, 1, 3, 4])
                            / np.power(np.sum([3, 1, 3, 4]) / 4, 4),
                            np.prod([5, 3, 1, 2])
                            / np.power(np.sum([5, 3, 1, 2]) / 4, 4),
                        ]
                    ),
                    1 / 13,
                ),
                # mode.cycle: 0.7917,
                mode.cycle: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 4, 4])
                            / np.power(np.sum([1, 1, 4, 4]) / 4, 4),  # noqa: E261 E501
                            np.prod([1, 3, 6]) / np.power(np.sum([1, 3, 6]) / 3, 3),
                            np.prod([3, 1, 6]) / np.power(np.sum([3, 1, 6]) / 3, 3),
                        ]
                    ),
                    1 / 10,
                ),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                # mode.lossy: 0.924481699264,
                mode.lossy: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 2, 2, 4])
                            / np.power(np.sum([1, 2, 2, 4]) / 4, 4),
                            np.prod([6]) / np.power(np.sum([6]) / 1, 1),
                            np.prod([1]) / np.power(np.sum([1]) / 1, 1),
                        ]
                    ),
                    1 / 6,
                ),
                # mode.normal: 0.848944998,
                mode.normal: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 2, 2, 4])
                            / np.power(
                                np.sum([1, 1, 2, 2, 4]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([3, 6]) / np.power(np.sum([3, 6]) / 2, 2),
                            np.prod([5]) / np.power(np.sum([5]) / 1, 1),
                            np.prod([7, 1]) / np.power(np.sum([7, 1]) / 2, 2),
                        ]
                    ),
                    1 / 10,
                ),
                # mode.redundant: 0.86439343863,
                mode.redundant: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 2, 2, 4, 1])
                            / np.power(
                                np.sum([1, 1, 2, 2, 4, 1]) / 6, 6
                            ),  # noqa: E261 E501
                            np.prod([3, 6, 2]) / np.power(np.sum([3, 6, 2]) / 3, 3),
                            np.prod([5, 6]) / np.power(np.sum([5, 6]) / 2, 2),
                            np.prod([7, 1, 3]) / np.power(np.sum([7, 1, 3]) / 3, 3),
                        ]
                    ),
                    1 / 14,
                ),
                # mode.cycle: 0.838985343,
                mode.cycle: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 2, 2, 4])
                            / np.power(
                                np.sum([1, 1, 2, 2, 4]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([4, 6]) / np.power(np.sum([4, 6]) / 2, 2),
                            np.prod([10]) / np.power(np.sum([10]) / 1, 1),
                            np.prod([9, 1]) / np.power(np.sum([9, 1]) / 2, 2),
                        ]
                    ),
                    1 / 10,
                ),
            },
            binding.end: {
                # mode.lossy: 0.924481699264,
                mode.lossy: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 2, 2, 4])
                            / np.power(np.sum([1, 2, 2, 4]) / 4, 4),
                            np.prod([6]) / np.power(np.sum([6]) / 1, 1),
                            np.prod([1]) / np.power(np.sum([1]) / 1, 1),
                        ]
                    ),
                    1 / 6,
                ),
                # mode.normal: 0.88086479457968535,
                mode.normal: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 2, 2, 4, 1])
                            / np.power(
                                np.sum([1, 2, 2, 4, 1]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([6, 2]) / np.power(np.sum([6, 2]) / 2, 2),
                            np.prod([6]) / np.power(np.sum([6]) / 1, 1),
                            np.prod([1, 3]) / np.power(np.sum([1, 3]) / 2, 2),
                        ]
                    ),
                    1 / 10,
                ),
                # mode.redundant: 0.86439343863,
                mode.redundant: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 1, 2, 2, 4, 1])
                            / np.power(
                                np.sum([1, 1, 2, 2, 4, 1]) / 6, 6
                            ),  # noqa: E261 E501
                            np.prod([3, 6, 2]) / np.power(np.sum([3, 6, 2]) / 3, 3),
                            np.prod([5, 6]) / np.power(np.sum([5, 6]) / 2, 2),
                            np.prod([7, 1, 3]) / np.power(np.sum([7, 1, 3]) / 3, 3),
                        ]
                    ),
                    1 / 14,
                ),
                # mode.cycle: 0.838985343,
                mode.cycle: np.float_power(
                    np.prod(
                        [
                            np.prod([1, 2, 2, 4, 1])
                            / np.power(
                                np.sum([1, 2, 2, 4, 1]) / 5, 5
                            ),  # noqa: E261 E501
                            np.prod([6, 4]) / np.power(np.sum([6, 4]) / 2, 2),
                            np.prod([10]) / np.power(np.sum([10]) / 1, 1),
                            np.prod([1, 9]) / np.power(np.sum([1, 9]) / 2, 2),
                        ]
                    ),
                    1 / 10,
                ),
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_3(self):
        X = ["C", "C", "C", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 1,
                mode.normal: 1,
                mode.redundant: 1,
                mode.cycle: 1,
            },
            binding.end: {
                mode.lossy: 1,
                mode.normal: 1,
                mode.redundant: 1,
                mode.cycle: 1,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_calculate_end_lossy_different_values_descriptive_information(self):
        X = ["C", "G"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_descriptive_information_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_end_lossy_different_values_descriptive_information_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, 0)

    def test_calculate_start_normal_regularity_1(self):
        X = ["2", "4", "2", "2", "4"]
        # 0.9587
        expected = np.float_power(
            np.prod(
                [
                    np.prod([1, 2, 1]) / np.power(np.sum([1, 2, 1]) / 3, 3),
                    np.prod([2, 3]) / np.power(np.sum([2, 3]) / 2, 2),
                ]
            ),
            1 / 5,
        )
        self.AssertCase(X, binding.start, mode.normal, expected)

    def AssertInEquality(self, X):
        X = np.asanyarray(X)
        order_seq = order(X)

        for b in [binding.start, binding.end]:
            for m in [mode.lossy, mode.normal, mode.redundant, mode.cycle]:
                intervals_seq = intervals(order_seq, b, m)
                r = regularity(intervals_seq)
                err_msg = f"0 <= r <= 1 | Binding {b}, mode {m}: " f"r={r}"
                self.assertTrue(0 <= r <= 1, err_msg)

    def test_inequality_1(self):
        X = ["10", "87", "10", "87", "10", "87"]
        self.AssertInEquality(X)

    def test_inequality_2(self):
        X = ["1", "1", "3", "1", "1"]
        self.AssertInEquality(X)

    def test_inequality_3(self):
        X = ["13", "13", "13", "13"]
        self.AssertInEquality(X)

    def test_inequality_4(self):
        X = ["A", "B", "A", "B"]
        self.AssertInEquality(X)

    def test_inequality_5(self):
        X = ["B"]
        self.AssertInEquality(X)
