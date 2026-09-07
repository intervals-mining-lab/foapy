import numpy as np


def geometric_means(intervals, dtype=None):
    """
    Calculates average geometric values of the intervals grouped by congeneric sequence.

    $$
    \\left[ \\Delta_{g_j} \\right]_{1 \\le j \\le m} =
    \\left[
    \\left( \\prod_{i=1}^{n_j} \\Delta_{ij} \\right)^{1/n_j}
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
        An array of the geometric means of congeneric intervals.

    Examples
    --------

    Calculate the geometric means of congeneric intervals of a sequence.

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

    result = foapy.congenerics.characteristics.geometric_means(intervals)
    print(result)
    # [1.58740105 2.         4.         6.        ]
    ```
    """  # noqa: W605, E501
    return np.asanyarray(
        [
            (
                np.power(
                    2,
                    np.sum(np.log2(line, dtype=dtype), dtype=dtype) / len(line),
                    dtype=dtype,
                )  # noqa: E501 E261
                if len(line) != 0
                else 0
            )
            for line in intervals
        ]
    )
