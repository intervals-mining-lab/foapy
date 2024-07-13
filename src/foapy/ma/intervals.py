import numpy.ma as ma

from foapy.exceptions import InconsistentOrderException, Not1DArrayException


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the uniform
    sequences in the given input sequence

    Parameters
    ----------
    X: masked_array
        Array to get unique values.

    binding: int
        Start = 1 - Intervals are extracted from left to right.
        End = 2 – Intervals are extracted from right to left.

    mode: int
        None = 1 - Both interval from the start of the sequence
        to the first element occurrence
        and interval from the
        last element occurrence to the end of the sequence are not taken into account.

        Normal = 2 - Interval from the start of the sequence to the first occurrence of
        the element (in case of binding to the beginning) or interval from the
        last occurrence
        of the element to the end of the sequence (in case of binding to the end)
        is taken into account.

        Cycle = 3 - Interval from the start of the sequence to the first
        element occurrence
        and interval from the last element occurrence to the end of the
        sequence are summed
        into one interval (as if sequence was cyclic). Interval is
        placed either in the
        beginning of intervals array (in case of binding to the
        beginning) or in the end
        (in case of binding to the end).

        Redundant = 4 - Both interval from start of the sequence
        to the first element
        occurrence and the interval from the last element occurrence
        to the end of the
        sequence are taken into account. Their placement in results
        array is determined
        by the binding.

    Returns
    -------
    result: array or Exception.
        Exception if not d1 array or wron mask, array otherwise.

    Examples
    --------

    """

    if X.ndim > 1:  # Checking for d1 array
        raise Not1DArrayException(
            {"message": f"Incorrect array form. Expected d1 array, exists {X.ndim}"}
        )
    arr_data = ma.getdata(X)
    unique_mask_X = ma.unique(arr_data[X.mask])
    for i in X:
        if i in unique_mask_X:  # Checking for exception O(n)
            raise InconsistentOrderException(
                {"message": f"Element {i} have mask and unmasked appearance"}
            )
    first_elements = {}
    position_elem = {}
    result_hash = {}

    if binding == 1:
        for idx, i in enumerate(X):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements:  # Checking for conditions
                first_elements[i] = idx
                position_elem[i] = idx
                result_hash[i] = []
                continue
            result_hash[i].append(idx - position_elem[i])
            position_elem[i] = idx

        if mode == 2:
            for i in first_elements:
                counter = first_elements[i]
                result_hash[i].insert(0, counter + 1)

        if mode == 3:
            for key, value in first_elements.items():
                result_hash[key].insert(0, len(X) - position_elem[key] + value)

        if mode == 4:
            for i in first_elements:
                counter = first_elements[i]
                result_hash[i].insert(0, counter + 1)
            for key, value in position_elem.items():
                result_hash[key].append(len(X) - value)
        return list(result_hash.values())
    if binding == 2:
        for i in X:
            if ma.is_masked(i) is True:
                continue
            result_hash[i] = []
        for idx, i in enumerate(reversed(X)):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements:  # Checking for conditions
                first_elements[i] = idx
                position_elem[i] = idx
                continue
            result_hash[i].insert(0, idx - position_elem[i])
            position_elem[i] = idx
        if mode == 2:
            for i in first_elements:
                counter = first_elements[i]
                result_hash[i].append(counter + 1)

        if mode == 3:
            for key, value in first_elements.items():
                result_hash[key].append(len(X) - position_elem[key] + value)

        if mode == 4:
            for i in first_elements:
                counter = first_elements[i]
                result_hash[i].append(counter + 1)
            for key, value in position_elem.items():
                result_hash[key].insert(0, len(X) - value)

    return list(result_hash.values())
