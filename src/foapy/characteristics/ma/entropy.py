import numpy as np


def entropy(intervals):
    """

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

    return np.asanyarray([np.log2(np.average(line)) for line in intervals])
