import numpy as np


def descriptive_information(intervals):
    """
    Calculation volume of sequence.

    Descriptive information is 2 to the power of identifying_information.

    param name = "intervals" (sequence of intervals).

    """
    from foapy.characteristics import identifying_information

    return np.power(2, identifying_information(intervals))
