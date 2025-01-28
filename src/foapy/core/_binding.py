class binding:
    """
    Binding enumeration used to determinate the direction of interval extraction.

    Examples
    ----------

    See [foapy.intervals()][foapy.intervals] function for code examples using bindings.

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

    start: int = 1
    """
    To sequence start (left-to-right direction).
    """

    end: int = 2
    """
    To  sequence end (right-to-left direction)
    """
