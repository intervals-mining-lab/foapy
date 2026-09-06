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


class PipelineFullSuite:
    """End-to-end pipeline: intervals_chain -> intervals_tuple -> intervals_distribution."""  # noqa: E501

    params = (length, ["Best", "DNA", "Normal", "Worst"])
    param_names = ["length", "case"]

    def setup(self, length, case):
        if case == "Best":
            self.data = best_case(length)
        elif case == "DNA":
            self.data = dna_case(length)
        elif case == "Normal":
            self.data = normal_case(length)
        else:
            self.data = worst_case(length)

    def time_pipeline_full(self, length, case):
        chain = intervals_chain(self.data, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        intervals_distribution(result)

    def peakmem_pipeline_full(self, length, case):
        chain = intervals_chain(self.data, binding.start, chain_mode.boundary)
        result = intervals_tuple(chain, binding.start, tuple_mode.normal)
        return intervals_distribution(result)
