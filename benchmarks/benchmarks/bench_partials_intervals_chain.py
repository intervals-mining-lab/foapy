import os

import numpy as np
import numpy.ma as ma
from asv_runner.benchmarks.mark import skip_params_if

from foapy.partials import intervals_chain

from .cases import (
    best_case,
    dna_case,
    normal_case,
    records_case,
    whole_slice_mask,
    worst_case,
)

length = [100, 10_000, 1_000_000]
cases = ["Dense", "PartialDNA", "PartialNormal", "FullyMasked"]
skip = [
    (1_000_000, "PartialNormal", 1, 1),
    (1_000_000, "PartialNormal", 1, 2),
    (1_000_000, "PartialNormal", 2, 1),
    (1_000_000, "PartialNormal", 2, 2),
    (1_000_000, "FullyMasked", 1, 1),
    (1_000_000, "FullyMasked", 1, 2),
    (1_000_000, "FullyMasked", 2, 1),
    (1_000_000, "FullyMasked", 2, 2),
]
timeout = 600


class PartialsIntervalsChainSuite:
    params = (length, cases, [1, 2], [1, 2])
    param_names = ["length", "case", "binding", "chain_mode"]

    def setup(self, length, case, binding, chain_mode):
        if case == "Dense":
            source = best_case(length)
            self.data = source
        elif case == "PartialDNA":
            source = dna_case(length)
            self.data = ma.masked_array(source, mask=np.arange(length) % 4 == 0)
        elif case == "PartialNormal":
            source = normal_case(length)
            self.data = ma.masked_array(source, mask=np.arange(length) % 2 == 0)
        else:
            source = worst_case(length)
            self.data = ma.masked_array(source, mask=np.ones(length, dtype=bool))
        self.binding = binding
        self.chain_mode = chain_mode

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_chain(self, length, case, binding, chain_mode):
        intervals_chain(self.data, self.binding, self.chain_mode)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_chain(self, length, case, binding, chain_mode):
        return intervals_chain(self.data, self.binding, self.chain_mode)


axis_length = [100, 10_000, 1_000_000]
axis_cases = ["Unmasked", "Gapped", "FullyMasked"]
axis_skip = [
    (1_000_000, width, axis, case, binding, chain_mode)
    for width in (2, 8)
    for axis in (0, 1)
    for case in axis_cases
    for binding in (1, 2)
    for chain_mode in (1, 2)
]


class PartialsAxisIntervalsChainSuite:
    params = (axis_length, [2, 8], [0, 1], axis_cases, [1, 2], [1, 2])
    param_names = [
        "length",
        "record_width",
        "axis",
        "case",
        "binding",
        "chain_mode",
    ]
    timeout = 600

    def setup(self, length, record_width, axis, case, binding, chain_mode):
        source = records_case(length, record_width, axis)
        mask = whole_slice_mask(length, record_width, axis, case)
        self.data = ma.masked_array(source, mask=mask)
        self.binding = binding
        self.chain_mode = chain_mode

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_chain(
        self, length, record_width, axis, case, binding, chain_mode
    ):
        intervals_chain(self.data, self.binding, self.chain_mode, axis=axis)

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_chain(
        self, length, record_width, axis, case, binding, chain_mode
    ):
        return intervals_chain(self.data, self.binding, self.chain_mode, axis=axis)
