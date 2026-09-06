from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain as core_intervals_chain
from foapy.exceptions import Not1DArrayException
from foapy.partials import intervals_chain


class TestPartialsIntervalsChain(TestCase):
    """
    Test foapy.partials.intervals_chain(X, binding, chain_mode) -> masked_array.

    Key semantic: gap positions (masked values) are preserved in output and
    their positional distances COUNT toward interval values.
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_array(self):
        X = ma.masked_array([], mask=[])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (0,)

    # -------------------------------------------------------------------------
    # Single element
    # -------------------------------------------------------------------------

    def test_single_unmasked_element_boundary(self):
        X = ma.masked_array(["a"], mask=[0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (1,)
        assert_array_equal(result.compressed(), [1])

    def test_single_masked_element_returns_masked(self):
        X = ma.masked_array(["a"], mask=[1])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (1,)
        assert np.all(ma.getmaskarray(result))

    # -------------------------------------------------------------------------
    # All unique symbols
    # -------------------------------------------------------------------------

    def test_all_unique_boundary_start(self):
        X = ma.masked_array(["a", "b", "c"], mask=[0, 0, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (3,)
        # Each symbol appears once; intervals = position + 1
        assert_array_equal(result.compressed(), [1, 2, 3])

    # -------------------------------------------------------------------------
    # All same symbol
    # -------------------------------------------------------------------------

    def test_all_same_boundary_start(self):
        X = ma.masked_array(["a", "a", "a"], mask=[0, 0, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        # Intervals: first=1, then consecutive diffs = 1, 1
        assert_array_equal(result.compressed(), [1, 1, 1])

    # -------------------------------------------------------------------------
    # Realistic dataset — no gaps
    # -------------------------------------------------------------------------

    def test_realistic_no_gaps_boundary_start(self):
        X = ma.masked_array(["b", "a", "b", "c", "b"], mask=[0, 0, 0, 0, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        expected = core_intervals_chain(
            ["b", "a", "b", "c", "b"], binding.start, chain_mode.boundary
        )
        assert_array_equal(result.compressed(), expected)

    # -------------------------------------------------------------------------
    # Gaps count toward distance — core semantic distinction
    # -------------------------------------------------------------------------

    def test_gaps_count_toward_interval_distance(self):
        # X = [-, C, T, C, -, G]
        X = ma.masked_array(
            ["_", "C", "T", "C", "_", "G"],
            mask=[1, 0, 0, 0, 1, 0],
        )
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        # C at position 1: first, interval = 1+1 = 2
        # T at position 2: first, interval = 2+1 = 3
        # C at position 3: second, prev at 1, interval = 3-1 = 2
        # G at position 5: first, interval = 5+1 = 6
        assert result.shape == (6,)
        assert_array_equal(ma.getmaskarray(result), [1, 0, 0, 0, 1, 0])
        assert_array_equal(result.compressed(), [2, 3, 2, 6])

    def test_single_gap_between_same_element(self):
        # X = [A, --, A] — gap should increase interval to 2 (not 1)
        X = ma.masked_array(["A", "x", "A"], mask=[0, 1, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (3,)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0])
        # A at position 0: first, interval = 1; A at position 2: prev=0, interval=2
        assert_array_equal(result.compressed(), [1, 2])

    def test_multiple_gaps_increase_interval(self):
        # X = [A, --, --, A] — two gaps → interval = 3
        X = ma.masked_array(["A", "x", "y", "A"], mask=[0, 1, 1, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(result.compressed(), [1, 3])

    def test_gaps_with_multiple_distinct_symbols(self):
        # X = [A, --, B, C, A, --, B] — previous gap tests only used a single
        # repeated symbol or a pair; this exercises perm/group_boundary with
        # several distinct groups of different sizes while gaps are present.
        X = ma.masked_array(
            ["A", "x", "B", "C", "A", "y", "B"],
            mask=[0, 1, 0, 0, 0, 1, 0],
        )
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0, 0, 0, 1, 0])
        # A: first=0+1=1, second=4-0=4
        # B: first=2+1=3, second=6-2=4
        # C: first=3+1=4
        assert_array_equal(result.compressed(), [1, 3, 4, 4, 4])

    # -------------------------------------------------------------------------
    # Fully masked
    # -------------------------------------------------------------------------

    def test_fully_masked_returns_full_mask(self):
        X = ma.masked_array(["a", "b", "c"], mask=[1, 1, 1])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (3,)
        assert np.all(ma.getmaskarray(result))

    # -------------------------------------------------------------------------
    # No-mask passthrough — must match core
    # -------------------------------------------------------------------------

    def test_no_mask_matches_core_boundary_start(self):
        data = ["b", "a", "b", "c", "b"]
        X = ma.masked_array(data, mask=[0] * 5)
        core_result = core_intervals_chain(data, binding.start, chain_mode.boundary)
        partial_result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert_array_equal(partial_result.compressed(), core_result)

    def test_no_mask_matches_core_boundary_end(self):
        data = ["b", "a", "b", "c", "b"]
        X = ma.masked_array(data, mask=[0] * 5)
        core_result = core_intervals_chain(data, binding.end, chain_mode.boundary)
        partial_result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(partial_result.compressed(), core_result)

    def test_no_mask_matches_core_cycle_start(self):
        data = ["b", "a", "b", "c", "b"]
        X = ma.masked_array(data, mask=[0] * 5)
        core_result = core_intervals_chain(data, binding.start, chain_mode.cycle)
        partial_result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert_array_equal(partial_result.compressed(), core_result)

    def test_no_mask_matches_core_cycle_end(self):
        data = ["b", "a", "b", "c", "b"]
        X = ma.masked_array(data, mask=[0] * 5)
        core_result = core_intervals_chain(data, binding.end, chain_mode.cycle)
        partial_result = intervals_chain(X, binding.end, chain_mode.cycle)
        assert_array_equal(partial_result.compressed(), core_result)

    # -------------------------------------------------------------------------
    # binding.end with gaps
    # -------------------------------------------------------------------------

    def test_binding_end_with_gaps(self):
        # X = [A, --, B, A] with binding.end
        X = ma.masked_array(["A", "x", "B", "A"], mask=[0, 1, 0, 0])
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert result.shape == (4,)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0, 0])

    def test_binding_end_with_gaps_values(self):
        # Same input as test_binding_end_with_gaps, but checking actual
        # values, not just shape/mask — verifies the position-reversal
        # arithmetic (n - 1 - orig_non_masked_idx) is correct with gaps.
        X = ma.masked_array(["A", "x", "B", "A"], mask=[0, 1, 0, 0])
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0, 0])
        assert_array_equal(result.compressed(), [3, 2, 1])

    # -------------------------------------------------------------------------
    # chain_mode.cycle with gaps
    # -------------------------------------------------------------------------

    def test_cycle_mode_with_gaps(self):
        X = ma.masked_array(["A", "x", "A"], mask=[0, 1, 0])
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        assert result.shape == (3,)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0])
        # n=3; A at positions 0,2
        # first (cycle): pos[0] + (n - pos[last]) = 0 + (3 - 2) = 1
        # second: pos[2] - pos[0] = 2
        assert_array_equal(result.compressed(), [1, 2])

    def test_binding_end_cycle_with_gaps(self):
        # binding.end + chain_mode.cycle combined with gaps was previously
        # untested — this exercises both reversal branches at once.
        X = ma.masked_array(["A", "x", "A"], mask=[0, 1, 0])
        result = intervals_chain(X, binding.end, chain_mode.cycle)
        assert result.shape == (3,)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0])
        assert_array_equal(result.compressed(), [2, 1])

    # -------------------------------------------------------------------------
    # Output mask identical to input mask
    # -------------------------------------------------------------------------

    def test_output_mask_identical_to_input_mask(self):
        mask = [0, 1, 0, 1, 0]
        X = ma.masked_array(["a", "b", "c", "d", "a"], mask=mask)
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        assert result.shape == (5,)
        assert_array_equal(ma.getmaskarray(result), mask)

    # -------------------------------------------------------------------------
    # Plain array auto-wrapping
    # -------------------------------------------------------------------------

    def test_plain_list_accepted(self):
        result = intervals_chain(["a", "b", "a"], binding.start, chain_mode.boundary)
        assert result.shape == (3,)

    # -------------------------------------------------------------------------
    # Error handling
    # -------------------------------------------------------------------------

    def test_invalid_binding_raises_value_error(self):
        X = ma.masked_array(["a"], mask=[0])
        with pytest.raises(ValueError):
            intervals_chain(X, 99, chain_mode.boundary)

    def test_invalid_chain_mode_raises_value_error(self):
        X = ma.masked_array(["a"], mask=[0])
        with pytest.raises(ValueError):
            intervals_chain(X, binding.start, 99)

    def test_2d_array_raises_not1d(self):
        X = ma.masked_array([[1, 2], [3, 4]])
        with pytest.raises(Not1DArrayException):
            intervals_chain(X, binding.start, chain_mode.boundary)

    def test_0d_array_raises_not1d(self):
        X = ma.asarray(1)
        with pytest.raises(Not1DArrayException):
            intervals_chain(X, binding.start, chain_mode.boundary)
