import sys

# We first need to detect if we're being called as part of the numpy setup
# procedure itself in a reliable manner.
try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from numpy source directory.\n")
else:
    from .inconsistent_order import InconsistentOrderException  # noqa: F401
    from .not_1d_array import Not1DArrayException  # noqa: F401

    __all__ = list({"InconsistentOrderException", "Not1DArrayException"})
