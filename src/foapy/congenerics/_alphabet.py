import numpy as np
from numpy.typing import ArrayLike

from foapy.partials import alphabet as partials_alphabet


def alphabet(X: ArrayLike) -> np.ndarray:
    """
    Extract the row labels of the congeneric decomposition of a sequence.

    Equivalent to :func:`foapy.partials.alphabet`: unique non-masked values
    of X in first-appearance order. Row j of :func:`foapy.congenerics.sequences`
    holds the symbol ``alphabet(X)[j]``.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        1-D sequence (plain or masked). Masked positions are excluded.

    Returns
    -------
    numpy.ndarray, shape (m,)
        Unique non-masked values in first-appearance order.

    Raises
    ------
    Not1DArrayException
        When X has more than one dimension.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    result = foapy.congenerics.alphabet(source)
    print(result)
    # ['a' 'b' 'c']
    ```
    """
    return partials_alphabet(X)
