from unittest import TestCase

from foapy.core import tuple_mode


class TestTupleMode(TestCase):
    """
    Test tuple_mode enum attributes.
    """

    def test_lossy_value(self):
        self.assertEqual(tuple_mode.lossy, 1)

    def test_normal_value(self):
        self.assertEqual(tuple_mode.normal, 2)

    def test_redundant_value(self):
        self.assertEqual(tuple_mode.redundant, 3)

    def test_all_values_are_different(self):
        self.assertNotEqual(tuple_mode.lossy, tuple_mode.normal)
        self.assertNotEqual(tuple_mode.lossy, tuple_mode.redundant)
        self.assertNotEqual(tuple_mode.normal, tuple_mode.redundant)

    def test_lossy_is_int(self):
        self.assertIsInstance(tuple_mode.lossy, int)

    def test_normal_is_int(self):
        self.assertIsInstance(tuple_mode.normal, int)

    def test_redundant_is_int(self):
        self.assertIsInstance(tuple_mode.redundant, int)
