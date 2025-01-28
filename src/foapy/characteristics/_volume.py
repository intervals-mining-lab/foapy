import numpy as np


def volume(intervals):
    """
    Calculation volume of sequence.

    Volume is the product of the elements of the intervals of the sequence.

    param name = "intervals" (sequence of intervals).

    """
    return np.prod(intervals)
