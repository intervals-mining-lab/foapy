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

    power = np.count_nonzero(unique_mask)

    groups = np.full_like(perm, -1)
    groups[perm[unique_mask]] = np.arange(0, power)
    alphabet_perm = groups[groups != -1]

    inverse_alphabet_perm = np.empty(power, dtype=np.intp)
    for idx, pos in np.ndenumerate(alphabet_perm):
        inverse_alphabet_perm[pos] = idx[0]

    result = np.empty(shape=data.shape, dtype=int)
    inverse_perm = np.empty(data.shape, dtype=np.intp)

    current = -1
    for idx, pos in np.ndenumerate(perm):
        if unique_mask[idx]:
            current = current + 1
        result[idx] = inverse_alphabet_perm[current]
        inverse_perm[pos] = idx[0]

    if return_alphabet:
        result_mask = np.full_like(unique_mask, False)
        result_mask[:1] = True
        result_mask[perm[unique_mask]] = True
        return (result[inverse_perm], data[result_mask])

    return result[inverse_perm]
