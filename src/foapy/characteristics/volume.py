import numpy as np

from foapy.intervals import intervals
from foapy.order import order


def volume(X, binding, mode):
    order_seq = order(X)
    intervals_seq = intervals(order_seq, binding, mode)
    return np.prod(intervals_seq)
