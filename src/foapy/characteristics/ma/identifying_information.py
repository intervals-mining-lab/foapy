import numpy as np


def identifying_information(intervals):
    """
    Identifying information is calculated
    as the logarithm base 2 (log₂) of the average
    value of the elements in the intervals of the sequence.

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
    >>> b = identifying_information(X)
    >>> b
    [1.5849 1 1]

    ----2----
    >>> X = [
        [1 1 4 4]
        [3 1 3]
        [5 3 1]
    ]
    >>> b = identifying_information(X)
    >>> b
    [1.3219 1.22239 1.5849]

    ----3----
    >>> X = [
        [1 4 4 1]
        [1 3 4]
        [3 1 2]
    ]
    >>> b = identifying_information(X)
    >>> b
    [1.1375 1.45943 1.4594]

    ----4----
    >>> X = [
        [4 1 3 3]
        ]
    >>> b = identifying_information(X)
    >>> b
    [1.4594]

    ----5----
    >>> X = [[]]
    >>> b = identifying_information(X)
    >>> b
    [0]

    ----6----
    >>> X = [[1]]
    >>> b = identifying_information(X)
    >>> b
    [0]

    ----7----
    >>> X = [
        [1 1 1 1 1]
    ]
    >>> b = identifying_information(X)
    >>> b
    [0]

    """

    return np.asanyarray(
        [np.log2(np.average(line)) if len(line) != 0 else 0 for line in intervals]
    )
