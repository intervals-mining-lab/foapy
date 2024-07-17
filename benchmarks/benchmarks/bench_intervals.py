import os

from asv_runner.benchmarks.mark import skip_params_if

from foapy.intervals import intervals

from .cases import best_case, dna_case, normal_case, worst_case

length = [5, 50, 500, 5000, 50000, 500000, 5000000, 50000000]
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
    mode = None
    binding = None

    def setup(self, length, case, binding, mode):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        elif case == "Worst":
            self.data = worst_case(length)
        self.mode = mode
        self.binding = binding

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def time_intervals(self, length, case, binding, mode):
        intervals(self.data, self.binding, self.mode)

    @skip_params_if(skip, os.getenv("QUICK_BENCHMARK") == "true")
    def peakmem_intervals(self, length, case, binding, mode):
        return intervals(self.data, self.binding, self.mode)
