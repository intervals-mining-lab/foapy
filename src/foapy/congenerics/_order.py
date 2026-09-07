import numpy as np
import numpy.ma as ma


def order(CS: ma.MaskedArray) -> ma.MaskedArray:
    """
    Compute the congeneric order of each row of a congeneric decomposition.

    Per the Congeneric Order definition, every non-masked value in every row
    is 0 (the sole alphabet index of a single-symbol row) — so no per-row
    computation is needed: CS's own mask already determines the result.

    Parameters
    ----------
    CS : numpy.ma.MaskedArray, shape (m, l)
        Output of :func:`foapy.congenerics.sequences`.

    Returns
    -------
    numpy.ma.MaskedArray, shape (m, l)
        Row j is masked wherever `CS[j]` is masked; non-masked positions
        hold 0.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    result = foapy.congenerics.order(CS)
    print(result)
    # [[0 -- 0 --]
    #  [-- 0 -- --]
    #  [-- -- -- 0]]
    ```
    """
    data = np.zeros(CS.shape, dtype=np.intp)
    return ma.masked_array(data, mask=ma.getmaskarray(CS))
