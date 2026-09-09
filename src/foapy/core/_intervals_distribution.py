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
    data = np.asanyarray(tuple_result)

    if data.ndim == 1:
        if axis is not None:
            _normalize_sequence_axis(data, axis)
        return _intervals_distribution_1d(data)

    return _apply_to_axis_lanes(data, axis, _intervals_distribution_1d)


def _intervals_distribution_1d(tuple_result: ndarray) -> ndarray:
    """Compute an interval distribution for one one-dimensional tuple."""
    if ma.isMaskedArray(tuple_result):
        ar = ma.asarray(tuple_result, dtype=np.intp).compressed()
    else:
        ar = np.asanyarray(tuple_result, dtype=np.intp)

    if ar.size == 0:
        return np.array([], dtype=np.intp)

    return np.bincount(ar - 1).astype(np.intp)
