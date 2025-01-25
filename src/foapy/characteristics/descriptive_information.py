import numpy as np

from foapy.characteristics.identifying_information import identifying_information


def descriptive_information(intervals):
    """
    Calculation volume of sequence.

    Descriptive information is 2 to the power of identifying_information.

    param name = "intervals" (sequence of intervals).

    """
    return np.power(2, identifying_information(intervals))
