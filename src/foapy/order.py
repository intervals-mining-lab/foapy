import numpy as np

from foapy.exceptions import Not1DArrayException


def order(X, return_alphabet=False):
    """
    Find array sequence  in order of their appearance

    Parameters
    ----------
    X: np.array
        Array to get unique values.

    return_alphabet: bool, optional
        If True also return array's alphabet

    Returns
    -------
    result: np.array or Exception.
        Exception if not d1 array, np.array otherwise.

    Examples
    --------

    ----1----
    >>> a = ['a', 'b', 'a', 'c', 'd']
    >>> b = order(a)
    >>> b
    [0, 1, 0, 2, 3]

    ----2----
    >>> a = ['a', 'c', 'c', 'e', 'd', 'a']
    >>> b, c = order(a, True)
    >>> b
    [0, 1, 1, 2, 3, 0]
    >>> c
    [a, c, e, d, a]

     ----3----
    >>> a = []
    >>> b = order(a)
    >>> b
    []

     ----4----
    >>> a = ["E"]
    >>> b = order(a)
    >>> b
    [0]

     ----5----
    >>> a = [1, 2, 2, 3, 4, 1]
    >>> b = order(a)
    >>> b
    [0, 1, 1, 2, 3, 0]

     ----6----
    >>> a = [[2, 2, 2], [2, 2, 2]]
    >>> b = order(a)
    >>> b
    Exception

     ----7----
    >>> a = [[[1], [3]], [[6], [9]], [[6], [3]]]
    >>> b = order(a)
    >>> b
    Exception
    """
    # ex.:
    # data = ['a', 'c', 'c', 'e', 'd', 'a']
    data = np.asanyarray(X)
    if data.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {data.ndim}"}
        )

    # Array of indices that sort elements in ascending order
    # ex.:
    #         a  a  c  c  d  e
    # perm = [0, 5, 1, 2, 4, 3]
    perm = data.argsort(kind="mergesort")

    # Create mask array to store True on positions where new value appears for the first
    # time in the sorted array to distinguish where subarray of one element ends and
    # another begins
    # ex.:
    #              a  a  c  c  d  e
    # perm      = [0, 5, 1, 2, 4, 3]
    # perm[1:]  = [   5, 1, 2, 4, 3]
    # perm[:-1] = [0, 5, 1, 2, 4   ]

    # data[perm[1:]]                    = [        'a',  'c',  'c',  'd',  'e']
    # data[perm[:-1]]                   = [        'a',  'a',   'c',  'c',  'd']
    # data[perm[1:]] != data[perm[:-1]] = [      False, True, False, True, True]
    # unique_mask                       = [True, False, True, False, True, True]
    #                                        a     a     c      c      d     e
    unique_mask = np.empty(data.shape, dtype=bool)
    # First element is always new
    unique_mask[:1] = True
    # Set true on positions where value differs from previous
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    # Create mask array to store True on positions of the data array
    # where new value appears for the first time
    # ex.:
    #                        a      a       c     c       d      e
    # unique_mask       = [True,  False,  True, False,  True,  True]
    # result_mask       = [False, False, False, False, False, False]
    # perm              = [    0,     5,     1,     2,     4,     3]
    # perm[unique_mask] = [    0,            1,            4,     3]
    # result_mask       = [True,   True, False,  True,  True, False]
    #                       a      c       c       e      d     a
    result_mask = np.zeros_like(unique_mask)
    result_mask[perm[unique_mask]] = True

    # Alphabet cardinality
    # ex.:
    #                  a      a     c     c     d     e
    # unique_mask = [True, False, True, False, True, True]
    # power       = 4
    power = np.count_nonzero(unique_mask)

    # Create inverse permutation array
    inverse_perm = np.empty(data.shape, dtype=np.intp)
    # ex.:
    #                           a  a  c  c  d  e
    # perm                   = [0, 5, 1, 2, 4, 3]
    # np.arange(ar.shape[0]) = [0, 1, 2, 3, 4, 5]
    # inverse_perm           = [0, 2, 3, 5, 4, 1]
    #                           a  c  c  e  d  a
    inverse_perm[perm] = np.arange(data.shape[0])

    # Fill tmp result array with cumulative sums of number of
    # unique values (starting from 0) to represent
    # each element as a number in resulting order.
    # Boolean cast is used to convert True to 1 and False to 0
    # ex.:
    #                                a      a     c      c     d     e
    # unique_mask                = [True, False, True, False, True, True]
    # np.cumsum(unique_mask)     = [   1,      1,   2,     2,    3,    4]
    # np.cumsum(unique_mask) - 1 = [   0,      0,   1,     1,    2,    3]
    # result                     = [   0,      0,   1,     1,    2,    3]
    result = np.cumsum(unique_mask) - 1

    # Create inverse alphabet permutation array
    # ex.:
    # power                             = 4
    # inverse_alphabet_perm             = [   0,      0,     0,     0]
    inverse_alphabet_perm = np.empty(power, dtype=np.intp)

    # ex.:
    #                                         a       a      c      c      d      e
    # result                            = [   0,      0,     1,     1,     2,     3]
    # inverse_perm                      = [   0,      2,     3,     5,     4,     1]
    # result[inverse_perm]              = [   0,      1,     1,     3,     2,     0]
    #                                         a       c      c      e      d      a
    # result_mask                       = [True,   True, False,  True,  True, False]
    # result[inverse_perm][result_mask] = [   0,      1,            3,     2       ]
    #                                         a       c             e      d
    # np.arange(power)                  = [   0,      1,     2,     3]
    # inverse_alphabet_perm             = [   0,      1,     3,     2]
    #                                         a       c      d      e
    inverse_alphabet_perm[result[inverse_perm][result_mask]] = np.arange(power)

    # Create result array replacing alphabet values with their order index
    # and reverse permutation to original order
    # ex.:
    #                                                a  c  d  e
    # inverse_alphabet_perm                       = [0, 1, 3, 2]

    #                                                a  a  c  c  d  e
    # result                                      = [0, 0, 1, 1, 2, 3]
    # inverse_alphabet_perm[result]               = [0, 0, 1, 1, 3, 2]
    # inverse_perm                                = [0, 2, 3, 5, 4, 1]
    # inverse_alphabet_perm[result][inverse_perm] = [0, 1, 1, 2, 3, 0]
    #                                                a  c  c  e  d  a
    result = inverse_alphabet_perm[result][inverse_perm]

    if return_alphabet:
        return result, data[result_mask]
    return result
