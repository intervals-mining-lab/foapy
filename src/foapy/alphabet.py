import numpy as np

from foapy.exceptions import Not1DArrayException


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
    result: np.array or Exception
    Exception if not d1 array, np.array otherwise.

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
    >>> a = []
    >>> result = alphabet(a)
    >>> result
    []

    ---4----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> result = alphabet(a)
    >>> result
    Exception
    """
    # ex.:
    # data = ['a', 'c', 'c', 'e', 'd', 'a']
    data = np.asanyarray(X)
    if data.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {data.ndim}"}
        )
    # Sort data positions
    # ex.:
    #         a  a  c  c  d  e
    # perm = [0, 5, 1, 2, 4, 3]
    perm = data.argsort(kind="mergesort")

    # Create tmp mask array to store True on positions where appears new value
    # ex.:
    #              a  a  c  c  d  e
    # perm      = [0, 5, 1, 2, 4, 3]
    # perm[1:]  = [   5, 1, 2, 4, 3]
    # perm[:-1] = [0, 5, 1, 2, 4   ]

    # data[perm[1:]]                    = [        'a',  'c',  'c',  'd',  'e']
    # data[perm[:-1]]                   = [        'a',  'a',   'c',  'c',  'd']
    # data[perm[1:]] != data[perm[:-1]] = [      False, True, False, True, True]
    # unique_mask                       = [True, False, True, False, True, True]
    #                                        a     a     c      c      d     e
    unique_mask = np.empty(data.shape, dtype=bool)
    # First element is new
    unique_mask[:1] = True
    # Set true on positions where value differs from previous
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    # Create tmp array that will store reverse sorted mask array
    # ex.:
    #                        a     a     c      c      d     e
    # unique_mask       = [True, False, True, False, True, True]
    # perm              = [   0,      5,   1,     2,    4,    3]
    # perm[unique_mask] = [   0,           1,           4,    3]
    # result_mask       = [True, True, False, True, True, False]
    #                        a     c     c      e      d     a
    result_mask = np.full_like(unique_mask, False)
    result_mask[perm[unique_mask]] = True

    # Return elements that are first appears of unique values
    # ex.:
    # data              = [ 'a',  'c',   'c',  'e',  'd',  'a' ]
    # result_mask       = [True, True, False, True, True, False]
    # data[result_mask] = [ 'a',  'c',         'e',  'd'       ]
    return data[result_mask]
