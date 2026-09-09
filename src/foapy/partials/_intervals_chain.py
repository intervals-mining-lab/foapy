from typing import Optional

import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from foapy.core._binding import binding as binding_cls
from foapy.core._chain_mode import chain_mode as chain_mode_cls
from foapy.core._factorize import _normalize_sequence_axis
from foapy.partials._order import order as partial_order


def intervals_chain(
    X: ArrayLike,
    binding: int,
    chain_mode: int,
    *,
    axis: Optional[int] = None,
) -> ma.MaskedArray:
    """
    Compute the partial intervals chain from a sequence with gaps.

    Unlike foapy.ma.intervals_chain, gap positions (masked values) are NOT
    compressed out. Interval distances are measured using actual positional
    indices in the full array, so gaps between two occurrences of the same
    element increase the measured interval.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        Raw sequence (plain or masked). Pass the original sequence, not the
        order output. With an explicit ``axis``, each complete orthogonal
        slice is one element. A slice must be wholly present or wholly masked;
        wholly masked slices are positional gaps.
    binding : int
        ``binding.start`` (1) — intervals extracted left-to-right.
        ``binding.end`` (2) — intervals extracted right-to-left.
    chain_mode : int
        ``chain_mode.boundary`` (1) — finite sequence; boundary intervals are
        distances from sequence edges to first/last occurrence.
        ``chain_mode.cycle`` (2) — cyclic; wrap-around distance used.
    axis : int, optional
        Sequence axis. If omitted, ``X`` must be one-dimensional. Negative
        axes follow NumPy conventions.

    Returns
    -------
    numpy.ma.MaskedArray, shape (n,), dtype numpy.intp
        Masked one-dimensional array where ``n`` is the selected-axis length.
        Present positions hold interval distances (≥1), and wholly masked
        slices remain masked. Gap positions count toward every distance.

    Raises
    ------
    Not1DArrayException
        When ``X`` is scalar, or is multidimensional without an explicit axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.
    ValueError
        When ``binding`` or ``chain_mode`` is invalid, or a selected-axis
        slice is only partially masked.

    Examples
    --------

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy
    from foapy.partials import intervals_chain

    X = ma.masked_array(
        ["_", "C", "T", "C", "_", "G"],
        mask=[True, False, False, False, True, False],
    )
    chain = intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
    print(chain.compressed())  # [2 3 2 6]
    print(chain.mask)  # [ True False False False True False]
    ```

    Dense input uses the same interface for either binding and chain mode:

    ``` py linenums="1"
    import foapy
    from foapy.partials import intervals_chain

    chain = intervals_chain(
        ["b", "a", "b", "c", "b"],
        foapy.binding.end,
        foapy.chain_mode.cycle,
    )
    print(chain)  # [2 5 2 5 1]
    ```

    With no masked positions, the non-masked values match
    :func:`foapy.intervals_chain` for the same binding and chain mode.

    A wholly masked row is a gap that remains in the selected-axis coordinate
    system and therefore counts toward interval distances:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(
        [[1, 2], [9, 9], [3, 4], [1, 2]],
        mask=[[0, 0], [1, 1], [0, 0], [0, 0]],
    )
    chain = foapy.partials.intervals_chain(
        source,
        foapy.binding.start,
        foapy.chain_mode.boundary,
        axis=0,
    )
    print(chain)  # [1 -- 3 3]
    ```
    """
    if binding not in {binding_cls.start, binding_cls.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    if chain_mode not in {chain_mode_cls.boundary, chain_mode_cls.cycle}:
        raise ValueError(
            {
                "message": (
                    "Invalid chain_mode value. "
                    "Use chain_mode.boundary or chain_mode.cycle."
                )
            }
        )

    data = ma.asarray(X)

    if data.ndim != 1:
        sequence_order = partial_order(data, axis=axis)
        return _intervals_chain_1d(sequence_order, binding, chain_mode)

    if axis is not None:
        _normalize_sequence_axis(data, axis)

    return _intervals_chain_1d(data, binding, chain_mode)


def _intervals_chain_1d(
    ar: ma.MaskedArray, binding: int, chain_mode: int
) -> ma.MaskedArray:
    """Compute an interval chain for an already validated 1-D partial sequence."""

    n = len(ar)
    full_mask = ma.getmaskarray(ar)
    orig_non_masked_idx = np.where(~full_mask)[0]
    compressed_values = ar.compressed()
    m = len(compressed_values)

    result_data = np.full(n, -1, dtype=np.intp)

    if m == 0:
        return ma.masked_array(result_data, mask=full_mask)

    # For binding.end, reverse both values and positions to compute right-to-left.
    if binding == binding_cls.end:
        work_values = compressed_values[::-1]
        work_pos = (n - 1 - orig_non_masked_idx)[::-1]
    else:
        work_values = compressed_values
        work_pos = orig_non_masked_idx

    # Stable sort by value — same element group detection as core.
    perm = work_values.argsort(kind="mergesort")

    # Detect group boundaries (first and last occurrence per unique value).
    group_boundary = np.empty(m + 1, dtype=bool)
    group_boundary[:1] = True
    group_boundary[1:-1] = work_values[perm[1:]] != work_values[perm[:-1]]
    group_boundary[-1:] = True

    first_mask_arr = group_boundary[:-1]
    last_mask_arr = group_boundary[1:]

    chain_compressed = np.empty(m, dtype=np.intp)

    # Consecutive position differences within each group.
    chain_compressed[1:] = work_pos[perm[1:]] - work_pos[perm[:-1]]

    # Boundary intervals for first occurrence of each group.
    if chain_mode == chain_mode_cls.cycle:
        delta = n - work_pos[perm[last_mask_arr]]
    else:
        delta = 1

    chain_compressed[first_mask_arr] = work_pos[perm[first_mask_arr]] + delta

    # Restore original compressed order via inverse permutation.
    inverse_perm = np.empty(m, dtype=np.intp)
    inverse_perm[perm] = np.arange(m)
    result_compressed = chain_compressed[inverse_perm]

    # Reverse result back to original (non-reversed) order for binding.end.
    if binding == binding_cls.end:
        result_compressed = result_compressed[::-1]

    result_data[orig_non_masked_idx] = result_compressed
    return ma.masked_array(result_data, mask=full_mask)
