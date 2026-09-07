import numpy as np
import numpy.ma as ma


def alphabet(CS: ma.MaskedArray) -> np.ndarray:
    """
    Extract the row labels of a congeneric decomposition.

    Per the Alphabet of Congeneric sequences definition, row j's label is
    its single non-masked value: ``alphabet(CS)[j] == CS[j].compressed()[0]``.

    Parameters
    ----------
    CS : numpy.ma.MaskedArray, shape (m, l)
        Output of :func:`foapy.congenerics.sequences`. Each row must have at
        least one non-masked position (guaranteed when CS was produced by
        `sequences`).

    Returns
    -------
    numpy.ndarray, shape (m,)
        Row labels, in row order.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    result = foapy.congenerics.alphabet(CS)
    print(result)
    # ['a' 'b' 'c']
    ```
    """
    m = CS.shape[0]
    if m == 0:
        return np.array([], dtype=CS.dtype)

    first_valid_col = (~ma.getmaskarray(CS)).argmax(axis=1)
    return CS.data[np.arange(m), first_valid_col]
