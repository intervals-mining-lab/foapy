import numpy as np


def arithmetic_mean(intervals, dtype=None):
    """
    Calculates average arithmetic value of intervals lengths
    grouped by congeneric sequence.

    $$
    \\left[ \\Delta_{a_j} \\right]_{1 \\le j \\le m} =
    \\left[ \\frac{1}{n_j} * \\sum_{i=1}^{n_j} \\Delta_{ij} \\right]_{1 \\le j \\le m}
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
        An array of the arithmetic means of congeneric intervals.

    Examples
    --------

    Calculate the arithmetic means of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.arithmetic_mean(intervals)
    print(result)
    # [1.66666667 2 4 6]
    ```

    Calculate the arithmetic means of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.arithmetic_mean(X)
    print(result)
    # [2.5 2.333 3]
    ```
    """  # noqa: W605

    return np.asanyarray(
        [
            np.sum(line, dtype=dtype) / len(line) if len(line) != 0 else 0
            for line in intervals
        ]
    )
