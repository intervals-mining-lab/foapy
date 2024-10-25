import numpy as np


def geometric_mean(intervals_seq):

    n = len(intervals_seq)

    return np.power(np.prod(intervals_seq), 1 / n)
