class binding:
    start = 1
    end = 2


class mode:
    lossy = 1
    normal = 2
    cycle = 3
    redundant = 4


def intervals(X, bind, mod):
    """
    Find a one-dimensional array of intervals in the
    given input sequence with the interval binding determined
    by the provided binding and mode flags.

    Parameters
    ----------
    X: one-dimensional array
        Array to get unique values.
    binding: int
        start = 1 - Intervals are extracted from left to right.
        end = 2 – Intervals are extracted from right to left.
    mode: int
        lossy = 1 - Both interval from the start of the sequence
        to the first element occurrence and interval from the
        last element occurrence to the end of the sequence
        are not taken into account.

        normal = 2 - Interval from the start of the sequence to
        the first occurrence of the element
        (in case of binding to the beginning)
        or interval from the last occurrence of the element to
        the end of the sequence
        (in case of binding to the end) is taken into account.

        cycle = 3 - Interval from the start of the sequence to
        the first element occurrence
        and interval from the last element occurrence to the
        end of the sequence are summed
        into one interval (as if sequence was cyclic).
        Interval is placed either in the beginning of
        intervals array (in case of binding to the beginning)
        or in the end (in case of binding to the end).

        redundant = 4 - Both interval from start of the sequence
        to the first element occurrence and the interval from
        the last element occurrence to the end of the
        sequence are taken into account. Their placement in results
        array is determined
        by the binding.
    Returns
    -------
    result: array or error.
        An error indicating that the binding or mode does not exist,
        otherwise the array.
    """
    # Validate binding
    if bind not in {binding.start, binding.end, 1, 2}:
        raise ValueError(
            {"message": "Invalid binding value. Use binding.start or binding.end."}
        )

    # Validate mode
    if mod not in {mode.lossy, mode.normal, mode.cycle, mode.redundant, 1, 2, 3, 4}:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )

    result = []
    counter = 0
    first_elements = {}
    position_elem = {}
    # Reverse the sequence if binding is to the end
    if bind == binding.end:
        X = X[::-1]

    for idx, elem in enumerate(X):
        if elem not in first_elements:
            first_elements[elem] = idx
            position_elem[elem] = idx
        else:
            interval = idx - position_elem[elem]
            result.append(interval)
            position_elem[elem] = idx

    if mod == mode.normal:
        for elem in first_elements:
            result.insert(first_elements[elem], first_elements[elem] + 1)

    elif mod == mode.cycle:
        for elem in first_elements:
            result.insert(
                first_elements[elem],
                len(X) - position_elem[elem] + first_elements[elem],
            )

    elif mod == mode.redundant:
        for elem in first_elements:
            result.insert(first_elements[elem], first_elements[elem] + 1)
        for i, counter in enumerate(sorted(position_elem.values())):
            result.insert(counter + i + 1, len(X) - counter)

    # Reverse result back if binding is to the end
    if bind == binding.end:
        result = result[::-1]

    return result
