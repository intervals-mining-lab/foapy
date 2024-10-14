import numpy as np

from foapy.order import order
from foapy.intervals import intervals

def volume(X, binding, mode):
    order_seq = order(X)
    intervals_seq = intervals(order_seq, binding, mode)
    return np.prod (intervals_seq)