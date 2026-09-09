import os

import numpy as np
import numpy.ma as ma
from asv_runner.benchmarks.mark import skip_params_if

from foapy import binding, chain_mode
from foapy.core import (
    intervals_chain,
    intervals_distribution,
    intervals_tuple,
    tuple_mode,
)

from .cases import best_case, dna_case, normal_case, worst_case

length = [100, 10_000, 1_000_000]
timeout = 600


class IntervalsDistributionSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"])
    param_names = ["length", "case"]

    def setup(self, length, case):
        if case == "Best":
            data = best_case(length)
        elif case == "DNA":
            data = dna_case(length)
        elif case == "Normal":
            data = normal_case(length)
        else:
            data = worst_case(length)
        chain = intervals_chain(data, binding.start, chain_mode.boundary)
        self.tuple_result = intervals_tuple(chain, binding.start, tuple_mode.normal)

    def time_intervals_distribution(self, length, case):
        intervals_distribution(self.tuple_result)

    def peakmem_intervals_distribution(self, length, case):
        return intervals_distribution(self.tuple_result)


axis_length = [100, 10_000, 1_000_000]
axis_cases = ["Plain", "Masked"]
axis_skip = [
    (1_000_000, lane_count, axis, case)
    for lane_count in (2, 8)
    for axis in (0, 1)
    for case in axis_cases
]


def _tuples_case(length, lane_count, axis, case):
    lanes = np.empty((lane_count, length), dtype=np.intp)
    for index in range(lane_count):
        maximum = 4 if index % 2 == 0 else 8
        lanes[index] = np.arange(length, dtype=np.intp) % maximum + 1

    if case == "Masked":
        mask = np.zeros_like(lanes, dtype=bool)
        mask[:, (length * 3) // 4 :] = True
        lanes = ma.masked_array(lanes, mask=mask)

    return lanes if axis == 1 else lanes.T


class AxisIntervalsDistributionSuite:
    params = (axis_length, [2, 8], [0, 1], axis_cases)
    param_names = ["length", "lane_count", "axis", "case"]
    timeout = 600

    def setup(self, length, lane_count, axis, case):
        self.tuples = _tuples_case(length, lane_count, axis, case)
        self.axis = axis

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_distribution(self, length, lane_count, axis, case):
        intervals_distribution(self.tuples, axis=self.axis)

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_distribution(self, length, lane_count, axis, case):
        return intervals_distribution(self.tuples, axis=self.axis)
