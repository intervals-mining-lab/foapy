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
