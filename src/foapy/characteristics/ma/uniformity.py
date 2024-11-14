import numpy as np

from foapy.characteristics.ma.average_remoteness import average_remoteness
from foapy.characteristics.ma.entropy import entropy


def uniformity(intervals):
    """
    Calculation geometric of sequence.
    Uniformity is the substraction between entropy and average remoteness
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

    return np.subtract(entropy(intervals), average_remoteness(intervals))
