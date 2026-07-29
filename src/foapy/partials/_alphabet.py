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
