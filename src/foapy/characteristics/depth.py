import numpy as np

from foapy.characteristics.volume import volume


def depth(intervals):
    
    return np.log2(volume(intervals))
    