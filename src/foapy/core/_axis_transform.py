from typing import Callable, Optional, Tuple

import numpy as np
import numpy.ma as ma
from numpy import ndarray

from foapy.core._factorize import _normalize_sequence_axis


def _axis_lanes(
    data: ndarray, axis: Optional[int]
) -> Tuple[int, Tuple[int, ...], ndarray]:
    """Return flattened 1-D lanes with the selected axis moved last."""
    normalized_axis = _normalize_sequence_axis(data, axis)
    outer_shape, lanes = _axis_lanes_for_normalized_axis(data, normalized_axis)
    return normalized_axis, outer_shape, lanes


def _axis_lanes_for_normalized_axis(
    data: ndarray, normalized_axis: int
) -> Tuple[Tuple[int, ...], ndarray]:
    """Return flattened lanes for an axis that was already normalized."""
    moved = np.moveaxis(data, normalized_axis, -1)
    outer_shape = moved.shape[:-1]
    lane_count = int(np.prod(outer_shape, dtype=np.intp)) if outer_shape else 1
    lanes = moved.reshape((lane_count, moved.shape[-1]))
    return outer_shape, lanes


def _apply_to_axis_lanes(
    data: ndarray,
    axis: Optional[int],
    function: Callable[[ndarray], ndarray],
    *,
    normalized_axis: Optional[int] = None,
) -> ma.MaskedArray:
    """Apply one vectorized function to the complete selected-axis lane batch."""
    if normalized_axis is None:
        normalized_axis, outer_shape, lanes = _axis_lanes(data, axis)
    else:
        outer_shape, lanes = _axis_lanes_for_normalized_axis(data, normalized_axis)
    results = ma.asarray(function(lanes), dtype=np.intp)
    moved_result = results.reshape(outer_shape + (results.shape[1],))
    return np.moveaxis(moved_result, -1, normalized_axis)


def _pack_axis_lane_values(
    values: ndarray,
    selected: ndarray,
    *,
    prefix: Optional[ndarray] = None,
) -> ma.MaskedArray:
    """Pack selected values after an optional fixed-width prefix per row."""
    selected = np.asarray(selected, dtype=bool)
    counts = np.count_nonzero(selected, axis=1)
    packed_length = int(np.max(counts, initial=0))

    if prefix is not None:
        prefix = np.asarray(prefix, dtype=np.intp)
        prefix_length = prefix.shape[1]
        result_values = np.empty(
            (selected.shape[0], prefix_length + packed_length), dtype=np.intp
        )
        result_mask = np.empty(result_values.shape, dtype=bool)
        result_values[:, :prefix_length] = prefix
        result_mask[:, :prefix_length] = False
        packed_mask = result_mask[:, prefix_length:]
        np.greater_equal(
            np.arange(packed_length, dtype=np.intp)[None, :],
            counts[:, None],
            out=packed_mask,
        )
        result_values[:, prefix_length:][~packed_mask] = np.broadcast_to(
            np.asarray(values, dtype=np.intp), selected.shape
        )[selected]
        return ma.masked_array(result_values, mask=result_mask)

    packed_mask = np.arange(packed_length, dtype=np.intp)[None, :] >= counts[:, None]
    packed_values = np.zeros((selected.shape[0], packed_length), dtype=np.intp)
    packed_values[~packed_mask] = np.broadcast_to(
        np.asarray(values, dtype=np.intp), selected.shape
    )[selected]
    return ma.masked_array(packed_values, mask=packed_mask)
