import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from foapy.exceptions import Not1DArrayException
from foapy.partials import order as partials_order


def sequences(X: ArrayLike) -> ma.MaskedArray:
    """
    Decompose a sequence into its congeneric sequences.

    Row ``j`` of the result holds the ``j``-th alphabet symbol (in
    first-appearance order) at its original positions and is masked
    everywhere else, including positions masked in the input.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D sequence (plain or masked). Masked positions are gaps.

    Returns
    -------
    numpy.ma.MaskedArray, shape (m, l)
        m = size of the alphabet of X, l = len(X). Row j is the congeneric
        sequence for the j-th alphabet symbol.

    Raises
    ------
    Not1DArrayException
        When X has more than one dimension.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    result = foapy.congenerics.sequences(source)
    print(result)
    # [['a' -- 'a' --]
    #  [-- 'b' -- --]
    #  [-- -- -- 'c']]
    ```

    See :func:`foapy.congenerics.order` for how to restore this result from
    `foapy.congenerics.order(CS, True)`'s `order` and `alphabet` outputs.
    """
    ar = ma.asarray(X)

    if ar.ndim > 1:
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {ar.ndim}"}
        )

    order_result, alphabet_values = partials_order(ar, return_alphabet=True)
    m = len(alphabet_values)
    length = len(ar)

    valid = ~ma.getmaskarray(order_result)
    row_idx = order_result.data[valid]
    col_idx = np.arange(length)[valid]

    data = np.tile(ar.data, (m, 1))
    mask = np.ones((m, length), dtype=bool)
    mask[row_idx, col_idx] = False

    return ma.masked_array(data, mask=mask)
