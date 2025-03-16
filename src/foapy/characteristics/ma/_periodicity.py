import numpy as np


def periodicity(intervals, dtype=None):
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

    Calculate the periodicity of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.periodicity(intervals)
    print(result)
    # [0.95244063 1.         1.         1.        ]
    ```

    Calculate the periodicity of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.periodicity(X)
    print(result)
    # [0.8        0.8914645  0.82207069]
    ```
    """  # noqa: W605

    from foapy.characteristics.ma import arithmetic_mean, geometric_mean

    geometric_mean_seq = geometric_mean(intervals, dtype=dtype)
    arithmetic_mean_seq = arithmetic_mean(intervals, dtype=dtype)
    return np.divide(
        geometric_mean_seq,
        arithmetic_mean_seq,
        where=arithmetic_mean_seq != 0.0,
        dtype=dtype,
    )
