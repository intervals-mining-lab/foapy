from typing import Optional, Union

import numpy as np
import numpy.ma as ma
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._axis_transform import _apply_to_axis_lanes
from foapy.core._binding import binding as binding_cls
from foapy.core._factorize import _normalize_sequence_axis
from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls


def intervals_tuple(
    chain: ArrayLike,
    binding: int,
    tuple_mode: int,
    *,
    axis: Optional[int] = None,
) -> Union[ndarray, ma.MaskedArray]:
    """
    Apply a boundary strategy to one or more partial interval-chain lanes.

    Within each lane, masked positions remain source-coordinate gaps while the
    tuple strategy is calculated, then are excluded from the lane result.
    With multidimensional input, ``axis`` selects independent one-dimensional
    lanes in the style of :func:`numpy.apply_along_axis`. Unequal result
    lengths are packed from index zero and trailing positions are masked.

    Parameters
    ----------
    chain : array_like or numpy.ma.MaskedArray
        One partial intervals chain, or a multidimensional collection of
        chains. Plain arrays are treated as fully unmasked.
    binding : int
        Must match the binding used to produce the chain.
        ``binding.start`` (1) or ``binding.end`` (2).
    tuple_mode : int
        ``tuple_mode.normal`` (2) — return the compressed (gap-free) chain
        unchanged.
        ``tuple_mode.lossy`` (1) — drop boundary (first-occurrence)
        intervals in addition to gaps.
        ``tuple_mode.redundant`` (3) — append one trailing complementary
        boundary interval per inferred unique symbol, measured against the
        true source domain length (gaps included).
    axis : int, optional
        Axis containing each independent interval chain. If omitted, ``chain``
        must be one-dimensional. Negative axes follow NumPy conventions.

    Returns
    -------
    numpy.ndarray or numpy.ma.MaskedArray
        One-dimensional input returns a plain ``numpy.intp`` array with gaps
        excluded. Multidimensional input always returns a masked
        ``numpy.intp`` array whose selected axis has the longest lane result;
        masks in this output are structural trailing padding, not source
        gaps. For ``binding.end``, each lane follows
        :func:`foapy.core.intervals_tuple`'s reversed processing frame.

    Raises
    ------
    ValueError
        When ``binding`` or ``tuple_mode`` is invalid.
    Not1DArrayException
        When input is scalar, or is multidimensional without an explicit
        axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.

    Examples
    --------

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy
    from foapy.partials import intervals_tuple

    chain = ma.masked_array(
        [0, 2, 3, 2, 0, 6],
        mask=[True, False, False, False, True, False],
    )
    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.normal))
    # [2 3 2 6]
    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.lossy))
    # [2]
    print(intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.redundant))
    # [2 3 2 6 4 3 1]
    ```

    Process two partial chains independently. The first lossy tuple has one
    value, so its second packed position is structurally masked:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    chains = ma.masked_array(
        [[1, 0, 3, 3, 0, 6], [0, 2, 1, 4, 2, 0]],
        mask=[[0, 1, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1]],
    )
    tuples = foapy.partials.intervals_tuple(
        chains,
        foapy.binding.start,
        foapy.tuple_mode.lossy,
        axis=1,
    )
    print(tuples)
    # [[3 --]
    #  [1 2]]

    print(foapy.intervals_distribution(tuples, axis=1))
    # [[0 0 1]
    #  [1 1 --]]
    ```

    The selected result dimension replaces the input axis. For shape
    ``(A, B, C)``, axes 0, 1, and 2 therefore produce ``(L, B, C)``,
    ``(A, L, C)``, and ``(A, B, L)`` respectively, where ``L`` is the longest
    lane result:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    batch = ma.stack([chains.T, chains.T])  # shape (2, 6, 2)
    result = foapy.partials.intervals_tuple(
        batch,
        foapy.binding.start,
        foapy.tuple_mode.lossy,
        axis=1,
    )
    print(result.shape)  # (2, 2, 2)
    ```
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
                "message": (
                    "Invalid tuple_mode value. "
                    "Use tuple_mode.lossy, normal, or redundant."
                )
            }
        )

    data = ma.asarray(chain)

    if data.ndim == 1:
        if axis is not None:
            _normalize_sequence_axis(data, axis)
        return _intervals_tuple_1d(data, binding, tuple_mode)

    return _apply_to_axis_lanes(
        data,
        axis,
        lambda lane: _intervals_tuple_1d(lane, binding, tuple_mode),
    )


def _intervals_tuple_1d(ar: ma.MaskedArray, binding: int, tuple_mode: int) -> ndarray:
    """Transform one partial interval-chain lane while retaining gap positions."""
    chain_mask = ma.getmaskarray(ar)
    compressed = ar.compressed().astype(np.intp)

    if tuple_mode == tuple_mode_cls.normal:
        return compressed

    if compressed.size == 0:
        return np.array([], dtype=np.intp)

    non_masked_idx = np.where(~chain_mask)[0]
    n_full = len(ar)

    if tuple_mode == tuple_mode_cls.lossy:
        return _lossy(compressed, non_masked_idx, binding, n_full)

    return _redundant(compressed, non_masked_idx, binding, n_full)


def _lossy(compressed, non_masked_idx, binding, n_full):
    # A boundary interval's value always exceeds its own real source
    # position (chain_mode.boundary sets it to position + 1; an interior
    # interval is a real distance from an earlier real position, so it can
    # never exceed its own position). Gaps make real positions diverge from
    # the compressed array's local index, so the test must use real
    # positions, not local index — unlike core, which can use local index
    # because its input never has gaps.
    if binding == binding_cls.end:
        work = compressed[::-1]
        work_pos = (n_full - 1 - non_masked_idx)[::-1]
    else:
        work = compressed
        work_pos = non_masked_idx

    first = work > work_pos
    return work[~first]


def _redundant(compressed, non_masked_idx, binding, n_full):
    # Mirrors core.intervals_tuple's redundant algorithm, but "previous
    # occurrence" is resolved via real source positions (searchsorted into
    # work_pos) rather than local index arithmetic, and trailing distances
    # are measured against the true source domain length (n_full, gaps
    # included) — gaps between a last occurrence and the domain edge, or
    # between two occurrences of the same symbol, must count.
    if binding == binding_cls.end:
        work = compressed[::-1]
        work_pos = (n_full - 1 - non_masked_idx)[::-1]
    else:
        work = compressed
        work_pos = non_masked_idx

    prev_pos = work_pos - work
    last_mask_arr = np.ones(len(work), dtype=bool)
    valid_prev = prev_pos >= 0
    if np.any(valid_prev):
        referred_pos = prev_pos[valid_prev]
        referred_idx = np.searchsorted(work_pos, referred_pos)
        last_mask_arr[referred_idx] = False

    trailing = n_full - work_pos[last_mask_arr]

    return np.concatenate((work, trailing)).astype(np.intp)
