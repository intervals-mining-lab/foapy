import numpy as np


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    ar = np.asanyarray(X)

    if ar.shape == (0,):
        return []

    if binding == 2:
        ar = ar[::-1]

    perm = ar.argsort(kind="mergesort")

    first_mask = np.empty(ar.shape, dtype=np.bool_)
    first_mask[:1] = True
    first_mask[1:] = ar[perm[1:]] != ar[perm[:-1]]

    if mode in [3, 4]:
        last_mask = np.empty(ar.shape, dtype=np.bool_)
        last_mask[-1] = True
        last_mask[:-1] = first_mask[1:]

    intervals = np.empty(ar.shape, dtype=np.intp)
    intervals[1:] = perm[1:] - perm[:-1]

    delta = len(ar) - perm[last_mask] if mode == 3 else 1
    intervals[first_mask] = perm[first_mask] + delta

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    for index, x in np.ndenumerate(perm):
        inverse_perm[x] = index[0]

    match mode:
        case 1:
            intervals[first_mask] = 0
            intervals = intervals[inverse_perm]
            result = intervals[intervals.nonzero()]
        case 2:
            result = intervals[inverse_perm]
        case 3:
            result = intervals[inverse_perm]
        case 4:
            result = np.zeros(shape=ar.shape + (2,), dtype=int)
            result[:, 0] = intervals
            result[last_mask, 1] = len(ar) - perm[last_mask]
            result = result[inverse_perm]
            result = result.ravel()
            result = result[result.nonzero()]

    if binding == 2:
        result = result[::-1]

    return result
