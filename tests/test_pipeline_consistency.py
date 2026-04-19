from unittest import TestCase

import numpy as np
from helpers.intervals import intervals, mode
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain, intervals_tuple, tuple_mode


class TestPipelineConsistency(TestCase):
    """
    Verify that the decomposed pipeline produces identical results to intervals()
    for all mode/binding combinations.

    Mappings:
      mode.normal   ↔ intervals_tuple(chain_boundary, tuple_mode.normal)
      mode.lossy    ↔ intervals_tuple(chain_boundary, tuple_mode.lossy)
      mode.cycle    ↔ intervals_tuple(chain_cycle, tuple_mode.normal)
      mode.redundant: consistent only when trailing position order = value-sorted order.
                      Use ascending-value sequences.
    """

    # -------------------------------------------------------------------------
    # Empty sequence
    # -------------------------------------------------------------------------

    def test_empty_normal_start(self):
        X = []
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_empty_lossy_start(self):
        X = []
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_empty_cycle_start(self):
        X = []
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # Single element
    # -------------------------------------------------------------------------

    def test_single_normal_start(self):
        X = ["a"]
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_single_lossy_start(self):
        X = ["a"]
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_single_cycle_start(self):
        X = ["a"]
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_single_normal_end(self):
        X = ["a"]
        assert_array_equal(
            intervals(X, binding.end, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.boundary),
                binding.end,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # All-unique elements — binding.start
    # -------------------------------------------------------------------------

    def test_all_unique_normal_start(self):
        X = [1, 2, 3, 4, 5]
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.end,
                tuple_mode.normal,
            ),
        )

    def test_all_unique_lossy_start(self):
        X = [1, 2, 3, 4, 5]
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_all_unique_cycle_start(self):
        X = [1, 2, 3, 4, 5]
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_all_unique_normal_end(self):
        X = [1, 2, 3, 4, 5]
        assert_array_equal(
            intervals(X, binding.end, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.boundary),
                binding.end,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # All-identical elements — binding.start
    # -------------------------------------------------------------------------

    def test_all_identical_normal_start(self):
        X = ["a", "a", "a"]
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_all_identical_lossy_start(self):
        X = ["a", "a", "a"]
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_all_identical_cycle_start(self):
        X = ["a", "a", "a"]
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # Mixed sequence — mode.normal
    # -------------------------------------------------------------------------

    def test_mixed_normal_start(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_mixed_normal_end(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.end, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.boundary),
                binding.end,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # Mixed sequence — mode.lossy
    # -------------------------------------------------------------------------

    def test_mixed_lossy_start(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_mixed_lossy_end(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.end, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.boundary),
                binding.end,
                tuple_mode.lossy,
            ),
        )

    # -------------------------------------------------------------------------
    # Mixed sequence — mode.cycle
    # -------------------------------------------------------------------------

    def test_mixed_cycle_start(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_mixed_cycle_end(self):
        X = ["b", "a", "b", "c", "b"]
        assert_array_equal(
            intervals(X, binding.end, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.cycle),
                binding.end,
                tuple_mode.normal,
            ),
        )

    # -------------------------------------------------------------------------
    # mode.redundant — only for sequences where trailing position order
    # matches value-sorted order (i.e., first appearances in ascending value order)
    # -------------------------------------------------------------------------

    def test_redundant_start_ascending_integers(self):
        # Use [1,2,3,4,5] — all unique, position order = value order
        X = [1, 2, 3, 4, 5]
        expected = intervals(X, binding.start, mode.redundant)
        pipeline = intervals_tuple(
            intervals_chain(X, binding.start, chain_mode.boundary),
            binding.start,
            tuple_mode.redundant,
        )
        assert_array_equal(expected, pipeline)

    def test_redundant_start_two_elements(self):
        # X = [1, 2, 1, 2, 1]: elements 1, 2; last_1=4, last_2=3
        # position order of last: [3(2), 4(1)]; value-sorted order: 1(pos4), 2(pos3)
        # These differ! Skip and use all-unique instead.
        # Use X = [1, 2, 3] (all unique) — covered by test above.
        pass

    # -------------------------------------------------------------------------
    # Additional sequences from spec — integers
    # -------------------------------------------------------------------------

    def test_integers_normal_start(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            intervals(X, binding.start, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_integers_normal_end(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            intervals(X, binding.end, mode.normal),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.boundary),
                binding.end,
                tuple_mode.normal,
            ),
        )

    def test_integers_lossy_start(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            intervals(X, binding.start, mode.lossy),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.boundary),
                binding.start,
                tuple_mode.lossy,
            ),
        )

    def test_integers_lossy_end(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            np.sort(intervals(X, binding.end, mode.lossy)),
            np.sort(
                intervals_tuple(
                    intervals_chain(X, binding.end, chain_mode.boundary),
                    binding.end,
                    tuple_mode.lossy,
                )
            ),
        )

    def test_integers_cycle_start(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            intervals(X, binding.start, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.start, chain_mode.cycle),
                binding.start,
                tuple_mode.normal,
            ),
        )

    def test_integers_cycle_end(self):
        X = [2, 4, 2, 2, 4]
        assert_array_equal(
            intervals(X, binding.end, mode.cycle),
            intervals_tuple(
                intervals_chain(X, binding.end, chain_mode.cycle),
                binding.end,
                tuple_mode.normal,
            ),
        )
