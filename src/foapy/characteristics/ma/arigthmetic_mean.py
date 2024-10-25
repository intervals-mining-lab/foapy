import numpy as np


def arigthmetic_mean(intervals):
    """
    Calculation volume of sequence.
    Volume is the product of the elements of the intervals of the sequence.

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

    return np.asanyarray([np.sum(line) / len(line) for line in intervals])
