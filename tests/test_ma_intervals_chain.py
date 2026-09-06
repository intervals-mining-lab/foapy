from unittest import TestCase

import numpy as np
import numpy.ma as ma
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain


class TestMaIntervalsChain(TestCase):
    """
    Test foapy.ma.intervals_chain(X, binding, chain_mode) -> ndarray.

    Masked values in X are treated as missing: they are skipped and intervals
    are computed over the remaining (unmasked) elements only.
    """

    # -------------------------------------------------------------------------
    # No masked values — equivalent to core intervals_chain
    # -------------------------------------------------------------------------

    def test_no_mask_matches_core(self):
        from foapy.ma import intervals_chain as ma_intervals_chain

        X_plain = ["b", "a", "b", "c", "b"]
        X_masked = ma.masked_array(X_plain, mask=[0, 0, 0, 0, 0])
        core_result = intervals_chain(X_plain, binding.start, chain_mode.boundary)
        ma_result = ma_intervals_chain(X_masked, binding.start, chain_mode.boundary)
        assert_array_equal(core_result, ma_result)

    # -------------------------------------------------------------------------
    # All masked — returns empty array
    # -------------------------------------------------------------------------

    def test_all_masked_returns_empty(self):
        from foapy.ma import intervals_chain as ma_intervals_chain

        X_masked = ma.masked_array(["a", "b", "c"], mask=[1, 1, 1])
        result = ma_intervals_chain(X_masked, binding.start, chain_mode.boundary)
        assert_array_equal(result, np.array([], dtype=np.intp))

    # -------------------------------------------------------------------------
    # Partially masked — skips masked values
    # -------------------------------------------------------------------------

    def test_partial_mask_boundary_start(self):
        from foapy.ma import intervals_chain as ma_intervals_chain

        # X = ["b", --, "b", "c", "b"] where -- is masked
        # Unmasked: ["b", "b", "c", "b"] (positions 0, 2, 3, 4 in original)
        # Compressed: ["b","b","c","b"] — n=4
        # chain: b at 0,1,3; c at 2
        # b: first=0→interval=1, 1-0=1, 3-1=2; c: first=2→interval=3
        # chain = [1, 1, 3, 2]
        X_masked = ma.masked_array(
            ["b", "a", "b", "c", "b"],
            mask=[0, 1, 0, 0, 0],
        )
        result = ma_intervals_chain(X_masked, binding.start, chain_mode.boundary)
        core_ref = intervals_chain(
            ["b", "b", "c", "b"], binding.start, chain_mode.boundary
        )
        assert_array_equal(result, core_ref)

    def test_partial_mask_cycle_start(self):
        from foapy.ma import intervals_chain as ma_intervals_chain

        # Unmasked: ["b", "b", "c", "b"] — cycle mode
        X_masked = ma.masked_array(
            ["b", "a", "b", "c", "b"],
            mask=[0, 1, 0, 0, 0],
        )
        result = ma_intervals_chain(X_masked, binding.start, chain_mode.cycle)
        core_ref = intervals_chain(
            ["b", "b", "c", "b"], binding.start, chain_mode.cycle
        )
        assert_array_equal(result, core_ref)

    def test_partial_mask_boundary_end(self):
        from foapy.ma import intervals_chain as ma_intervals_chain

        X_masked = ma.masked_array(
            ["b", "a", "b", "c", "b"],
            mask=[0, 1, 0, 0, 0],
        )
        result = ma_intervals_chain(X_masked, binding.end, chain_mode.boundary)
        core_ref = intervals_chain(
            ["b", "b", "c", "b"], binding.end, chain_mode.boundary
        )
        assert_array_equal(result, core_ref)
