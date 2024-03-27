import numpy as np


class InconsistentOrderException(Exception):  # Initialise Exception class
    pass


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
    convert_arr = np.array(X)
    print(np.shape(convert_arr))
    if convert_arr.ndim > 1:  # Checking for d1 array
        raise InconsistentOrderException(
            {"message": "Incorrect array form. Excpected d1 array"}
        )
    result = np.array([])

    for i in convert_arr:
        if i not in result:

            result = np.append(result, i)

    return result


print(type(alphabet([1, 2, 3])))
