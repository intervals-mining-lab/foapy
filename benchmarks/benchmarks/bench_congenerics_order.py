import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.congenerics import order, sequences

from .cases import best_case, dna_case, normal_case, worst_case

length = [100, 1_000, 10_000]
cases = ["Best", "DNA", "Normal", "Worst"]
# Normal (m ~ 0.2*l) and Worst (m = l) scale row count with length; skip them
# at the largest length so the (m, l) matrix stays bounded. Best (m=1) and
# DNA (m=4) stay cheap at any length.
skip = [(10_000, "Normal"), (10_000, "Worst")]


class CongenericsOrderSuite:
    params = (length, cases)
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Best":
            source = best_case(length)
        elif case == "DNA":
            source = dna_case(length)
        elif case == "Normal":
            source = normal_case(length)
        else:
            source = worst_case(length)
        # order(CS) takes the decomposition itself, not the raw source.
        self.data = sequences(source)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_order(self, length, case):
        order(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_order(self, length, case):
        return order(self.data)
