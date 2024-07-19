import numpy as np
import numpy.ma as ma

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
    if bind not in {binding.start, binding.end, 1, 2}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    # Validate mode
    if mod not in {mode.lossy, mode.normal, mode.cycle, mode.redundant, 1, 2, 3, 4}:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )

    if X.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {X.ndim}"}
        )

    arr_data = ma.getdata(X)
    unique_mask_X = ma.unique(arr_data[X.mask])
    for i in X:
        if i in unique_mask_X:  # Checking for exception O(n)
            raise InconsistentOrderException(
                {"message": f"Element {i} have mask and unmasked appearance"}
            )

    ar = np.asanyarray(X[~X.mask])  # Removing masked obejcts

    if ar.shape == (0,):
        return []

    if bind == binding.end:
        ar = ar[::-1]

    perm = ar.argsort(kind="mergesort")
    mask_shape = ar.shape
    mask = np.empty(mask_shape[0] + 1, dtype=bool)
    mask[:1] = True
    mask[1:-1] = ar[perm[1:]] != ar[perm[:-1]]
    mask[-1:] = True  # or  mask[-1] = True

    first_mask = mask[:-1]
    last_mask = mask[1:]

    intervals = np.empty(ar.shape, dtype=np.intp)
    intervals[1:] = perm[1:] - perm[:-1]

    delta = len(ar) - perm[last_mask] if mod == mode.cycle else 1
    intervals[first_mask] = perm[first_mask] + delta

    indecies = np.argwhere(ar[perm[1:]] != ar[perm[:-1]]).ravel()
    cut = indecies + 1
    result_split = np.array_split(intervals, cut)  # Split for 2d array

    if mod == mode.lossy:
        # _, indexes = np.unique(result_split, axis=0, return_index=True)
        # result = result_split[np.sort(indexes)]
        result = [i[1:] for i in result_split]

    elif mod == mode.normal:
        result = result_split
    elif mod == mode.cycle:
        result = result_split
    elif mod == mode.redundant:
        # result = np.zeros(shape=ar.shape + (2,), dtype=int)
        # result[:, 0] = intervals
        # result[last_mask, 1] = len(ar) - perm[last_mask]
        # result = result[inverse_perm]
        # result = result.ravel()
        # result = result[result != 0]

        for idx, i in enumerate(result_split):
            result_split[idx] = np.insert(i, len(i), len(ar) - perm[last_mask][idx])
        result = result_split

    if bind == binding.end:
        result = result[::-1]

    return result
