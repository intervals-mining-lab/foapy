import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from ._sequences import sequences


def order(X: ArrayLike) -> ma.MaskedArray:
    """
    Compute the congeneric order of each row of the congeneric decomposition.

    Per the Congeneric Order definition, every non-masked value in every row
    is 0 (the sole alphabet index of a single-symbol row) — so no per-row
    computation is needed: the mask of :func:`foapy.congenerics.sequences`
    already determines the result entirely.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D sequence (plain or masked). Masked positions are gaps.

    Returns
    -------
    numpy.ma.MaskedArray, shape (m, l)
        Row j is masked wherever `sequences(X)[j]` is masked; non-masked
        positions hold 0.

    Raises
    ------
    Not1DArrayException
        When X has more than one dimension.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    result = foapy.congenerics.order(source)
    print(result)
    # [[0 -- 0 --]
    #  [-- 0 -- --]
    #  [-- -- -- 0]]
    ```
    """
    CS = sequences(X)
    data = np.zeros(CS.shape, dtype=np.intp)
    return ma.masked_array(data, mask=ma.getmaskarray(CS))
