import numpy as np


def identifying_information(intervals):
    """
    Calculate the identifying information of the congeneric intervals.

    $$
    \\left[ H_j \\right]_{1 \\le j \\le m} =
    \\left[
    \\log_2 { \\left(\\frac{1}{n_j} * \\sum_{i=1}^{n_j} \\Delta_{ij} \\right) }
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
        An array of the identifying information of congeneric intervals.

    Examples
    --------

    Calculate the identifying information of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.identifying_information(intervals)
    print(result)
    # [0.73696559 1.         2.         2.5849625 ]
    ```

    Calculate the identifying information of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.identifying_information(X)
    print(result)
    # [1.32192809 1.22239242 1.5849625 ]
    ```
    """  # noqa: W605

    return np.asanyarray(
        [np.log2(np.average(line)) if len(line) != 0 else 0 for line in intervals]
    )
