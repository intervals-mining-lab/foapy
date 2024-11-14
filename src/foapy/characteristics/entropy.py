import numpy as np

from foapy.intervals import intervals as intervals_1
from foapy.ma.intervals import intervals
from foapy.ma.order import order
from foapy.order import order as order_1


def entropy(X, binding, mode):
    order_X = order(X)
    order_X_1 = order_1(X)
    intervals_X_1 = intervals_1(order_X_1, binding, mode)
    intervals_X = intervals(order_X, binding, mode)
    res = []
    for i in intervals_X:
        res.append(len(i) / len(intervals_X_1) * np.log2(np.sum(i) / len(i)))

    return np.sum(np.asanyarray(res))
