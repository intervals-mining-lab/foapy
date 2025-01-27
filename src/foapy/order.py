import numpy as np

from foapy.exceptions import Not1DArrayException


def order(X, return_alphabet=False):
    """

    Decompose an array into an order and an alphabet.

    The alphabet is a list of all unique values from the input array in order of their first appearance.
    The order is an array of indices that maps each element in the input array to its position
    in the alphabet.

    | Input array X | Order       | Alphabet  | Note                                              |
    |---------------|-------------|-----------|---------------------------------------------------|
    | [ x y x z ]   | [ 0 1 0 2 ] | [ x y z ] | Example decomposition to an order and an alphabet |
    | [ y x y z ]   | [ 0 1 0 2 ] | [ y x z ] | Same order as above, different alphabet           |
    | [ y y x z ]   | [ 0 0 1 2 ] | [ y x z ] | Same alphabet as above, different order           |
    | [ ]           | [ ]         | [ ]       | Empty array                                       |

    Parameters
    ----------
    X : array_like
        Array to decompose into an order and an alphabet. Must be a 1-dimensional array.

    return_alphabet : bool, optional
        If True also return array's alphabet

    Returns
    -------
    order : ndarray
        Order of X

    alphabet : ndarray
        Alphabet of X. Only provided if `return_alphabet` is True.

    Raises
    -------
    Not1DArrayException
        When X parameter is not d1 array

    Examples
    --------

    Get an order of a chars sequence.

    ``` py linenums="1"
    import foapy
    source = ['a', 'b', 'a', 'c', 'd']
    order = foapy.order(source)
    print(order)
    # [0, 1, 0, 2, 3]
    ```

    Reconstruct original sequence from the order and the alphabet.

    ``` py linenums="1"
    import foapy
    source = ['a', 'c', 'c', 'e', 'd', 'a']
    order, alphabet = foapy.order(source, True)
    print(order, alphabet)
    # [0, 1, 1, 2, 3, 0] ['a', 'c', 'e', 'd']
    restored = alphabet[order]
    print(restored)
    # ['a', 'c', 'c', 'e', 'd', 'a']
    ```

    An order of an empty sequence is empty array.

    ``` py linenums="1"
    import foapy
    source = []
    order = foapy.order(source)
    print(order)
    # []
    ```

    Getting an order of an array with more than 1 dimension is not allowed

    ``` py linenums="1"
    import foapy
    source = [[[1], [3]], [[6], [9]], [[6], [3]]]
    order = foapy.order(source)
    # Not1DArrayException: {'message': 'Incorrect array form. Expected d1 array, exists 3'}
    ```
    """  # noqa: E501

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
