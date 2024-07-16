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

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    for index, x in np.ndenumerate(perm):
        inverse_perm[x] = index[0]

    indecies = np.argwhere(ar[perm[1:]] != ar[perm[:-1]]).ravel()

    intervals = np.empty(ar.shape, dtype=np.intp)
    intervals[1:] = perm[1:] - perm[:-1]

    match mode:
        case 1:
            intervals[0] = 0
            intervals[1:][indecies] = 0
            intervals = intervals[inverse_perm]
            result = intervals[intervals.nonzero()]
        case 2:
            intervals[0] = perm[0] + 1
            intervals[1:][indecies] = perm[1:][indecies] + 1
            result = intervals[inverse_perm]
        case 3:
            length = len(ar)
            first_index = indecies[0]
            middle_indexes = indecies[1:-1]
            last_index = indecies[-1]

            intervals[0] = perm[0] + length - perm[:-1][first_index]
            intervals[1:][middle_indexes] = (
                perm[1:][middle_indexes] + length - perm[1:-1][middle_indexes]
            )
            intervals[1:][last_index] = perm[1:][last_index] + length - perm[-1]

            result = intervals[inverse_perm]
        case 4:
            intervals[0] = perm[0] + 1
            intervals[1:][indecies] = perm[1:][indecies] + 1

            result = np.zeros(shape=ar.shape + (2,), dtype=int)
            result[:, 0] = intervals
            result[:, 1][indecies] = len(ar) - perm[:-1][indecies]
            result[-1, 1] = len(ar) - perm[-1]
            result = result[inverse_perm]
            result = result.ravel()
            result = result[result.nonzero()]

    if binding == 2:
        result = result[::-1]

    return result
