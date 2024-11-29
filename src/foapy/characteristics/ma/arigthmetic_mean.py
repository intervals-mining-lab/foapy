import numpy as np


def arigthmetic_mean(intervals):
    """
    Calculation arigthmetic_mean of sequence.
    Arigthmetic_mean is the addition of the elements of the intervals
    divide by length of its intervals of the sequence.

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
    >>> b = arigthmetic_mean(X)
    >>> b
    [3 2 2]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = arigthmetic_mean(X)
    >>> b
    [2.5 2.333 3]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = arigthmetic_mean(X)
    >>> b
    [2.5 2.66 2]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = arigthmetic_mean(X)
    >>> b
    [2.75]

    ----5----
    >>> X = [[]]
    >>> b = arigthmetic_mean(X)
    >>> b
    [0]

    ----6----
    >>> X = [[1]]
    >>> b = arigthmetic_mean(X)
    >>> b
    [1]

    ----7----
    >>> X = [
        [1 1 1 1 1]
    ]
    >>> b = arigthmetic_mean(X)
    >>> b
    [1]

    """
    return np.asanyarray(
        [np.sum(line) / len(line) if len(line) != 0 else 0 for line in intervals],
        dtype=float,
    )
