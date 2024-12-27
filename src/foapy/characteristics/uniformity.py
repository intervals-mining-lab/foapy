import numpy as np

from foapy.characteristics.average_remoteness import average_remoteness
from foapy.characteristics.identifying_information import identifying_information


def uniformity(intervals):
    """
    Calculation uniformity of sequence.

    Uniformity is the difference between identifying_information and average remoteness.

    param name = "intervals" (sequence of intervals) .

    total_elements - сombine all intervals into one array.

    """
    total_elements = np.concatenate(intervals)

    return np.array(
        identifying_information(intervals) - average_remoteness(total_elements)
    )
