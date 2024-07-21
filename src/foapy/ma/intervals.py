import numpy as np

from foapy.constants_intervals import binding as binding_constant
from foapy.constants_intervals import mode as mode_constant
from foapy.exceptions import InconsistentOrderException, Not1DArrayException


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the uniform
    sequences in the given input sequence

    Parameters
    ----------
    X: masked_array
        Array to get intervals.

    binding: int
        binding.start = 1 - Intervals are extracted from left to right.
        binding.end = 2 – Intervals are extracted from right to left.

    mode: int
        mode.lossy = 1 - Both interval from the start of the sequence
        to the first element occurrence and interval from the
        last element occurrence to the end of the sequence are not taken into account.

        mode.normal = 2 - Interval from the start of the sequence to the
        first occurrence of the element or interval from the last occurrence
        of the element to the end of the sequence is taken into account.

        mode.cycle = 3 - Interval from the start of the sequence to the first
        element occurrence
        and interval from the last element occurrence to the end of the
        sequence are summed
        into one interval (as if sequence was cyclic). Interval is
        placed either in the
        beginning of intervals array (in case of binding to the
        beginning) or in the end.

        mode.redundant = 4 - Both interval from start of the sequence
        to the first element
        occurrence and the interval from the last element occurrence
        to the end of the
        sequence are taken into account. Their placement in results
        array is determined
        by the binding.

    Returns
    -------
    result: array or Exception.
        Exception if not d1 array or wrong mask, array otherwise.

    Examples
    --------

    ----1----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.start, mode.lossy)
    >>> b
    [
        [5],
        [1, 4],
        [],
        []
    ]

     ----2----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.end, mode.lossy)
    >>> b
    [
        [5],
        [1, 4],
        [],
        []
    ]

     ----3----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.start, mode.normal)
    >>> b
    [
        [1, 2, 1],
        [2, 3]
    ]

      ----4----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.end, mode.normal)
    >>> b
    [
        [2, 1, 2],
        [3, 1]
    ]

    ----5----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.start, mode.cycle)
    >>> b
    [
        [2, 2, 1],
        [2, 3]
    ]

    ----6----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.end, mode.cycle)
    >>> b
    [
        [2, 1, 2],
        [3, 2]
    ]

    ----7----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.start, mode.redunant)
    >>> b
    [
        [1, 2, 1, 2],
        [2, 3, 1]
    ]

    ----8----
    >>> a = [2, 4, 2, 2, 4]
    >>> b = intervals(X, binding.end, mode.redunant)
    >>> b
    [
        [1, 2, 1, 2],
        [2, 3, 1]
    ]

    ----9----
    >>> a = ['a', 'b', 'c', 'a', 'b', 'c', 'c', 'c', 'b', 'a', 'c', 'b', 'c']
    >>> mask = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = intervals(X, binding.end, mode.redunant)
    >>> b
    Exception

    ----10----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> mask = [[0, 0, 0], [0, 0, 0]]
    >>> masked_a = ma.masked_array(a, mask)
    >>> b = intervals(X, binding.end, mode.redunant)
    >>> b
    Exception
    """
    # Validate binding
    if binding not in {binding_constant.start, binding_constant.end, 1, 2}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    # Validate mode
    if mode not in {
        mode_constant.lossy,
        mode_constant.normal,
        mode_constant.cycle,
        mode_constant.redundant,
        1,
        2,
        3,
        4,
    }:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )
    if X.shape == (0,):
        return []

    if X.ndim != 2:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d2 array, exists {X.ndim}"}
        )

    length = X.shape[1]

    positions = np.empty(X.shape[0], dtype=object)
    intervals = np.empty(X.shape[0], dtype=object)

    for i in range(X.shape[0]):

        unique = X[i][~X[i].mask]
        unique = set(unique)
        if len(unique) > 1:
            # raise exception
            raise InconsistentOrderException(
                {"message": f"Elements {X[i]} have wrong appearance"}
            )

        ar = X[i] if binding == 1 else X[i][::-1]
        positions[i] = np.argwhere(ar != None).flatten()  # noqa: E711
    for i, _ in enumerate(positions):
        if len(_) == 0:
            intervals[i] = np.array([], dtype=int)
            continue
        tail_intervals = positions[i][1:] - positions[i][:-1]
        # ---------------------
        # redunant
        delta = 2 if mode == 4 else 1
        intevals_length = tail_intervals.shape[0] + delta

        intervals[i] = np.empty(intevals_length, dtype=int)

        # ---------------------
        # redunant
        if mode == 4:
            intervals[i][1:-1] = tail_intervals
        else:
            intervals[i][1:] = tail_intervals
        # ---------------------

        if mode == mode_constant.lossy:
            intervals[i] = intervals[i][1:]
        elif mode == mode_constant.normal:
            intervals[i][:1] = positions[i][:1] + 1
        elif mode == mode_constant.cycle:
            intervals[i][:1] = positions[i][:1] + length - positions[i][-1:]
        elif mode == mode_constant.redundant:
            intervals[i][:1] = positions[i][:1] + 1
            intervals[i][-1:] = length - positions[i][-1:]

    if binding == 2:
        for i, _ in enumerate(intervals):
            intervals[i] = intervals[i][::-1]

    return intervals
