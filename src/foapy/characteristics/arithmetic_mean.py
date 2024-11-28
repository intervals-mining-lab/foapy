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

    return np.sum(intervals) / n
