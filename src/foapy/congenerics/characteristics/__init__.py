import sys

try:
    __FOAPY_SETUP__
except NameError:
    __FOAPY_SETUP__ = False

if __FOAPY_SETUP__:
    sys.stderr.write(
        "Running from foapy.congenerics.characteristics source directory.\n"
    )
else:
    from ._arithmetic_means import arithmetic_means  # noqa: F401
    from ._average_remotenesses import average_remotenesses  # noqa: F401
    from ._depths import depths  # noqa: F401
    from ._descriptive_information import descriptive_information  # noqa: F401
    from ._geometric_means import geometric_means  # noqa: F401
    from ._identifying_information import identifying_information  # noqa: F401
    from ._identifying_informations import identifying_informations  # noqa: F401
    from ._periodicities import periodicities  # noqa: F401
    from ._regularity import regularity  # noqa: F401
    from ._uniformities import uniformities  # noqa: F401
    from ._uniformity import uniformity  # noqa: F401
    from ._volumes import volumes  # noqa: F401

    __all__ = list(
        {
            "descriptive_information",
            "identifying_information",
            "regularity",
            "uniformity",
            "arithmetic_means",
            "average_remotenesses",
            "depths",
            "geometric_means",
            "identifying_informations",
            "periodicities",
            "uniformities",
            "volumes",
        }
    )

    def __dir__():
        return __all__
