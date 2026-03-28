from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy.core import intervals_distribution


class TestMaIntervalsDistribution(TestCase):
    """
    Test foapy.ma.intervals_distribution(tuple_result) -> ndarray.

    Delegates to core intervals_distribution.
    """

    def test_matches_core(self):
        from foapy.ma import intervals_distribution as ma_intervals_distribution

        chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        assert_array_equal(
            ma_intervals_distribution(chain),
            intervals_distribution(chain),
        )

    def test_empty(self):
        from foapy.ma import intervals_distribution as ma_intervals_distribution

        assert_array_equal(
            ma_intervals_distribution(np.array([], dtype=np.intp)),
            np.array([], dtype=np.intp),
        )
