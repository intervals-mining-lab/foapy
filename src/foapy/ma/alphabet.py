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
    perm = data.argsort(kind="mergesort")

    mask_shape = data.shape
    unique_mask = np.empty(mask_shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    first_appears_indecies = np.argwhere(unique_mask).ravel()
    count_true_in_mask_by_slice = np.add.reduceat(
        ma.getmaskarray(X[perm]), first_appears_indecies
    )
    slice_length = np.diff(np.r_[first_appears_indecies, len(X)])
    consistency_index = count_true_in_mask_by_slice / slice_length
    consistency_errors = np.argwhere(
        (consistency_index != 0) & (consistency_index != 1)
    ).ravel()
    if len(consistency_errors) > 0:
        i = data[consistency_errors[0]]
        raise InconsistentOrderException(
            {"message": f"Element '{i}' have mask and unmasked appearance"}
        )

    result_mask = np.full_like(unique_mask, False)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True
    return X[result_mask]
