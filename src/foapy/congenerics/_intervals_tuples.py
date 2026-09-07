import numpy as np
from numpy.typing import ArrayLike

from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls

from ._intervals_chains import _chain_work_frame, _from_work_frame
from ._intervals_chains import _validate as _validate_chain_args
from ._sequences import sequences


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
    X: ArrayLike, binding: int, chain_mode: int, tuple_mode: int
) -> np.ndarray:
    """
    Compute the congeneric interval tuples for each row of the decomposition,
    padded to a common width.

    Row j (before padding) is `foapy.partials.intervals_tuple` applied to row
    j of :func:`foapy.congenerics.intervals_chains`. ``chain_mode`` and
    ``tuple_mode`` are independent parameters: ``chain_mode`` selects how the
    chain is built, ``tuple_mode`` selects the boundary strategy applied to
    it, matching ``foapy.partials.intervals_chain``/``intervals_tuple``.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D sequence (plain or masked). Masked positions are gaps.
    binding : int
        ``binding.start`` or ``binding.end``.
    chain_mode : int
        ``chain_mode.boundary`` or ``chain_mode.cycle``.
    tuple_mode : int
        ``tuple_mode.lossy``, ``tuple_mode.normal``, or ``tuple_mode.redundant``.

    Returns
    -------
    numpy.ndarray, shape (m, x), dtype numpy.intp
        Row j holds its interval tuple values, right-padded with 0 to the
        width of the longest row (x).

    Raises
    ------
    Not1DArrayException
        When X has more than one dimension.
    ValueError
        When ``binding``, ``chain_mode``, or ``tuple_mode`` is invalid.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    result = foapy.congenerics.intervals_tuples(
        source,
        foapy.binding.start,
        foapy.chain_mode.boundary,
        foapy.tuple_mode.normal,
    )
    print(result)
    # [[1 2]
    #  [2 0]
    #  [4 0]]
    ```
    """
    _validate_chain_args(binding, chain_mode)
    _validate_tuple_mode(tuple_mode)

    CS = sequences(X)
    chain_work, valid_work, is_first_work, last_valid_per_row, length = (
        _chain_work_frame(CS, binding, chain_mode)
    )

    if tuple_mode == tuple_mode_cls.normal:
        # Normal mode always uses natural (un-flipped) column order,
        # regardless of binding — unlike lossy/redundant below.
        values = _from_work_frame(chain_work, binding)
        keep = _from_work_frame(valid_work, binding)
        return _pack_rows(values, keep)

    if tuple_mode == tuple_mode_cls.lossy:
        keep = valid_work & ~is_first_work
        return _pack_rows(chain_work, keep)

    # redundant: keep every occurrence (in work-frame order) plus one
    # trailing complementary value per row, measured from that row's actual
    # last occurrence to the true domain edge.
    extra = length - last_valid_per_row
    return _pack_rows(chain_work, valid_work, extra=extra)
