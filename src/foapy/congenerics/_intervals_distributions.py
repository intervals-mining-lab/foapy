import numpy as np


def intervals_distributions(tuples: np.ndarray) -> np.ndarray:
    """
    Compute the congeneric interval-value distributions for each row of the
    tuple matrix, padded to a shared global width.

    Row j (before padding) is `foapy.core.intervals_distribution` applied to
    the nonzero values in row j of `tuples`. Zeros are structural padding
    added by :func:`foapy.congenerics.intervals_tuples` and are excluded from
    frequency counts. The output width is a single value shared by every row
    — the maximum interval value found across *all* rows — so column i means
    "count of interval value i + 1" consistently across rows. Computed as a
    single vectorized scatter-add (``numpy.add.at`` over every row's real
    tuple entries at once) rather than one histogram per row.

    Parameters
    ----------
    tuples : numpy.ndarray, shape (m, x)
        Zero-padded output of :func:`foapy.congenerics.intervals_tuples`.

    Returns
    -------
    numpy.ndarray, shape (m, y), dtype numpy.intp
        Row j holds counts of interval values 1..y for the j-th congeneric
        sequence; trailing 0s mean zero occurrences of that interval value.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    chains = foapy.congenerics.intervals_chains(
        CS, foapy.binding.start, foapy.chain_mode.boundary
    )
    tuples = foapy.congenerics.intervals_tuples(
        chains, foapy.binding.start, foapy.tuple_mode.normal
    )
    result = foapy.congenerics.intervals_distributions(tuples)
    print(result)
    # [[1 1 0 0]
    #  [0 1 0 0]
    #  [0 0 0 1]]
    ```
    """
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
