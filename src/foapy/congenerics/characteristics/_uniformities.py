import numpy as np


def uniformities(intervals, dtype=None):
    """
    Calculates uniformity of the intervals grouped by congeneric sequence.

    $$
    \\left[ u_j \\right]_{1 \\le j \\le m} =
    \\left[
    \\log_2 { \\left(\\frac{1}{n_j} * \\sum_{i=1}^{n_j} \\Delta_{ij} \\right) } -
    \\frac{1}{n_j} * \\sum_{i=1}^{n_j} \\log_2 \\Delta_{ij}
    \\right]_{1 \\le j \\le m}
    $$

    where \\( \\Delta_{ij} \\) represents $i$-th interval of $j$-th
    congeneric intervals array, \\( n_j \\) is the total
    number of intervals in $j$-th congeneric intervals array
    and $m$ is number of congeneric intervals arrays.

    Parameters
    ----------
    intervals : array_like
        An array of congeneric intervals array
    dtype : dtype, optional
        The dtype of the output

    Returns
    -------
    : array
        An array of the uniformity of congeneric intervals.

    Examples
    --------

    Calculate the uniformities of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    CS = foapy.congenerics.sequences(source)
    chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
    tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
    intervals = [row[row != 0] for row in tuples]

    print(intervals)
    # [array([1, 2, 2]), array([2]), array([4]), array([6])]

    result = foapy.congenerics.characteristics.uniformities(intervals)
    print(result)
    # [0.07030559 0.         0.         0.        ]
    ```
    """  # noqa: W605, E501

    from foapy.congenerics.characteristics import (
        average_remotenesses,
        identifying_informations,
    )

    return np.subtract(
        identifying_informations(intervals, dtype=dtype),
        average_remotenesses(intervals, dtype=dtype),
        dtype=dtype,
    )
