from unittest import TestCase

import numpy as np

from foapy import binding, chain_mode, tuple_mode
from foapy.congenerics import intervals_chains as congenerics_intervals_chains
from foapy.congenerics import intervals_distributions
from foapy.congenerics import intervals_tuples as congenerics_intervals_tuples
from foapy.congenerics import sequences as congenerics_sequences
from foapy.core import intervals_distribution as core_intervals_distribution


class TestCongenericsIntervalsDistributions(TestCase):
    """
    Test foapy.congenerics.intervals_distributions(tuples).

    tuples is the output of foapy.congenerics.intervals_tuples(chains,
    binding, tuple_mode). Width is shared across all rows: the maximum
    interval value found in any row. Input padding is ignored, and rows whose
    own maximum is smaller are right-padded with 0.
    """

    def test_width_shared_across_rows(self):
        datasets = [
            ["a", "b", "a", "c", "b"],
            ["a", "a", "a"],
            ["a", "b", "c", "d"],
        ]
        for data in datasets:
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
                            tuples = congenerics_intervals_tuples(chains, b, tm)
                            result = intervals_distributions(tuples)
                            rows = [row[row != 0] for row in tuples]
                            expected_dists = [
                                core_intervals_distribution(row) for row in rows
                            ]
                            width = max(
                                (len(dist) for dist in expected_dists), default=0
                            )
                            assert result.shape == (tuples.shape[0], width)
                            for j, expected in enumerate(expected_dists):
                                np.testing.assert_array_equal(
                                    result[j, : len(expected)], expected
                                )
                                assert (result[j, len(expected) :] == 0).all()

    def test_padding_means_zero_occurrences(self):
        # 'a' occurs with interval spread 1..2, 'c' is a singleton
        # (max interval much larger) — 'a' row must be zero-padded to match.
        CS = congenerics_sequences(["a", "b", "a", "c"])
        chains = congenerics_intervals_chains(CS, binding.start, chain_mode.boundary)
        tuples = congenerics_intervals_tuples(chains, binding.start, tuple_mode.normal)
        result = intervals_distributions(tuples)
        row_a = result[0]
        assert row_a[-1] == 0

    def test_input_padding_is_ignored(self):
        tuples = np.array([[1, 2, 0], [3, 0, 0]], dtype=np.intp)
        result = intervals_distributions(tuples)
        np.testing.assert_array_equal(
            result,
            np.array([[1, 1, 0], [0, 0, 1]], dtype=np.intp),
        )

    def test_empty_input(self):
        CS = congenerics_sequences([])
        chains = congenerics_intervals_chains(CS, binding.start, chain_mode.boundary)
        tuples = congenerics_intervals_tuples(chains, binding.start, tuple_mode.normal)
        result = intervals_distributions(tuples)
        assert result.shape == (0, 0)

    def test_rows_with_only_padding_have_zero_width(self):
        tuples = np.zeros((2, 3), dtype=np.intp)
        result = intervals_distributions(tuples)
        assert result.shape == (2, 0)
        assert result.dtype == np.intp
