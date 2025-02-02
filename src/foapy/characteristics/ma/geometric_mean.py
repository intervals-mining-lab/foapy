import numpy as np


def geometric_mean(intervals):
    """
    Calculation of the geometric mean of a sequence:
    The geometric mean is calculated as the nth root
    of the product of the elements in the sequence,
    where  n  is the number of elements in the sequence.

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
    >>>      [1 3]
    >>>      [3 1]
    >>>      ]
    >>> b = ma.geometric_mean(X)
    >>> b
    [2.5198  1.73205 1.73205]

    ----2----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 4 4]
    >>>  [3 1 3]
    >>>  [5 3 1]
    >>> ]
    >>> b = ma.geometric_mean(X)
    >>> b
    [2 2.08 2.466]

    ----3----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 4 4 1]
    >>>  [1 3 4]
    >>>  [3 1 2]
    >>> ]
    >>> b = ma.geometric_mean(X)
    >>> b
    [2 2.28942 1.8171]

    ----4----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [4 1 3 3]
    >>>  ]
    >>> b = ma.geometric_mean(X)
    >>> b
    [2.449489]

    ----5----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[]]
    >>> b = ma.geometric_mean(X)
    >>> b
    [0]

    ----6----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[1]]
    >>> b = ma.geometric_mean(X)
    >>> b
    [0]

    ----7----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [0 0 0 0 0]
    >>> ]
    >>> b = ma.geometric_mean(X)
    >>> b
    [0]

    """
    return np.asanyarray(
        [
            np.power(np.prod(line), 1 / len(line)) if len(line) != 0 else 0
            for line in intervals
        ],
        dtype=float,
    )
