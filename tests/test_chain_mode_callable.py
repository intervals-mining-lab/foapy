from unittest import TestCase

import numpy as np
import pytest

from foapy import binding, chain_mode
from foapy.core import intervals_chain


class TestChainModeNotConstructable(TestCase):
    """
    Verify that chain_mode cannot be instantiated.

    chain_mode is a named-constant namespace. Calling it as a constructor
    must raise TypeError. Its class attributes and use in intervals_chain
    remain unaffected.
    """

    # -------------------------------------------------------------------------
    # chain_mode — not constructable
    # -------------------------------------------------------------------------

    def test_chain_mode_not_constructable(self):
        with pytest.raises(TypeError):
            chain_mode()

    def test_chain_mode_not_constructable_with_chain(self):
        chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        with pytest.raises(TypeError):
            chain_mode(chain)

    def test_chain_mode_not_constructable_with_string(self):
        with pytest.raises(TypeError):
            chain_mode("boundary")

    def test_chain_mode_not_constructable_with_2d_array(self):
        with pytest.raises(TypeError):
            chain_mode(np.array([[1, 2], [3, 4]]))

    # -------------------------------------------------------------------------
    # Named constants remain accessible and usable in intervals_chain
    # -------------------------------------------------------------------------

    def test_chain_mode_constants_accessible(self):
        self.assertEqual(chain_mode.boundary, 1)
        self.assertEqual(chain_mode.cycle, 2)

    def test_chain_mode_boundary_usable_in_intervals_chain(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(len(chain), len(X))

    def test_chain_mode_cycle_usable_in_intervals_chain(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(len(chain), len(X))

    def test_cycle_chain_sum_divisible_by_n(self):
        X = [2, 4, 2, 2, 4]
        n = len(X)
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(int(np.sum(chain)) % n, 0)
