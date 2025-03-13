import numpy as np
from test_characteristics.characterisitcs_test import CharacteristicsTest

from foapy import binding, intervals, mode
from foapy.characteristics import volume


class TestVolume(CharacteristicsTest):
    """
    Test list for volume calculate

    The 'volume' function calculates a characteristic volume based
    on the intervals provided.

    Test setup :
    1. Input sequence X.
    2. Transform sequence into order using 'order' function.
    3. Calculate intervals using 'intervals' function with appropriate binding and mode.
    4. Determine expected output.
    5. Match actual output from 'volume' with expected output.

    """

    epsilon = np.float_power(10, -100)

    def target(self, X, dtype=None):
        return volume(X, dtype)

    def test_dataset_1(self):
        X = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 144,
                mode.normal: 2160,
                mode.redundant: 17280,
                mode.cycle: 5184,
            },
            binding.end: {
                mode.lossy: 144,
                mode.normal: 1152,
                mode.redundant: 17280,
                mode.cycle: 5184,
            },
        }
        self.AssertBatch(X, expected, dtype=dtype)

    def test_dataset_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        dtype = None
        expected = {
            binding.start: {
                mode.lossy: 96,
                mode.normal: 10080,
                mode.redundant: 362880,
                mode.cycle: 34560,
            },
            binding.end: {
                mode.lossy: 96,
                mode.normal: 3456,
                mode.redundant: 362880,
                mode.cycle: 34560,
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

    def test_calculate_end_lossy_different_values_volume(self):
        X = ["C", "G"]
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_volume_1(self):
        X = ["A", "C", "G", "T"]
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def test_calculate_end_lossy_different_values_volume_2(self):
        X = ["2", "1"]
        self.AssertCase(X, binding.end, mode.lossy, 1)

    def test_calculate_start_lossy_different_values_volume(self):
        X = ["B", "A", "C", "D"]
        self.AssertCase(X, binding.start, mode.lossy, 1)

    # def test_calculate_start_lossy_empty_values_volume(self):
    #     X = []
    #     self.AssertCase(X, binding.start, mode.lossy, [])

    def test_calculate_start_normal_volume_1(self):
        X = ["2", "4", "2", "2", "4"]
        self.AssertCase(X, binding.start, mode.normal, 12)

    def test_overflow_int64_volume(self):
        length = 10
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        result = volume(intervals_seq)
        self.assertNotEqual(result, 0)

        length = 1000
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        result = volume(intervals_seq)
        # 0 or negative values are symptom of overflow
        self.assertTrue(result <= 0)

    def test_overflow_longdouble_volume(self):
        length = 1000
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        result = volume(intervals_seq, dtype=np.longdouble)
        self.assertNotEqual(result, 0)

        length = 10000
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        result = volume(intervals_seq, dtype=np.longdouble)
        self.assertEqual(result, np.longdouble("inf"))
