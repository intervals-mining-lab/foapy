import numpy as np


def average_remoteness(intervals):
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

    Returns
    -------
    : array
        An array of the average remoteness of congeneric intervals.

    Examples
    --------

    Calculate the average remoteness of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    intervals = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.ma.average_remoteness(intervals)
    print(result)
    # [0.66666667 1.         2.         2.5849625 ]
    ```

    Calculate the average remoteness of congeneric intervals of a sequence.

    ``` py linenums="1"
    import foapy

    X = []
    X.append([1, 1, 4, 4])
    X.append([3, 1, 3])
    X.append([5, 3, 1])

    result = foapy.characteristics.ma.average_remoteness(X)
    print(result)
    # [1.         1.05664167 1.30229687]
    ```
    """  # noqa: W605

    from foapy.characteristics.ma import depth

    size = np.array([len(elem) for elem in intervals])
    depth_seq = depth(intervals)
    res = np.divide(depth_seq, size, out=np.zeros_like(depth_seq), where=size != 0)
    return res
