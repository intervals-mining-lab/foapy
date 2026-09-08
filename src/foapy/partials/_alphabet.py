from typing import Optional

import numpy as np
from numpy.typing import ArrayLike

from foapy.partials._factorize import stable_partial_factorize


def alphabet(X: ArrayLike, *, axis: Optional[int] = None) -> np.ndarray:
    """
    Extract the alphabet of a dense or partial sequence.

    Unique present elements are returned in first-appearance order. With an
    explicit ``axis``, each complete orthogonal slice is one element. A slice
    must be wholly present or wholly masked; wholly masked slices are gaps and
    are excluded.

    Parameters
    ----------
    X : array_like or numpy.ma.MaskedArray
        Sequence (plain or masked). If ``axis`` is omitted it must be 1-D.
    axis : int, optional
        Sequence axis. Negative axes follow NumPy conventions. The returned
        alphabet retains this axis in the same position.

    Returns
    -------
    alphabet : numpy.ndarray
        Plain array of unique non-gap elements in first-appearance order. For
        an explicit axis, the input rank and all orthogonal dimensions are
        preserved while the selected axis has alphabet length.

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
    Extract an alphabet from an ordinary sequence:

    ``` py linenums="1"
    import foapy

    source = ['a', 'c', 'c', 'e', 'd', 'a']
    result = foapy.partials.alphabet(source)
    print(result)
    # ['a' 'c' 'e' 'd']
    ```

    Masked scalar positions are excluded:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(['a', 'x', 'b', 'a'], mask=[0, 1, 0, 0])
    result = foapy.partials.alphabet(source)
    print(result)
    # ['a' 'b']
    ```

    Fully masked rows are excluded when rows are selected as elements:

    ``` py linenums="1"
    import numpy.ma as ma
    import foapy

    source = ma.masked_array(
        [[1, 2], [9, 9], [3, 4], [1, 2]],
        mask=[[0, 0], [1, 1], [0, 0], [0, 0]],
    )
    result = foapy.partials.alphabet(source, axis=0)
    print(result)
    # [[1 2]
    #  [3 4]]
    ```

    A plain or fully unmasked multidimensional input produces the same
    alphabet as :func:`foapy.core.alphabet` for the same axis.
    """
    _, result = stable_partial_factorize(X, axis=axis)
    return result
