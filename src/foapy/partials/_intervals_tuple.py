import numpy as np
import numpy.ma as ma

from foapy.core._binding import binding as binding_cls
from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls


def intervals_tuple(chain, binding: int, tuple_mode: int) -> np.ndarray:
    """
    Apply a boundary handling strategy to a partial intervals chain, dropping
    gaps and returning the final flat tuple of interval values.

    Unlike ``partials.intervals_chain`` (position-preserving, aligned to the
    source sequence), ``intervals_tuple`` returns a plain array: gap (masked)
    positions carry no positional meaning once a boundary strategy has been
    applied, so they are excluded from the result rather than masked within
    it — matching ``foapy.core.intervals_tuple``'s return type.

    Parameters
    ----------
    chain : array_like or numpy.ma.MaskedArray
        1-D intervals chain produced by ``partials.intervals_chain``.
        Plain arrays are auto-wrapped (treated as fully unmasked).
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

    Returns
    -------
    numpy.ndarray
        1-D array, dtype ``numpy.intp``, with all gap positions excluded.
        For ``binding.end``, element order follows
        ``foapy.core.intervals_tuple``'s own (reversed-frame) convention
        rather than the source sequence's left-to-right order.

    Raises
    ------
    ValueError
        When ``binding`` or ``tuple_mode`` is invalid.

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

    Dense input (no gaps) matches :func:`foapy.core.intervals_tuple` exactly,
    including element order for ``binding.end``:

    ``` py linenums="1"
    import foapy
    from foapy.partials import intervals_tuple

    chain = [1, 2, 2, 4, 2]
    print(intervals_tuple(chain, foapy.binding.end, foapy.tuple_mode.lossy))
    # [2 2 1]
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
