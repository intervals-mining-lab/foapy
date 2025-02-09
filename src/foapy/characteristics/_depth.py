import numpy as np


def depth(intervals):
    """
    Calculation depth of intervals.

    $$ G=\\sum_{i=1}^{n} \\log_2 \\Delta_{i} $$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals

    Returns
    -------
    : float
        The depth of the input array of intervals.

    Examples
    --------

    Calculate the depth of intervals of a sequence.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.depth(intervals)
    print(result)
    # 7.584962500721156
    ```

    """
    from foapy.characteristics import volume

    return np.log2(volume(intervals))
