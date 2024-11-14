import numpy as np


def arithmetic_mean(intervals_seq):

    n = len(intervals_seq)

    return np.sum(intervals_seq) / n
