import numpy as np


def arigthmetic_mean(intervals):
    """
    Arithmetic mean is calculated as the sum of
    the elements of the sequence divided
    by the number of elements in the sequence.

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
    >>>      [1 4 4]
    >>>     [1 3]
    >>>     [3 1]
    >>>     ]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [3 2 2]

    ----2----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 4 4]
    >>>  [3 1 3]
    >>>  [5 3 1]
    >>> ]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [2.5 2.333 3]

    ----3----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 4 4 1]
    >>>  [1 3 4]
    >>>  [3 1 2]
    >>> ]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [2.5 2.66 2]

    ----4----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [4 1 3 3]
    >>>  ]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [2.75]

    ----5----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[]]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [0]

    ----6----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[1]]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [1]

    ----7----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 1 1 1]
    >>> ]
    >>> b = ma.arigthmetic_mean(X)
    >>> b
    [1]

    """
    return np.asanyarray(
        [np.sum(line) / len(line) if len(line) != 0 else 0 for line in intervals],
        dtype=float,
    )
