import numpy as np


def volume(intervals):
    """
    Calculation volume of the intervals.

    \[ G = \prod_{i=1}^{n} \Delta_{i} \]

    where \( \Delta_{i} \) represents each interval and \( n \)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals (any number type array allowed).

    Returns
    -------
    : float
        The volume of the input array of intervals.
    """  # noqa: W605

    return np.prod(intervals)
