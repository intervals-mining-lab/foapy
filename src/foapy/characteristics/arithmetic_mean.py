import numpy as np


def arithmetic_mean(intervals):
    """
    Calculation arithmetic mean of sequence.

    The arithmetic mean is the sum of all intervals divided
    by the number of intervals in the sequence.

    Param name = "intervals" (sequence of intervals) .

    The variable n is the number of intervals in the sequence.

    """

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return np.sum(intervals) / n
