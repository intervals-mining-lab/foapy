import numpy as np

from foapy.characteristics.ma.depth import depth


def average_remoteness(intervals):
    """
    Calculation geometric of sequence.
    Average remoteness is the Depth divide by number of intervals
    in the given congeneric sequence.

    Parameters
    ----------
    X: two-dimensional array
        Source array sequence.

    Returns
    -------
    result: array.

    Examples
    --------


    """

    size = np.asanyarray([len(elem) for elem in intervals])
    res = depth(intervals) / size
    return res
