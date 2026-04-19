import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy import chain_mode
from foapy.core import intervals_chain, intervals_tuple, tuple_mode

from .cases import best_case, dna_case, normal_case, worst_case

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]

# mode integer values: 1=lossy, 2=normal, 3=cycle, 4=redundant
_CHAIN_MODE = {
    1: chain_mode.boundary,
    2: chain_mode.boundary,
    3: chain_mode.cycle,
    4: chain_mode.boundary,
}
_TUPLE_MODE = {
    1: tuple_mode.lossy,
    2: tuple_mode.normal,
    3: tuple_mode.normal,
    4: tuple_mode.redundant,
}

skip = [
    (5000000, "Worst", 1, 1),
    (5000000, "DNA", 1, 1),
    (5000000, "Normal", 1, 1),
    (5000000, "Best", 1, 1),
    (50000000, "Worst", 1, 1),
    (50000000, "DNA", 1, 1),
    (50000000, "Normal", 1, 1),
    (50000000, "Best", 1, 1),
    (5000000, "Worst", 1, 2),
    (5000000, "DNA", 1, 2),
    (5000000, "Normal", 1, 2),
    (5000000, "Best", 1, 2),
    (50000000, "Worst", 1, 2),
    (50000000, "DNA", 1, 2),
    (50000000, "Normal", 1, 2),
    (50000000, "Best", 1, 2),
    (5000000, "Worst", 1, 3),
    (5000000, "DNA", 1, 3),
    (5000000, "Normal", 1, 3),
    (5000000, "Best", 1, 3),
    (50000000, "Worst", 1, 3),
    (50000000, "DNA", 1, 3),
    (50000000, "Normal", 1, 3),
    (50000000, "Best", 1, 3),
    (5000000, "Worst", 1, 4),
    (5000000, "DNA", 1, 4),
    (5000000, "Normal", 1, 4),
    (5000000, "Best", 1, 4),
    (50000000, "Worst", 1, 4),
    (50000000, "DNA", 1, 4),
    (50000000, "Normal", 1, 4),
    (50000000, "Best", 1, 4),
    (5000000, "Worst", 2, 1),
    (5000000, "DNA", 2, 1),
    (5000000, "Normal", 2, 1),
    (5000000, "Best", 2, 1),
    (50000000, "Worst", 2, 1),
    (50000000, "DNA", 2, 1),
    (50000000, "Normal", 2, 1),
    (50000000, "Best", 2, 1),
    (5000000, "Worst", 2, 2),
    (5000000, "DNA", 2, 2),
    (5000000, "Normal", 2, 2),
    (5000000, "Best", 2, 2),
    (50000000, "Worst", 2, 2),
    (50000000, "DNA", 2, 2),
    (50000000, "Normal", 2, 2),
    (50000000, "Best", 2, 2),
    (5000000, "Worst", 2, 3),
    (5000000, "DNA", 2, 3),
    (5000000, "Normal", 2, 3),
    (5000000, "Best", 2, 3),
    (50000000, "Worst", 2, 3),
    (50000000, "DNA", 2, 3),
    (50000000, "Normal", 2, 3),
    (50000000, "Best", 2, 3),
    (5000000, "Worst", 2, 4),
    (5000000, "DNA", 2, 4),
    (5000000, "Normal", 2, 4),
    (5000000, "Best", 2, 4),
    (50000000, "Worst", 2, 4),
    (50000000, "DNA", 2, 4),
    (50000000, "Normal", 2, 4),
    (50000000, "Best", 2, 4),
]
timeout = 600


class IntervalsSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"], [1, 2], [1, 2, 3, 4])
    param_names = ["length", "case", "binding", "mode"]

    data = None
    chain_mode_val = None
    tuple_mode_val = None
    binding_val = None

    def setup(self, length, case, binding_int, mode_int):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        elif case == "Worst":
            self.data = worst_case(length)
        self.binding_val = binding_int
        self.chain_mode_val = _CHAIN_MODE[mode_int]
        self.tuple_mode_val = _TUPLE_MODE[mode_int]

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals(self, length, case, binding_int, mode_int):
        intervals_tuple(
            intervals_chain(self.data, self.binding_val, self.chain_mode_val),
            self.binding_val,
            self.tuple_mode_val,
        )

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals(self, length, case, binding_int, mode_int):
        return intervals_tuple(
            intervals_chain(self.data, self.binding_val, self.chain_mode_val),
            self.binding_val,
            self.tuple_mode_val,
        )
