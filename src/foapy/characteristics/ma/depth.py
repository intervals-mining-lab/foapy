import numpy as np

from foapy.characteristics.ma.volume import volume


def depth(intervals):
    """
    Calculation depth of sequence.
    Depth is the log2 of the volume.

    Parameters
    ----------
    X: two-dimensional array
        Source array sequence.


    Returns
    -------
    result: array.

    Examples
    --------
    """
    return np.asanyarray([np.log2(line) for line in volume(intervals)])
