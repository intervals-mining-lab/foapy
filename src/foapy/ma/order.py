import numpy as np
import numpy.ma as ma

from foapy.alphabet import alphabet
from foapy.exceptions import Not1DArrayException


def order(X, return_alphabet=False) -> np.ma.MaskedArray:
    """
    Find array sequence  in order of their appearance

    Parameters
    ----------
    X: masked_array
        Array to get unique values.

    return_alphabet: bool, optional
        If True also return array's alphabet

    Returns
    -------
    result: masked_array or Exception.
        Exception if not d1 array, masked_array otherwise.

    Examples
    --------

    ----1----
    >>> a = ['a', 'b', 'a', 'c', 'd']
    >>> b = order(a)
    >>> b
    [
    [0, -- 0, -- --]
    [-- 1 -- -- --]
    [-- -- -- 2, --]
    [-- -- -- -- 3]
    ]

    ----2----
    >>> a = ['a', 'b', 'a', 'c', 'd']
    >>> result, alphabet = order(a, True)
    >>> result
    [
    [0, -- 0, -- --]
    [-- 1 -- -- --]
    [-- -- -- 2, --]
    [-- -- -- -- 3]
    ]
    >>> alphabet
    ['a', 'b', 'c', 'd']

     ----3----
    >>> a = [1, 4, 1000, 4, 15]
    >>> b = order(a)
    >>> b
    [
    [0 -- -- -- --]
    [-- 1 -- 1 --]
    [-- -- 2 -- --]
    [-- -- -- -- 3]
    ]

     ----4----
    >>> a = ["a", "c", "c", "e", "d", "a"]
    >>> b = order(a)
    >>> b
    [
    [0 -- -- -- -- 0]
    [-- 1 1 -- -- --]
    [-- -- -- 2 -- --]
    [-- -- -- -- 3 --]
    ]

     ----5----
    >>> a = [1, 2, 2, 3, 4, 1]
    >>> b = order(a)
    >>> b
    [
    [0 -- -- -- -- 0]
    [-- 1 1 -- -- --]
    [-- -- -- 2 -- --]
    [-- -- -- -- 3 --]
    ]

     ----6----
    >>> a = ["ATC", "CGT", "ATC"]
    >>> b = order(a)
    >>> b
    [
    [0 -- 0]
    [-- 1 --]
    ]

     ----7----
    >>> a = []
    >>> b = order(a)
    >>> b
    []

     ----8----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> b = order(a)
    >>> b
    Exception

     ----9----
    >>> a = [[[1], [3]], [[6], [9]], [[6], [3]]]
    >>> b = order(a)
    >>> b
    Exception
    """
    if X.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {X.ndim}"}
        )

    alphabet_values = alphabet(X)

    result = np.empty((len(alphabet_values), (len(X))), np.int64)
    mask = np.ones((len(alphabet_values), (len(X))), np.int64)

    alphabet_seq = {}
    counter = 0
    for i in ma.getdata(alphabet_values):
        alphabet_seq[counter] = i
        counter += 1
    for idx_row, i in alphabet_seq.items():  # getting array sequence
        for idx_col, j in enumerate(ma.getdata(X)):
            if i == j:
                result[idx_row][idx_col] = idx_row
                mask[idx_row][idx_col] = 0

    if return_alphabet:  # Checking for get alhabet (optional)
        return ma.masked_array(result, mask=mask), alphabet_values
    return ma.masked_array(result, mask=mask)
