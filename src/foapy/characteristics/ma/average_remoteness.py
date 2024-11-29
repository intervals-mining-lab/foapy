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
    size = np.array([len(elem) for elem in intervals])
    depth_seq = depth(intervals)
    res = np.divide(depth_seq, size, out=np.zeros_like(depth_seq), where=size != 0)

    return res
