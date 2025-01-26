import numpy as np

import foapy.constants_intervals as constants


def intervals(X, binding, mode):
    """

    Function to extract intervals from a sequence.

    An interval is defined as the distance between consecutive occurrences
    of elements in the sequence, with boundary intervals counted as positions
    from sequence edges to first/last occurrence. The intervals are extracted

    === "binding.end"

        |         |  b |  a |  b |  c |  b |
        |:-------:|:--:|:--:|:--:|:--:|:--:|
        | b       |  2 | <- |  2 | <- |  1 |
        | a       |    |  4 | <- | <- | <- |
        | c       |    |    |    |  2 | <- |
        | result  |  2 |  4 |  2 |  2 |  1 |

    The mode parameter determines how to handle the intervals at the
    sequence boundaries:
    - normal: Include first/last boundary interval based on binding
    - cycle: Combine boundary intervals as one cyclic interval
    - redundant: Include both boundary intervals
    - lossy: Ignore boundary intervals

    Example how different modes handle intervals are extracted when binding.start

    === "mode.normal"

        |        |  b |  a |  b |  c |  b |
        |:------:|:--:|:--:|:--:|:--:|:--:|
        | b      |  1 | -> |  2 | -> |  2 |
        | a      | -> |  2 |    |    |    |
        | c      | -> | -> | -> |  4 |    |
        | result |  1 |  2 |  2 |  4 |  2 |

    === "mode.cycle"

        |        | transition |  a |  b |  c |  b |  b | transition |
        |:------:|:----------:|:--:|:--:|:--:|:--:|:--:|:----------:|
        | b      |     (1)    |  1 | -> |  2 | -> |  2 |     (1)    |
        | a      |     (2)    | -> |  5 | -> | -> | -> |     (2)    |
        | c      |     (3)    | -> | -> | -> |  5 | -> |     (3)    |
        | result |            |  1 |  5 |  2 |  5 |  2 |            |

    === "mode.lossy"

        |        |  b |  a |  b |  c |  b |
        |:------:|:--:|:--:|:--:|:--:|:--:|
        | b      |  x | -> |  2 | -> |  2 |
        | a      | -> |  x |    |    |    |
        | c      | -> | -> | -> |  x |    |
        | result |    |    |  2 |    |  2 |

    === "mode.redundant"

        |        |  a |  b |  c |  b |  b | end   |
        |:------:|:--:|:--:|:--:|:--:|:--:|:-----:|
        | b      |  1 | -> |  2 | -> |  2 | 1     |
        | a      | -> |  2 | -> | -> | -> | 4     |
        | c      | -> | -> | -> |  4 | -> | 2     |
        | result |  1 |  2 |  2 |  4 |  2 | 1 4 2 |
    # Not1DArrayException:
    # {'message': 'Incorrect array form. Expected d1 array, exists 2'}
    ```
    """

    # Validate binding
    if binding not in {constants.binding.start, constants.binding.end}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    # Validate mode
    valid_modes = [
        constants.mode.lossy,
        constants.mode.normal,
        constants.mode.cycle,
        constants.mode.redundant,
    ]
    if mode not in valid_modes:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )

    ar = np.asanyarray(X)

    if ar.shape == (0,):
        return []

    if binding == constants.binding.end:
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

    delta = len(ar) - perm[last_mask] if mode == constants.mode.cycle else 1
    intervals[first_mask] = perm[first_mask] + delta

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(ar.shape[0])

    if mode == constants.mode.lossy:
        intervals[first_mask] = 0
        intervals = intervals[inverse_perm]
        result = intervals[intervals != 0]
    elif mode == constants.mode.normal:
        result = intervals[inverse_perm]
    elif mode == constants.mode.cycle:
        result = intervals[inverse_perm]
    elif mode == constants.mode.redundant:
        result = intervals[inverse_perm]
        redundant_intervals = len(ar) - perm[last_mask]
        if binding == constants.binding.end:
            redundant_intervals = redundant_intervals[::-1]
        result = np.concatenate((result, redundant_intervals))
    if binding == constants.binding.end:
        result = result[::-1]

    return result
