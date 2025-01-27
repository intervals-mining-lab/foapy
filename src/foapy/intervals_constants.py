class binding:
    """
    Binding enumeration used to determinate the direction of interval extraction.

    Attributes
    ----------
    start : int
        Left-to-right direction (from sequence start).
    end : int
        Right-to-left direction (from sequence end)

    Examples
    ----------

    See [foapy.intervals()][foapy.intervals.intervals] function for code examples using bindings.

    === "binding.start"

        |         |  b |  a |  b |  c | b |
        |:-------:|:--:|:--:|:--:|:--:|:-:|
        | b       |  1 | -> |  2 | -> | 2 |
        | a       | -> |  2 |    |    |   |
        | c       | -> | -> | -> |  4 |   |
        | result  |  1 |  2 |  2 |  4 | 2 |

    === "binding.end"

        |         |  b |  a |  b |  c |  b |
        |:-------:|:--:|:--:|:--:|:--:|:--:|
        | b       |  2 | <- |  2 | <- |  1 |
        | a       |    |  4 | <- | <- | <- |
        | c       |    |    |    |  2 | <- |
        | result  |  2 |  4 |  2 |  2 |  1 |


    """  # noqa: E501

    start = 1
    end = 2


class mode:
    """
    Mode enumeration used to determinate handling the intervals at the sequence boundaries.

    Attributes
    ----------
    normal : int
        Include first/last boundary interval based on binding
    cycle : int
        Sumarize boundary intervals as one cyclic interval
    lossy : int
        Ignore boundary intervals
    redundant : int
        Include both (first and last) boundary intervals

    Examples
    ----------

    See [foapy.intervals()][foapy.intervals.intervals] function for code examples using modes.

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

    lossy = 1
    normal = 2
    cycle = 3
    redundant = 4
