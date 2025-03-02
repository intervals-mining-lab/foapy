import numpy as np

from foapy.characteristics.ma import average_remoteness, identifying_information


def uniformity(intervals):
    """
    Calculate the uniformity of the congeneric intervals.

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

    Returns
    -------
    : array
        An array of the uniformity of congeneric intervals.

    Examples
    --------

    Calculate the uniformity of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.uniformity(intervals)
    print(result)
    # [0.07029893 0.         0.         0.        ]
    ```

    Calculate the uniformity of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.uniformity(X)
    print(result)
    # [0.32192809 0.16575075 0.28266564]
    ```
    """  # noqa: W605

    return np.subtract(
        identifying_information(intervals), average_remoteness(intervals)
    )
