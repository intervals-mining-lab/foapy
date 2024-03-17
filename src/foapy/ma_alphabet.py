import numpy as np
import numpy.ma as ma


def ma_alphabet(mask_arr) -> np.ma.MaskedArray:
    """
    Implementation of ordered set - alphabet of elements.
    Alphabet is list of all unique elements in particular sequence.
    Parametres
    ----------
    X: masked_array
        Array to get unique values.

    Returns
    -------
    result: masked_array or Exception
        Exception if wrong mask, masked_array otherwise.

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
    ['а' --]

    ----7----
    >>> a = ['a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'c']
    >>> mask = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = ma_alphabet(masked_a)
    >>> b
    Exception
    """

    result_arr = []
    unique_mask_obj = ma.unique(ma.getdata(mask_arr)[mask_arr.mask])
    for arr_index in mask_arr:
        if arr_index in unique_mask_obj:  # Checking for exception
            return Exception
        elif arr_index not in result_arr:  # Adding alphabet values
            result_arr.append(arr_index)
    return ma.masked_array(result_arr)  # Return and convert array
