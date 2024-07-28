import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.ma.alphabet import alphabet

from .ma_cases import best_case, dna_case, normal_case, worst_case

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
skip = [
    (500000, "Worst"),
    (500000, "DNA"),
    (500000, "Best"),
    (500000, "Normal"),
    (5000000, "Worst"),
    (5000000, "DNA"),
    (5000000, "Normal"),
    (5000000, "Best"),
    (50000000, "Worst"),
    (50000000, "DNA"),
    (50000000, "Normal"),
    (50000000, "Best"),
]


class MaAlphabetSuite:
    params = (length, ["Best", "DNA", "Normal", "Worst"])
    param_names = ["length", "case"]

    data = None

    def setup(self, length, case):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        elif case == "Worst":
            self.data = worst_case(length)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_alphabet(self, length, case):
        alphabet(self.data)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_alphabet(self, length, case):
        return alphabet(self.data)
