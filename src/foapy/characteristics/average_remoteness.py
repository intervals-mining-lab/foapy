from foapy.characteristics.depth import depth


def average_remoteness(intervals):
    """
    Calculation geometric of sequence.

    Average remoteness is the Depth divide by number of intervals
    in the given congeneric sequence.

    Param name = "intervals" (sequence of intervals).

    The variable n is the number of intervals in the sequence.

    """
    n = len(intervals)

    return depth(intervals) / n
