import numpy as np

from foapy.characteristics.volume import volume


def depth(intervals):
    """
    Calculation depth of sequence.

    Depth is the log2 of the volume.

    param name = "intervals" (sequence of intervals)

    """
    return np.log2(volume(intervals))
