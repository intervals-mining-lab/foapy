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
    convert_arr = np.asanyarray(X)
    if convert_arr.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {
                "message": "Incorrect array form. Expected d1 array,"
                + f"exists {convert_arr.ndim}"
            }
        )

    _, indexes = np.unique(convert_arr, return_index=True)
    return convert_arr[np.sort(indexes)]
