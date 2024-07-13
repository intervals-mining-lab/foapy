import numpy as np
from numpy import nonzero


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    convert_arr = np.asanyarray(X)
    shape = convert_arr.shape

    if mode == 4:
        shape = shape + (2,)

    result = np.zeros(shape=shape, dtype=int)

    first_elements = {}
    position_elem = {}

    # Reverse the sequence if binding is to the end
    if binding == 2:
        convert_arr = convert_arr[::-1]

    for idx, elem in enumerate(convert_arr):
        if elem not in first_elements:
            first_elements[elem] = idx
        else:
            interval = idx - position_elem[elem]
            if mode == 4:
                result[idx][0] = interval
            else:
                result[idx] = interval
        position_elem[elem] = idx

    if mode == 1:
        result = result[nonzero(result)]

    if mode == 2:
        for elem in first_elements:
            result[first_elements[elem]] = first_elements[elem] + 1

    elif mode == 3:
        for elem in first_elements:
            result[first_elements[elem]] = (
                len(X) - position_elem[elem] + first_elements[elem]
            )

    elif mode == 4:
        for elem in first_elements:
            result[first_elements[elem]][0] = first_elements[elem] + 1
        for elem in position_elem:
            counter = position_elem[elem]
            result[counter][1] = len(X) - counter

        result = result.ravel()
        result = result[nonzero(result)]

    # Reverse result back if binding is to the end
    if binding == 2:
        result = result[::-1]

    return result
