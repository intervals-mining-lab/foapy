import numpy
from numpy import fix


def best_case(length):
    return numpy.ones((length,), dtype=int)


def dna_case(length):
    nucleotides = ["A", "C", "G", "T"]
    return numpy.random.choice(nucleotides, length)


def normal_case(length):
    alphabet = numpy.arange(0, fix(length * 0.2), dtype=int)
    return numpy.random.choice(alphabet, length)


def worst_case(length):
    return numpy.random.rand(length)


def records_case(length, width, axis):
    """Deterministic repeated records with the selected sequence axis."""
    distinct = max(1, length // 2)
    codes = numpy.arange(length, dtype=int) % distinct
    offsets = numpy.arange(width, dtype=int)
    records = codes[:, None] * (width + 1) + offsets[None, :]
    return records if axis == 0 else records.T


def whole_slice_mask(length, width, axis, case):
    """Build a uniform per-record mask for multidimensional partials."""
    if case == "Unmasked":
        gaps = numpy.zeros(length, dtype=bool)
    elif case == "Gapped":
        gaps = numpy.arange(length) % 5 == 0
    else:
        gaps = numpy.ones(length, dtype=bool)

    mask = numpy.broadcast_to(gaps[:, None], (length, width)).copy()
    return mask if axis == 0 else mask.T
