import numpy as np
import numpy.ma as ma

from foapy.core._order import order as core_order
from foapy.exceptions import Not1DArrayException


def order(X, return_alphabet=False):
    """
        Map a partial sequence to its order, preserving gap positions.

        Parameters
        ----------
        X : array_like or numpy.ma.MaskedArray
            1-D sequence (plain or masked). Masked positions are treated as gaps
            and are preserved in the output.
        return_alphabet : bool, optional
            If True, also return the alphabet of non-masked unique values.

        Returns
        -------
        result : numpy.ma.MaskedArray, shape (n,), dtype numpy.intp
            Masked 1-D array of the same length as X. Non-masked positions hold
            the element's 0-based alphabet index (first-appearance order).
            Masked positions are identical to the input mask.
        alphabet : numpy.ndarray, shape (p,)
            Only returned when return_alphabet=True. Unique non-masked values in
            first-appearance order. p = number of unique non-masked values.

        Raises
        ------
        Not1DArrayException
            When X has more than one dimension.

        Examples
        --------
        Map a partial sequence to its order. Masked positions (gaps) keep their
        position in the output but stay masked; the index count only advances
        over non-masked values:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy.partials import order

        X = ma.masked_array(['a', 'x', 'b', 'a', 'y'], mask=[0, 1, 0, 0, 1])
        result = order(X)
        print(result)
        # [0 -- 1 0 --]
    ```

        The order of an empty sequence is an empty masked array:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy.partials import order

        X = ma.masked_array([], mask=[])
        result = order(X)
        print(result)
        # []
    ```

        If all positions are masked, every position in the result stays masked:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy.partials import order

        X = ma.masked_array(['a', 'b', 'c'], mask=[1, 1, 1])
        result = order(X)
        print(result)
        # [-- -- --]
    ```

        A plain list or ndarray without a mask works the same as foapy.order:

    ``` py linenums="1"
        from foapy.partials import order

        X = ['a', 'b', 'a', 'c']
        result = order(X)
        print(result)
        # [0 1 0 2]
    ```

        Masking doesn't just skip a value — it removes the position entirely,
        so a value can "reappear" as first occurrence if its earlier occurrence
        is masked:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy.partials import order

        X = ma.masked_array(['a', 'x', 'b', 'a', 'b'], mask=[0, 1, 0, 0, 0])
        result = order(X)
        print(result)
        # [0 -- 1 0 1]
    ```

        With ``return_alphabet=True``, also get the unique non-masked values in
        first-appearance order:

    ``` py linenums="1"
        import numpy.ma as ma
        from foapy.partials import order

        X = ma.masked_array(['a', 'x', 'b', 'a', 'y'], mask=[0, 1, 0, 0, 1])
        result, alphabet = order(X, return_alphabet=True)
        print(result)
        # [0 -- 1 0 --]
        print(alphabet)
        # ['a' 'b']
    ```
    """
    ar = ma.asarray(X)

    if ar.ndim > 1:
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {ar.ndim}"}
        )

    n = len(ar)
    full_mask = ma.getmaskarray(ar)
    compressed = ar.compressed()

    if len(compressed) == 0:
        result_data = np.zeros(n, dtype=np.intp)
        result = ma.masked_array(result_data, mask=full_mask)
        if return_alphabet:
            return result, np.array([], dtype=ar.dtype)
        return result

    order_compressed, alphabet_values = core_order(compressed, return_alphabet=True)

    result_data = np.zeros(n, dtype=np.intp)
    result_data[~full_mask] = order_compressed
    result = ma.masked_array(result_data, mask=full_mask)

    if return_alphabet:
        return result, alphabet_values
    return result
