import numpy as np
from numpy import ndarray

from foapy.core import mode as constants_mode


def intervals_chain(ar: ndarray, mode: int) -> ndarray:
    """
    Build an intervals chain from a 1-D array.

    An intervals chain is an n-tuple of natural numbers representing the distance
    between equal elements in a sequence. This function encapsulates the core
    chain-building logic: given a 1-D array [ar] (already oriented for the chosen
    binding direction) and a [mode], it computes the raw intervals array before
    any binding-specific reversal is applied.

    The function supports four behavioural strategies at sequence boundaries:

    * **normal / bounded** ([mode.normal]) – the leading boundary interval
      (distance from the virtual start to the first occurrence) is included;
      the trailing boundary interval is not added.
    * **cyclic** ([mode.cycle]) – the leading and trailing boundary intervals
      are summed into a single interval placed at the position of the first
      occurrence, as if the sequence were circular.
    * **lossy** ([mode.lossy]) – boundary (first-occurrence) intervals are set
      to [0] so the caller can filter them out.
    * **redundant** ([mode.redundant]) – same as [mode.normal] for the chain itself;
      the caller is responsible for appending the trailing boundary intervals.

    Parameters
    ----------
    ar : ndarray
        1-D array whose intervals chain is to be built.  For [binding.end]
        the caller must reverse [ar] **before** passing it here, and reverse
        the result afterwards.
    mode : int
        One of [mode.lossy], [mode.normal], [mode.cycle],
        [mode.redundant].  Controls how boundary intervals are handled.

    Returns
    -------
    chain : ndarray
        Raw intervals array of the same length as [ar], in the original
        element order.  For [mode.lossy] the boundary zeros are still
        present; filtering is left to the caller.

    Notes
    -----
    This function is the low-level building block used by
    [foapy.intervals].  It does not validate [mode] or the shape
    of [ar] – validation is the responsibility of the caller.

    Examples
    --------
    Build a bounded (normal) intervals chain:

    >>> import numpy as np
    >>> from foapy.core import intervals_chain
    >>> from foapy.core import mode
    >>> ar = np.asarray(['b', 'a', 'b', 'c', 'b'])
    >>> intervals_chain(ar, mode.normal)
    array([1, 2, 2, 4, 2])

    Build a cyclic intervals chain (leading boundary becomes wrap-around sum):

    >>> intervals_chain(ar, mode.cycle)
    array([1, 5, 2, 5, 2])

    For lossy mode the first-occurrence intervals are zeroed out so the
    caller can filter them with [result][result != 0]:

    >>> intervals_chain(ar, mode.lossy)
    array([0, 0, 2, 0, 2])
    """

    perm = ar.argsort(kind="mergesort")

    mask = np.empty(ar.shape[0] + 1, dtype=bool)
    mask[:1] = True
    mask[1:-1] = ar[perm[1:]] != ar[perm[:-1]]
    mask[-1:] = True  # or mask[-1:] = True

    first_mask = mask[:-1]
    last_mask = mask[1:]

    chain = np.empty(ar.shape, dtype=np.intp)
    chain[1:] = perm[1:] - perm[:-1]

    delta = len(ar) - perm[last_mask] if mode == constants_mode.cycle else 1
    chain[first_mask] = perm[first_mask] + delta

    if mode == constants_mode.lossy:
        chain[first_mask] = 0

    inverse_perm = np.empty(ar.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(ar.shape[0])
    chain = chain[inverse_perm]

    return chain
