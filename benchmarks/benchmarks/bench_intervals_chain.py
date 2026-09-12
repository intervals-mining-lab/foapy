import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.core import intervals_chain

from .cases import best_case, dna_case, normal_case, records_case, worst_case

length = [100, 10_000, 1_000_000]
skip = [
    (1_000_000, "Worst", 1, 1),
    (1_000_000, "Worst", 1, 2),
    (1_000_000, "Worst", 2, 1),
    (1_000_000, "Worst", 2, 2),
]
timeout = 600


class IntervalsChainSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"], [1, 2], [1, 2])
    param_names = ["length", "case", "binding", "chain_mode"]

    def setup(self, length, case, b, cm):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        else:
            self.data = worst_case(length)
        self.binding = b
        self.chain_mode = cm

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_chain(self, length, case, b, cm):
        intervals_chain(self.data, self.binding, self.chain_mode)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_chain(self, length, case, b, cm):
        return intervals_chain(self.data, self.binding, self.chain_mode)


axis_length = [100, 10_000, 1_000_000]
axis_skip = [
    (1_000_000, width, axis, binding, chain_mode)
    for width in (2, 8)
    for axis in (0, 1)
    for binding in (1, 2)
    for chain_mode in (1, 2)
]


class AxisIntervalsChainSuite:
    params = (axis_length, [2, 8], [0, 1], [1, 2], [1, 2])
    param_names = ["length", "record_width", "axis", "binding", "chain_mode"]
    timeout = 600

    def setup(self, length, record_width, axis, binding, chain_mode):
        self.data = records_case(length, record_width, axis)
        self.binding = binding
        self.chain_mode = chain_mode

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_chain(self, length, record_width, axis, binding, chain_mode):
        intervals_chain(self.data, self.binding, self.chain_mode, axis=axis)

    @skip_params_if(axis_skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_chain(self, length, record_width, axis, binding, chain_mode):
        return intervals_chain(self.data, self.binding, self.chain_mode, axis=axis)
