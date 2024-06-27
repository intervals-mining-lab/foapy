from foapy.order import order


def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    order_list = order(X)
    result = []
    print(order_list)
    first_elements_arr = []
    counter = 0
    row = []
    if binding == 1 and mode == 1:  # binding Start, mode=None
        col = 0
        for idx_row, i in enumerate(order_list):
            for j in range(col, len(order_list)):
                if i == order_list[j] and idx_row in row:
                    result.append(j - counter)
                    counter = j
                    break
                if i == order_list[j] and idx_row not in row:
                    counter = j
                    first_elements_arr.append(order_list[j])
                    row.append(idx_row)
            col += 1

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

    return result
