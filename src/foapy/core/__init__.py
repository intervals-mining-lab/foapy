import sys

# We first need to detect if we're being called as part of the numpy setup
# procedure itself in a reliable manner.
try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from foapy.core source directory.\n")
else:
    # isort: off
    from ._alphabet import alphabet  # noqa: F401
    from ._binding import binding  # noqa: F401
    from ._mode import mode  # noqa: F401
    from ._intervals_chain import intervals_chain  # noqa: F401
    from ._intervals_tuple import intervals_tuple  # noqa: F401
    from ._intervals_distribution import intervals_distribution  # noqa: F401
    from ._intervals import intervals  # noqa: F401
    from ._order import order  # noqa: F401

    # isort: on

    __all__ = list({"binding", "mode", "intervals", "order", "alphabet",
                    "intervals_chain", "intervals_tuple", "intervals_distribution"})

    def __dir__():
        return __all__
