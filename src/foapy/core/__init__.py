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
    from ._chain_mode import chain_mode  # noqa: F401
    from ._mode import mode  # noqa: F401
    from ._tuple_mode import tuple_mode  # noqa: F401
    from ._intervals import intervals  # noqa: F401
    from ._intervals_chain import intervals_chain  # noqa: F401
    from ._intervals_distribution import intervals_distribution  # noqa: F401
    from ._intervals_tuple import intervals_tuple  # noqa: F401
    from ._is_valid_intervals_chain import is_valid_intervals_chain  # noqa: F401
    from ._order import order  # noqa: F401

    # isort: on

    __all__ = list(
        {
            "binding",
            "chain_mode",
            "mode",
            "tuple_mode",
            "intervals",
            "intervals_chain",
            "intervals_distribution",
            "intervals_tuple",
            "is_valid_intervals_chain",
            "order",
            "alphabet",
        }
    )

    def __dir__():
        return __all__
