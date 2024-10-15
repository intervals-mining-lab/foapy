import numpy as np

from foapy.characteristics.ma.volume import volume


def depth(intervals):
    """
    Calculation depth of sequence.
    Depth is the log2 of the volume.

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
    """
    return np.asanyarray([np.log2(line) for line in volume(intervals)])
