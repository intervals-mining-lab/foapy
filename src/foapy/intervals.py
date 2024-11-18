import numpy as np

from foapy import binding, mode


def intervals(X, bind, mod):
    """
    Find a one-dimensional array of intervals in the
    given input sequence with the interval binding determined
    by the provided binding and mode flags.

    Parameters
    ----------
    X: one-dimensional array
        Array to get unique values.
    binding: int
        start = 1 - Intervals are extracted from left to right.
        end = 2 – Intervals are extracted from right to left.
    mode: int
        lossy = 1 - Both interval from the start of the sequence
        to the first element occurrence and interval from the
        last element occurrence to the end of the sequence
        are not taken into account.

        normal = 2 - Interval from the start of the sequence to
        the first occurrence of the element
        (in case of binding to the beginning)
        or interval from the last occurrence of the element to
        the end of the sequence
        (in case of binding to the end) is taken into account.

        cycle = 3 - Interval from the start of the sequence to
        the first element occurrence
        and interval from the last element occurrence to the
        end of the sequence are summed
        into one interval (as if sequence was cyclic).
        Interval is placed either in the beginning of
        intervals array (in case of binding to the beginning)
        or in the end (in case of binding to the end).

        redundant = 4 - Both interval from start of the sequence
        to the first element occurrence and the interval from
        the last element occurrence to the end of the
        sequence are taken into account. Their placement in results
        array is determined
        by the binding.
    Returns
    -------
    result: array or error.
        An error indicating that the binding or mode does not exist,
        otherwise the array.
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

    ar = np.asanyarray(X)

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

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(ar.shape[0])

    if mod == mode.lossy:
        intervals[first_mask] = 0
        intervals = intervals[inverse_perm]
        result = intervals[intervals != 0]
    elif mod == mode.normal:
        result = intervals[inverse_perm]
    elif mod == mode.cycle:
        result = intervals[inverse_perm]
    elif mod == mode.redundant:
        result = np.zeros(shape=ar.shape + (2,), dtype=int)
        result[:, 0] = intervals
        result[last_mask, 1] = len(ar) - perm[last_mask]
        result = result[inverse_perm]
        result = result.ravel()
        result = result[result != 0]

    if bind == binding.end:
        result = result[::-1]

    return result
