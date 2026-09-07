import numpy as np
import numpy.ma as ma

from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls

from ._intervals_chains import (
    _from_work_frame,
    _occurrence_positions,
    _validate_binding,
)


def _validate_tuple_mode(tuple_mode: int) -> None:
    if tuple_mode not in {
        tuple_mode_cls.lossy,
        tuple_mode_cls.normal,
        tuple_mode_cls.redundant,
    }:
        raise ValueError(
            {
                "message": (
                    "Invalid tuple_mode value. "
                    "Use tuple_mode.lossy, normal, or redundant."
                )
            }
        )


def _pack_rows(
    values: np.ndarray, keep: np.ndarray, extra: np.ndarray = None
) -> np.ndarray:
    """
    Compact each row's `keep`-selected entries (in column order) to the left
    of a 0-padded (m, x) result, optionally appending one extra value per row
    after the compacted entries. Vectorized via a cumulative-count scatter:
    no Python-level loop over rows.
    """
    m = values.shape[0]
    counts = keep.sum(axis=1)
    if extra is not None:
        counts = counts + 1
    width = int(counts.max()) if counts.size else 0

    result = np.zeros((m, width), dtype=np.intp)
    if width == 0:
        return result

    rank = np.cumsum(keep, axis=1) - 1
    rows, cols = np.nonzero(keep)
    result[rows, rank[rows, cols]] = values[rows, cols]

    if extra is not None:
        result[np.arange(m), counts - 1] = extra

    return result


def intervals_tuples(
    chains: ma.MaskedArray, binding: int, tuple_mode: int
) -> np.ndarray:
    """
    Compute the congeneric interval tuples for each row of the decomposition,
    padded to a common width.

    Row j (before padding) is `foapy.partials.intervals_tuple` applied to row
    j of `chains`. ``binding`` must match the binding used to produce
    `chains`.

    Parameters
    ----------
    chains : numpy.ma.MaskedArray, shape (m, l)
        Output of :func:`foapy.congenerics.intervals_chains`.
    binding : int
        ``binding.start`` or ``binding.end``. Must match the binding used to
        produce `chains`.
    tuple_mode : int
        ``tuple_mode.lossy``, ``tuple_mode.normal``, or ``tuple_mode.redundant``.

    Returns
    -------
    numpy.ndarray, shape (m, x), dtype numpy.intp
        Row j holds its interval tuple values, right-padded with 0 to the
        width of the longest row (x).

    Raises
    ------
    ValueError
        When ``binding`` or ``tuple_mode`` is invalid.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    chains = foapy.congenerics.intervals_chains(
        CS, foapy.binding.start, foapy.chain_mode.boundary
    )
    result = foapy.congenerics.intervals_tuples(
        chains,
        foapy.binding.start,
        foapy.tuple_mode.normal,
    )
    print(result)
    # [[1 2]
    #  [2 0]
    #  [4 0]]
    ```
    """
    _validate_binding(binding)
    _validate_tuple_mode(tuple_mode)

    valid_final = ~ma.getmaskarray(chains)
    data_final = np.asarray(ma.filled(chains, 0))
    length = chains.shape[1]

    if tuple_mode == tuple_mode_cls.normal:
        # Normal mode always uses natural (un-flipped) column order,
        # regardless of binding — unlike lossy/redundant below.
        return _pack_rows(data_final, valid_final)

    valid_work = _from_work_frame(valid_final, binding)
    chain_work = _from_work_frame(data_final, binding)
    _, is_first_work, last_valid_per_row = _occurrence_positions(valid_work)

    if tuple_mode == tuple_mode_cls.lossy:
        keep = valid_work & ~is_first_work
        return _pack_rows(chain_work, keep)

    # redundant: keep every occurrence (in work-frame order) plus one
    # trailing complementary value per row, measured from that row's actual
    # last occurrence to the true domain edge.
    extra = length - last_valid_per_row
    return _pack_rows(chain_work, valid_work, extra=extra)
