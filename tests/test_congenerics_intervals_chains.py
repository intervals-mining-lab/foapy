from unittest import TestCase

import pytest
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.congenerics import intervals_chains
from foapy.congenerics import order as congenerics_order
from foapy.congenerics import sequences as congenerics_sequences
from foapy.partials import intervals_chain as partials_intervals_chain

_DATASETS = [
    ["a", "b", "a", "c", "b"],
    ["a", "a", "a"],
    ["a", "b", "c", "d"],
]


class TestCongenericsIntervalsChains(TestCase):
    """
    Test foapy.congenerics.intervals_chains(CS, binding, chain_mode).

    CS is the output of foapy.congenerics.sequences(X) (or, equivalently,
    foapy.congenerics.order(CS), since only the mask matters). Row j MUST
    equal foapy.partials.intervals_chain(sequences(X)[j], binding,
    chain_mode) for every j.
    """

    def test_row_wise_parity_with_partials(self):
        bindings = [binding.start, binding.end]
        chain_modes = [chain_mode.boundary, chain_mode.cycle]
        for data in _DATASETS:
            for b in bindings:
                for cm in chain_modes:
                    with self.subTest(data=data, binding=b, chain_mode=cm):
                        CS = congenerics_sequences(data)
                        result = intervals_chains(CS, b, cm)
                        assert result.shape == CS.shape
                        for j in range(CS.shape[0]):
                            expected = partials_intervals_chain(CS[j], b, cm)
                            assert_array_equal(result.mask[j], expected.mask)
                            assert_array_equal(result[j].filled(0), expected.filled(0))

    def test_accepts_order_result(self):
        for data in _DATASETS:
            with self.subTest(data=data):
                CS = congenerics_sequences(data)
                order_result = congenerics_order(CS)
                expected = intervals_chains(CS, binding.start, chain_mode.boundary)
                result = intervals_chains(
                    order_result, binding.start, chain_mode.boundary
                )
                assert_array_equal(result.mask, expected.mask)
                assert_array_equal(result.filled(0), expected.filled(0))

    def test_invalid_binding_raises(self):
        CS = congenerics_sequences(["a", "b"])
        with pytest.raises(ValueError):
            intervals_chains(CS, 999, chain_mode.boundary)

    def test_invalid_chain_mode_raises(self):
        CS = congenerics_sequences(["a", "b"])
        with pytest.raises(ValueError):
            intervals_chains(CS, binding.start, 999)

    def test_empty_input(self):
        CS = congenerics_sequences([])
        result = intervals_chains(CS, binding.start, chain_mode.boundary)
        assert result.shape == (0, 0)
