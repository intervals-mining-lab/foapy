import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from foapy.core._alphabet import alphabet as core_alphabet
from foapy.exceptions import Not1DArrayException


def alphabet(X: ArrayLike) -> np.ndarray:
    """
    Extract the alphabet of a partial sequence.

    Unique unmasked values are returned in the order of their first
    unmasked appearance. Masked positions are ignored, so a value that is
    masked at its first occurrence is introduced when it is encountered
    later in an unmasked position.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D sequence (plain or masked). Masked positions are excluded.

    Returns
    -------
    alphabet : numpy.ndarray, shape (p,)
        Unique non-masked values in first-appearance order.
        p = number of unique non-masked values. Empty array when all positions
        are masked or input is empty.

    Raises
    ------
    Not1DArrayException
        When X has more than one dimension.

    Examples
    --------
    Extract an alphabet from an ordinary sequence:

    ``` py linenums="1"
    import foapy

    source = ['a', 'c', 'c', 'e', 'd', 'a']
    alphabet = foapy.partials.alphabet(source)
    print(alphabet)
    # ['a', 'c', 'e', 'd']
    ```

    Masked positions are excluded from the alphabet:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(['a', 'x', 'b', 'a'], mask=[0, 1, 0, 0])
    alphabet = foapy.partials.alphabet(source)
    print(alphabet)
    # ['a', 'b']
    ```

    If the first occurrence of a value is masked, a later unmasked
    occurrence determines its position in the alphabet:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(['a', 'a', 'b', 'a'], mask=[1, 0, 0, 0])
    alphabet = foapy.partials.alphabet(source)
    print(alphabet)
    # ['a', 'b']
    ```

    An empty or fully masked sequence has an empty alphabet:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(['a', 'b'], mask=[1, 1])
    alphabet = foapy.partials.alphabet(source)
    print(alphabet)
    # []
    ```

    Inputs with more than one dimension are rejected:

    ``` py linenums="1"
    import foapy

    source = [[1, 2], [3, 4]]
    alphabet = foapy.partials.alphabet(source)
    # Not1DArrayException:
    # {'message': 'Incorrect array form. Expected d1 array, exists 2'}
    ```
    """
    ar = ma.asarray(X)

    if ar.ndim > 1:
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {ar.ndim}"}
        )

    compressed = ar.compressed()
    if len(compressed) == 0:
        return np.array([], dtype=ar.dtype)

    return core_alphabet(compressed)
