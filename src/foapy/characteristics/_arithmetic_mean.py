import numpy as np


def arithmetic_mean(intervals):
    """
    Calculate the arithmetic mean of the intervals.

    $$ \\Delta_a = \\frac{1}{n} * \\sum_{i=1}^{n} \\Delta_{i} $$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals

    Returns
    -------
    : float
        The arithmetic mean of the input array of intervals.

    Examples
    --------

    Calculate the arithmetic mean of intervals of a sequence.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.arithmetic_mean(intervals)
    print(result)
    # 2.8333333333333335
    ```
    """  # noqa: W605

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return np.sum(intervals) / n
