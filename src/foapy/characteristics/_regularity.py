import numpy as np


def regularity(intervals):
    """
    Calculation regularity of sequence.

    Regularity is the geometric mean divided by descriptive information.

    param name = "intervals" (sequence of intervals).

    total_elements - сombine all intervals into one array.

    """
    from foapy.characteristics import descriptive_information, geometric_mean

    total_elements = np.concatenate(intervals)

    return np.array(geometric_mean(total_elements) / descriptive_information(intervals))
