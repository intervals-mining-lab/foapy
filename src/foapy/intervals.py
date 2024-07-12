def intervals(X, binding, mode):
    """
    Finding array of array of intervals of the
    uniform  sequences in the given input sequence
    """
    order_list = X
    result = []
    print(order_list)
    counter = 0
    first_elements = {}
    position_elem = {}
    if binding == 1:  # binding Start

        for idx, i in enumerate(X):
            if i not in first_elements:
                first_elements[i] = idx
                position_elem[i] = idx
            else:
                interval = idx - position_elem[i]
                result.append(interval)
                position_elem[i] = idx

        if mode == 2:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, counter + 1)

        if mode == 3:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, len(X) - position_elem[i] + first_elements[i])

        if mode == 4:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, counter + 1)
            j = 1
            for counter in sorted(position_elem.values()):
                result.insert(counter + j, len(X) - counter)
                j = j + 1

    if binding == 2:  # binding End

        X_rev = X[::-1]

        for idx, i in enumerate(X_rev):
            if i not in first_elements:
                first_elements[i] = idx
                position_elem[i] = idx
            else:
                interval = idx - position_elem[i]
                result.append(interval)
                position_elem[i] = idx

        if mode == 2:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, counter + 1)

        if mode == 3:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, len(X) - position_elem[i] + first_elements[i])

        if mode == 4:
            for i in first_elements:
                counter = first_elements[i]
                result.insert(counter, counter + 1)
            j = 1
            for counter in sorted(position_elem.values()):
                result.insert(counter + j, len(X) - counter)
                j += 1

        result = result[::-1]

    return result
