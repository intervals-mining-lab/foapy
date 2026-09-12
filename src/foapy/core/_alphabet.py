from typing import Optional

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._factorize import _normalize_sequence_axis, _stable_factorize


def alphabet(X: ArrayLike, *, axis: Optional[int] = None) -> ndarray:
    """
    Get unique sequence elements in order of their first appearance.

    The alphabet is constructed by scanning the input array from left to right and adding each new
    unique value encountered. This preserves the order of the first appearance of each element, which
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
        Sequence to factorize. With an explicit ``axis``, each complete
        orthogonal slice indexed along that axis is one sequence element.
    axis : int, optional
        Sequence axis. If omitted, ``X`` must be 1-dimensional. Negative
        axes follow NumPy conventions.

    Returns
    -------
    : ndarray
        Unique elements in first-appearance order. For an explicit axis, the
        result has the same rank as ``X`` and only that axis changes length.

    Raises
    -------
    Not1DArrayException
        When ``X`` is scalar, or is multidimensional without an explicit axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.

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

    Rows can be treated as complete elements by selecting axis 0:

    ``` py linenums="1"
    import numpy as np
    import foapy
    source = np.array([[2, 1], [3, 4], [2, 1]])
    result = foapy.alphabet(source, axis=0)
    print(result)
    # [[2 1]
    #  [3 4]]
    ```

    For a 3-dimensional input, selecting axis 1 treats ``source[:, i, :]``
    as element ``i``. Equivalent negative axes are accepted:

    ``` py linenums="1"
    import numpy as np
    import foapy

    source = np.array(
        [
            [[1, 2], [3, 4], [1, 2]],
            [[5, 6], [7, 8], [5, 6]],
        ]
    )
    result = foapy.alphabet(source, axis=-2)
    print(result.shape)
    # (2, 2, 2)
    ```

    See :func:`foapy.order` for reconstruction with ``numpy.take``.
    """  # noqa: E501

    data = np.asanyarray(X)

    if data.ndim != 1:
        _, result = _stable_factorize(data, axis=axis)
        return result

    if axis is not None:
        _normalize_sequence_axis(data, axis)

    # Keep the legacy scalar-element path independent from order: computing
    # an inverse mapping roughly doubled its work and memory use.
    perm = data.argsort(kind="mergesort")

    unique_mask = np.empty(data.shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    result_mask = np.full_like(unique_mask, False)
    result_mask[:1] = True
    result_mask[perm[unique_mask]] = True
    return data[result_mask]
