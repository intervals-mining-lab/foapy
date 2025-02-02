import numpy as np


def uniformity(intervals):
    """
    Calculation uniformity of sequence.

    Uniformity is the difference between identifying_information and average remoteness.

    param name = "intervals" (sequence of intervals).

    total_elements - сombine all intervals into one array.

    """
    from foapy.characteristics import average_remoteness, identifying_information

    total_elements = np.concatenate(intervals)

    return np.array(
        identifying_information(intervals) - average_remoteness(total_elements)
    )
