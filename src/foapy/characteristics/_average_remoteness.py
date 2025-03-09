def average_remoteness(intervals, dtype=None):
    """
    Calculates average remoteness of intervals.

    $$ g = \\frac{1}{n} * \\sum_{i=1}^{n} \\log_2 \\Delta_{i} $$


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
        The average remoteness of the input array of intervals.

    Examples
    --------

    Calculate the average remoteness of intervals of a sequence.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.average_remoteness(intervals)
    print(result)
    # 1.2641604167868594
    ```

    Improve precision by specifying a dtype.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.average_remoteness(intervals)
    print(result)
    # 1.2641604167868593636
    """  # noqa: W605

    from foapy.characteristics import depth

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return depth(intervals, dtype=dtype) / n
