import sys

try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from foapy.congenerics source directory.\n")
else:
    from ._alphabet import alphabet  # noqa: F401
    from ._intervals_chains import intervals_chains  # noqa: F401
    from ._intervals_distributions import intervals_distributions  # noqa: F401
    from ._intervals_tuples import intervals_tuples  # noqa: F401
    from ._order import order  # noqa: F401
    from ._sequences import sequences  # noqa: F401

    __all__ = list(
        {
            "sequences",
            "alphabet",
            "order",
            "intervals_chains",
            "intervals_tuples",
            "intervals_distributions",
            "characteristics",
        }
    )

    def __getattr__(attr):
        if attr == "characteristics":
            import foapy.congenerics.characteristics as characteristics

            return characteristics

        raise AttributeError("module {!r} has no attribute {!r}".format(__name__, attr))
