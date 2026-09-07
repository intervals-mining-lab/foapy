from typing import Tuple, Union

import numpy as np
import numpy.ma as ma

from foapy.congenerics._alphabet import alphabet as congenerics_alphabet


def order(
    CS: ma.MaskedArray,
    return_alphabet: bool = False,
) -> Union[ma.MaskedArray, Tuple[ma.MaskedArray, np.ndarray]]:
    """
    Compute the congeneric order of each row of a congeneric decomposition.

    Per the Congeneric Order definition, every non-masked value in every row
    is 0 (the sole alphabet index of a single-symbol row) — so no per-row
    computation is needed: CS's own mask already determines the result.

    Parameters
    ----------
    CS : numpy.ma.MaskedArray, shape (m, l)
        Output of :func:`foapy.congenerics.sequences`.

    return_alphabet : bool, optional
        If True also return the row labels of CS, as computed by
        :func:`foapy.congenerics.alphabet`.

    Returns
    -------
    order : numpy.ma.MaskedArray, shape (m, l)
        Row j is masked wherever `CS[j]` is masked; non-masked positions
        hold 0.

    alphabet : numpy.ndarray, shape (m,)
        Row labels of CS. Only provided if `return_alphabet` is True.

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

    Also return the row labels of CS.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    result, alphabet = foapy.congenerics.order(CS, True)
    print(result, alphabet)
    # [[0 -- 0 --]
    #  [-- 0 -- --]
    #  [-- -- -- 0]] ['a' 'b' 'c']
    ```

    Reconstruct the congeneric decomposition (`CS`, as returned by
    :func:`foapy.congenerics.sequences`) from `order` and `alphabet`. Since
    every non-masked value in `order` is 0, row `j`'s values are simply
    `alphabet[j]` broadcast across the row, kept at the positions where
    `order` (equivalently `CS`) is non-masked.

    ``` py linenums="1"
    import numpy as np
    import numpy.ma as ma
    import foapy

    source = ['a', 'b', 'a', 'c']
    CS = foapy.congenerics.sequences(source)
    order, alphabet = foapy.congenerics.order(CS, True)

    restored = ma.masked_array(
        np.broadcast_to(alphabet[:, None], order.shape),
        mask=ma.getmaskarray(order),
    )
    print(restored)
    # [['a' -- 'a' --]
    #  [-- 'b' -- --]
    #  [-- -- -- 'c']]
    ```
    """
    data = np.zeros(CS.shape, dtype=np.intp)
    result = ma.masked_array(data, mask=ma.getmaskarray(CS))

    if return_alphabet:
        return result, congenerics_alphabet(CS)
    return result
