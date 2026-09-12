from typing import Optional, Union

import numpy as np
import numpy.ma as ma
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._axis_transform import _apply_to_axis_lanes
from foapy.core._factorize import _normalize_sequence_axis


def intervals_distribution(
    tuple_result: ArrayLike, *, axis: Optional[int] = None
) -> Union[ndarray, ma.MaskedArray]:
    """
    Compute frequency distributions of interval-tuple lanes.

    For one-dimensional input, count how many times each positive interval
    value occurs. For multidimensional input, ``axis`` selects independent
    one-dimensional tuples in the style of :func:`numpy.apply_along_axis`.
    Masked positions, including padding from axis-aware
    :func:`foapy.intervals_tuple`, are excluded from counts.

    Parameters
    ----------
    tuple_result : array_like or numpy.ma.MaskedArray
        One interval tuple, or a multidimensional collection of tuples.
        Unmasked values must be strictly positive integers.
    axis : int, optional
        Axis containing each independent tuple. If omitted, ``tuple_result``
        must be one-dimensional. Negative axes follow NumPy conventions.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        One-dimensional input returns a plain ``numpy.intp`` array of length
        ``max(tuple_result)``. Multidimensional input returns a masked
        ``numpy.intp`` array whose selected axis is the longest lane
        distribution. Shorter distributions have trailing masked bins;
        zero-frequency bins within a lane's distribution remain unmasked.

    Raises
    ------
    Not1DArrayException
        When input is scalar, or is multidimensional without an explicit
        axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.

    Examples
    --------

    ``` py linenums="1"
    import numpy as np
    from foapy.core import intervals_distribution

    print(intervals_distribution(np.array([1, 2, 2, 4, 2])))
    # [1 3 0 1]

    print(intervals_distribution(np.array([])))
    # []
    ```

    Process independent tuple rows. The zero in the first distribution is a
    real count, not padding:

    ``` py linenums="1"
    import numpy as np
    import foapy

    tuples = np.array([[1, 1, 3, 1], [1, 2, 1, 3]])
    result = foapy.intervals_distribution(tuples, axis=1)
    print(result)
    # [[3 0 1]
    #  [2 1 1]]
    ```
    """
    if (
        axis is None
        and type(tuple_result) is ndarray
        and tuple_result.ndim == 1
        and tuple_result.dtype == np.intp
    ):
        if tuple_result.size == 0:
            return np.array([], dtype=np.intp)
        return np.bincount(tuple_result - 1).astype(np.intp)

    data = np.asanyarray(tuple_result)

    if data.ndim == 1:
        if axis is not None:
            _normalize_sequence_axis(data, axis)
        if ma.isMaskedArray(data):
            data = ma.asarray(data, dtype=np.intp).compressed()
        elif data.dtype != np.intp:
            data = np.asanyarray(data, dtype=np.intp)
        return _intervals_distribution_1d(data)

    return _apply_to_axis_lanes(data, axis, _intervals_distribution_lanes)


def _intervals_distribution_1d(tuple_result: ndarray) -> ndarray:
    """Compute an interval distribution for one one-dimensional tuple."""
    if tuple_result.size == 0:
        return np.array([], dtype=np.intp)

    return np.bincount(tuple_result - 1).astype(np.intp)


def _intervals_distribution_lanes(tuple_results: ndarray) -> ma.MaskedArray:
    """Compute distributions for a complete prepared tuple-lane batch."""
    values = np.asarray(ma.getdata(tuple_results), dtype=np.intp)
    valid = ~ma.getmaskarray(tuple_results)
    if np.any(values[valid] <= 0):
        raise ValueError("interval values must be positive")

    result_length = int(np.max(values, where=valid, initial=0))
    counts = np.zeros((values.shape[0], result_length), dtype=np.intp)
    lane_indices = np.broadcast_to(
        np.arange(values.shape[0], dtype=np.intp)[:, None], values.shape
    )
    np.add.at(counts, (lane_indices[valid], values[valid] - 1), 1)
    lane_maximums = np.max(values, axis=1, where=valid, initial=0)
    structural_mask = (
        np.arange(result_length, dtype=np.intp)[None, :] >= lane_maximums[:, None]
    )
    return ma.masked_array(counts, mask=structural_mask)
