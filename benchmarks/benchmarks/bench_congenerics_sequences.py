import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.congenerics import sequences

from .cases import best_case, dna_case, normal_case, worst_case

length = [100, 1_000, 10_000]
cases = ["Best", "DNA", "Normal", "Worst"]
# Normal (m ~ 0.2*l) and Worst (m = l) scale row count with length; skip them
# at the largest length so the (m, l) matrix stays bounded. Best (m=1) and
# DNA (m=4) stay cheap at any length.
skip = [(10_000, "Normal"), (10_000, "Worst")]


class CongenericsSequencesSuite:
    params = (length, cases)
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        else:
            self.data = worst_case(length)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_sequences(self, length, case):
        sequences(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_sequences(self, length, case):
        return sequences(self.data)
