import numpy as np


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    order_list = X
    result = []
    print(order_list)
    first_elements_arr = []
    counter = 0
    row = []
    if binding == 1 and mode == 1:  # binding Start, mode=None
        first_elements_arr = {}
        position_elem = {}

        for idx, i in enumerate(X):
            if i not in first_elements_arr:
                first_elements_arr[i] = idx
                position_elem[i] = idx
                continue
            else:
                interval = idx - position_elem[i]
                result.append(interval)
                position_elem[i] = idx

    elif binding == 2 and mode == 1:  # binding End, mode=None
        col = len(order_list) - 1
        temp_result = []
        for idx_row in range(len(order_list) - 1, -1, -1):
            i = order_list[idx_row]
            for j in range(col, -1, -1):
                if i == order_list[j] and idx_row in row:
                    temp_result.append(counter - j)
                    counter = j
                    break
                if i == order_list[j] and idx_row not in row:
                    counter = j
                    first_elements_arr.append(order_list[j])
                    row.append(idx_row)
            col -= 1

        result.extend(temp_result[::-1])  # Adding temporary results in reverse order

    elif binding == 1 and mode == 2:  # binding Start, mode=Normal
        first_occurrences = {}

        for idx, elem in enumerate(order_list):
            if elem not in first_occurrences:
                first_occurrences[elem] = idx
                interval = idx + 1
            else:
                interval = idx - first_occurrences[elem]

            result.append(interval)
            first_occurrences[elem] = idx

    elif binding == 2 and mode == 2:  # binding End, mode=Normal
        last_occurrences = {}
        col = len(order_list)

        for idx in range(col - 1, -1, -1):
            elem = order_list[idx]
            if elem not in last_occurrences:
                last_occurrences[elem] = idx
                interval = col - idx
            else:
                interval = last_occurrences[elem] - idx

            result.append(interval)
            last_occurrences[elem] = idx

        result.reverse()

    elif binding == 1 and mode == 3:  # binding Start, mode=Cycle
        counter = 0
        double_arr = np.concatenate((order_list, order_list))
        for idx_row in range(len(order_list), len(double_arr)):
            counter = idx_row
            word = double_arr[idx_row]

            for idx_col in range(idx_row - 1, -1, -1):
                if word == double_arr[idx_col]:

                    result.append(counter - idx_col)
                    counter = idx_col
                    break

    elif binding == 2 and mode == 3:  # binding End, mode=Cycle
        counter = 0
        double_arr = np.concatenate((order_list, order_list))
        for idx_row in range(0, len(order_list)):
            counter = idx_row
            word = double_arr[idx_row]

            for idx_col in range(idx_row + 1, len(double_arr), 1):
                if word == double_arr[idx_col]:

                    result.append(-(counter - idx_col))
                    counter = idx_col
                    break

    return result


print(intervals([2, 4, 2, 2, 4], 1, 1))
