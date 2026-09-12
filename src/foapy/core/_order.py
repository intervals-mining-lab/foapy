from typing import Optional, Tuple, Union

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._factorize import _normalize_sequence_axis, _stable_factorize


def order(
    X: ArrayLike,
    return_alphabet: bool = False,
    *,
    axis: Optional[int] = None,
) -> Union[ndarray, Tuple[ndarray, ndarray]]:
    """

    Decompose a sequence into its one-dimensional order and alphabet.

    Alphabet is a list of all unique values from the input array in order of their first appearance.
    Order is an array of indices that maps each element in the input array to its position
    in the alphabet.

    | Input array X | Order       | Alphabet  | Note                                              |
    |---------------|-------------|-----------|---------------------------------------------------|
    | [ x y x z ]   | [ 0 1 0 2 ] | [ x y z ] | Example decomposition into order and alphabet     |
    | [ y x y z ]   | [ 0 1 0 2 ] | [ y x z ] | Same order as above, different alphabet           |
    | [ y y x z ]   | [ 0 0 1 2 ] | [ y x z ] | Same alphabet as above, different order           |
    | [ ]           | [ ]         | [ ]       | Empty array                                       |

    Parameters
    ----------
    X : array_like
        Sequence to factorize. With an explicit ``axis``, each complete
        orthogonal slice indexed along that axis is one sequence element.

    return_alphabet : bool, optional
        If True also return array's alphabet
    axis : int, optional
        Sequence axis. If omitted, ``X`` must be 1-dimensional. Negative
        axes follow NumPy conventions.

    Returns
    -------
    order : ndarray
        One-dimensional order of length ``X.shape[axis]`` for an explicit
        axis, or ``len(X)`` for the legacy one-dimensional call.

    alphabet : ndarray
        Alphabet of X. Only provided if ``return_alphabet`` is True. For an
        explicit axis it retains the input rank and axis placement.

    Raises
    -------
    Not1DArrayException
        When ``X`` is scalar, or is multidimensional without an explicit axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.

    Examples
    --------

    Get an order of a characters sequence.

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

    Treat complete rows as elements and reconstruct the source:

    ``` py linenums="1"
    import numpy as np
    import foapy
    source = np.array([[2, 1], [3, 4], [2, 1]])
    result, alphabet = foapy.order(source, True, axis=0)
    print(result)
    # [0 1 0]
    restored = np.take(alphabet, result, axis=0)
    print(np.array_equal(restored, source))
    # True
    ```

    The same rule applies to an interior axis of a 3-dimensional input:

    ``` py linenums="1"
    import numpy as np
    import foapy

    source = np.array(
        [
            [[1, 2], [3, 4], [1, 2]],
            [[5, 6], [7, 8], [5, 6]],
        ]
    )
    result, alphabet = foapy.order(source, True, axis=-2)
    print(result)
    # [0 1 0]
    restored = np.take(alphabet, result, axis=-2)
    print(np.array_equal(restored, source))
    # True
    ```
    """  # noqa: E501

    data = np.asanyarray(X)

    if data.ndim != 1:
        result, alphabet = _stable_factorize(data, axis=axis)

        if return_alphabet:
            return result, alphabet
        return result

    if axis is not None:
        _normalize_sequence_axis(data, axis)

    # This is the original scalar-element algorithm. In particular, the
    # alphabet selection remains conditional on return_alphabet.
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
