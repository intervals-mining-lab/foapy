from unittest import TestCase

import foapy
import foapy.congenerics as congenerics


class TestCongenericsPackageBoundary(TestCase):
    """
    foapy.congenerics MUST expose the six pipeline functions plus the
    characteristics subpackage, MUST NOT add them to the top-level foapy
    namespace, and MUST NOT expose an inverse/reconstruction function.
    """

    EXPECTED = {
        "sequences",
        "alphabet",
        "order",
        "intervals_chains",
        "intervals_tuples",
        "intervals_distributions",
        "characteristics",
    }

    def test_submodule_exposes_exactly_six_functions(self):
        assert set(congenerics.__all__) == self.EXPECTED
        for name in self.EXPECTED:
            assert hasattr(congenerics, name)

    def test_functions_not_added_at_top_level(self):
        # "order"/"alphabet" exist at top level from foapy.core (not congenerics).
        # "characteristics" exists at top level as foapy.characteristics.
        top_level_ok = {"order", "alphabet", "characteristics"}
        for name in self.EXPECTED:
            assert not hasattr(foapy, name) or name in top_level_ok
        # Verify top-level implementations are from core, not congenerics.
        assert foapy.order is not congenerics.order
        assert foapy.alphabet is not congenerics.alphabet
        assert foapy.characteristics is not congenerics.characteristics

    def test_no_inverse_function_present(self):
        for name in dir(congenerics):
            assert "inverse" not in name.lower()
            assert "reconstruct" not in name.lower()
