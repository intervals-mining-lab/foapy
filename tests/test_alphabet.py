from unittest import TestCase

from foapy.alphabet import alphabet

"""Test list of unique array elements"""


class TestAlphabet(TestCase):

    def test_string_values(self):
        X = ["a", "c", "c", "e", "d", "a"]
        expected = ["a", "c", "e", "d"]
        exists = alphabet(X)
        self.assertEqual(expected, exists)

    def test_int_values(self):
        X = [0, 1, 2, 3, 4]
        expected = [0, 1, 2, 3, 4]
        exists = alphabet(X)
        self.assertEqual(expected, exists)

    def test_void(self):
        X = []
        expected = []
        exists = alphabet(X)
        self.assertEqual(expected, exists)
