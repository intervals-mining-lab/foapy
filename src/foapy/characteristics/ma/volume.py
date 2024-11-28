import numpy as np


def volume(intervals):
    """
    Calculation volume of sequence.
    Volume is the product of the elements of the intervals of the sequence.

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
    >>> a = [
            [0 0 -- -- -- 0 -- -- -- 0]
            [-- -- 1 1 -- -- 1 -- -- --]
            [-- -- -- -- 2 -- -- 2 2 --]
            ]
    >>> b = volume(a)
    >>> b
    [16  3  3]

    ----2----
    >>> a = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = volume(a)
    >>> b
    [16 9  15]

    ----3----
    >>> a = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = volume(a)
    >>> b
    [16 12 6]

    ----4----
    >>> a = [
        [-- -- -- 1 1 -- -- 1 -- --]
        ]
    >>> b = volume(a)
    >>> b
    [6]

    ----5----
    >>> a = [--]
    >>> b = volume(a)
    >>> b
    []

    ----6----
    >>> a = ["B"]
    >>> b = volume(a)
    >>> b
    [1]

    ----7----
    >>> a = [
        [1 1 1 1 1]
    ]
    >>> b = volume(a)
    >>> b
    [1]

    ----8----
    >>> a = [
        []
        ]
    >>> b = volume(a)
    >>> b
    []
    """

    return np.asanyarray([np.prod(line) for line in intervals])
