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
