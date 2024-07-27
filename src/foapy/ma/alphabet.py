import numpy as np
import numpy.ma as ma

from foapy.exceptions import InconsistentOrderException, Not1DArrayException


def alphabet(X) -> np.ma.MaskedArray:
    """
    Implementation of ordered set - alphabet of elements.
    Alphabet is list of all unique elements in particular sequence.

    Parameters
    ----------
    X: masked_array
        Array to get unique values.

    Returns
    -------
    result: masked_array or Exception.
        Exception if wrong mask or not d1 array, masked_array otherwise.

    Examples
    --------

    ----1----
    >>> a = ['a', 'c', 'c', 'e', 'd', 'a']
    >>> mask = [0, 0, 0, 1, 0, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    ['a' 'c' -- 'd']

    ----2----
    >>> a = ['a', 'c', 'c', 'e', 'd', 'a']
    >>> mask = [0, 0, 0, 0, 0, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    ['a' 'c' 'e' 'd']

    ----3----
    >>> a = [1, 2, 2, 3, 4, 1]
    >>> mask = [0, 0, 0, 0, 0, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    [1 2 3 4]

    ----4----
    >>> a = []
    >>> mask = []
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    []

    ----5----
    >>> a = ['a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'c']
    >>> mask = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    ['а' -- 'c']

    ----6----
    >>> a = ['a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'c']
    >>> mask = [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    ['а' -- --]

    ----7----
    >>> a = ['a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'c']
    >>> mask = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    Exception

     ----8----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> mask = [[0, 0, 0], [0, 0, 0]]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    Exception
    """

    if X.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {X.ndim}"}
        )

    data = ma.getdata(X)
    mask = ma.getmaskarray(X)
    perm = data.argsort(kind="mergesort")

    mask_shape = data.shape
    unique_mask = np.empty(mask_shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]
    alphabet_indices = np.sort(perm[unique_mask])

    left_borders = np.argwhere(unique_mask).ravel()

    right_borders = np.empty(left_borders.shape, dtype=int)
    right_borders[:-1] = left_borders[1:]
    right_borders[-1:] = len(X)

    for idx, left in np.ndenumerate(left_borders):
        right = right_borders[idx]
        valid = (
            np.all(mask[perm][left:right])
            if mask[perm][left]
            else np.all(~mask[perm][left:right])
        )
        if not valid:
            i = data[perm[left]]
            raise InconsistentOrderException(
                {"message": f"Element '{i}' have mask and unmasked appearance"}
            )

    return ma.masked_array(data[alphabet_indices], mask[alphabet_indices])
