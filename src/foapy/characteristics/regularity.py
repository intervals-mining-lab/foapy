import numpy as np

from foapy.characteristics.descriptive_information import descriptive_information
from foapy.characteristics.geometric_mean import geometric_mean


def regularity(intervals):
    """
    Calculation regularity of sequence.

    Regularity is the geometric mean divided by descriptive information.

    param name = "intervals" (sequence of intervals) .

    total_elements - сombine all intervals into one array.

    """

    total_elements = np.concatenate(intervals)

    return np.array(geometric_mean(total_elements) / descriptive_information(intervals))
