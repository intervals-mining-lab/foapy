import numpy as np


def geometric_mean(intervals):
    """
    Calculation geometric mean of sequence.

    The geometric mean is the root of the number of intervals in a sequence
    from the product of all intervals.

    Param name = "intervals" (sequence of intervals) .

    The variable n is the number of intervals in the sequence.

    The variable volume is the product of all intervals in the sequence.

    """
    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    volume = np.prod(intervals)

    return np.power(volume, 1 / n)
