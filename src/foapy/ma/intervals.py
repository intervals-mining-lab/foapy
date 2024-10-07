import numpy as np
from numpy import ma

from foapy.constants_intervals import binding, mode
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

    mask = ma.getmaskarray(X)
    data = ma.getdata(X)

    power = mask.shape[0]
    if power == 0:
        return np.array([])

    if len(mask.shape) != 2:
        message = f"Incorrect array form. Expected d2 array, exists {len(mask.shape)}"
        raise Not1DArrayException({"message": message})

    length = mask.shape[1]

    if bind == binding.end:
        mask = mask[:, ::-1]
        data = data[:, ::-1]

    def preserve_previous(x, y):
        return x if y == 0 else y

    preserve_previous_ufunc = np.frompyfunc(preserve_previous, 2, 1)

    positions = np.tile(np.arange(0, length + 1), (power, 1))
    positions[:, :-1][mask] = 0
    first_indexes = np.min(
        positions[:, :-1], initial=length, axis=1, where=~mask
    ).reshape(power, 1)

    inconsistent_first_indexes = np.min(
        positions[:, :-1], initial=length - 1, axis=1, where=~mask
    ).reshape(power, 1)
    inconsistent_indeces = np.argwhere(
        ~np.all(
            np.where(
                mask, np.take_along_axis(data, inconsistent_first_indexes, 1), data
            )
            == np.take_along_axis(data, inconsistent_first_indexes, 1),
            axis=1,
        )
    ).ravel()

    if len(inconsistent_indeces) != 0:
        i = X[inconsistent_indeces[0]]
        raise InconsistentOrderException(
            {"message": f"Elements {i} have wrong appearance"}
        )

    accumulater_positions = preserve_previous_ufunc.accumulate(positions, axis=1)
    intervals = np.tile(np.arange(0, length + 1), (power, 1))
    intervals[:, 1:] = positions[:, 1:] - accumulater_positions[:, :-1]

    delta = intervals[:, -1:] if mod == mode.cycle else 1

    np.put_along_axis(
        intervals,
        first_indexes,
        np.take_along_axis(intervals, first_indexes, 1) + delta,
        1,
    )
    intervals[mask[:, 0], 0] = -1
    intervals[np.all(mask, axis=1), -1:] = 0
    intervals[intervals < 0] = 0

    if mod == mode.lossy:
        np.put_along_axis(intervals, first_indexes, 0, 1)
        result = intervals[:, :-1]
    elif mod == mode.normal:
        result = intervals[:, :-1]
    elif mod == mode.cycle:
        result = intervals[:, :-1]
    elif mod == mode.redundant:
        result = intervals

    if bind == binding.end:
        # For binding to the end, we need to reverse the result
        result = result[:, ::-1]

    size = np.count_nonzero(result, axis=1)
    result = result.ravel()
    result = result[result != 0]
    result = np.array_split(result, np.cumsum(size)[:-1])

    return result
