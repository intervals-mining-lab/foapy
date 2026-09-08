from typing import Optional, Tuple, Union

import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from foapy.partials._factorize import stable_partial_factorize


def order(
    X: ArrayLike,
    return_alphabet: bool = False,
    *,
    axis: Optional[int] = None,
) -> Union[ma.MaskedArray, Tuple[ma.MaskedArray, np.ndarray]]:
    """
    Map a dense or partial sequence to its one-dimensional order.

    With an explicit ``axis``, each complete orthogonal slice is one element.
    A slice must be wholly present or wholly masked. Wholly masked slices are
    excluded from the alphabet and remain masked in the order. Plain sequences
    are treated as fully unmasked.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        Sequence (plain or masked). If ``axis`` is omitted it must be 1-D.
    return_alphabet : bool, optional
        If True, also return the alphabet of present unique elements.
    axis : int, optional
        Sequence axis. Negative axes follow NumPy conventions. The returned
        alphabet retains this axis in the same position.

    Returns
    -------
    result : numpy.ma.MaskedArray, shape (n,), dtype numpy.intp
        One-dimensional order with length ``X.shape[axis]`` for an explicit
        axis, or ``len(X)`` otherwise. Present positions hold first-appearance
        alphabet indices; whole-slice gaps remain masked.
    alphabet : numpy.ndarray
        Only returned when ``return_alphabet=True``. Plain array of unique
        present elements. For an explicit axis it retains the input rank and
        selected axis placement.

    Raises
    ------
    Not1DArrayException
        When ``X`` is scalar, or is multidimensional without an explicit axis.
    ValueError
        When a slice along an explicit axis is only partially masked.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.

    Examples
    --------
    Preserve gaps in a scalar sequence:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(
        ['a', 'x', 'b', 'a'], mask=[False, True, False, False]
    )
    result, alphabet = foapy.partials.order(source, return_alphabet=True)
    print(result, alphabet)
    # [0 -- 1 0] ['a' 'b']
    ```

    Factorize complete rows while preserving a wholly masked row as a gap:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(
        [[1, 2], [9, 9], [3, 4], [1, 2]],
        mask=[[0, 0], [1, 1], [0, 0], [0, 0]],
    )
    result, alphabet = foapy.partials.order(
        source, return_alphabet=True, axis=0
    )
    print(result)
    # [0 -- 1 0]
    print(alphabet)
    # [[1 2]
    #  [3 4]]
    ```

    Reconstruct the observed columns and broadcast the order mask:

    ``` py linenums="1"
    import numpy as np
    import numpy.ma as ma

    restored_data = np.take(alphabet, result.filled(0), axis=0)
    restored_mask = np.broadcast_to(result.mask[:, None], source.shape)
    restored = ma.masked_array(restored_data, mask=restored_mask)
    print(ma.allequal(restored, source))
    # True
    ```

    Values stored underneath gap masks are intentionally not part of the
    partial sequence. Plain or fully unmasked inputs have the same alphabet
    and non-masked order values as their :mod:`foapy.core` counterparts.
    """
    result, alphabet = stable_partial_factorize(X, axis=axis)

    if return_alphabet:
        return result, alphabet
    return result
