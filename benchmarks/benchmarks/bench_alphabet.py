import os

import numpy
from asv_runner.benchmarks.mark import skip_params_if
from numpy import fix

from foapy.alphabet import alphabet

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
skip = [
    (500000, "Worst"),
    (500000, "DNA"),
    (500000, "Best"),
    (500000, "Normal"),
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
    return numpy.ones((length,), dtype=int)


def dna_case(length):
    nucleotides = ["A", "C", "G", "T"]
    return numpy.random.choice(nucleotides, length)


def normal_case(length):
    alphabet = numpy.arange(0, fix(length * 0.2), dtype=int)
    return numpy.random.choice(alphabet, length)


def worst_case(length):
    return numpy.random.rand(length)


class AlphabetSuite:
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
