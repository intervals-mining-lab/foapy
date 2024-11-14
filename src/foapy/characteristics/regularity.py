import numpy as np

from foapy.characteristics.descriptive_information import descriptive_information
from foapy.characteristics.geometric_mean import geometric_mean
from foapy.intervals import intervals
from foapy.order import order


def regularity(X, binding, mode):
    order_X = order(X)
    intervals_X = intervals(order_X, binding, mode)

    return np.array(
        geometric_mean(intervals_X) / descriptive_information(X, binding, mode)
    )
