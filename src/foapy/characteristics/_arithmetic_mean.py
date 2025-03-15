import numpy as np


def arithmetic_mean(intervals, dtype=None):
    """
    Calculates average arithmetic value of intervals lengths.

    $$ \\Delta_a = \\frac{1}{n} * \\sum_{i=1}^{n} \\Delta_{i} $$

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
        The arithmetic mean of the input array of intervals.

    Examples
    --------

    Calculate the arithmetic mean of intervals of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.arithmetic_mean(intervals)
    print(result)
    # 2.8333333333333335

    # Improve precision by specifying a dtype.
    result = foapy.characteristics.arithmetic_mean(intervals, dtype=np.longdouble)
    print(result)
    # 2.8333333333333333333
    ```

    Improve precision by specifying a dtype.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    ```

    """  # noqa: W605

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return np.sum(intervals, dtype=dtype) / n
