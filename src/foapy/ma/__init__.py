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
    from ._alphabet import alphabet  # noqa: F401
    from ._intervals import intervals  # noqa: F401
    from ._order import order  # noqa: F401

    __all__ = list({"order", "intervals", "alphabet"})
