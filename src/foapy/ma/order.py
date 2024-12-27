import numpy as np
import numpy.ma as ma

from foapy import order as general_order
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

    order, alphabet_values = general_order(ma.getdata(X), return_alphabet=True)

    power = len(alphabet_values)
    length = len(X)

    result_data = np.tile(order, power).reshape(power, length)
    alphabet_indecies = np.arange(power).reshape(power, 1)
    result_mask = result_data != alphabet_indecies

    indecies_selector = np.any(~np.logical_or(result_mask, ma.getmaskarray(X)), axis=1)

    if np.any(indecies_selector):
        result_data = result_data[indecies_selector]
        result_mask = result_mask[indecies_selector]
    else:
        # If all items are masked we need define empty array explicity
        # otherwise, the result shape would be (0, length)
        # that affect compare arrays
        # (test tests/test_ma_order.py::TestMaOrder::test_void_int_values_with_mask)
        result_data = []
        result_mask = []

    result = ma.masked_array(result_data, mask=result_mask)

    if return_alphabet:  # Checking for get alphabet (optional)
        return result, alphabet_values[indecies_selector]
    return result
