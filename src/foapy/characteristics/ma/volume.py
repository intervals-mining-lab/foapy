import numpy as np
import numpy.ma as ma

from foapy.ma.intervals import intervals
from foapy.ma.order import order


def volume(X, binding, mode):
    """
    Calculation volume of sequence.
    Volume is the product of the elements of the intervals of the sequence.

    Parameters
    ----------
    X: one-dimensional array ?????
        Source array sequence.
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
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [16  3  3]

    ----2----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.normal)
    >>> b
    [16 12  6]

    ----3----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.end,  mode.normal)
    >>> b
    [16 36 30]

    ----4----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.redundant)
    >>> b
    [16 36 30]

    ----5----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.cycle)
    >>> b
    [16 18 18]

    ----6----
    >>> a = ["B", "A"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [1 1]

    ----7----
    >>> a = ["B", "A", "C", "D"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [1 1 1 1]
    """
    order_seq = order(ma.masked_array(X))
    intervals_seq = intervals(order_seq, binding, mode)
    return np.asanyarray([np.prod(line) for line in intervals_seq])
