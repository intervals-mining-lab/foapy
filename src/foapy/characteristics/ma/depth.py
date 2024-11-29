import numpy as np

from foapy.characteristics.ma.volume import volume


def depth(intervals):
    """
    Calculation depth of sequence.
    Depth is the log2 of the volume, where volume is the
    product of the elements of the intervals of the sequence .

    Parameters
    ----------
    X: two-dimensional intervals sequence array
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
    [4 1.585 1.585]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = depth(X)
    >>> b
    [4 3.1699 3.9069]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = depth(X)
    >>> b
    [4 3.585 2.585]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = depth(X)
    >>> b
    [5.1699]

    ----5----
    >>> X = [[]]
    >>> b = depth(X)
    >>> b
    []

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
    return np.asanyarray([np.log2(line) for line in volume(intervals)])
