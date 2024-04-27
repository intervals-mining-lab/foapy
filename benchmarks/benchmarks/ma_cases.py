import numpy
import numpy.ma as ma
from numpy import fix

def best_case(length):
    return ma.masked_array(numpy.ones((length,), dtype=int), mask=[0] * length)


def dna_case(length):
    nucleotides = ["A", "C", "G", "T"]
    alphabet = numpy.random.choice(nucleotides, length)
    generate_mask = numpy.unique(numpy.random.choice(alphabet, 1))
    mask = ([1 if mask_obj in generate_mask else 0 for mask_obj in alphabet],)
    return ma.masked_array(alphabet, mask=mask)


def normal_case(length):

    alphabet = numpy.random.choice(
        numpy.arange(0, fix(length * 0.2), dtype=int), length
    )
    generate_mask = numpy.unique(
        numpy.random.choice(alphabet, numpy.random.randint(0, length))
    )
    mask = ([1 if mask_obj in generate_mask else 0 for mask_obj in alphabet],)

    return ma.masked_array(alphabet, mask)


def worst_case(length):
    alphabet = numpy.random.rand(length)
    generate_mask = numpy.unique(
        numpy.random.choice(alphabet, numpy.random.randint(0, length))
    )
    mask = ([1 if mask_obj in generate_mask else 0 for mask_obj in alphabet],)

    return ma.masked_array(alphabet, mask)