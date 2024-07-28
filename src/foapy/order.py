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

    mask_shape = data.shape
    unique_mask = np.empty(mask_shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    inverse_perm = np.empty(data.shape, dtype=np.intp)
    for index, x in np.ndenumerate(perm):
        inverse_perm[x] = index[0]

    result_mask = np.full_like(unique_mask, False)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True
    alphabet_values = data[result_mask]

    alphabet_perm = alphabet_values.argsort(kind="mergesort")
    groups = np.arange(0, len(alphabet_values))
    result = np.empty(shape=data.shape, dtype=int)

    current = -1
    for idx, pos in np.ndenumerate(perm):
        if unique_mask[idx]:
            current = current + 1
        result[idx] = groups[alphabet_perm][current]

    if return_alphabet:
        return result[inverse_perm], alphabet_values
    return result[inverse_perm]
