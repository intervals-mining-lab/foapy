import numpy as np


def volume(intervals):
    """
    Calculates volumes of the intervals grouped by congeneric sequence.

    $$
    \\left[ V_j \\right]_{1 \\le j \\le m} =
    \\left[
    \\prod_{i=1}^{n_j} \\Delta_{ij}
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
        An array of the volumes of congeneric intervals.

    Examples
    --------

    Calculate the volumes of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.volume(intervals)
    print(result)
    # [4 2 4 6]
    ```

    Calculate the volumes of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.volume(X)
    print(result)
    # [16  9 15]
    ```
    """  # noqa: W605

    return np.asanyarray([np.prod(line) for line in intervals])
