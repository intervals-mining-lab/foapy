from unittest import TestCase

import numpy as np

from foapy import binding, chain_mode
from foapy.core import intervals_chain


class TestChainModeCallable(TestCase):
    """
    Test chain_mode(chain) callable form.

    Verifies that chain_mode(chain) correctly identifies whether a chain was
    built with chain_mode.boundary or chain_mode.cycle via the sum property:
    in cycle mode, every element's interval group sums to n.
    """

    # -------------------------------------------------------------------------
    # Empty chain — returns chain_mode.cycle by default
    # -------------------------------------------------------------------------

    def test_empty_chain_returns_cycle(self):
        chain = np.array([], dtype=np.intp)
        result = chain_mode(chain)
        self.assertEqual(result, chain_mode.cycle)

    def test_empty_list_returns_cycle(self):
        result = chain_mode([])
        self.assertEqual(result, chain_mode.cycle)

    # -------------------------------------------------------------------------
    # Chains from chain_mode.boundary
    # -------------------------------------------------------------------------

    def test_boundary_mixed_start(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    def test_boundary_mixed_end(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    def test_boundary_integers_start(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    def test_boundary_all_unique_start(self):
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    def test_boundary_all_unique_end(self):
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    # -------------------------------------------------------------------------
    # Chains from chain_mode.cycle
    # -------------------------------------------------------------------------

    def test_cycle_mixed_start(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(chain_mode(chain), chain_mode.cycle)

    def test_cycle_mixed_end(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        self.assertEqual(chain_mode(chain), chain_mode.cycle)

    def test_cycle_integers_start(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(chain_mode(chain), chain_mode.cycle)

    def test_cycle_integers_end(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        self.assertEqual(chain_mode(chain), chain_mode.cycle)

    def test_cycle_all_identical_start(self):
        X = ["a", "a", "a"]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(chain_mode(chain), chain_mode.cycle)

    # -------------------------------------------------------------------------
    # Sum property: cycle chains sum to n * k
    # -------------------------------------------------------------------------

    def test_cycle_chain_sum_divisible_by_n(self):
        X = [2, 4, 2, 2, 4]
        n = len(X)
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(int(np.sum(chain)) % n, 0)

    def test_boundary_chain_sum_may_not_divide_n(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        # boundary sum = 1+2+2+4+2=11, n=5, 11%5=1 ≠ 0
        self.assertEqual(chain_mode(chain), chain_mode.boundary)

    # -------------------------------------------------------------------------
    # Invalid input
    # -------------------------------------------------------------------------

    def test_invalid_2d_array(self):
        # 2D arrays are coerced to intp — rely on size==0 or valid; no raise expected
        # for strictly invalid non-array input
        result = chain_mode(np.array([[1, 2], [3, 4]]))
        # Should not raise; returns some mode value
        self.assertIn(result, {chain_mode.boundary, chain_mode.cycle})
