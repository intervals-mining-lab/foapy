import numpy as np

from foapy.characteristics.average_remoteness import average_remoteness
from foapy.characteristics.entropy import entropy


def uniformity(intervals):
    """
    Calculation uniformity of sequence.

    Uniformity is the difference between entropy and average remoteness.

    param name = "intervals" (sequence of intervals) .

    total_elements - сombine all intervals into one array.

    """
    total_elements = np.concatenate(intervals)

    return np.array(entropy(intervals) - average_remoteness(total_elements))
