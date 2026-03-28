import numpy as np


class binding:
    """
    Binding enumeration used to determine the direction of interval extraction.

    When used as a callable ``binding(chain)``, infers the binding direction
    from the structural properties of an intervals chain (plain 1-D ndarray):

    - If the first element of the chain equals 1, the chain was built left-to-right
      (``binding.start``).
    - If the last element equals 1 (and the first does not), the chain was built
      right-to-left (``binding.end``).
    - For empty or ambiguous chains, returns ``binding.start`` by convention.

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
    To  sequence end (right-to-left direction).
    """

    def __new__(cls, chain):
        """
        Infer the binding direction from the structural properties of an intervals chain.  # noqa: E501

        The first element of a ``binding.start`` chain always equals 1 (the boundary
        interval of the sequence's first element). The last element of a ``binding.end``
        chain always equals 1. For empty or symmetric chains, returns ``binding.start``.

        Parameters
        ----------
        chain : array_like
            A 1-D intervals chain produced by ``intervals_chain``.

        Returns
        -------
        int
            ``binding.start`` or ``binding.end``.

        Raises
        ------
        ValueError
            When ``chain`` is not a 1-D array-like.
        """
        try:
            ar = np.asanyarray(chain, dtype=np.intp)
        except (TypeError, ValueError) as e:
            raise ValueError(
                {"message": "chain must be a 1-D array-like of integers."}
            ) from e

        if ar.ndim != 1:
            raise ValueError(
                {"message": "chain must be a 1-D array. Got ndim={}.".format(ar.ndim)}
            )

        if ar.size == 0:
            return cls.start

        if ar[-1] == 1 and ar[0] != 1:
            return cls.end

        return cls.start
