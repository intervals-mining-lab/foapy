import numpy as np

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

    data = np.asanyarray(X)
    if data.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {data.ndim}"}
        )

    perm = data.argsort(kind="mergesort")

    unique_mask = np.empty(data.shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    result_mask = np.zeros_like(unique_mask)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True

    power = np.count_nonzero(unique_mask)

    inverse_perm = np.empty(data.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(data.shape[0])

    result = np.cumsum(unique_mask) - 1
    inverse_alphabet_perm = np.empty(power, dtype=np.intp)
    inverse_alphabet_perm[result[inverse_perm][result_mask]] = np.arange(power)

    result = inverse_alphabet_perm[result][inverse_perm]

    if return_alphabet:
        return result, data[result_mask]
    return result
