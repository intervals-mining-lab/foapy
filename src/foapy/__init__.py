import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError


# We first need to detect if we're being called as part of the numpy setup
# procedure itself in a reliable manner.
try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from foapy source directory.\n")
else:
    from foapy.core import alphabet  # noqa: F401
    from foapy.core import binding  # noqa: F401
    from foapy.core import intervals  # noqa: F401
    from foapy.core import mode  # noqa: F401
    from foapy.core import order  # noqa: F401

    # public submodules are imported lazily, therefore are accessible from
    # __getattr__. Note that `distutils` (deprecated) and `array_api`
    # (experimental label) are not added here, because `from foapy import *`
    # must not raise any warnings - that's too disruptive.
    __foapy_submodules__ = {"ma", "exceptions", "core", "characteristics"}

    __all__ = list(
        __foapy_submodules__
        | {"order", "intervals", "alphabet", "binding", "mode"}
        | {"__version__", "__array_namespace_info__"}
    )

    def __getattr__(attr):
        if attr == "core":
            import foapy.core as core

            return core

        if attr == "characteristics":
            import foapy.characteristics as characteristics

            return characteristics

        if attr == "exceptions":
            import foapy.exceptions as exceptions

            return exceptions
        if attr == "ma":
            import foapy.ma as ma

            return ma

        raise AttributeError(
            "module {!r} has no attribute " "{!r}".format(__name__, attr)
        )

    def __dir__():
        public_symbols = globals().keys() | __foapy_submodules__
        public_symbols += {
            "exceptions" "ma",
            "order",
            "intervals",
            "alphabet",
            "binding",
            "mode",
            "version",
        }
        return list(public_symbols)
