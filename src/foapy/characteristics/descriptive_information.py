import numpy as np

from foapy.characteristics.entropy import entropy


def descriptive_information(X, binding, mode):

    return np.power(2, entropy(X, binding, mode))
