import numpy as np

from foapy.characteristics.entropy import entropy


def descriptive_information(intervals):
    """
    Calculation volume of sequence.

    Descriptive information is 2 to the power of entropy.

    param name = "intervals" (sequence of intervals) .

    """
    return np.power(2, entropy(intervals))
