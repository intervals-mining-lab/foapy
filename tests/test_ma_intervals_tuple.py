from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal

from foapy.core import intervals_tuple, tuple_mode


class TestMaIntervalsTuple(TestCase):
    """
    Test foapy.ma.intervals_tuple(chain, tuple_mode) -> ndarray.

    Delegates to core intervals_tuple; masked chain values are treated as
    plain integers (chain values are never masked).
    """

    def test_normal_matches_core(self):
        from foapy.ma import intervals_tuple as ma_intervals_tuple

        chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        assert_array_equal(
            ma_intervals_tuple(chain, tuple_mode.normal),
            intervals_tuple(chain, tuple_mode.normal),
        )

    def test_lossy_matches_core(self):
        from foapy.ma import intervals_tuple as ma_intervals_tuple

        chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        assert_array_equal(
            ma_intervals_tuple(chain, tuple_mode.lossy),
            intervals_tuple(chain, tuple_mode.lossy),
        )

    def test_redundant_matches_core(self):
        from foapy.ma import intervals_tuple as ma_intervals_tuple

        chain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
        assert_array_equal(
            ma_intervals_tuple(chain, tuple_mode.redundant),
            intervals_tuple(chain, tuple_mode.redundant),
        )

    def test_empty_chain(self):
        from foapy.ma import intervals_tuple as ma_intervals_tuple

        chain = np.array([], dtype=np.intp)
        assert_array_equal(
            ma_intervals_tuple(chain, tuple_mode.normal),
            np.array([], dtype=np.intp),
        )
