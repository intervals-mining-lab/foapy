import os

import numpy as np
import numpy.ma as ma
from asv_runner.benchmarks.mark import skip_params_if

from foapy.partials import intervals_tuple

lengths = [100, 10_000, 1_000_000]
gap_cases = ["Dense", "Gapped"]
timeout = 600


def _partial_chain_rows(length, lane_count, gap_case, binding_value):
    data = np.zeros((lane_count, length), dtype=np.intp)
    mask = np.zeros_like(data, dtype=bool)

    for lane_index in range(lane_count):
        if gap_case == "Gapped":
            mask[lane_index, lane_index % 7 :: 7] = True

        positions = np.flatnonzero(~mask[lane_index])
        if binding_value == 1:
            values = np.diff(np.concatenate(([-1], positions)))
        else:
            values = np.diff(np.concatenate((positions, [length])))
        data[lane_index, positions] = values

    return ma.masked_array(data, mask=mask)


one_dimensional_skip = [
    (1_000_000, gap_case, binding_value, tuple_mode_value)
    for gap_case in gap_cases
    for binding_value in (1, 2)
    for tuple_mode_value in (1, 2, 3)
]


class PartialsIntervalsTupleSuite:
    params = (lengths, gap_cases, [1, 2], [1, 2, 3])
    param_names = ["length", "case", "binding", "tuple_mode"]
    timeout = 600

    def setup(self, length, gap_case, binding_value, tuple_mode_value):
        self.chain = _partial_chain_rows(length, 1, gap_case, binding_value)[0]
        self.binding = binding_value
        self.tuple_mode = tuple_mode_value

    @skip_params_if(
        one_dimensional_skip,
        os.getenv("QUICK_BENCHMARK") == "true",
    )
    def time_intervals_tuple(self, length, gap_case, binding_value, tuple_mode_value):
        intervals_tuple(self.chain, self.binding, self.tuple_mode)

    @skip_params_if(
        one_dimensional_skip,
        os.getenv("QUICK_BENCHMARK") == "true",
    )
    def peakmem_intervals_tuple(
        self, length, gap_case, binding_value, tuple_mode_value
    ):
        return intervals_tuple(self.chain, self.binding, self.tuple_mode)


axis_skip = [
    (1_000_000, lane_count, axis, gap_case, binding_value, tuple_mode_value)
    for lane_count in (2, 8)
    for axis in (0, 1)
    for gap_case in gap_cases
    for binding_value in (1, 2)
    for tuple_mode_value in (1, 2, 3)
]


class AxisPartialsIntervalsTupleSuite:
    params = (lengths, [2, 8], [0, 1], gap_cases, [1, 2], [1, 2, 3])
    param_names = [
        "length",
        "lane_count",
        "axis",
        "case",
        "binding",
        "tuple_mode",
    ]
    timeout = 600

    def setup(
        self,
        length,
        lane_count,
        axis,
        gap_case,
        binding_value,
        tuple_mode_value,
    ):
        chains = _partial_chain_rows(
            length,
            lane_count,
            gap_case,
            binding_value,
        )
        self.chains = chains if axis == 1 else chains.T
        self.axis = axis
        self.binding = binding_value
        self.tuple_mode = tuple_mode_value

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_tuple(
        self,
        length,
        lane_count,
        axis,
        gap_case,
        binding_value,
        tuple_mode_value,
    ):
        intervals_tuple(
            self.chains,
            self.binding,
            self.tuple_mode,
            axis=self.axis,
        )

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_tuple(
        self,
        length,
        lane_count,
        axis,
        gap_case,
        binding_value,
        tuple_mode_value,
    ):
        return intervals_tuple(
            self.chains,
            self.binding,
            self.tuple_mode,
            axis=self.axis,
        )
