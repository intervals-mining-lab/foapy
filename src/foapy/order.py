import numpy as np

from foapy.alphabet import alphabet
from foapy.exceptions import Not1DArrayException


def order(X, return_alphabet=False):
    """
    Find array sequence  in order of their appearance

    Parameters
    ----------
    X: np.array
        Array to get unique values.

    return_alphabet: bool, optional
        If True also return array's alphabet

    Returns
    -------
    result: np.array or Exception.
        Exception if not d1 array, np.array otherwise.

    Examples
    --------

    ----1----
    >>> a = ['a', 'b', 'a', 'c', 'd']
    >>> b = order(a)
    >>> b
    [0, 1, 0, 2, 3]

    ----2----
    >>> a = ['a', 'c', 'c', 'e', 'd', 'a']
    >>> b, c = order(a, True)
    >>> b
    [0, 1, 1, 2, 3, 0]
    >>> c
    [a, c, e, d, a]

     ----3----
    >>> a = []
    >>> b = order(a)
    >>> b
    []

     ----4----
    >>> a = ["E"]
    >>> b = order(a)
    >>> b
    [0]

     ----5----
    >>> a = [1, 2, 2, 3, 4, 1]
    >>> b = order(a)
    >>> b
    [0, 1, 1, 2, 3, 0]

     ----6----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> b = order(a)
    >>> b
    Exception

     ----7----
    >>> a = [[[1], [3]], [[6], [9]], [[6], [3]]]
    >>> b = order(a)
    >>> b
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
    alphabet_values = alphabet(X)

    result = []

    for i in convert_arr:  # getting mask for array
        result.append(np.where(alphabet_values == i)[0][0])

    if return_alphabet:
        return np.array(result), alphabet_values

    return np.array(result)
