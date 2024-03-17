import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.ma_alphabet import ma_alphabet


class TestMaFunctions:
    """
    Test functions for masked_arrays
    """

    def test_ma_alphabet(self):
        """Test list of unique masked_array elements"""
        # ----test_1----
        assert_equal(
            ma_alphabet(
                ma.masked_array(["a", "c", "c", "e", "d", "a"], [0, 0, 0, 1, 0, 0])
            ),
            ma.masked_array(["a", "c", ma.masked, "d"]),
        )

        # ----test_2----
        assert_equal(
            ma_alphabet(
                ma.masked_array(["a", "c", "c", "e", "d", "a"], [0, 0, 0, 0, 0, 0])
            ),
            ma.masked_array(["a", "c", "e", "d"]),
        )

        # ----test_3----
        assert_equal(
            ma_alphabet(ma.masked_array([1, 2, 2, 3, 4, 1], [0, 0, 0, 0, 0, 0])),
            ma.masked_array([1, 2, 3, 4]),
        )

        # ----test_4----
        assert_equal(ma_alphabet(ma.masked_array([], [])), [])

        # ----test_5----
        assert_equal(
            ma_alphabet(
                ma.masked_array(
                    ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
                    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                )
            ),
            ma.masked_array(["a", ma.masked, "c"]),
        )

        # ----test_6----
        assert_equal(
            ma_alphabet(
                ma.masked_array(
                    ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
                    [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                )
            ),
            ma.masked_array(["a", ma.masked]),
        )

        # ----test_7----
        assert_equal(
            ma_alphabet(
                ma.masked_array(
                    ["a", "b", "c", "a", "b", "c", "c", "c", "b", "a", "c", "b", "c"],
                    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                )
            ),
            Exception,
        )
