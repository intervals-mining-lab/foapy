def average_remoteness(intervals):
    """
    Calculation average remoteness of sequence.

    Average remoteness is the Depth divide by number of intervals
    in the given congeneric sequence.

    Param name = "intervals" (sequence of intervals).

    The variable n is the number of intervals in the sequence.

    """
    from foapy.characteristics import depth

    n = len(intervals)

    # Check for an empty list or a list with zeros
    if n == 0 or all(x == 0 for x in intervals):
        return 0

    return depth(intervals) / n
