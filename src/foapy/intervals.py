import numpy as np

import foapy.intervals_constants as constants


def intervals(X, binding, mode):
    """
    Function to extract intervals from a sequence.

    An interval is defined as the distance between consecutive occurrences
    of elements in the sequence, with boundary intervals counted as positions
    from sequence edges to first/last occurrence. The intervals are extracted
    based on the specified binding direction (start or end) and mode (lossy, normal,
    cycle, or redundant).

    The intervals can be extracted from left to right (binding.start)
    or right to left (binding.end).

    Example how intervals are extracted when

    === "binding.start"

        |         |  b |  a |  b |  c | b |
        |:-------:|:--:|:--:|:--:|:--:|:-:|
        | b       |  1 | -> |  2 | -> | 2 |
        | a       | -> |  2 |    |    |   |
        | c       | -> | -> | -> |  4 |   |
        | result  |  1 |  2 |  2 |  4 | 2 |

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


    Parameters
    ----------
    X: array_like
        Array to exctact an intervals from. Must be a 1-dimensional array.
    binding: int
        start = 1 - Intervals are extracted from left to right.
        end = 2 – Intervals are extracted from right to left.
    mode: int
        Mode handling the intervals at the sequence boundaries:

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
    order : ndarray
        Intervals extracted from the sequence

    Raises
    -------
    Not1DArrayException
        When X parameter is not a 1-dimensional array

    ValueError
        When binding or mode is not valid

    Examples
    --------

    Get intervals from a sequence binding to start and mode.normal.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    print(intervals)
    # [1 2 2 3 2 5]
    ```

    Get intervals from a emprty sequence.
    ``` py linenums="1"
    import foapy

    source = []
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    print(intervals)
    # []
    ```

    Getting an intervals of an array with more than 1 dimension is not allowed.
    ``` py linenums="1"
    import foapy
    source = [[1, 2], [3, 4]]
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    # Not1DArrayException:
    # {'message': 'Incorrect array form. Expected d1 array, exists 2'}
    ```
    """  # noqa: E501

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
