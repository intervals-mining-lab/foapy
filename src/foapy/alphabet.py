import numpy as np

from foapy.exceptions import Not1DArrayException


def alphabet(X) -> np.ndarray:
    """
    Get an alphabet - a list of unique values from an array in order of their first appearance.

    The alphabet is constructed by scanning the input array from left to right and adding each new
    unique value encountered. This preserves the order of first appearance of each element, which
    can be important for maintaining relationships between elements in the original sequence.

    | Input array X | Alphabet  | Note                                   |
    |---------------|-----------|----------------------------------------|
    | [ b a b c ]   | [ b a c ] | 'b' appears before 'a'                 |
    | [ a b c b ]   | [ a b c ] | Same values but 'a' appears before 'b' |
    | [ 2 1 3 2 1 ] | [ 2 1 3 ] | 2 appears first, then 1, then 3        |
    | [ ]           | [ ]       | Empty alphabet                         |

    Parameters
    ----------
    X : array_like
        Array to extract an alphabet from. Must be a 1-dimensional array.

    Returns
    -------
    : ndarray
        Alphabet of X - array of unique values in order of first appearance

    Raises
    -------
    Not1DArrayException
        When X parameter is not a 1-dimensional array

    Examples
    --------
    Get an alphabet from a sequence of characters.
    Note that the alphabet contains unique values in order of first appearance:

    ``` py linenums="1"
    import foapy
    source = ['a', 'c', 'c', 'e', 'd', 'a']
    alphabet = foapy.alphabet(source)
    print(alphabet)
    # ['a', 'c', 'e', 'd']
    ```

    An alphabet of an empty sequence is an empty array:

    ``` py linenums="1"
    import foapy
    source = []
    alphabet = foapy.alphabet(source)
    print(alphabet)
    # []
    ```

    Getting an alphabet from an array with more than 1 dimension is not allowed:

    ``` py linenums="1"
    import foapy
    source = [[[1], [3]], [[6], [9]], [[6], [3]]]
    alphabet = foapy.alphabet(source)
    # Not1DArrayException: {'message': 'Incorrect array form. Expected d1 array, exists 3'}
    ```
    """  # noqa: E501

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

    result_mask = np.full_like(unique_mask, False)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True
    return data[result_mask]
