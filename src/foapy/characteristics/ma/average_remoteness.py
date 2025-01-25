import numpy as np

from foapy.characteristics.ma.depth import depth


def average_remoteness(intervals):
    """
    Calculation of the average remoteness of a sequence:
    The average remoteness is calculated as the depth
    divided by the number of intervals in the
    given congeneric sequence.

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
    >>> b = average_remoteness(X)
    >>> b
    [1.3333 0.79248 0.79248]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = average_remoteness(X)
    >>> b
    [1  1.05664 1.30229]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = average_remoteness(X)
    >>> b
    [1 1.1949 0.8616]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = average_remoteness(X)
    >>> b
    [1.2925]

    ----5----
    >>> X = [[]]
    >>> b = average_remoteness(X)
    >>> b
    [0]

    ----6----
    >>> X = [[1]]
    >>> b = average_remoteness(X)
    >>> b
    [0]

    ----7----
    >>> X = [
        [1 1 1 1 1]
    ]
    >>> b = average_remoteness(X)
    >>> b
    [0]

    """
    size = np.array([len(elem) for elem in intervals])
    depth_seq = depth(intervals)
    res = np.divide(depth_seq, size, out=np.zeros_like(depth_seq), where=size != 0)
    return res
