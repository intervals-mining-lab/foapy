import numpy as np
from numpy import ma

from foapy import binding, mode
from foapy.exceptions import InconsistentOrderException, Not1DArrayException


def intervals(X, bind, mod):
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
    if bind not in {binding.start, binding.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    # Validate mode
    if mod not in {mode.lossy, mode.normal, mode.cycle, mode.redundant}:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )
    # ex.:
    # ar = ['a', 'c', 'c', 'e', 'd', 'a']

    power = X.shape[0]
    if power == 0:
        return np.array([])

    if len(X.shape) != 2:
        message = f"Incorrect array form. Expected d2 array, exists {len(X.shape)}"
        raise Not1DArrayException({"message": message})

    length = X.shape[1]

    mask = ma.getmaskarray(X)

    verify_data = X[~mask]
    verify_positions = np.transpose(np.argwhere(~mask))
    verify = np.empty(verify_data.shape[0], dtype=bool)
    verify[:1] = False
    verify[1:] = np.logical_xor(
        verify_positions[0, 1:] != verify_positions[0, :-1],
        verify_data[1:] != verify_data[:-1],
    )

    if not np.all(~verify):
        failed_indexes = verify_positions[0, verify]
        i = X[failed_indexes[0]]
        raise InconsistentOrderException(
            {"message": f"Elements {i} have wrong appearance"}
        )

    extended_mask = np.empty((power, length + 1), dtype=bool)
    if bind == binding.end:
        extended_mask[:, :-1] = ~mask[::-1, ::-1]
    else:
        extended_mask[:, :-1] = ~mask
    extended_mask[:, -1] = np.any(extended_mask[:, :-1], axis=1)

    positions = np.transpose(np.argwhere(extended_mask))

    border_indexes = np.empty(positions.shape[1] + 1, dtype=bool)
    border_indexes[:1] = True
    border_indexes[1:-1] = positions[0, 1:] != positions[0, :-1]
    border_indexes[-1:] = True

    first_indexes = np.argwhere(border_indexes[:-1]).ravel()
    last_indexes = np.argwhere(border_indexes[1:]).ravel()

    indecies = np.zeros(positions.shape[1], dtype=int)
    indecies[1:] = positions[1, 1:] - positions[1, :-1]
    delta = indecies[last_indexes] if mod == mode.cycle else 1
    indecies[first_indexes] = positions[1][first_indexes] + delta

    split_boarders = np.zeros(power * 2, dtype=int)

    if mod == mode.lossy:
        split_boarders[positions[0][last_indexes[:1]] * 2] = first_indexes[:1] + 1
        split_boarders[positions[0][last_indexes[1:]] * 2] = (
            np.fmax(last_indexes[:-1], first_indexes[1:]) + 1
        )
        split_boarders[positions[0][last_indexes] * 2 + 1] = last_indexes
    elif mod == mode.normal:
        split_boarders[positions[0][last_indexes[:1]] * 2] = 0
        split_boarders[positions[0][last_indexes[1:]] * 2] = last_indexes[:-1] + 1
        split_boarders[positions[0][last_indexes] * 2 + 1] = last_indexes
    elif mod == mode.cycle:
        split_boarders[positions[0][last_indexes[:1]] * 2] = 0
        split_boarders[positions[0][last_indexes[1:]] * 2] = last_indexes[:-1] + 1
        split_boarders[positions[0][last_indexes] * 2 + 1] = last_indexes
    elif mod == mode.redundant:
        split_boarders[positions[0][last_indexes[:1]] * 2] = 0
        split_boarders[positions[0][last_indexes[1:]] * 2] = 0
        split_boarders[positions[0][last_indexes] * 2 + 1] = last_indexes + 1

    preserve_previous = np.frompyfunc(lambda x, y: x if y == 0 else y, 2, 1)
    split_boarders = preserve_previous.accumulate(split_boarders)
    if bind == binding.end:
        split_boarders[:-1] = np.diff(split_boarders)
        split_boarders[-1:] = len(indecies) - split_boarders[-1]
        split_boarders = np.cumsum(split_boarders[::-1])
        indecies = indecies[::-1]

    indecies = np.array_split(indecies, split_boarders)
    return indecies[1:-1:2]
