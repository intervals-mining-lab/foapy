from unittest import TestCase

import numpy as np
import pytest

from foapy import binding, chain_mode, tuple_mode


class TestEnumNamespaceNotConstructable(TestCase):
    """
    Verify that binding, chain_mode, and tuple_mode cannot be instantiated.

    These types are named-constant namespaces. Calling them as constructors
    must raise TypeError. Their class attributes remain accessible.
    """

    # -------------------------------------------------------------------------
    # binding — not constructable
    # -------------------------------------------------------------------------

    def test_binding_not_constructable(self):
        with pytest.raises(TypeError):
            binding()

    def test_binding_not_constructable_with_chain(self):
        with pytest.raises(TypeError):
            binding(np.array([1, 2, 2], dtype=np.intp))

    def test_binding_not_constructable_with_int(self):
        with pytest.raises(TypeError):
            binding(1)

    # -------------------------------------------------------------------------
    # chain_mode — not constructable
    # -------------------------------------------------------------------------

    def test_chain_mode_not_constructable(self):
        with pytest.raises(TypeError):
            chain_mode()

    def test_chain_mode_not_constructable_with_arg(self):
        with pytest.raises(TypeError):
            chain_mode("boundary")

    # -------------------------------------------------------------------------
    # tuple_mode — not constructable
    # -------------------------------------------------------------------------

    def test_tuple_mode_not_constructable(self):
        with pytest.raises(TypeError):
            tuple_mode()

    def test_tuple_mode_not_constructable_with_arg(self):
        with pytest.raises(TypeError):
            tuple_mode(1)

    # -------------------------------------------------------------------------
    # Named constants remain accessible
    # -------------------------------------------------------------------------

    def test_binding_constants_accessible(self):
        self.assertEqual(binding.start, 1)
        self.assertEqual(binding.end, 2)

    def test_chain_mode_constants_accessible(self):
        self.assertEqual(chain_mode.boundary, 1)
        self.assertEqual(chain_mode.cycle, 2)

    def test_tuple_mode_constants_accessible(self):
        self.assertEqual(tuple_mode.lossy, 1)
        self.assertEqual(tuple_mode.normal, 2)
        self.assertEqual(tuple_mode.redundant, 3)
