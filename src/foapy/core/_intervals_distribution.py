import numpy as np
from numpy import ndarray

from foapy.core import intervals_tuple as _intervals_tuple  # noqa: F401


def intervals_distribution(tuple_result: ndarray) -> ndarray:
    """
    Calculate intervals distribution from an intervals tuple.

    An intervals distribution is an n-tuple of natural numbers where the
    index represents the interval length and the value is the count of
    its appearances in the intervals tuple.

    Caller is responsible for preparing the tuple_result correctly:
    - For mode.lossy: boundary intervals already removed by intervals_tuple
    - For mode.redundant: trailing intervals already appended by intervals_tuple
    - For mode.normal, mode.cycle: pass tuple_result as-is

    Parameters
    ----------
    tuple_result : ndarray
        Intervals tuple produced by intervals_tuple.

    Returns
    -------
    result : ndarray
        Array of length max(tuple_result) where result[i] is the count
        of interval value i+1 in the tuple.

    Examples
    --------
    >>> import numpy as np
    >>> from foapy import binding, mode
    >>> from foapy.core import intervals_chain
    >>> from foapy.core import intervals_tuple
    >>> from foapy.core import intervals_distribution
    >>> ar = np.asarray([2, 4, 2, 2, 4])

    From documentation example - chain [1, 2, 3, 2, 4, 6]:

    >>> intervals_distribution(np.array([1, 2, 3, 2, 4, 6]))
    array([1, 2, 1, 1, 0, 1])

    Normal mode:

    >>> chain = intervals_chain(ar, mode.normal)
    >>> tpl = intervals_tuple(ar, chain, mode.normal, binding.start)
    >>> intervals_distribution(tpl)
    array([2, 2, 1])

    Lossy mode — boundary intervals already removed:

    >>> chain = intervals_chain(ar, mode.lossy)
    >>> tpl = intervals_tuple(ar, chain, mode.lossy, binding.start)
    >>> intervals_distribution(tpl)
    array([1, 1, 1])

    Redundant mode — trailing intervals already appended:

    >>> chain = intervals_chain(ar, mode.redundant)
    >>> tpl = intervals_tuple(ar, chain, mode.redundant, binding.start)
    >>> intervals_distribution(tpl)
    array([2, 3, 1])

    Empty tuple:

    >>> intervals_distribution(np.array([]))
    array([])
    """

    if len(tuple_result) == 0:
        return np.array([], dtype=np.intp)

    max_interval = int(tuple_result.max())
    distribution = np.zeros(max_interval, dtype=np.intp)
    for interval in tuple_result:
        distribution[int(interval) - 1] += 1

    return distribution
