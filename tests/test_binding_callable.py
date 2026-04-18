from unittest import TestCase

import numpy as np
import pytest

from foapy import binding, chain_mode
from foapy.core import intervals_chain


class TestBindingCallable(TestCase):
    """
    Test binding(chain) callable form.

    Verifies that binding(chain) correctly identifies the binding direction
    used to produce an intervals chain from its structural properties.
    """

    # -------------------------------------------------------------------------
    # Empty chain — returns binding.start by default
    # -------------------------------------------------------------------------

    def test_empty_chain_returns_start(self):
        chain = np.array([], dtype=np.intp)
        result = binding(chain)
        self.assertEqual(result, binding.start)

    def test_empty_list_returns_start(self):
        result = binding([])
        self.assertEqual(result, binding.start)

    # -------------------------------------------------------------------------
    # Chains from binding.start
    # -------------------------------------------------------------------------

    def test_start_boundary_mixed(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.start)

    def test_start_boundary_integers(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.start)

    def test_start_boundary_all_unique(self):
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.start)

    def test_start_cycle_mixed(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(binding(chain), binding.start)

    def test_start_cycle_integers(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.start, chain_mode.cycle)
        self.assertEqual(binding(chain), binding.start)

    def test_start_single_element(self):
        X = ["a"]
        chain = intervals_chain(X, binding.start, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.start)

    # -------------------------------------------------------------------------
    # Chains from binding.end
    # -------------------------------------------------------------------------

    def test_end_boundary_mixed(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.end)

    def test_end_boundary_mixed_2(self):
        X = ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        print(chain)
        # n = 10
        #              ["C", "C", "A", "C", "G", "C", "T", "T", "A", "C"]
        #              [ 0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
        #              ["1", "2", "6", "2", "10","4", "1", "9", "4", "1"]
        #              [ 0,   1,   2,   3,   4,   5,   8,   17,  13,  11]
        #              ["1", "2", "6", "2",      "4", "1"               ]

        # start
        #              ["1", "2", "6", "2", "10","4", "1", "9", "4", "1"]
        #              [ 0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
        #              ["-1","-1", "-4", "1","-6", "-1", "5", "2", "4", "8"]

        # end
        #              ["1", "2", "6", "2", "10","4", "1", "9", "4", "1"]
        #              [ 0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
        #              ["2", "4", "9", "6", "15", "10", "8", "17", "13", "11"]
        #              ["2", "4", "9", "6", "5", "0", "8", "7", "3", "1"]

        self.assertEqual(binding(chain), binding.end)

    def test_end_boundary_integers(self):
        X = [2, 4, 2, 2, 4]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.end)

    def test_end_boundary_all_unique(self):
        X = [1, 2, 3, 4, 5]
        chain = intervals_chain(X, binding.end, chain_mode.boundary)
        self.assertEqual(binding(chain), binding.end)

    def test_end_cycle_mixed(self):
        X = ["b", "a", "b", "c", "b"]
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        self.assertEqual(binding(chain), binding.end)

    def test_end_cycle_integers(self):
        # Use a sequence where X[-1] appears at position 0 in the original,
        # giving a cyclic interval of 1 at chain[-1] and making binding detectable.
        X = [2, 4, 2, 4, 2]  # X[0]==X[-1]==2, wraps around
        chain = intervals_chain(X, binding.end, chain_mode.cycle)
        self.assertEqual(binding(chain), binding.end)

    # -------------------------------------------------------------------------
    # Invalid input
    # -------------------------------------------------------------------------

    def test_invalid_input_raises_value_error(self):
        with pytest.raises(ValueError):
            binding("not_a_chain")

    def test_invalid_2d_array_raises_value_error(self):
        with pytest.raises(ValueError):
            binding(np.array([[1, 2], [3, 4]]))
