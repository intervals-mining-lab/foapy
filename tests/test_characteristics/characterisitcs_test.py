from unittest import TestCase

import numpy as np

import foapy.ma as ma
from foapy import binding, intervals, mode, order


class CharacteristicsTest(TestCase):
    epsilon = np.float_power(10, -100)

    def target(self, X):
        pass

    def AssertCase(self, X, binding, mode, expected, dtype=None):
        order_seq = order(X)
        intervals_seq = intervals(order_seq, binding, mode)
        exists = self.target(intervals_seq, dtype)

        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        err_message = f"Binding: {binding}, Mode: {mode}, Diff: {diff} > {self.epsilon}"
        self.assertTrue(diff < self.epsilon, err_message)

    def AssertBatch(self, X, batch, dtype=None):
        for _binding, v in batch.items():
            for _mode, expected in v.items():
                self.AssertCase(X, _binding, _mode, expected, dtype)

    def GetPrecision(self, length, dtype=None):
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = intervals(X, binding.start, mode.normal)
        return self.target(intervals_seq, dtype)


class CharacteristicsInfromationalTest(CharacteristicsTest):

    def AssertCase(self, X, binding, mode, expected, dtype=None):
        X = np.array(X)
        order_seq = ma.order(X)
        intervals_seq = ma.intervals(order_seq, binding, mode)
        exists = self.target(intervals_seq, dtype)

        if expected < exists:
            diff = exists - expected
        else:
            diff = expected - exists
        err_message = f"Binding: {binding}, Mode: {mode}, Diff: {diff} > {self.epsilon}"
        self.assertTrue(diff < self.epsilon, err_message)


class MACharacteristicsTest(TestCase):
    epsilon = np.float_power(10, -100)

    def target(self, X):
        pass

    def AssertCase(self, X, binding, mode, expected, dtype=None):
        order_seq = ma.order(X)
        intervals_seq = ma.intervals(order_seq, binding, mode)
        expected = np.array(expected)
        exists = self.target(intervals_seq, dtype)

        self.assertEqual(len(expected), len(exists))

        diff = np.absolute(expected - exists)
        err_message = f"Binding: {binding}, Mode: {mode}, Diff: {diff} > {self.epsilon}"
        self.assertTrue(np.all(diff < self.epsilon), err_message)

    def AssertBatch(self, X, batch, dtype=None):
        for _binding, v in batch.items():
            for _mode, expected in v.items():
                self.AssertCase(X, _binding, _mode, expected, dtype)

    def GetPrecision(self, length, dtype=None):
        alphabet = np.arange(0, np.fix(length * 0.2), dtype=int)
        X = np.random.choice(alphabet, length)
        intervals_seq = ma.intervals(X, binding.start, mode.normal)
        return self.target(intervals_seq, dtype)
