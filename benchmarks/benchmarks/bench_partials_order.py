import os

import numpy as np
import numpy.ma as ma
from asv_runner.benchmarks.mark import skip_params_if

from foapy.partials import order

from .cases import (
    best_case,
    dna_case,
    normal_case,
    records_case,
    whole_slice_mask,
    worst_case,
)

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
cases = ["Unmasked", "PartialDNA", "PartialNormal", "FullyMasked"]
skip = [(5000000, case) for case in cases] + [(50000000, case) for case in cases]


class PartialsOrderSuite:
    params = (length, cases)
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Unmasked":
            self.data = best_case(length)
        elif case == "PartialDNA":
            source = dna_case(length)
            self.data = ma.masked_array(source, mask=np.arange(length) % 4 == 0)
        elif case == "PartialNormal":
            source = normal_case(length)
            self.data = ma.masked_array(source, mask=np.arange(length) % 2 == 0)
        elif case == "FullyMasked":
            source = worst_case(length)
            self.data = ma.masked_array(source, mask=np.ones(length, dtype=bool))

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_order(self, length, case):
        order(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_order(self, length, case):
        return order(self.data)


class PartialsAxisOrderSuite:
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

    def time_order(self, length, record_width, axis, case):
        order(self.data, axis=axis)

    def peakmem_order(self, length, record_width, axis, case):
        return order(self.data, axis=axis)
