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

    ----1----
    >>> X = [
            [1 4 4]
            [1 3]
            [3 1]
            ]
    >>> b = depth(X)
    >>> b
    [0.2516 0.2075 0.2075]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = depth(X)
    >>> b
    [0.3219 0.1657 0.2826]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = depth(X)
    >>> b
    [0.3219 0.22005 0.13834]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = depth(X)
    >>> b
    [0.16569]

    ----5----
    >>> X = [[]]
    >>> b = depth(X)
    >>> b
    [0]

    ----6----
    >>> X = [[1]]
    >>> b = depth(X)
    >>> b
    [0]

    ----7----
    >>> X = [
        [1 1 1 1 1]
    ]
    >>> b = depth(X)
    >>> b
    [0]

    """
    return np.subtract(entropy(intervals), average_remoteness(intervals))
