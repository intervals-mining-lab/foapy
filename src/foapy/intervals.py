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
    # Reverse the sequence if binding is to the end
    if binding == 2:
        X = X[::-1]

    for idx, elem in enumerate(X):
        if elem not in first_elements:
            first_elements[elem] = idx
            position_elem[elem] = idx
        else:
            interval = idx - position_elem[elem]
            result.append(interval)
            position_elem[elem] = idx

    if mode == 2:
        for elem in first_elements:
            result.insert(first_elements[elem], first_elements[elem] + 1)

    elif mode == 3:
        for elem in first_elements:
            result.insert(
                first_elements[elem],
                len(X) - position_elem[elem] + first_elements[elem],
            )

    elif mode == 4:
        for elem in first_elements:
            result.insert(first_elements[elem], first_elements[elem] + 1)
        for i, counter in enumerate(sorted(position_elem.values())):
            result.insert(counter + i + 1, len(X) - counter)

    # Reverse result back if binding is to the end
    if binding == 2:
        result = result[::-1]

    return result
