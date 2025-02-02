class mode:
    """
    Mode enumeration used to determinate handling the intervals at the sequence boundaries.

    Examples
    ----------

    See [foapy.intervals()][foapy.intervals] function for code examples using modes.

    Example how different modes handle intervals are extracted when binding.start

    === "mode.normal"

        |        |  b |  a |  b |  c |  b |
        |:------:|:--:|:--:|:--:|:--:|:--:|
        | b      |  1 | -> |  2 | -> |  2 |
        | a      | -> |  2 |    |    |    |
        | c      | -> | -> | -> |  4 |    |
        | result |  1 |  2 |  2 |  4 |  2 |

    === "mode.cycle"

        |        | transition |  a |  b |  c |  b |  b | transition |
        |:------:|:----------:|:--:|:--:|:--:|:--:|:--:|:----------:|
        | b      |     (1)    |  1 | -> |  2 | -> |  2 |     (1)    |
        | a      |     (2)    | -> |  5 | -> | -> | -> |     (2)    |
        | c      |     (3)    | -> | -> | -> |  5 | -> |     (3)    |
        | result |            |  1 |  5 |  2 |  5 |  2 |            |

    === "mode.lossy"

        |        |  b |  a |  b |  c |  b |
        |:------:|:--:|:--:|:--:|:--:|:--:|
        | b      |  x | -> |  2 | -> |  2 |
        | a      | -> |  x |    |    |    |
        | c      | -> | -> | -> |  x |    |
        | result |    |    |  2 |    |  2 |

    === "mode.redundant"

        |        |  a |  b |  c |  b |  b | end   |
        |:------:|:--:|:--:|:--:|:--:|:--:|:-----:|
        | b      |  1 | -> |  2 | -> |  2 | 1     |
        | a      | -> |  2 | -> | -> | -> | 4     |
        | c      | -> | -> | -> |  4 | -> | 2     |
        | result |  1 |  2 |  2 |  4 |  2 | 1 4 2 |


    """  # noqa: E501

    lossy: int = 1
    """
    Ignore boundary intervals
    """

    normal: int = 2
    """
    Include first/last boundary interval based on binding
    """

    cycle: int = 3
    """
    Sumarize boundary intervals as one cyclic interval
    """

    redundant: int = 4
    """
    Include both (first and last) boundary intervals
    """
