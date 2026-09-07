import numpy as np


def average_remotenesses(intervals, dtype=None):
    """
    Calculates average remoteness of the intervals grouped by congeneric sequence.

    $$
    \\left[ g_j \\right]_{1 \\le j \\le m} =
    \\left[
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
        An array of the average remoteness of congeneric intervals.

    Examples
    --------

    Calculate the average remotenesses of congeneric intervals of a sequence.

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

    result = foapy.congenerics.characteristics.average_remotenesses(intervals)
    print(result)
    # [0.66666667 1.         2.         2.5849625 ]
    ```
    """  # noqa: W605, E501

    from foapy.congenerics.characteristics import depths

    size = np.array([len(elem) for elem in intervals])
    depth_seq = depths(intervals, dtype=dtype)
    res = np.divide(
        depth_seq,
        size,
        out=np.zeros_like(depth_seq),
        where=size != 0,
        dtype=dtype,
    )
    return res
