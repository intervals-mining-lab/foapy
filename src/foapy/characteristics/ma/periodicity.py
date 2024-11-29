import numpy as np

from foapy.characteristics.ma.arigthmetic_mean import arigthmetic_mean
from foapy.characteristics.ma.geometric_mean import geometric_mean


def periodicity(intervals):
    """
    Calculation periodicity of sequence.
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

    ----1----
    >>> X = [
            [1 4 4]
            [1 3]
            [3 1]
            ]
    >>> b = periodicity(X)
    >>> b
    [0.83994 0.86602 0.86602]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = periodicity(X)
    >>> b
    [0.8 0.89136 0.82207]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = periodicity(X)
    >>> b
    [0.8 0.8585 0.9085]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = periodicity(X)
    >>> b
    [0.8907]

    ----5----
    >>> X = [[]]
    >>> b = periodicity(X)
    >>> b
    [1]

    ----6----
    >>> X = [[1]]
    >>> b = periodicity(X)
    >>> b
    [1]

    ----7----
    >>> X = [
        [1 1 1 1 1]
    ]
    >>> b = periodicity(X)
    >>> b
    [1]
    """
    geometric_mean_seq = geometric_mean(intervals)
    arigthmetic_mean_seq = arigthmetic_mean(intervals)
    return np.divide(
        geometric_mean_seq,
        arigthmetic_mean_seq,
        out=np.zeros_like(geometric_mean_seq),
        where=arigthmetic_mean_seq != 0,
    )
