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
    data = np.asanyarray(X)
    if data.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {data.ndim}"}
        )

    perm = data.argsort(kind="mergesort")

    mask_shape = data.shape
    unique_mask = np.empty(mask_shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    result_mask = np.full_like(unique_mask, False)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True
    return data[result_mask]
