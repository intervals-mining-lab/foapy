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
    moved = np.moveaxis(data, normalized_axis, -1)
    outer_shape = moved.shape[:-1]
    lane_count = int(np.prod(outer_shape, dtype=np.intp)) if outer_shape else 1
    lanes = moved.reshape((lane_count, moved.shape[-1]))
    return normalized_axis, outer_shape, lanes


def _apply_to_axis_lanes(
    data: ndarray,
    axis: Optional[int],
    function: Callable[[ndarray], ndarray],
    *,
    preserve_input_length_without_lanes: bool = False,
) -> ma.MaskedArray:
    """Apply a 1-D function to every selected-axis lane and mask padding."""
    normalized_axis, outer_shape, lanes = _axis_lanes(data, axis)
    results = [np.asarray(function(lane), dtype=np.intp) for lane in lanes]

    if results:
        result_length = max(result.size for result in results)
    elif preserve_input_length_without_lanes:
        result_length = data.shape[normalized_axis]
    else:
        result_length = 0

    packed = ma.masked_all((lanes.shape[0], result_length), dtype=np.intp)
    for index, result in enumerate(results):
        length = result.size
        packed.data[index, :length] = result
        packed.mask[index, :length] = False

    moved_result = packed.reshape(outer_shape + (result_length,))
    return np.moveaxis(moved_result, -1, normalized_axis)
