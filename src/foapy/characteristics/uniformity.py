import numpy as np

from foapy.characteristics.average_remoteness import average_remoteness
from foapy.characteristics.entropy import entropy
from foapy.intervals import intervals
from foapy.order import order


def uniformity(X, binding, mode):
    order_X = order(X)
    intervals_X = intervals(order_X, binding, mode)

    return np.array(entropy(X, binding, mode) - average_remoteness(intervals_X))
