import numpy as np
import numpy.ma as ma

from foapy.core._binding import binding as binding_cls
from foapy.core._chain_mode import chain_mode as chain_mode_cls


def _validate_binding(binding: int) -> None:
    if binding not in {binding_cls.start, binding_cls.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )


def _validate(binding: int, chain_mode: int) -> None:
    _validate_binding(binding)

    if chain_mode not in {chain_mode_cls.boundary, chain_mode_cls.cycle}:
        raise ValueError(
            {
                "message": (
                    "Invalid chain_mode value. "
                    "Use chain_mode.boundary or chain_mode.cycle."
                )
            }
        )


def _occurrence_positions(valid_work: np.ndarray):
    """
    Locate, per row of a work-frame validity mask, the previous occurrence
    column, the first occurrence, and the last occurrence — the bookkeeping
    shared by chain construction (:func:`_chain_work_frame`) and by anything
    consuming an already-built chain's mask (e.g.
    ``congenerics.intervals_tuples``), computed for every row at once via a
    shifted running maximum along columns (``numpy.maximum.accumulate``)
    rather than a per-row Python loop.

    Returns
    -------
    prev_valid : ndarray, shape (m, l)
        Work-frame column index of the previous occurrence in this row, or
        -1 if there is none.
    is_first_work : ndarray of bool, shape (m, l)
        True at each row's first occurrence in work-frame order.
    last_valid_per_row : ndarray, shape (m,)
        Work-frame column index of each row's last occurrence.
    """
    m, length = valid_work.shape
    col_idx = np.arange(length)
    pos_or_neg1 = np.where(valid_work, col_idx, -1)

    shifted = np.full_like(pos_or_neg1, -1)
    if length > 1:
        shifted[:, 1:] = pos_or_neg1[:, :-1]
    prev_valid = np.maximum.accumulate(shifted, axis=1)

    is_first_work = (prev_valid == -1) & valid_work

    if length:
        last_valid_per_row = pos_or_neg1.max(axis=1)
    else:
        last_valid_per_row = np.zeros(m, dtype=np.intp)

    return prev_valid, is_first_work, last_valid_per_row


def _chain_work_frame(CS: ma.MaskedArray, binding: int, chain_mode: int):
    """
    Compute the congeneric interval chain in "work frame" column order.

    Work frame is the natural left-to-right order for ``binding.start``, and
    the column-reversed order for ``binding.end`` — matching
    ``foapy.partials.intervals_chain``'s internal processing frame. A
    congeneric row has exactly one non-empty symbol, so its interval chain
    reduces to "distance to the previous non-masked column in this row".

    Returns
    -------
    chain_work : ndarray, shape (m, l)
    valid_work : ndarray of bool, shape (m, l)
    is_first_work : ndarray of bool, shape (m, l)
        True at each row's first occurrence in work-frame order.
    last_valid_per_row : ndarray, shape (m,)
        Work-frame column index of each row's last occurrence.
    length : int
    """
    length = CS.shape[1]
    valid = ~ma.getmaskarray(CS)
    valid_work = valid[:, ::-1] if binding == binding_cls.end else valid

    prev_valid, is_first_work, last_valid_per_row = _occurrence_positions(valid_work)

    col_idx = np.arange(length)
    if chain_mode == chain_mode_cls.cycle:
        delta = (length - last_valid_per_row)[:, None]
    else:
        delta = 1

    chain_work = np.where(
        is_first_work,
        col_idx[None, :] + delta,
        col_idx[None, :] - prev_valid,
    ).astype(np.intp)

    return chain_work, valid_work, is_first_work, last_valid_per_row, length


def _from_work_frame(arr_work: np.ndarray, binding: int) -> np.ndarray:
    return arr_work[:, ::-1] if binding == binding_cls.end else arr_work


def intervals_chains(
    CS: ma.MaskedArray, binding: int, chain_mode: int
) -> ma.MaskedArray:
    """
    Compute the congeneric interval chains for each row of the decomposition.

    Row j is `foapy.partials.intervals_chain` applied to row j of `CS`.
    Only `CS`'s mask matters — every non-masked value in every row is
    equivalent for this computation — so `CS` may be either the output of
    :func:`foapy.congenerics.sequences` or of
    :func:`foapy.congenerics.order`.

    Parameters
    ----------
    CS : numpy.ma.MaskedArray, shape (m, l)
        Output of :func:`foapy.congenerics.sequences` or
        :func:`foapy.congenerics.order`.
    binding : int
        ``binding.start`` or ``binding.end``.
    chain_mode : int
        ``chain_mode.boundary`` or ``chain_mode.cycle``.

    Returns
    -------
    numpy.ma.MaskedArray, shape (m, l)
        Row j is the interval chain of the j-th congeneric sequence.

    Raises
    ------
    ValueError
        When ``binding`` or ``chain_mode`` is invalid.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    result = foapy.congenerics.intervals_chains(
        CS, foapy.binding.start, foapy.chain_mode.boundary
    )
    print(result)
    # [[1 -- 2 --]
    #  [-- 2 -- --]
    #  [-- -- -- 4]]
    ```
    """
    _validate(binding, chain_mode)

    chain_work, valid_work, _, _, _ = _chain_work_frame(CS, binding, chain_mode)

    chain_final = _from_work_frame(chain_work, binding)
    valid_final = _from_work_frame(valid_work, binding)

    data = np.where(valid_final, chain_final, 0).astype(np.intp)
    return ma.masked_array(data, mask=~valid_final)
