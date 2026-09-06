import sys

try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from foapy source directory.\n")
else:
    from ._alphabet import alphabet  # noqa: F401
    from ._intervals_chain import intervals_chain  # noqa: F401
    from ._intervals_tuple import intervals_tuple  # noqa: F401
    from ._order import order  # noqa: F401

    __all__ = list(
        {
            "order",
            "alphabet",
            "intervals_chain",
            "intervals_tuple",
        }
    )
