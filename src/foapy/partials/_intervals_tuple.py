import numpy as np
import numpy.ma as ma

from foapy.core._binding import binding as binding_cls
from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls


def intervals_tuple(chain, binding: int, tuple_mode: int) -> ma.MaskedArray:
    """
        Apply a boundary handling strategy to a partial intervals chain.

        Parameters
        ----------
        chain : array_like or numpy.ma.MaskedArray
            1-D intervals chain produced by ``partials.intervals_chain``.
            Plain arrays are auto-wrapped (treated as fully unmasked).
        binding : int
            Must match the binding used to produce the chain.
            ``binding.start`` (1) or ``binding.end`` (2).
        tuple_mode : int
            ``tuple_mode.normal`` (2) — return chain unchanged.
            ``tuple_mode.lossy`` (1) — mask boundary (first-occurrence) intervals
            in-place; output length equals input length.
            ``tuple_mode.redundant`` (3) — append k trailing complementary
            boundary intervals; output length = n + k.

        Returns
        -------
        numpy.ma.MaskedArray
            ``normal`` / ``lossy``: shape (n,), dtype numpy.intp.
            ``redundant``: shape (n + k,), dtype numpy.intp.

        Raises
        ------
        ValueError
            When ``binding`` or ``tuple_mode`` is invalid.

        Examples
        --------
        ``tuple_mode.normal`` returns the chain unchanged:

    ``` py linenums="1"
        import numpy as np
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        print(result)
        # [-- 2 3 2 -- 6]
    ```

        ``tuple_mode.lossy`` additionally masks boundary (first-occurrence)
        intervals, keeping the same length:

    ``` py linenums="1"
        import numpy as np
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        print(result)
        # [-- -- -- 2 -- --]
    ```

        ``tuple_mode.redundant`` appends trailing complementary boundary
        intervals, extending the length:

    ``` py linenums="1"
        import numpy as np
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array(
            [0, 2, 3, 2, 0, 6], mask=[1, 0, 0, 0, 1, 0], dtype=np.intp
        )
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        print(result)
        # [-- 2 3 2 -- 6 4 3 1]
    ```

        An empty chain stays empty in every mode:

    ``` py linenums="1"
        import numpy as np
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array([], mask=[], dtype=np.intp)
        result = intervals_tuple(chain, binding.start, tuple_mode.redundant)
        print(result)
        # []
    ```

        A fully masked chain stays fully masked:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array([2, 3, 2, 6], mask=[1, 1, 1, 1])
        result = intervals_tuple(chain, binding.start, tuple_mode.lossy)
        print(result)
        # [-- -- -- --]
    ```

        With ``binding.end``, the same modes apply but boundaries are detected
        right-to-left:

    ``` py linenums="1"
        import numpy as np
        import numpy.ma as ma
        from foapy import binding, tuple_mode
        from foapy.partials import intervals_tuple

        chain = ma.masked_array([2, 0, 3, 2], mask=[0, 1, 0, 0], dtype=np.intp)
        result = intervals_tuple(chain, binding.end, tuple_mode.normal)
        print(result)
        # [2 -- 3 2]
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

    ar = ma.asarray(chain)

    if tuple_mode == tuple_mode_cls.normal:
        return ar.copy()

    chain_mask = ma.getmaskarray(ar)
    non_masked_idx = np.where(~chain_mask)[0]
    compressed = ar.compressed().astype(np.intp)
    m = len(compressed)

    if m == 0:
        return ar.copy()

    if tuple_mode == tuple_mode_cls.lossy:
        return _lossy(ar, chain_mask, non_masked_idx, compressed, binding)

    return _redundant(ar, chain_mask, non_masked_idx, compressed, binding, len(ar))


def _lossy(ar, chain_mask, non_masked_idx, compressed, binding):
    # A boundary interval is larger than its distance from the boundary in
    # the traversal direction. Compressed indices discard gap lengths, so
    # comparisons must use positions in the original array.
    work = compressed[::-1] if binding == binding_cls.end else compressed
    work_pos = (
        (len(ar) - 1 - non_masked_idx)[::-1]
        if binding == binding_cls.end
        else non_masked_idx
    )
    first = work > work_pos
    m = len(work)

    if binding == binding_cls.end:
        # Indices in reversed compressed → map back to original compressed order.
        boundary_compressed_idx = m - 1 - np.where(first)[0]
    else:
        boundary_compressed_idx = np.where(first)[0]

    boundary_orig_positions = non_masked_idx[boundary_compressed_idx]

    new_mask = chain_mask.copy()
    new_mask[boundary_orig_positions] = True
    return ma.masked_array(ar.data.copy(), mask=new_mask)


def _redundant(ar, chain_mask, non_masked_idx, compressed, binding, n_full):
    # Compute trailing intervals using actual positional distances in the full array.
    # Uses the same "last occurrence" detection as core.intervals_tuple.redundant
    # but substitutes full-array positions for compressed positions.
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

    result_data = np.concatenate([ar.data, trailing])
    result_mask = np.concatenate([chain_mask, np.zeros(len(trailing), dtype=bool)])
    return ma.masked_array(result_data, mask=result_mask)
