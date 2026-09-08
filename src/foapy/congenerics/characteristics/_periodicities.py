import numpy as np


def periodicities(intervals, dtype=None):
    """
    Calculates periodicity of the intervals grouped by congeneric sequence.

    $$
    \\left[ \\tau_j \\right]_{1 \\le j \\le m} =
    \\left[
    \\left( \\prod_{i=1}^{n_j} \\Delta_{ij} \\right)^{1/n_j} *
    \\frac{ n_j }{ \\sum_{i=1}^{n_j} \\Delta_{ij} }
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
        An array of the periodicity of congeneric intervals.

    Examples
    --------

    Calculate the periodicities of congeneric intervals of a sequence.

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

    result = foapy.congenerics.characteristics.periodicities(intervals)
    print(result)
    # [0.95244121 1.         1.         1.        ]
    ```

    Calculate the periodicities of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.congenerics.characteristics.periodicities(X)
    print(result)
    # [0.8        0.8914645  0.82207069]
    ```
    """  # noqa: W605, E501

    from foapy.congenerics.characteristics import arithmetic_means, geometric_means

    geometric_means_seq = geometric_means(intervals, dtype=dtype)
    arithmetic_means_seq = arithmetic_means(intervals, dtype=dtype)
    return np.divide(
        geometric_means_seq,
        arithmetic_means_seq,
        where=arithmetic_means_seq != 0.0,
        dtype=dtype,
    )
