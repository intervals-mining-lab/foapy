import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.congenerics import intervals_chains

from .cases import best_case, dna_case, normal_case, worst_case

length = [100, 1_000, 10_000]
cases = ["Best", "DNA", "Normal", "Worst"]
# Normal (m ~ 0.2*l) and Worst (m = l) scale row count with length; skip them
# at the largest length so the (m, l) matrix stays bounded. Best (m=1) and
# DNA (m=4) stay cheap at any length.
skip = [
    (10_000, "Normal", binding, chain_mode)
    for binding in (1, 2)
    for chain_mode in (1, 2)
] + [
    (10_000, "Worst", binding, chain_mode)
    for binding in (1, 2)
    for chain_mode in (1, 2)
]
timeout = 600


class CongenericsIntervalsChainsSuite:
    params = (length, cases, [1, 2], [1, 2])
    param_names = ["length", "case", "binding", "chain_mode"]

    data = None

    def setup(self, length, case, binding, chain_mode):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        else:
            self.data = worst_case(length)
        self.binding = binding
        self.chain_mode = chain_mode

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals_chains(self, length, case, binding, chain_mode):
        intervals_chains(self.data, self.binding, self.chain_mode)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals_chains(self, length, case, binding, chain_mode):
        return intervals_chains(self.data, self.binding, self.chain_mode)
