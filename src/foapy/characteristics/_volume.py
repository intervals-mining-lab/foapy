import numpy as np


def volume(intervals):
    """
    Calculation geometric mean of intervals.

    $$ G=\\prod_{i=1}^{n} \\Delta_{i}$$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals

    Returns
    -------
    : float
        The volume of the input array of intervals.

    Examples
    --------

    Calculate the geometric mean of intervals of a sequence.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.volume(intervals)
    print(result)
    # 192
    ```
    """  # noqa: W605

    return np.prod(intervals)
