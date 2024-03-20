from unittest import TestCase

import numpy.ma as ma
from numpy.ma.testutils import assert_equal

from foapy.ma.alphabet import alphabet


class TestMaAlphabet(TestCase):
    """
    Test list of unique masked_array elements
    """

    def test_string_values_with_mask(self):
        assert_equal(
            alphabet(
                ma.masked_array(["a", "c", "c", "e", "d", "a"], [0, 0, 0, 1, 0, 0])
            ),
            ma.masked_array(["a", "c", "e", "d"], mask=[0, 0, 1, 0]),
        )

    def test_string_values_with_no_mask(self):
        assert_equal(
            alphabet(
                ma.masked_array(["a", "c", "c", "e", "d", "a"], [0, 0, 0, 0, 0, 0])
            ),
            ma.masked_array(["a", "c", "e", "d"], mask=[0, 0, 0, 0]),
        )

    def test_integer_values_with_no_mask(self):
        assert_equal(
            alphabet(ma.masked_array([1, 2, 2, 3, 4, 1], [0, 0, 0, 0, 0, 0])),
            ma.masked_array([1, 2, 3, 4], mask=[0, 0, 0, 0]),
        )

    def test_with_no_values(self):
        assert_equal(alphabet(ma.masked_array([], [])), [])

    def test_several_mask_obj(self):
        assert_equal(
            alphabet(
                ma.masked_array(
                    ["a", "b", "c", "c", "b", "a"],
                    [0, 1, 1, 1, 1, 0],
                )
            ),
            ma.masked_array(["a", "b", "c"], mask=[0, 1, 1]),
        )

    def test_with_exception(self):
        assert_equal(
            alphabet(
                ma.masked_array(
                    ["a", "b", "c", "a", "b", "c", "b", "a"],
                    [0, 1, 0, 0, 0, 0, 1, 0],
                )
            ),
            Exception,
        )
