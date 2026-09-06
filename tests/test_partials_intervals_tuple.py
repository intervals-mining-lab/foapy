from unittest import TestCase

import numpy as np
import numpy.ma as ma
import pytest
from numpy.testing import assert_array_equal

from foapy import binding
from foapy.core import intervals_tuple as core_intervals_tuple
from foapy.core import tuple_mode
from foapy.partials import intervals_tuple


class TestPartialsIntervalsTuple(TestCase):
    """
    Test foapy.partials.intervals_tuple(chain, binding, tuple_mode) -> ndarray.

    tuple_mode.normal : gap-free values, unchanged relative order.
    tuple_mode.lossy  : gap-free values with boundary intervals also dropped;
                        for binding.end, follows core's reversed-frame order.
    tuple_mode.redundant : gap-free values followed by k trailing intervals,
                        trailing distances measured against the true source
                        domain length (gaps included).
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_normal(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert isinstance(result, np.ndarray)
        assert not isinstance(result, ma.MaskedArray)
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_empty_lossy(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_empty_redundant(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert_array_equal(result, np.array([], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Fully masked input
    # -------------------------------------------------------------------------

    def test_fully_masked_normal(self):
        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1])
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_fully_masked_lossy(self):
        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1])
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert_array_equal(result, np.array([], dtype=np.intp))

    def test_fully_masked_redundant(self):
        # Same code path as empty, but for a genuinely fully-masked
        # (non-empty) input rather than a zero-length one.
        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert_array_equal(result, np.array([], dtype=np.intp))

    # -------------------------------------------------------------------------
    # tuple_mode.normal — gaps dropped, non-masked values unchanged
    # -------------------------------------------------------------------------

    def test_normal_returns_plain_ndarray(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert isinstance(result, np.ndarray)
        assert not isinstance(result, ma.MaskedArray)

    def test_normal_drops_gaps(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert_array_equal(result, [2, 3, 2, 6])

    def test_normal_binding_end_drops_gaps(self):
        chain = ma.masked_array([2, 0, 3, 2], mask=[0, 1, 0, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.end, tuple_mode.normal)
        assert_array_equal(result, [2, 3, 2])

    # -------------------------------------------------------------------------
    # tuple_mode.lossy — boundary intervals and gaps both dropped
    # -------------------------------------------------------------------------

    def test_lossy_drops_boundary_and_gap_values(self):
        # compressed = [2, 3, 2, 6] at real positions [1,2,3,5]; boundary
        # test uses real positions: 2>1=T, 3>2=T, 2>3=F, 6>5=T -> only the
        # value at real position 3 (the second C) survives.
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert_array_equal(result, [2])

    def test_lossy_keeps_repeated_symbols_separated_by_gaps(self):
        # The second occurrence's interval (4) is measured against its real
        # source position (4), not its compressed local index (2) — using
        # local index here would wrongly flag it as a boundary and drop it.
        chain = ma.masked_array([1, 0, 3, 4, 4], mask=[0, 1, 0, 1, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert_array_equal(result, [4])

    def test_lossy_no_mask_matches_core(self):
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(plain_chain, binding.start, tuple_mode.lossy)
        partial_result = intervals_tuple(masked_chain, binding.start, tuple_mode.lossy)
        assert_array_equal(partial_result, core_result)

    def test_lossy_binding_end_no_mask_matches_core_exactly(self):
        # For binding.end, partials now follows core's own reversed-frame
        # order exactly (no re-mapping to left-to-right source order).
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(plain_chain, binding.end, tuple_mode.lossy)
        partial_result = intervals_tuple(masked_chain, binding.end, tuple_mode.lossy)
        assert_array_equal(partial_result, core_result)

    def test_lossy_binding_end_with_gaps(self):
        # binding.end + gaps: exercises the reversed-frame real-position
        # test, not just the multiset/no-gap parity checks above.
        chain = ma.masked_array([2, 0, 2, 2, 1], mask=[0, 1, 0, 0, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.end, tuple_mode.lossy)
        assert_array_equal(result, [2, 2])

    # -------------------------------------------------------------------------
    # tuple_mode.redundant — trailing intervals appended, gap-aware
    # -------------------------------------------------------------------------

    def test_redundant_length_greater_than_compressed(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert len(result) > len(chain.compressed())

    def test_redundant_trailing_is_gap_aware(self):
        # X = [_, C, T, C, _, G] -> chain (start, boundary) = [_, 2, 3, 2, _, 6]
        # n_full = 6 (gaps count toward the trailing distance).
        # Naive compressed-length-based math (core's own local formula, m=4)
        # would give trailing [3, 2, 1]; the gap-aware answer is [4, 3, 1].
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert_array_equal(result, [2, 3, 2, 6, 4, 3, 1])

    def test_redundant_uses_full_positions_for_repeated_symbols(self):
        # A appears at real positions 0 and 4 (its complementary interval is
        # 1); B at real position 2 (its complementary interval is 3). Using
        # compressed local index instead of real positions would mismatch
        # which occurrence each trailing value belongs to.
        chain = ma.masked_array([1, 0, 3, 0, 4], mask=[0, 1, 0, 1, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert_array_equal(result, [1, 3, 4, 3, 1])

    def test_redundant_binding_end_with_gaps(self):
        # binding.end + redundant + gaps: exercises the
        # (n_full - 1 - non_masked_idx)[::-1] reversal branch together with
        # real-position "previous occurrence" resolution.
        chain = ma.masked_array([3, 0, 2, 1], mask=[0, 1, 0, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.end, tuple_mode.redundant)
        assert_array_equal(result, [1, 2, 3, 3, 1])

    def test_redundant_no_mask_matches_core_values(self):
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(
            plain_chain, binding.start, tuple_mode.redundant
        )
        partial_result = intervals_tuple(
            masked_chain, binding.start, tuple_mode.redundant
        )
        assert_array_equal(partial_result, core_result)

    def test_redundant_binding_end_no_mask_matches_core_exactly(self):
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(
            plain_chain, binding.end, tuple_mode.redundant
        )
        partial_result = intervals_tuple(
            masked_chain, binding.end, tuple_mode.redundant
        )
        assert_array_equal(partial_result, core_result)

    # -------------------------------------------------------------------------
    # Error handling
    # -------------------------------------------------------------------------

    def test_invalid_binding_raises_value_error(self):
        chain = ma.masked_array([1, 2], mask=[0, 0], dtype=np.intp)
        with pytest.raises(ValueError):
            intervals_tuple(chain, 99, tuple_mode.normal)

    def test_invalid_tuple_mode_raises_value_error(self):
        chain = ma.masked_array([1, 2], mask=[0, 0], dtype=np.intp)
        with pytest.raises(ValueError):
            intervals_tuple(chain, binding.start, 99)

    # -------------------------------------------------------------------------
    # Plain array auto-wrapping
    # -------------------------------------------------------------------------

    def test_plain_array_accepted(self):
        plain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        result = intervals_tuple(plain, binding.start, tuple_mode.normal)
        assert isinstance(result, np.ndarray)
        assert not isinstance(result, ma.MaskedArray)
        assert_array_equal(result, plain)
