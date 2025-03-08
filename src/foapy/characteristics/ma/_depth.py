import numpy as np


def depth(intervals):
    """
    Calculates depth of the intervals grouped by congeneric sequence.

    $$
    \\left[ G_j \\right]_{1 \\le j \\le m} =
    \\left[  \\sum_{i=1}^{n_j} \\log_2 \\Delta_{ij} \\right]_{1 \\le j \\le m}
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
        An array of the depths of congeneric intervals.

    Examples
    --------

    Calculate the depth of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.depth(intervals)
    print(result)
    # [2.        1.        2.        2.5849625]
    ```

    Calculate the depth of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.depth(X)
    print(result)
    # [4.        3.169925  3.9068906]
    ```
    """  # noqa: W605

    from foapy.characteristics.ma import volume

    return np.asanyarray([np.log2(line) for line in volume(intervals)])
