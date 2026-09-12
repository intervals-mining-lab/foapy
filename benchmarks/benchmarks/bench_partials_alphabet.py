import os

import numpy as np
import numpy.ma as ma
from asv_runner.benchmarks.mark import skip_params_if

from foapy.partials import alphabet

from .cases import (
    best_case,
    dna_case,
    normal_case,
    records_case,
    whole_slice_mask,
    worst_case,
)

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
cases = ["Best", "DNA", "Normal", "Worst"]
skip = [(5000000, case) for case in cases] + [(50000000, case) for case in cases]


class PartialsAlphabetSuite:
    params = (length, cases)
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Best":
            source = best_case(length)
        elif case == "DNA":
            source = dna_case(length)
        elif case == "Normal":
            source = normal_case(length)
        else:
            source = worst_case(length)

        # Keep the unmasked case directly comparable to foapy.alphabet.
        if case == "Best":
            self.data = source
        elif case == "DNA":
            self.data = ma.masked_array(source, mask=np.arange(length) % 4 == 0)
        elif case == "Normal":
            self.data = ma.masked_array(source, mask=np.arange(length) % 2 == 0)
        else:
            self.data = ma.masked_array(source, mask=np.ones(length, dtype=bool))

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_alphabet(self, length, case):
        alphabet(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_alphabet(self, length, case):
        return alphabet(self.data)


class PartialsAxisAlphabetSuite:
    params = (
        [5, 50, 500, 5000, 50000],
        [2, 8],
        [0, 1],
        ["Unmasked", "Gapped", "FullyMasked"],
    )
    param_names = ["length", "record_width", "axis", "case"]

    data = None

    def setup(self, length, record_width, axis, case):
        source = records_case(length, record_width, axis)
        mask = whole_slice_mask(length, record_width, axis, case)
        self.data = ma.masked_array(source, mask=mask)

    def time_alphabet(self, length, record_width, axis, case):
        alphabet(self.data, axis=axis)

    def peakmem_alphabet(self, length, record_width, axis, case):
        return alphabet(self.data, axis=axis)
