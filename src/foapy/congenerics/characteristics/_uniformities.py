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

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.congenerics.characteristics.uniformities(X)
    print(result)
    # [0.32192809 0.16575075 0.28266564]
    ```
    """  # noqa: W605

    from foapy.congenerics.characteristics import (
        average_remotenesses,
        identifying_informations,
    )

    return np.subtract(
        identifying_informations(intervals, dtype=dtype),
        average_remotenesses(intervals, dtype=dtype),
        dtype=dtype,
    )
