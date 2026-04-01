import numpy as np
from numpy import ndarray

from foapy.core._binding import binding as binding_cls
from foapy.core._tuple_mode import tuple_mode as tuple_mode_cls


def intervals_tuple(chain, tuple_mode: int) -> ndarray:
    """
    Apply a boundary handling strategy to a plain 1-D intervals chain.

    Takes a chain produced by ``intervals_chain`` and transforms it according
    to the requested ``tuple_mode``:

    - ``tuple_mode.normal``: return the chain unchanged.
    - ``tuple_mode.lossy``: remove boundary (first-/last-occurrence) intervals,
      keeping only interior intervals between repeated occurrences.
    - ``tuple_mode.redundant``: append the complementary boundary intervals
      (trailing for ``binding.start`` chains, leading for ``binding.end``
      chains), so every element contributes both its start-side and end-side
      boundary interval.

    The binding direction is inferred automatically from the chain structure
    (see :class:`foapy.binding`).

    Parameters
    ----------
    chain : array_like
        A 1-D intervals chain produced by ``intervals_chain``.
        Must be a 1-D array of positive integers.
    tuple_mode : int
        Boundary handling strategy.  Use one of the class attributes on
        :class:`foapy.core.tuple_mode`:

        ``tuple_mode.normal`` = 2 – return the chain as-is.

        ``tuple_mode.lossy`` = 1 – drop boundary intervals.

        ``tuple_mode.redundant`` = 3 – include both boundary intervals for
        every element.

    Returns
    -------
    ndarray
        1-D integer array of intervals.  Length equals ``n`` for *normal*,
        ``n - k`` for *lossy*, and ``n + k`` for *redundant*, where ``n`` is
        the chain length and ``k`` is the number of unique elements inferred
        from the chain.

    Raises
    ------
    ValueError
        When ``tuple_mode`` is not a recognised value.

    Examples
    --------

    ``` py linenums="1"
    import foapy
    from foapy.core import intervals_chain, intervals_tuple

    X = ['b', 'a', 'b', 'c', 'b']
    chain = intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
    # chain = [1, 2, 2, 4, 2]

    print(intervals_tuple(chain, foapy.tuple_mode.normal))
    # [1 2 2 4 2]

    print(intervals_tuple(chain, foapy.tuple_mode.lossy))
    # [2 2]

    print(intervals_tuple(chain, foapy.tuple_mode.redundant))
    # [1 2 2 4 2 4 2 1]
    ```
    """
    valid_modes = {
        tuple_mode_cls.lossy,
        tuple_mode_cls.normal,
        tuple_mode_cls.redundant,
    }
    if tuple_mode not in valid_modes:
        raise ValueError(
            {
                "message": "Invalid tuple_mode value. Use tuple_mode.lossy, normal, or redundant."  # noqa: E501
            }
        )

    ar = np.asanyarray(chain, dtype=np.intp)

    if ar.size == 0:
        return np.array([], dtype=np.intp)

    if tuple_mode == tuple_mode_cls.normal:
        return ar.copy()

    n = ar.size
    positions = np.arange(n, dtype=np.intp)

    # Infer binding direction to choose correct boundary detection formula.
    b = binding_cls(ar)

    if b == binding_cls.end:
        ar = ar[::-1]

    # boundary interval at position i iff ar[i] > i
    boundary_mask = ar > positions

    delta = len(boundary_mask[boundary_mask])

    if tuple_mode == tuple_mode_cls.lossy:
        delta = -delta

    result_length = n + delta

    result = np.empty(result_length, dtype=np.intp)

    if tuple_mode == tuple_mode_cls.lossy:
        result[:result_length] = ar[~boundary_mask]
    else:
        result[:n] = ar

    if tuple_mode == tuple_mode_cls.redundant:
        # Trailing intervals: n - last_pos for each unique element.
        # Last occurrences = positions not pointed to as "previous" by any other.
        non_bnd_pos = positions[~boundary_mask]
        prev_pos = non_bnd_pos - ar[~boundary_mask]
        is_prev = np.zeros(n, dtype=bool)
        is_prev[prev_pos] = True
        last_mask = ~is_prev
        trailing = n - positions[last_mask]

        # if b == binding_cls.end:
        #     trailing = trailing[::-1]

        result[n:] = trailing

    if b == binding_cls.end:
        result = result[::-1]

    return result
