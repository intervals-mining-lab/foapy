import sys

# We first need to detect if we're being called as part of the numpy setup
# procedure itself in a reliable manner.
try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write("Running from foapy.characteristics source directory.\n")
else:
    from ._arithmetic_mean import arithmetic_mean  # noqa: F401
    from ._average_remoteness import average_remoteness  # noqa: F401
    from ._depth import depth  # noqa: F401
    from ._descriptive_information import descriptive_information  # noqa: F401
    from ._geometric_mean import geometric_mean  # noqa: F401
    from ._identifying_information import identifying_information  # noqa: F401
    from ._regularity import regularity  # noqa: F401
    from ._uniformity import uniformity  # noqa: F401
    from ._volume import volume  # noqa: F401

    __all__ = list(
        {
            "volume",
            "arithmetic_mean",
            "geometric_mean",
            "average_remoteness",
            "depth",
            "descriptive_information",
            "identifying_information",
            "regularity",
            "uniformity",
        }
    )

    def __dir__():
        return __all__
