import numpy as np


def depth(intervals, dtype=None):
    """
    Calculates depth of intervals.

    $$ G=\\sum_{i=1}^{n} \\log_2 \\Delta_{i} $$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals
    dtype : dtype, optional
        The dtype of the output.

    Returns
    -------
    : float
        The depth of the input array of intervals.

    Examples
    --------

    Calculate the depth of intervals of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.depth(intervals)
    print(result)
    # 7.584962500721156

    # Improve precision by specifying a dtype.
    result = foapy.characteristics.depth(intervals, dtype=np.longdouble)
    print(result)
    # 7.5849625007211561815
    ```
    """
    return np.sum(np.log2(intervals, dtype=dtype), dtype=dtype)
