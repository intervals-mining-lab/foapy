import numpy as np


def depth(intervals):
    """
    Calculation depth of sequence.

    Depth is the log2 of the volume.

    param name = "intervals" (sequence of intervals).

    """
    from foapy.characteristics import volume

    return np.log2(volume(intervals))
