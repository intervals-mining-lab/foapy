"""
Pipeline consistency tests: partials functions must equal core functions
when input has no masked positions (SC-003).
"""

from unittest import TestCase

import numpy.ma as ma
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import alphabet as core_alphabet
from foapy.core import intervals_chain as core_intervals_chain
from foapy.core import intervals_tuple as core_intervals_tuple
from foapy.core import order as core_order
from foapy.core import (
    tuple_mode,
)
from foapy.partials import alphabet as partials_alphabet
from foapy.partials import intervals_chain as partials_intervals_chain
from foapy.partials import intervals_tuple as partials_intervals_tuple
from foapy.partials import order as partials_order

_DATASETS = [
    ["a", "b", "a", "c", "b"],
    ["a", "a", "a"],
    ["a", "b", "c", "d"],
    [1, 2, 3, 2, 1],
]


class TestPartialsCoreConsistency(TestCase):
    """
    Verify that foapy.partials produces the same results as foapy.core
    when the input has no masked positions.
    """

    def _unmasked(self, data):
        return ma.masked_array(data, mask=[0] * len(data))

    # -------------------------------------------------------------------------
    # order
    # -------------------------------------------------------------------------

    def test_order_matches_core_for_all_datasets(self):
        for data in _DATASETS:
            with self.subTest(data=data):
                X = self._unmasked(data)
                core_result = core_order(data)
                partial_result = partials_order(X)
                assert_array_equal(
                    partial_result.compressed(),
                    core_result,
                    err_msg=f"order mismatch for {data}",
                )

    # -------------------------------------------------------------------------
    # alphabet
    # -------------------------------------------------------------------------

    def test_alphabet_matches_core_for_all_datasets(self):
        for data in _DATASETS:
            with self.subTest(data=data):
                X = self._unmasked(data)
                core_result = core_alphabet(data)
                partial_result = partials_alphabet(X)
                assert_array_equal(
                    partial_result,
                    core_result,
                    err_msg=f"alphabet mismatch for {data}",
                )

    # -------------------------------------------------------------------------
    # intervals_chain — all binding × chain_mode combinations
    # -------------------------------------------------------------------------

    def test_intervals_chain_matches_core_all_combinations(self):
        bindings = [binding.start, binding.end]
        chain_modes = [chain_mode.boundary, chain_mode.cycle]
        for data in _DATASETS:
            for b in bindings:
                for cm in chain_modes:
                    with self.subTest(data=data, binding=b, chain_mode=cm):
                        X = self._unmasked(data)
                        core_result = core_intervals_chain(data, b, cm)
                        partial_result = partials_intervals_chain(X, b, cm)
                        expected_err_msg = (
                            f"intervals_chain mismatch for {data}, b={b}, cm={cm}"
                        )
                        assert_array_equal(
                            partial_result.compressed(),
                            core_result,
                            err_msg=expected_err_msg,
                        )

    # -------------------------------------------------------------------------
    # intervals_tuple — all binding × tuple_mode combinations
    # -------------------------------------------------------------------------

    def test_intervals_tuple_normal_matches_core(self):
        for data in _DATASETS:
            for b in [binding.start, binding.end]:
                for cm in [chain_mode.boundary, chain_mode.cycle]:
                    with self.subTest(data=data, binding=b, chain_mode=cm):
                        chain = core_intervals_chain(data, b, cm)
                        masked_chain = ma.masked_array(chain, mask=[0] * len(chain))
                        core_result = core_intervals_tuple(chain, b, tuple_mode.normal)
                        partial_result = partials_intervals_tuple(
                            masked_chain, b, tuple_mode.normal
                        )
                        assert_array_equal(partial_result, core_result)

    def test_intervals_tuple_lossy_matches_core(self):
        for data in _DATASETS:
            for b in [binding.start, binding.end]:
                for cm in [chain_mode.boundary, chain_mode.cycle]:
                    with self.subTest(data=data, binding=b, chain_mode=cm):
                        chain = core_intervals_chain(data, b, cm)
                        masked_chain = ma.masked_array(chain, mask=[0] * len(chain))
                        core_result = core_intervals_tuple(chain, b, tuple_mode.lossy)
                        partial_result = partials_intervals_tuple(
                            masked_chain, b, tuple_mode.lossy
                        )
                        # For binding.end, partials now follows core's own
                        # reversed-frame order exactly — compare directly.
                        assert_array_equal(partial_result, core_result)

    def test_intervals_tuple_redundant_matches_core(self):
        for data in _DATASETS:
            for b in [binding.start, binding.end]:
                for cm in [chain_mode.boundary, chain_mode.cycle]:
                    with self.subTest(data=data, binding=b, chain_mode=cm):
                        chain = core_intervals_chain(data, b, cm)
                        masked_chain = ma.masked_array(chain, mask=[0] * len(chain))
                        core_result = core_intervals_tuple(
                            chain, b, tuple_mode.redundant
                        )
                        partial_result = partials_intervals_tuple(
                            masked_chain, b, tuple_mode.redundant
                        )
                        # For binding.end, partials now follows core's own
                        # reversed-frame order exactly — compare directly,
                        # both the compressed portion and the trailing one.
                        assert_array_equal(partial_result, core_result)
