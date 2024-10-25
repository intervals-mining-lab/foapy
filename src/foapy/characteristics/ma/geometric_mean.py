import numpy as np


def geometric_mean(intervals):
    """
    Calculation geometric of sequence.
    Geometric mean is the square root of the product sequence.

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

    return np.asanyarray([np.power(np.prod(line), 1 / len(line)) for line in intervals])
