from unittest import TestCase

import numpy as np

from foapy import intervals, order


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
