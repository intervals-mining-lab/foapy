import numpy.ma as ma

from foapy.ma.order import order
from foapy.order import order as count_occurrences


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
        Exception if not d1 array or wro, array otherwise.

    Examples
    --------

    """

    result = []
    order_list = order(X)
    first_elements_arr = {}
    position_elem = {}
    result_hash = {}
    if binding == 1 and mode == 1:  # binding Start, mode=None
        for idx, i in enumerate(X):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements_arr:  # Checking for conditions
                first_elements_arr[i] = idx
                position_elem[i] = idx
                result_hash[i] = []
                continue
            result_hash[i].append(idx - position_elem[i])
            position_elem[i] = idx

        result = list(result_hash.values())
        return result
    if binding == 2 and mode == 1:  # binding End, mode=None
        # invert_arr = X[::-1]
        # return intervals(invert_arr,1,1)
        first_elements_arr = []
        for i in order_list:
            col_result = []
            for idx_col, j in enumerate(i[::-1]):
                if j not in first_elements_arr and ma.is_masked(j) is False:
                    first_elements_arr.append(j)
                    counter = idx_col
                    continue
                if ma.is_masked(j) is False:
                    col_result.insert(0, idx_col - counter)
                    counter = idx_col
            result.append(col_result)
        return result
    if binding == 1 and mode == 2:  # binding Start, mode=Normal
        for idx, i in enumerate(X):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements_arr:  # Checking for conditions
                first_elements_arr[i] = idx
                position_elem[i] = idx
                result_hash[i] = []
                result_hash[i].append(idx + 1)
                continue
            result_hash[i].append(idx - position_elem[i])
            position_elem[i] = idx

        result = list(result_hash.values())
        return result
    if binding == 2 and mode == 2:  # binding End, mode=Normal
        # invert_arr = X[::-1]
        # return intervals(invert_arr,1,2)
        first_elements_arr = []
        for i in order_list:  # getting array sequence
            col_result = []
            for idx_col, j in enumerate(i[::-1]):
                if j not in first_elements_arr and ma.is_masked(j) is False:
                    first_elements_arr.append(j)
                    col_result.append(idx_col + 1)
                    counter = idx_col
                    continue
                if ma.is_masked(j) is False:

                    col_result.insert(0, idx_col - counter)
                    counter = idx_col

            result.append(col_result)
        return result
    if binding == 1 and mode == 3:  # binding Start, mode=Cycle
        for idx, i in enumerate(X):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements_arr:  # Checking for conditions
                first_elements_arr[i] = idx
                position_elem[i] = idx
                result_hash[i] = []
                continue

            result_hash[i].append(idx - position_elem[i])
            position_elem[i] = idx

        for key, value in first_elements_arr.items():
            result_hash[key].insert(0, len(X) - position_elem[key] + value)

        result = list(result_hash.values())
        return result

    if binding == 2 and mode == 3:  # binding End, mode=Cycle
        # invert_arr = X[::-1]
        # return intervals(invert_arr,1,3)
        double_arr = ma.concatenate((order_list, order_list), axis=1)
        for i, j in enumerate(double_arr):  # getting array sequence
            col_result = []
            for idx_row in range(0, order_list.shape[1]):
                if ma.is_masked(j[idx_row]) is False:
                    counter = idx_row
                else:
                    continue
                for idx_col in range(idx_row + 1, len(j) + 1, 1):
                    if ma.is_masked(j[idx_col]) is False:
                        col_result.append(idx_col - counter)
                        counter = idx_col
                        break

            result.append(col_result)
        return result
    if binding == 1 and mode == 4:  # binding Start, mode=Redundant
        for idx, i in enumerate(X):  # getting array sequence
            if ma.is_masked(i) is True:
                continue
            if i not in first_elements_arr:  # Checking for conditions
                first_elements_arr[i] = idx
                position_elem[i] = idx
                result_hash[i] = []
                result_hash[i].append(idx + 1)
                continue
            result_hash[i].append(idx - position_elem[i])
            position_elem[i] = idx
        for key, value in position_elem.items():
            result_hash[key].append(len(X) - value)

        result = list(result_hash.values())
        return result
    if binding == 2 and mode == 4:  # binding End, mode=Redundant
        # invert_arr = X[::-1]
        # return intervals(invert_arr,1,4)
        ndict = {}
        for i in count_occurrences(X.compressed()):
            if i not in ndict:
                ndict[i] = 1
            else:
                ndict[i] += 1
        first_elements_arr = []
        for i in order_list:  # getting array sequence
            col_result = []
            for idx_col, j in enumerate(i[::-1]):

                if j not in first_elements_arr and ma.is_masked(j) is False:
                    if ndict[j] == 1:
                        col_result.insert(0, len(X) - idx_col)
                        col_result.insert(1, idx_col + 1)
                        counter = idx_col
                        first_elements_arr.append(j)
                        continue

                    first_elements_arr.append(j)
                    col_result.append(idx_col + 1)
                    counter = idx_col
                    ndict[j] = ndict[j] - 1
                    continue
                if ma.is_masked(j) is False:
                    if ndict[j] == 1:

                        col_result.insert(0, len(X) - idx_col)
                        col_result.insert(1, idx_col - counter)
                        counter = idx_col
                        continue
                    col_result.insert(0, idx_col - counter)
                    counter = idx_col
                    ndict[j] = ndict[j] - 1

            result.append(col_result)
        return result
