import numpy.ma as ma

from foapy.ma.order import order


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
        Exception if not d1 array, array otherwise.

    Examples
    --------

    """

    order_list = order(X)
    result = []
    if binding == 1 and mode == 1:  # binding Start, mode=None
        first_elements_arr = []
        for i in order_list:  # getting array sequence
            col_result = []
            for idx_col, j in enumerate(i):
                if j not in first_elements_arr and ma.is_masked(j) is False:
                    first_elements_arr.append(j)
                    counter = idx_col
                    continue
                if ma.is_masked(j) is False:
                    col_result.append(idx_col - counter)
                    counter = idx_col
            result.append(col_result)
        return result
    if binding == 2 and mode == 1:  # binding End, mode=None
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
        first_elements_arr = []
        counter = 0
        for i in order_list:  # getting array sequence
            col_result = []
            for idx_col, j in enumerate(i):
                if j not in first_elements_arr and ma.is_masked(j) is False:
                    first_elements_arr.append(j)
                    col_result.append(idx_col + 1)
                    counter = idx_col
                    continue
                if ma.is_masked(j) is False:

                    col_result.append(idx_col - counter)
                    counter = idx_col

            result.append(col_result)
        return result
    if binding == 2 and mode == 2:  # binding End, mode=Normal
        first_elements_arr = []
        counter = 0
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
        first_elements_arr = []
        counter = 0
        double_arr = ma.concatenate((order_list, order_list), axis=1)
        for i, j in enumerate(double_arr):  # getting array sequence
            col_result = []
            for idx_row in range(order_list.shape[1], len(j)):
                if ma.is_masked(j[idx_row]) is False:
                    counter = idx_row
                else:
                    continue
                for idx_col in range(idx_row - 1, -1, -1):
                    if ma.is_masked(j[idx_col]) is False:
                        col_result.append(counter - idx_col)
                        counter = idx_col
                        break

            result.append(col_result)
        return result

    if binding == 2 and mode == 3:  # binding End, mode=Cycle
        pass
    if binding == 1 and mode == 4:  # binding Start, mode=Redundant
        pass
    if binding == 2 and mode == 4:  # binding End, mode=Redundant
        pass
