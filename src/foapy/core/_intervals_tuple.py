from typing import Optional, Union

import numpy as np
import numpy.ma as ma
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._axis_transform import _apply_to_axis_lanes, _pack_axis_lane_values
from foapy.core._binding import binding as binding_cls
from foapy.core._factorize import _normalize_sequence_axis
from foapy.core._intervals_chain_validation import is_valid_intervals_chain
from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls


def intervals_tuple(
    chain: ArrayLike,
    binding: int,
    tuple_mode: int,
    *,
    axis: Optional[int] = None,
) -> Union[ndarray, ma.MaskedArray]:
    """
    Apply a boundary strategy to interval-chain lanes.

    A one-dimensional input is transformed directly. For multidimensional
    input, ``axis`` selects independent one-dimensional chains in the style
    of :func:`numpy.apply_along_axis`; every combination of coordinates on
    the other dimensions is processed separately.

    - ``tuple_mode.normal``: return the chain unchanged.
    - ``tuple_mode.lossy``: remove boundary (first-/last-occurrence) intervals,
      keeping only interior intervals between repeated occurrences.
    - ``tuple_mode.redundant``: append the complementary boundary intervals
      (trailing for ``binding.start`` chains, leading for ``binding.end``
      chains), so every element contributes both its start-side and end-side
      boundary interval.

    Parameters
    ----------
    chain : array_like
        One intervals chain, or a multidimensional collection of chains.
        Each selected-axis lane must be a one-dimensional chain produced by
        :func:`foapy.intervals_chain`.
    binding : int
        ``binding.start`` (1) — chain was produced left-to-right.
        ``binding.end`` (2) — chain was produced right-to-left.
        Must match the binding used in the ``intervals_chain`` call.
    tuple_mode : int
        Boundary handling strategy.  Use one of the class attributes on
        :class:`foapy.core.tuple_mode`:

        ``tuple_mode.normal`` = 2 – return the chain as-is.

        ``tuple_mode.lossy`` = 1 – drop boundary intervals.

        ``tuple_mode.redundant`` = 3 – include both boundary intervals for
        every element.
    axis : int, optional
        Axis containing each independent chain. If omitted, ``chain`` must be
        one-dimensional. Negative axes follow NumPy conventions.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        One-dimensional input returns a plain ``numpy.intp`` array. Its
        length is ``n`` for *normal*, ``n - k`` for *lossy*, and ``n + k``
        for *redundant*, where ``k`` is the inferred number of elements.
        Multidimensional input returns a masked ``numpy.intp`` array. The
        selected axis is replaced by the longest lane result; shorter lane
        results are packed from index zero and trailing positions are masked.

    Raises
    ------
    Not1DArrayException
        When input is scalar, or is multidimensional without an explicit
        axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.
    ValueError
        When ``binding`` or ``tuple_mode`` is invalid, or internal interval-
        chain validation fails.

    Examples
    --------

    ``` py linenums="1"
    import foapy
    from foapy.core import intervals_chain, intervals_tuple

    X = ['b', 'a', 'b', 'c', 'b']
    chain = intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
    # chain = [1, 2, 2, 4, 2]

    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.normal))
    # [1 2 2 4 2]

    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.lossy))
    # [2 2]

    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.redundant))
    # [1 2 2 4 2 4 2 1]
    ```

    Process independent row chains and preserve unequal lossy lengths with
    trailing masks:

    ``` py linenums="1"
    import numpy as np
    import foapy

    chains = np.array([[1, 1, 1, 1], [1, 2, 3, 4]])
    result = foapy.intervals_tuple(
        chains,
        foapy.binding.start,
        foapy.tuple_mode.lossy,
        axis=1,
    )
    print(result)
    # [[1 1 1]
    #  [-- -- --]]
    ```

    Three-dimensional lane processing follows the same rule:

    ``` py linenums="1"
    batch = np.stack((chains.T, chains.T))  # shape (2, 4, 2)
    result = foapy.intervals_tuple(
        batch,
        foapy.binding.start,
        foapy.tuple_mode.lossy,
        axis=1,
    )
    print(result.shape)  # (2, 3, 2)
    ```

    In general, for shape ``(A, B, C)``, selecting axes 0, 1, or 2 produces
    ``(L, B, C)``, ``(A, L, C)``, or ``(A, B, L)`` respectively.
    """

    if binding not in {binding_cls.start, binding_cls.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    valid_modes = {
        tuple_mode_cls.lossy,
        tuple_mode_cls.normal,
        tuple_mode_cls.redundant,
    }
    if tuple_mode not in valid_modes:
        raise ValueError(
            {
                "message": "Invalid tuple_mode value. Use tuple_mode.lossy, normal, or redundant."  # noqa: E501
            }
        )

    data = chain if isinstance(chain, np.ndarray) else np.asanyarray(chain)

    if data.ndim == 1:
        if axis is not None:
            _normalize_sequence_axis(data, axis)
        prepared = data if data.dtype == np.intp else np.asanyarray(data, dtype=np.intp)
        if not is_valid_intervals_chain(prepared):
            raise ValueError({"message": "Invalid intervals chain."})
        return _intervals_tuple_1d(prepared, binding, tuple_mode)

    prepared = data if data.dtype == np.intp else np.asanyarray(data, dtype=np.intp)

    return _apply_to_axis_lanes(
        prepared,
        axis,
        lambda lanes: _validated_intervals_tuple_lanes(lanes, binding, tuple_mode),
    )


def _validated_intervals_tuple_lanes(
    lanes: ndarray, binding: int, tuple_mode: int
) -> ma.MaskedArray:
    """Validate and transform a prepared interval-chain lane batch."""
    if not is_valid_intervals_chain(lanes, axis=1):
        raise ValueError({"message": "Invalid intervals chain."})
    return _intervals_tuple_lanes(lanes, binding, tuple_mode)


def _intervals_tuple_lanes(
    lanes: ndarray, binding: int, tuple_mode: int
) -> ma.MaskedArray:
    """Apply one tuple mode to a complete prepared lane batch."""
    if tuple_mode == tuple_mode_cls.normal:
        return ma.masked_array(lanes.copy(), mask=np.zeros(lanes.shape, dtype=bool))

    work = lanes[:, ::-1] if binding == binding_cls.end else lanes
    positions = np.broadcast_to(
        np.arange(work.shape[1], dtype=np.intp)[None, :], work.shape
    )

    if tuple_mode == tuple_mode_cls.lossy:
        return _pack_axis_lane_values(work, work <= positions)

    prev_pos = positions - work
    last = np.ones(work.shape, dtype=bool)
    valid_prev = prev_pos >= 0
    lane_indices = np.broadcast_to(
        np.arange(work.shape[0], dtype=np.intp)[:, None], work.shape
    )
    last[lane_indices[valid_prev], prev_pos[valid_prev]] = False
    trailing = work.shape[1] - np.arange(work.shape[1], dtype=np.intp)[None, :]
    prefix_width = work.shape[1] * min(work.shape[0], 1)
    return _pack_axis_lane_values(
        trailing,
        last,
        prefix=work[:, :prefix_width],
    )


def _intervals_tuple_1d(ar: ndarray, binding: int, tuple_mode: int) -> ndarray:
    """Apply a tuple mode to one already validated interval chain."""

    if ar.size == 0:
        return np.array([], dtype=np.intp)

    if tuple_mode == tuple_mode_cls.normal:
        return ar.copy()

    if tuple_mode == tuple_mode_cls.lossy:
        return _lossy(ar, binding)

    return _redundant(ar, binding)


def _lossy(ar: ndarray, binding: int) -> ndarray:
    if binding == binding_cls.end:
        ar = ar[::-1]

    positions = np.arange(ar.size, dtype=np.intp)
    first = ar > positions
    return ar[~first]


def _redundant(ar: ndarray, binding: int) -> ndarray:
    if binding == binding_cls.end:
        ar = ar[::-1]

    n = ar.size
    positions = np.arange(n, dtype=np.intp)
    prev_pos = positions - ar
    last_mask = np.ones_like(positions, dtype=bool)
    last_mask[prev_pos[prev_pos >= 0]] = False
    trailing = n - positions[last_mask]
    return np.concatenate((ar, trailing))
