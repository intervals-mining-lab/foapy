import numpy.ma as ma

from foapy.core._order import order as core_order
from foapy.exceptions import Not1DArrayException


def alphabet(X):
    """
    Extract the alphabet of a partial sequence.

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
    Get an alphabet from a partial sequence.
    Masked positions are excluded, remaining values keep first-appearance order:

    ``` py linenums="1"
    import numpy.ma as ma
    from foapy.partials import alphabet

    X = ma.masked_array(['a', 'b', 'a', 'c'], mask=[0, 1, 0, 0])
    result = alphabet(X)
    print(result)
    # ['a' 'c']
    ```

    An alphabet of an empty sequence is an empty array:

    ``` py linenums="1"
    import numpy.ma as ma
    from foapy.partials import alphabet

    X = ma.masked_array([], mask=[])
    result = alphabet(X)
    print(result)
    # []
    ```

    If all positions are masked, the alphabet is empty:

    ``` py linenums="1"
    import numpy.ma as ma
    from foapy.partials import alphabet

    X = ma.masked_array(['a', 'b', 'c'], mask=[1, 1, 1])
    result = alphabet(X)
    print(result)
    # []
    ```

    A plain list or ndarray without a mask works the same as foapy.alphabet:

    ``` py linenums="1"
    from foapy.partials import alphabet

    X = ['a', 'b', 'a']
    result = alphabet(X)
    print(result)
    # ['a' 'b']
    ```

    Masking doesn't just skip a value — it removes the position entirely,
    so a value can "reappear" as first occurrence if its earlier occurrence is masked:

    ``` py linenums="1"
    import numpy.ma as ma
    from foapy.partials import alphabet

    X = ma.masked_array(['a', 'x', 'b', 'a', 'b'], mask=[0, 1, 0, 0, 0])
    result = alphabet(X)
    print(result)
    # ['a' 'b']
    ```
    """
    ar = ma.asarray(X)

    if ar.ndim > 1:
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {ar.ndim}"}
        )

    compressed = ar.compressed()
    if len(compressed) == 0:
        import numpy as np

        return np.array([], dtype=ar.dtype)

    _, alphabet_values = core_order(compressed, return_alphabet=True)
    return alphabet_values
