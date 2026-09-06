from unittest import TestCase

from foapy.core import chain_mode


class TestChainMode(TestCase):
    """
    Test chain_mode enum attributes.
    """

    def test_boundary_value(self):
        self.assertEqual(chain_mode.boundary, 1)

    def test_cycle_value(self):
        self.assertEqual(chain_mode.cycle, 2)

    def test_boundary_and_cycle_are_different(self):
        self.assertNotEqual(chain_mode.boundary, chain_mode.cycle)

    def test_boundary_is_int(self):
        self.assertIsInstance(chain_mode.boundary, int)

    def test_cycle_is_int(self):
        self.assertIsInstance(chain_mode.cycle, int)
