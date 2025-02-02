import numpy as np


def volume(intervals):
    """
    Calculation of the volume of a sequence:
    Volume is calculated as the product
    of the elements in the intervals of the sequence.

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
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>      [1 4 4]
    >>>      [1 3]
    >>>      [3 1]
    >>>     ]
    >>> b = ma.volume(X)
    >>> b
    [16  3  3]

    ----2----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>> [1 1 4 4]
    >>> [3 1 3]
    >>> [5 3 1]
    >>> ]
    >>> b = ma.volume(X)
    >>> b
    [16 9  15]

    ----3----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>> [1 4 4 1]
    >>> [1 3 4]
    >>> [3 1 2]
    ]
    >>> b = ma.volume(X)
    >>> b
    [16 12 6]

    ----4----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>> [4 1 3 3]
    >>> ]
    >>> b = ma.volume(X)
    >>> b
    [36]

    ----5----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[]]
    >>> b = ma.volume(X)
    >>> b
    []

    ----6----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[1]]
    >>> b = ma.volume(X)
    >>> b
    [1]

    ----7----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>> [1 1 1 1 1]
    >>> ]
    >>> b = ma.volume(X)
    >>> b
    [1]

    """

    return np.asanyarray([np.prod(line) for line in intervals])
