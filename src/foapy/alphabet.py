import numpy as np


def alphabet(X) -> np.ndarray:
    """
    Implementation of ordered set - alphabet of elements.
    Alphabet is list of all unique elements in particular sequence.
    Parametres
    —--------
    X: array
    Array to get unique values.

    Returns
    —-----
    result: array.

    Examples
    —------
    ----1----
    >>> a = ['a', 'c', 'c', 'e', 'd', 'a']
    >>> result = alphabet(a)
    >>> result
    ['a', 'c', 'e', 'd']

    ----2----
    >>> a = [0, 1, 2, 3, 4]
    >>> result = alphabet(a)
    >>> result
    [0, 1, 2, 3, 4]

    ---3----
    >>> a = [0, 1, 2, 3, 4]
    >>> result = alphabet(a)
    >>> result
    []
    """
    result = []

    for i in X:
        if i not in result:
            result.append(i)

    return result