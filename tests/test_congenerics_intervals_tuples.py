from unittest import TestCase

import numpy as np
import pytest

from foapy import binding, chain_mode, tuple_mode
from foapy.congenerics import intervals_chains as congenerics_intervals_chains
from foapy.congenerics import intervals_tuples
from foapy.congenerics import sequences as congenerics_sequences
from foapy.partials import intervals_tuple as partials_intervals_tuple

_DATASETS = [
    ["a", "b", "a", "c", "b"],
    ["a", "a", "a"],
    ["a", "b", "c", "d"],
]


class TestCongenericsIntervalsTuples(TestCase):
    """
    Test foapy.congenerics.intervals_tuples(chains, binding, tuple_mode).

    chains is the output of foapy.congenerics.intervals_chains(CS, binding,
    chain_mode). Result is a rectangular (m, x) ndarray; row j's unpadded
    prefix MUST match foapy.partials.intervals_tuple on that row's chain,
    and the remainder MUST be right-padded with 0.
    """

    def test_rows_padded_to_widest_row(self):
        for data in _DATASETS:
            for b in (binding.start, binding.end):
                for cm in (chain_mode.boundary, chain_mode.cycle):
                    for tm in (
                        tuple_mode.normal,
                        tuple_mode.lossy,
                        tuple_mode.redundant,
                    ):
                        with self.subTest(
                            data=data, binding=b, chain_mode=cm, tuple_mode=tm
                        ):
                            CS = congenerics_sequences(data)
                            chains = congenerics_intervals_chains(CS, b, cm)
                            result = intervals_tuples(chains, b, tm)
                            expected_rows = [
                                partials_intervals_tuple(chains[j], b, tm)
                                for j in range(chains.shape[0])
                            ]
                            width = max((len(row) for row in expected_rows), default=0)
                            assert result.shape == (chains.shape[0], width)
                            for j, expected in enumerate(expected_rows):
                                np.testing.assert_array_equal(
                                    result[j, : len(expected)], expected
                                )
                                assert (result[j, len(expected) :] == 0).all()

    def test_chain_mode_independently_affects_result(self):
        CS = congenerics_sequences(["a", "b", "a"])
        chains_boundary = congenerics_intervals_chains(
            CS, binding.start, chain_mode.boundary
        )
        chains_cycle = congenerics_intervals_chains(CS, binding.start, chain_mode.cycle)
        t_boundary = intervals_tuples(chains_boundary, binding.start, tuple_mode.normal)
        t_cycle = intervals_tuples(chains_cycle, binding.start, tuple_mode.normal)
        assert not np.array_equal(t_boundary, t_cycle)

    def test_invalid_binding_raises(self):
        CS = congenerics_sequences(["a", "b"])
        chains = congenerics_intervals_chains(CS, binding.start, chain_mode.boundary)
        with pytest.raises(ValueError):
            intervals_tuples(chains, 999, tuple_mode.normal)

    def test_invalid_tuple_mode_raises(self):
        CS = congenerics_sequences(["a", "b"])
        chains = congenerics_intervals_chains(CS, binding.start, chain_mode.boundary)
        with pytest.raises(ValueError):
            intervals_tuples(chains, binding.start, 999)

    def test_empty_input(self):
        CS = congenerics_sequences([])
        chains = congenerics_intervals_chains(CS, binding.start, chain_mode.boundary)
        result = intervals_tuples(chains, binding.start, tuple_mode.normal)
        assert result.shape == (0, 0)
