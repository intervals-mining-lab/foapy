import numpy as np
from numpy import nonzero


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    ar = np.asanyarray(X)
    shape = ar.shape

    if shape == (0,):
        return []

    if mode == 4:
        shape = shape + (2,)

    result = np.zeros(shape=shape, dtype=int)

    if binding == 2:
        ar = ar[::-1]

    perm = ar.argsort(kind="mergesort")
    inverse_perm = perm.argsort(kind="mergesort")

    aux = ar[perm]

    first_mask = np.empty(ar.shape, dtype=np.bool_)
    first_mask[:1] = True
    first_mask[1:] = aux[1:] != aux[:-1]

    intervals = np.empty(ar.shape, dtype=np.intp)
    match mode:
        case 1:
            intervals[1:] = perm[1:] - perm[:-1]
            intervals[first_mask] = perm[first_mask] + 1

            result = (intervals[inverse_perm])[np.invert(first_mask[inverse_perm])]

        case 2:
            intervals[1:] = perm[1:] - perm[:-1]
            intervals[first_mask] = perm[first_mask] + 1
            result = intervals[inverse_perm]

        case 3:
            last_mask = np.empty(ar.shape, dtype=np.bool_)
            last_mask[-1] = True
            last_mask[:-1] = aux[1:] != aux[:-1]

            intervals[1:] = perm[1:] - perm[:-1]
            intervals[first_mask] = len(ar) - perm[last_mask] + perm[first_mask]
            result = intervals[inverse_perm]

        case 4:
            last_mask = np.empty(ar.shape, dtype=np.bool_)
            last_mask[-1] = True
            last_mask[:-1] = aux[1:] != aux[:-1]

            intervals[1:] = perm[1:] - perm[:-1]
            intervals[first_mask] = perm[first_mask] + 1
            result[:, 0] = intervals
            result[last_mask, 1] = len(X) - perm[last_mask]
            result = result[inverse_perm]
            result = result.ravel()
            result = result[nonzero(result)]

    if binding == 2:
        result = result[::-1]

    return result
