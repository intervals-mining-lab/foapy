import numpy as np


def geometric_mean(intervals, dtype=None):
    """
    Calculates average geometric value of intervals lengths.

    $$ \\Delta_g=\\sqrt[n]{\\prod_{i=1}^{n} \\Delta_{i}}$$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals
    dtype : dtype, optional
        The dtype of the output

    Returns
    -------
    : float
        The geometric mean of the input array of intervals.

    Examples
    --------

    Calculate the geometric mean of intervals of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.geometric_mean(intervals)
    print(result)
    # 2.4018739103520055

    # Improve precision by specifying a dtype.
    result = foapy.characteristics.geometric_mean(intervals, dtype=np.longdouble)
    print(result)
    # 2.4018739103520053365
    ```
    """
    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    volume = np.prod(intervals, dtype=dtype)

    return np.power(volume, 1 / n, dtype=dtype)
