import numpy as np
from numpy.typing import ArrayLike

from ._intervals_tuples import intervals_tuples


def intervals_distributions(
    X: ArrayLike, binding: int, chain_mode: int, tuple_mode: int
) -> np.ndarray:
    """
    Compute the congeneric interval-value distributions for each row of the
    decomposition, padded to a shared global width.

    Row j (before padding) is `foapy.core.intervals_distribution` applied to
    row j's unpadded tuple from :func:`foapy.congenerics.intervals_tuples`.
    Unlike `intervals_tuples`, the padding width is a single value shared by
    every row — the maximum interval value found across *all* rows — so
    column i means "count of interval value i + 1" consistently across rows.
    Computed as a single vectorized scatter-add (``numpy.add.at`` over every
    row's real tuple entries at once) rather than one histogram per row.

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
    numpy.ndarray, shape (m, y), dtype numpy.intp
        Row j holds counts of interval values 1..y for the j-th congeneric
        sequence; trailing 0s mean zero occurrences of that interval value.

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
    result = foapy.congenerics.intervals_distributions(
        source,
        foapy.binding.start,
        foapy.chain_mode.boundary,
        foapy.tuple_mode.normal,
    )
    print(result)
    # [[1 1 0]
    #  [0 1 0]
    #  [0 0 1]]
    ```
    """
    tuples = intervals_tuples(X, binding, chain_mode, tuple_mode)
    m = tuples.shape[0]

    # 0 never occurs as a real interval value, so it unambiguously marks
    # intervals_tuples()'s right-padding and can be excluded directly.
    keep = tuples != 0
    if not keep.any():
        return np.zeros((m, 0), dtype=np.intp)

    rows, cols = np.nonzero(keep)
    values = tuples[rows, cols]
    width = int(values.max())

    result = np.zeros((m, width), dtype=np.intp)
    np.add.at(result, (rows, values - 1), 1)
    return result
