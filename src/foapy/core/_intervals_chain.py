from typing import Optional

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.core._binding import binding as binding_cls
from foapy.core._chain_mode import chain_mode as chain_mode_cls
from foapy.core._factorize import _normalize_sequence_axis
from foapy.core._order import order as core_order


def intervals_chain(
    X: ArrayLike,
    binding: int,
    chain_mode: int,
    *,
    axis: Optional[int] = None,
) -> ndarray:
    """
    Compute the raw intervals chain from a sequence.

    The intervals chain is the n-tuple of distances between consecutive
    occurrences of the same element, with the first occurrence's distance
    measured from the sequence boundary (or cyclically). The chain values
    alone are sufficient to determine both binding direction and chain mode
    via structural mathematical properties.

    Parameters
    ----------
    X : array_like
        Input sequence. With an explicit ``axis``, each complete orthogonal
        slice indexed along that axis is one sequence element. No pre-ordering
        via :func:`foapy.order` is required.
    binding : int
        ``binding.start`` (1) — intervals extracted left-to-right.
        ``binding.end`` (2) — intervals extracted right-to-left.
    chain_mode : int
        ``chain_mode.boundary`` (1) — sequence treated as finite; boundary
        intervals are distances from sequence edges to first/last occurrence.
        ``chain_mode.cycle`` (2) — sequence treated as circular; leading and
        trailing boundary distances are combined into a single cyclic interval.
    axis : int, optional
        Sequence axis. If omitted, ``X`` must be one-dimensional. Negative
        axes follow NumPy conventions.

    Returns
    -------
    ndarray
        Plain one-dimensional ndarray of dtype ``intp`` containing one raw
        interval per sequence element in original selected-axis order. Its
        length is ``X.shape[axis]`` for an explicit axis, or ``len(X)`` for a
        legacy one-dimensional call. All values are positive integers ≥ 1 and
        no greater than the sequence-axis length.

    Raises
    ------
    Not1DArrayException
        When ``X`` is scalar, or is multidimensional without an explicit axis.
    numpy.exceptions.AxisError
        When an explicit axis is out of range.
    ValueError
        When ``binding`` is not ``binding.start`` or ``binding.end``.
        When ``chain_mode`` is not ``chain_mode.boundary`` or ``chain_mode.cycle``.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    X = ['b', 'a', 'b', 'c', 'b']
    chain = foapy.intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
    print(chain)  # [1 2 2 4 2]
    ```

    ``` py linenums="1"
    import foapy

    X = ['b', 'a', 'b', 'c', 'b']
    chain = foapy.intervals_chain(X, foapy.binding.start, foapy.chain_mode.cycle)
    print(chain)  # [1 5 2 5 2]
    ```

    ``` py linenums="1"
    import foapy

    source = []
    chain = foapy.intervals_chain(source, foapy.binding.start, foapy.chain_mode.boundary)  # noqa: E501
    print(chain)  # []
    ```

    Treat complete rows as sequence elements. The returned chain is still
    one-dimensional and can be passed directly to :func:`foapy.intervals_tuple`:

    ``` py linenums="1"
    import numpy as np
    import foapy

    source = np.array([[1, 2], [3, 4], [1, 2], [5, 6], [1, 2]])
    chain = foapy.intervals_chain(
        source,
        foapy.binding.start,
        foapy.chain_mode.boundary,
        axis=0,
    )
    print(chain)  # [1 2 2 4 2]
    ```

    Columns can be selected in the same way, including through an equivalent
    negative axis:

    ``` py linenums="1"
    import numpy as np
    import foapy

    source = np.array([[1, 3, 1, 5], [2, 4, 2, 6]])
    chain = foapy.intervals_chain(
        source,
        foapy.binding.start,
        foapy.chain_mode.boundary,
        axis=-1,
    )
    print(chain)  # [1 2 2 4]
    ```
    """
    if binding not in {binding_cls.start, binding_cls.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    if chain_mode not in {chain_mode_cls.boundary, chain_mode_cls.cycle}:
        raise ValueError(
            {
                "message": (
                    "Invalid chain_mode value. "
                    "Use chain_mode.boundary or chain_mode.cycle."
                )
            }
        )

    data = np.asanyarray(X)

    if data.ndim != 1:
        sequence_order = core_order(data, axis=axis)
        return _intervals_chain_1d(sequence_order, binding, chain_mode)

    if axis is not None:
        _normalize_sequence_axis(data, axis)

    return _intervals_chain_1d(data, binding, chain_mode)


def _intervals_chain_1d(ar: ndarray, binding: int, chain_mode: int) -> ndarray:
    """Compute an interval chain for an already validated 1-D sequence."""

    if ar.shape[0] == 0:
        return np.array([], dtype=np.intp)

    if binding == binding_cls.end:
        ar = ar[::-1]

    perm = ar.argsort(kind="mergesort")

    n = ar.shape[0]
    mask = np.empty(n + 1, dtype=bool)
    mask[:1] = True
    mask[1:-1] = ar[perm[1:]] != ar[perm[:-1]]
    mask[-1:] = True

    first_mask = mask[:-1]
    last_mask = mask[1:]

    chain = np.empty(ar.shape, dtype=np.intp)
    chain[1:] = perm[1:] - perm[:-1]

    if chain_mode == chain_mode_cls.cycle:
        delta = n - perm[last_mask]
    else:
        delta = 1

    chain[first_mask] = perm[first_mask] + delta

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(n)

    result = chain[inverse_perm]

    if binding == binding_cls.end:
        result = result[::-1]

    return result
