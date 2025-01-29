import numpy as np


def arithmetic_mean(intervals):
    """
    Calculate the arithmetic mean of the intervals.

    \[ \Delta_a = \sum_{i=1}^{n} \\frac{\Delta_{i}}{n} \]

    where \( \Delta_{i} \) represents each interval and \( n \)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals (any number type array allowed).

    Returns
    -------
    : float
        The arithmetic mean of the input array of intervals.
    """  # noqa: W605

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return np.sum(intervals) / n
