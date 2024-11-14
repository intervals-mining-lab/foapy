import numpy as np

from foapy.characteristics.ma.arigthmetic_mean import arigthmetic_mean
from foapy.characteristics.ma.geometric_mean import geometric_mean


def periodicity(intervals):
    """
    Calculation geometric of sequence.
    Periodicity is the substraction between entropy and average remoteness
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

    return np.divide(geometric_mean(intervals), arigthmetic_mean(intervals))
