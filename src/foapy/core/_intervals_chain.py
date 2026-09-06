import numpy as np
from numpy import ndarray

from foapy.core._binding import binding as binding_cls
from foapy.core._chain_mode import chain_mode as chain_mode_cls
from foapy.exceptions import Not1DArrayException


def intervals_chain(X, binding: int, chain_mode: int) -> ndarray:
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
        Input sequence (strings, integers, or any comparable elements).
        Must be 1-dimensional. No pre-ordering via ``order()`` is required.
    binding : int
        ``binding.start`` (1) — intervals extracted left-to-right.
        ``binding.end`` (2) — intervals extracted right-to-left.
    chain_mode : int
        ``chain_mode.boundary`` (1) — sequence treated as finite; boundary
        intervals are distances from sequence edges to first/last occurrence.
        ``chain_mode.cycle`` (2) — sequence treated as circular; leading and
        trailing boundary distances are combined into a single cyclic interval.

    Returns
    -------
    ndarray
        Plain 1-D ndarray of dtype ``intp`` containing the raw interval chain
        in original sequence order. All values are positive integers ≥ 1 and
        ≤ ``len(X)``.

    Raises
    ------
    Not1DArrayException
        When ``X`` is not a 1-dimensional array.
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

    ar = np.asanyarray(X)

    if ar.ndim != 1:
        raise Not1DArrayException(
            {"message": (f"Incorrect array form. Expected d1 array, exists {ar.ndim}")}
        )

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
