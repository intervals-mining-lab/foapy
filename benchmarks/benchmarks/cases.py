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
