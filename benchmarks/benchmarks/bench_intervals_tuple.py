import os

import numpy as np
from asv_runner.benchmarks.mark import skip_params_if

from foapy import binding, chain_mode
from foapy.core import intervals_chain, intervals_tuple

from .cases import best_case, dna_case, normal_case, worst_case

length = [100, 10_000, 1_000_000]
timeout = 600


class IntervalsTupleSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"], [1, 2, 3])
    param_names = ["length", "case", "tuple_mode"]

    def setup(self, length, case, tm):
        if case == "Best":
            data = best_case(length)
        elif case == "DNA":
            data = dna_case(length)
        elif case == "Normal":
            data = normal_case(length)
        else:
            data = worst_case(length)
        self.chain = intervals_chain(data, binding.start, chain_mode.boundary)
        self.tuple_mode = tm

    def time_intervals_tuple(self, length, case, tm):
        intervals_tuple(self.chain, binding.start, self.tuple_mode)

    def peakmem_intervals_tuple(self, length, case, tm):
        return intervals_tuple(self.chain, binding.start, self.tuple_mode)


axis_length = [100, 10_000, 1_000_000]
axis_cases = ["Uniform", "Variable"]
axis_skip = [
    (1_000_000, lane_count, axis, case, binding_value, tuple_mode_value)
    for lane_count in (2, 8)
    for axis in (0, 1)
    for case in axis_cases
    for binding_value in (1, 2)
    for tuple_mode_value in (1, 2, 3)
]


def _chains_case(length, lane_count, axis, case, binding_value):
    chains = np.ones((lane_count, length), dtype=np.intp)
    if case == "Variable":
        boundary = np.arange(1, length + 1, dtype=np.intp)
        if binding_value == binding.end:
            boundary = boundary[::-1]
        chains[1::2] = boundary
    return chains if axis == 1 else chains.T


class AxisIntervalsTupleSuite:
    params = (axis_length, [2, 8], [0, 1], axis_cases, [1, 2], [1, 2, 3])
    param_names = [
        "length",
        "lane_count",
        "axis",
        "case",
        "binding",
        "tuple_mode",
    ]
    timeout = 600

    def setup(self, length, lane_count, axis, case, binding_value, tuple_mode_value):
        self.chains = _chains_case(length, lane_count, axis, case, binding_value)
        self.axis = axis
        self.binding = binding_value
        self.tuple_mode = tuple_mode_value

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_tuple(
        self, length, lane_count, axis, case, binding_value, tuple_mode_value
    ):
        intervals_tuple(self.chains, self.binding, self.tuple_mode, axis=self.axis)

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_tuple(
        self, length, lane_count, axis, case, binding_value, tuple_mode_value
    ):
        return intervals_tuple(
            self.chains, self.binding, self.tuple_mode, axis=self.axis
        )
