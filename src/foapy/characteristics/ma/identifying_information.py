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
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>       [1 4 4]
    >>>       [1 3]
    >>>       [3 1]
    >>>     ]
    >>> b = ma.identifying_information(X)
    >>> b
    [1.5849 1 1]

    ----2----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 4 4]
    >>>  [3 1 3]
    >>>  [5 3 1]
    >>> ]
    >>> b = ma.identifying_information(X)
    >>> b
    [1.3219 1.22239 1.5849]

    ----3----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 4 4 1]
    >>>  [1 3 4]
    >>>  [3 1 2]
    >>> ]
    >>> b = ma.identifying_information(X)
    >>> b
    [1.1375 1.45943 1.4594]

    ----4----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [4 1 3 3]
    >>>  ]
    >>> b = ma.identifying_information(X)
    >>> b
    [1.4594]

    ----5----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[]]
    >>> b = ma.identifying_information(X)
    >>> b
    [0]

    ----6----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[1]]
    >>> b = ma.identifying_information(X)
    >>> b
    [0]

    ----7----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 1 1 1]
    >>> ]
    >>> b = ma.identifying_information(X)
    >>> b
    [0]

    """

    return np.asanyarray(
        [np.log2(np.average(line)) if len(line) != 0 else 0 for line in intervals]
    )
