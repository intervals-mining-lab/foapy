from foapy.characteristics.depth import depth


def average_remoteness(intervals_seq):

    n = len(intervals_seq)

    return depth(intervals_seq) / n
