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
    # ex.:
    # ar = ['a', 'c', 'c', 'e', 'd', 'a']
    ar = np.asanyarray(X)

    if ar.shape == (0,):
        return []

    if bind == binding.end:
        # For binding to the end, we need to reverse the array
        # ar = ['a', 'd', 'e', 'c', 'c', 'a']
        ar = ar[::-1]

    # Sort data positions
    # ex.:
    #         a  a  c  c  d  e
    # perm = [0, 5, 1, 2, 4, 3]
    perm = ar.argsort(kind="mergesort")

    # Create tmp mask array to store True on positions where appears new value.
    # Create shape length +1 of source,
    # because we want to use the array for all binding modes.
    # ex.:
    # Create tmp mask array to store True on positions where appears new value
    # ex.:
    #              a  a  c  c  d  e
    # perm      = [0, 5, 1, 2, 4, 3]
    # perm[1:]  = [   5, 1, 2, 4, 3]
    # perm[:-1] = [0, 5, 1, 2, 4   ]

    # data[perm[1:]]                    = [        'a',  'c',   'c',  'd',  'e'      ]
    # data[perm[:-1]]                   = [        'a',  'a',   'c',  'c',  'd'      ]
    # data[perm[1:]] != data[perm[:-1]] = [      False, True, False, True, True      ]
    # unique_mask                       = [True, False, True, False, True, True, True]
    # First appears                          a     a     c      c      d     e
    # Last appears                                 a     a      c      c     d     e

    mask_shape = ar.shape
    mask = np.empty(mask_shape[0] + 1, dtype=bool)
    mask[:1] = True
    mask[1:-1] = ar[perm[1:]] != ar[perm[:-1]]
    mask[-1:] = True  # or  mask[-1] = True

    # Save masks first and last appears of elements
    # ex.:
    #
    # unique_mask = [True, False, True, False, True, True, True]
    # first_mask  = [True, False, True, False, True, True      ]
    #                  a     a     c      c      d     e
    # last_mask   = [      False, True, False, True, True, True]
    #                        a     a     c      c      d     e
    first_mask = mask[:-1]
    last_mask = mask[1:]

    # Create tmp array to count intervals
    intervals = np.empty(ar.shape, dtype=np.intp)

    # Count intervals between elements.
    # Intervals of first elements appears would be wrong on that stage.
    # We will fix that later.
    # ex.:
    #                         a  a   c  c  d   e
    # perm                 = [0, 5,  1, 2, 4,  3]
    # perm[1:]             = [   5,  1, 2, 4,  3]
    # perm[:-1]            = [   0,  5, 1, 2,  4]
    # perm[1:] - perm[:-1] = [   5, -4, 1, 2, -1]
    # intervals            = [0, 5, -4, 1, 2, -1]
    #                         ^      ^         ^ - wrong intervals
    intervals[1:] = perm[1:] - perm[:-1]

    # Fix first and last intervals
    # For any mode except cycle delta would be 1
    # For cycle mode delta would be an array

    # ex.:
    # len(ar)                   = 6
    #                                  a     a      c     c     d     e
    # perm                      = [    0,    5,     1,    2,    4,    3]
    # last_mask                 = [False, True, False, True, True, True]
    # perm[last_mask]           = [          5,           2,    4,    3]
    # len(ar) - perm[last_mask] = [          1,           4,    2,    3]
    # delta                     = [          1,           4,    2,    3]
    #                                        a            c     d     e
    delta = len(ar) - perm[last_mask] if mod == mode.cycle else 1

    # ex.:
    #                                  a     a      c     c     d     e
    # perm                      = [    0,    5,     1,    2,    4,    3]
    # first_mask                = [True, False, True, False, True, True]
    # perm[first_mask]          = [    0,           1,           4,    3]
    #                                  a            c            d     e
    # For all modes except cycle
    #                                 a      a     c      c     d     e
    # intervals                 = [   0,     5,   -4,     1,    2,   -1]
    # perm[first_mask] + delta  = [   1,           2,           5,    4]
    # first_mask                = [True, False, True, False, True, True]
    # intervals                 = [   1,     5,    2,     1,    5,    4]
    #                                 a      a     c      c     d     e

    # For cycle mode
    #                                 a      a     c      c     d     e
    # intervals                 = [   0,      5,  -4,     1,    2,   -1]
    # first_mask                = [True, False, True, False, True, True]
    # perm[first_mask]          = [   0,           1,           4,    3]
    # delta                     = [   1,           4,           2,    3]
    # perm[first_mask] + delta  = [   1,           5,           6,    6]
    # intervals                 = [   1,     5,    5,     1,    6,    6]
    #                                 a      a     c      c     d     e
    intervals[first_mask] = perm[first_mask] + delta

    # Create inverse permutation array
    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    # ex.:
    #                           a  a  c  c  d  e
    # perm                   = [0, 5, 1, 2, 4, 3]
    # np.arange(ar.shape[0]) = [0, 1, 2, 3, 4, 5]
    # inverse_perm           = [0, 2, 3, 5, 4, 1]
    #                           a  c  c  e  d  a
    inverse_perm[perm] = np.arange(ar.shape[0])

    # Create result array depending on mode
    if mod == mode.lossy:
        # For lossy mode we ignore intervals for a first appearance of the element
        # ex.:
        #                                 a      a     c      c     d     e
        # intervals                 = [   1,     5,    5,     1,    6,    6]
        # first_mask                = [True, False, True, False, True, True]
        # intervals                 = [   0,     5,    0,     1,    0,    0]
        #                                 a      a     c      c     d     e
        intervals[first_mask] = 0

        # Permute intervals array to the original order
        # ex.:
        #                              a  a  c  c  d  e
        # intervals                 = [0, 5, 0, 1, 0, 0]
        # inverse_perm              = [0, 2, 3, 5, 4, 1]
        # intervals                 = [0, 0, 1, 0, 0, 5]
        #                              a  c  c  e  d  a
        intervals = intervals[inverse_perm]

        # Remove zeros from the array
        # ex.:
        #                              a  c  c  e  d  a
        # intervals                 = [0, 0, 1, 0, 0, 5]
        # intervals[intervals != 0] = [      1,       5]
        # result                    = [      1,       5]
        #                                    c        a
        result = intervals[intervals != 0]
    elif mod == mode.normal:
        # For normal mode we permute intervals array to the original order
        # ex.:
        #                            a  a  c  c  d  e
        # intervals               = [1, 5, 2, 1, 5, 4]
        # inverse_perm            = [0, 2, 3, 5, 4, 1]
        # intervals[inverse_perm] = [1, 2, 1, 4, 5, 5]
        #                            a  c  c  e  d  a
        # result                  = [1, 2, 1, 4, 5, 5]
        result = intervals[inverse_perm]
    elif mod == mode.cycle:
        # For cycle mode we permute intervals array to the original order
        # ex.:
        #                            a  a  c  c  d  e
        # intervals               = [1, 5, 5, 1, 6, 6]
        # inverse_perm            = [0, 2, 3, 5, 4, 1]
        # intervals[inverse_perm] = [1, 2, 1, 4, 5, 5]
        #                            a  c  c  e  d  a
        # result                  = [1, 5, 1, 6, 5, 5]
        result = intervals[inverse_perm]
    elif mod == mode.redundant:
        # For redundant mode we need to count intervals for the first and last
        # appearance of an element

        # ex.:
        #                            a  a  c  c  d  e
        # intervals               = [1, 5, 2, 1, 5, 4]
        # inverse_perm            = [0, 2, 3, 5, 4, 1]
        # intervals[inverse_perm] = [1, 2, 1, 4, 5, 5]
        #                            a  c  c  e  d  a
        # result                  = [1, 2, 1, 4, 5, 5]

        # Create 2-dimensional array size of (2, len(ar))
        # Zero row is for intervals the first appearance of the element and intervals
        # for intermediate appearances
        # First row will store intervals for the last appearance of the element
        result = np.zeros(shape=ar.shape + (2,), dtype=int)

        # ex.:
        #                a  a  c  c  d  e
        # intervals =   [1, 5, 2, 1, 5, 4]
        # result    = [
        #               [1, 5, 2, 1, 5, 4]
        #               [0, 0, 0, 0, 0, 0]
        #             ]
        result[:, 0] = intervals

        # Set intervals for the last appearance of the element to the first row

        # ex.:
        #                                  a     a      c     c     d     e
        # perm                      = [    0,    5,     1,    2,    4,    3]
        # last_mask                 = [False, True, False, True, True, True]
        # perm[last_mask]           = [          5,           2,    4,    3]
        # len(ar) - perm[last_mask] = [          1,           4,    2,    3]
        # result                    = [
        #                               [   1,    5,    2,    1,    5,    4]
        #                               [   0,    1,    0,    4,    2,    3]
        #                             ]
        result[last_mask, 1] = len(ar) - perm[last_mask]

        # Permute intervals array to the original order
        # ex.:
        #                           a  a  c  c  d  e
        # result               = [
        #                          [1, 5, 2, 1, 5, 4]
        #                          [0, 1, 0, 4, 2, 3]
        #                        ]
        # inverse_perm         =   [0, 2, 3, 5, 4, 1]
        # result[inverse_perm] = [
        #                          [1, 2, 1, 4, 5, 5]
        #                          [0, 0, 4, 3, 2, 1]
        #                        ]
        #                           a  c  c  e  d  a
        result = result[inverse_perm]

        # Flatten result array
        # ex.:
        #                           a  c  c  e  d  a
        # result[inverse_perm] = [
        #                          [1, 2, 1, 4, 5, 5]
        #                          [0, 0, 4, 3, 2, 1]
        #                        ]
        # result.ravel()       = [ 1, 0, 2, 0, 1, 4, 4, 3, 5, 2, 5, 1]
        #                        |  a  |  c  |  c  |  e  |  d  |  a  |
        result = result.ravel()

        # Exclude zeros from the result
        # result               = [ 1, 0, 2, 0, 1, 4, 4, 3, 5, 2, 5, 1]
        #                        |  a  |  c  |  c  |  e  |  d  |  a  |

        # result[result != 0] = [ 1, 2, 1, 4, 4, 3, 5, 2, 5, 1]
        #                       |a |c |  c  |  e  |  d  |  a  |
        result = result[result != 0]

    if bind == binding.end:
        # For binding to the end, we need to reverse the result
        result = result[::-1]

    return result
