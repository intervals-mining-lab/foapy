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
    Test foapy.partials.intervals_tuple(chain, binding, tuple_mode) -> masked_array.

    tuple_mode.normal : same length, same mask, values unchanged.
    tuple_mode.lossy  : same length, boundary positions additionally masked.
    tuple_mode.redundant : length n+k, k trailing unmasked intervals appended.
    """

    # -------------------------------------------------------------------------
    # Empty input
    # -------------------------------------------------------------------------

    def test_empty_normal(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert result.shape == (0,)

    def test_empty_lossy(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert result.shape == (0,)

    def test_empty_redundant(self):
        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert result.shape == (0,)

    # -------------------------------------------------------------------------
    # Fully masked input
    # -------------------------------------------------------------------------

    def test_fully_masked_normal(self):
        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1])
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert result.shape == (4,)
        assert np.all(ma.getmaskarray(result))

    def test_fully_masked_lossy(self):
        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1])
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert result.shape == (4,)
        assert np.all(ma.getmaskarray(result))

    # -------------------------------------------------------------------------
    # tuple_mode.normal — mask and values unchanged
    # -------------------------------------------------------------------------

    def test_normal_preserves_mask(self):
        mask = [1, 0, 0, 0, 1, 0]
        chain = ma.masked_array([0, 2, 3, 2, 0, 6], mask=mask, dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert result.shape == (6,)
        assert_array_equal(ma.getmaskarray(result), mask)

    def test_normal_preserves_values(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        assert_array_equal(result.compressed(), [2, 3, 2, 6])

    # -------------------------------------------------------------------------
    # tuple_mode.lossy — boundary positions additionally masked, same length
    # -------------------------------------------------------------------------

    def test_lossy_same_length_as_input(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        assert len(result) == len(chain)

    def test_lossy_masks_boundary_positions(self):
        # compressed = [2, 3, 2, 6] at positions [1,2,3,5]
        # compressed indices [0,1,2,3], boundary: compressed[i] > i
        # 2>0=T, 3>1=T, 2>2=F, 6>3=T
        # boundary compressed indices: [0,1,3] → original positions [1,2,5]
        # non-boundary: compressed index [2] → original position [3]
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        # positions [1,2,5] additionally masked; [3] remains unmasked
        expected_mask = [1, 1, 1, 0, 1, 1]
        assert_array_equal(ma.getmaskarray(result), expected_mask)
        assert_array_equal(result.compressed(), [2])

    def test_lossy_original_mask_preserved(self):
        # Input mask positions must remain masked in output
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        input_mask = ma.getmaskarray(chain)
        output_mask = ma.getmaskarray(result)
        # All originally masked positions must still be masked
        assert np.all(output_mask[input_mask])

    def test_lossy_no_mask_non_boundary_values_kept(self):
        # For an unmasked chain, lossy should keep same non-boundary values as core
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(plain_chain, binding.start, tuple_mode.lossy)
        partial_result = intervals_tuple(masked_chain, binding.start, tuple_mode.lossy)
        assert_array_equal(partial_result.compressed(), core_result)

    # -------------------------------------------------------------------------
    # tuple_mode.redundant — trailing intervals appended
    # -------------------------------------------------------------------------

    def test_redundant_length_greater_than_input(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        assert len(result) > len(chain)

    def test_redundant_trailing_elements_unmasked(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        # Trailing elements (beyond len(chain)) must be unmasked
        assert not np.any(ma.getmaskarray(result)[len(chain) :])

    def test_redundant_input_portion_mask_unchanged(self):
        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        # The first n positions must preserve the original mask
        assert_array_equal(
            ma.getmaskarray(result)[: len(chain)], ma.getmaskarray(chain)
        )

    def test_redundant_no_mask_matches_core_values(self):
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(
            plain_chain, binding.start, tuple_mode.redundant
        )
        partial_result = intervals_tuple(
            masked_chain, binding.start, tuple_mode.redundant
        )
        # All values (original + trailing) should match core
        assert_array_equal(partial_result.data, core_result)

    # -------------------------------------------------------------------------
    # binding.end
    # -------------------------------------------------------------------------

    def test_lossy_binding_end_no_mask_same_values_as_core(self):
        # For binding.end, position-preserving partials returns non-boundary values
        # in left-to-right order; core returns them in right-to-left order.
        # The multisets must be equal.
        plain_chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        masked_chain = ma.masked_array(plain_chain, mask=[0] * 5)
        core_result = core_intervals_tuple(plain_chain, binding.end, tuple_mode.lossy)
        partial_result = intervals_tuple(masked_chain, binding.end, tuple_mode.lossy)
        assert_array_equal(
            np.sort(partial_result.compressed()),
            np.sort(core_result),
        )

    def test_normal_binding_end_preserves_mask(self):
        chain = ma.masked_array([2, 0, 3, 2], mask=[0, 1, 0, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.end, tuple_mode.normal)
        assert_array_equal(ma.getmaskarray(result), [0, 1, 0, 0])

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
        assert result.shape == plain.shape
