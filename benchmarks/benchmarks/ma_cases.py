import numpy
import numpy.ma as ma
from numpy import fix


def best_case(length):
    return ma.masked_array(numpy.ones((length,), dtype=int), mask=[0] * length)


def dna_case(length):
    rng = numpy.random.default_rng()
    alphabet = numpy.asanyarray(["A", "C", "G", "T"])
    power = len(alphabet)
    alphabet_mask = numpy.random.choice([True, False], power)
    indecies = rng.integers(0, power, length)
    return ma.masked_array(alphabet[indecies], alphabet_mask[indecies])


def normal_case(length):
    rng = numpy.random.default_rng()
    power = int(fix(length * 0.2))
    alphabet = numpy.linspace(0, power, power)
    alphabet_mask = numpy.random.choice([True, False], power)
    indecies = rng.integers(0, power, length)
    return ma.masked_array(alphabet[indecies], alphabet_mask[indecies])


def worst_case(length):
    rng = numpy.random.default_rng()
    power = length
    alphabet = numpy.linspace(0, power, power)
    alphabet_mask = numpy.random.choice([True, False], power)
    indecies = rng.integers(0, power, length)
    return ma.masked_array(alphabet[indecies], alphabet_mask[indecies])
