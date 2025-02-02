import numpy as np

from foapy.characteristics.ma.volume import volume


def depth(intervals):
    """
    Calculation of the depth of a sequence:
    Depth is calculated as the logarithm base 2 (log₂) of the volume,
    where the volume is the product of the elements
    of the intervals in the sequence.

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
    >>>      ]
    >>> b = ma.depth(X)
    >>> b
    [4 1.585 1.585]

    ----2----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 4 4]
    >>>  [3 1 3]
    >>>  [5 3 1]
    >>> ]
    >>> b = ma.depth(X)
    >>> b
    [4 3.1699 3.9069]

    ----3----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 4 4 1]
    >>>  [1 3 4]
    >>>  [3 1 2]
    >>> ]
    >>> b = ma.depth(X)
    >>> b
    [4 3.585 2.585]

    ----4----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [4 1 3 3]
    >>>  ]
    >>> b = ma.depth(X)
    >>> b
    [5.1699]

    ----5----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[]]
    >>> b = ma.depth(X)
    >>> b
    []

    ----6----
    >>> import foapy.characteristics.ma as ma
    >>> X = [[1]]
    >>> b = ma.depth(X)
    >>> b
    [0]

    ----7----
    >>> import foapy.characteristics.ma as ma
    >>> X = [
    >>>  [1 1 1 1 1]
    >>> ]
    >>> b = ma.depth(X)
    >>> b
    [0]

    """
    return np.asanyarray([np.log2(line) for line in volume(intervals)])
