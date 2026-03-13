import numpy as np
from numpy import ndarray

from foapy.core import binding as constants_binding
from foapy.core import mode as constants_mode


def intervals_tuple(ar: ndarray, chain: ndarray, mode: int, binding: int) -> ndarray:
    """
    Convert an intervals chain into a final intervals tuple.

    Applies unchaining strategies to the raw intervals chain produced by
    [intervals_chain], handling boundary intervals according to the given mode.

    Parameters
    ----------
    ar : ndarray
        1-D array (already oriented for binding direction) used to compute
        trailing boundary intervals for [mode.redundant].
    chain : ndarray
        Raw intervals chain produced by [intervals_chain].
    mode : int
        One of [mode.lossy], [mode.normal], [mode.cycle], [mode.redundant].
    binding : int
        One of [binding.start], [binding.end]. Used to correctly order
        trailing boundary intervals for [mode.redundant].

    Returns
    -------
    result : ndarray
        Final intervals tuple.

    Examples
    --------
    >>> import numpy as np
    >>> from foapy.core import mode, binding
    >>> from foapy.core import intervals_chain
    >>> from foapy.core import intervals_tuple
    >>> ar = np.asarray(['b', 'a', 'b', 'c', 'b'])

    Normal mode — chain is returned as-is:

    >>> chain = intervals_chain(ar, mode.normal)
    >>> intervals_tuple(ar, chain, mode.normal)
    array([1, 2, 2, 4, 2])

    Lossy mode — boundary (zero) intervals are removed:

    >>> chain = intervals_chain(ar, mode.lossy)
    >>> intervals_tuple(ar, chain, mode.lossy)
    array([2, 2])

    Redundant mode — trailing boundary intervals are appended:

    >>> chain = intervals_chain(ar, mode.redundant)
    >>> intervals_tuple(ar, chain, mode.redundant)
    array([1, 2, 2, 4, 2, 4, 1, 2])
    """

    if mode == constants_mode.lossy:
        return chain[chain != 0]

    if mode == constants_mode.redundant:
        perm = ar.argsort(kind="mergesort")
        mask = np.empty(ar.shape[0] + 1, dtype=bool)
        mask[:1] = True
        mask[1:-1] = ar[perm[1:]] != ar[perm[:-1]]
        mask[-1:] = True
        last_mask = mask[1:]
        trailing = len(ar) - perm[last_mask]
        if binding == constants_binding.end:
            trailing = trailing[::-1]
        return np.concatenate((chain, trailing))

    return chain
