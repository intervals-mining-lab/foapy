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
            When X has more than one dimension.
        ValueError
            When ``binding`` or ``chain_mode`` is invalid.

        Examples
        --------
        Gaps (masked positions) are preserved and their positional distance
        counts toward the interval of the next occurrence of the same element:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ma.masked_array(['_', 'C', 'T', 'C', '_', 'G'], mask=[1, 0, 0, 0, 1, 0])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        print(result)
        # [-- 2 3 2 -- 6]
    ```

        The intervals chain of an empty sequence is an empty masked array:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ma.masked_array([], mask=[])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        print(result)
        # []
    ```

        If all positions are masked, every position in the result stays masked:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ma.masked_array(['a', 'b', 'c'], mask=[1, 1, 1])
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        print(result)
        # [-- -- --]
    ```

        A plain list or ndarray without a mask matches foapy.intervals_chain:

    ``` py linenums="1"
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ['b', 'a', 'b', 'c', 'b']
        result = intervals_chain(X, binding.start, chain_mode.boundary)
        print(result)
        # [1 2 2 4 2]
    ```

        With ``binding.end``, intervals are measured right-to-left:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ma.masked_array(['A', 'x', 'B', 'A'], mask=[0, 1, 0, 0])
        result = intervals_chain(X, binding.end, chain_mode.boundary)
        print(result)
        # [3 -- 2 1]
    ```

        With ``chain_mode.cycle``, the first occurrence's interval wraps around
        from the last occurrence instead of measuring from the sequence edge:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, chain_mode
        from foapy.partials import intervals_chain

        X = ma.masked_array(['A', 'x', 'A'], mask=[0, 1, 0])
        result = intervals_chain(X, binding.start, chain_mode.cycle)
        print(result)
        # [1 -- 2]
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

    ar = ma.asarray(X)

    if ar.ndim > 1:
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
