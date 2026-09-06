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
