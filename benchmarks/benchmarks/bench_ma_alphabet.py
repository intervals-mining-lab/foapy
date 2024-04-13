import os

import numpy
from asv_runner.benchmarks.mark import skip_params_if
from numpy import fix
import numpy.ma as ma
from foapy.ma.alphabet import alphabet

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
skip = [
    (5000000, "Worst"),
    (5000000, "DNA"),
    (5000000, "Normal"),
    (5000000, "Best"),
    (50000000, "Worst"),
    (50000000, "DNA"),
    (50000000, "Normal"),
    (50000000, "Best"),
]


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
        numpy.random.choice(alphabet, numpy.random.randint(0, length * 0.1))
    )
    mask = ([1 if mask_obj in generate_mask else 0 for mask_obj in alphabet],)

    return ma.masked_array(alphabet, mask)


def worst_case(length):
    alphabet = numpy.random.rand(length)
    generate_mask = numpy.unique(
        numpy.random.choice(alphabet, numpy.random.randint(0, length * 0.2))
    )
    mask = ([1 if mask_obj in generate_mask else 0 for mask_obj in alphabet],)

    return ma.masked_array(alphabet, mask)


class MaAlphabetSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"])
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        elif case == "Worst":
            self.data = worst_case(length)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_alphabet(self, length, case):
        alphabet(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def mem_alphabet(self, length, case):
        return alphabet(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_alphabet(self, length, case):
        return alphabet(self.data)
