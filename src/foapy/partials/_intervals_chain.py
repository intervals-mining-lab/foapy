import numpy as np
import numpy.ma as ma

from foapy.core._binding import binding as binding_cls
from foapy.core._chain_mode import chain_mode as chain_mode_cls
from foapy.exceptions import Not1DArrayException


def intervals_chain(X, binding: int, chain_mode: int) -> ma.MaskedArray:
    """
    Compute the partial intervals chain from a sequence with gaps.

    Unlike foapy.ma.intervals_chain, gap positions (masked values) are NOT
    compressed out. Interval distances are measured using actual positional
    indices in the full array, so gaps between two occurrences of the same
    element increase the measured interval.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D raw sequence (plain or masked). Pass the original sequence, not
        the order output. Masked positions are treated as gaps.
    binding : int
        ``binding.start`` (1) — intervals extracted left-to-right.
        ``binding.end`` (2) — intervals extracted right-to-left.
    chain_mode : int
        ``chain_mode.boundary`` (1) — finite sequence; boundary intervals are
        distances from sequence edges to first/last occurrence.
        ``chain_mode.cycle`` (2) — cyclic; wrap-around distance used.

    Returns
    -------
    numpy.ma.MaskedArray, shape (n,), dtype numpy.intp
        Masked 1-D array of the same length as X. Non-masked positions hold
        the interval distance (≥1). Masked positions are identical to the
        input mask.

    Raises
    ------
    Not1DArrayException
        When X is not a 1-dimensional array.
    ValueError
        When ``binding`` or ``chain_mode`` is invalid.

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

    ar = ma.asarray(X)

    if ar.ndim != 1:
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {ar.ndim}"}
        )

    n = len(ar)
    full_mask = ma.getmaskarray(ar)
    orig_non_masked_idx = np.where(~full_mask)[0]
    compressed_values = ar.compressed()
    m = len(compressed_values)

    result_data = np.zeros(n, dtype=np.intp)

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
    perm = np.argsort(work_values, kind="mergesort")

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
