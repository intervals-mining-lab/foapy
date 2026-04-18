from foapy.core._intervals_tuple import intervals_tuple as core_intervals_tuple


def intervals_tuple(chain, binding: int, tuple_mode: int):
    """
    Apply a boundary handling strategy to an intervals chain.

    Delegates directly to :func:`foapy.core.intervals_tuple`.  Chain values
    are never masked, so no masked-array handling is needed.

    Parameters
    ----------
    chain : array_like
        A 1-D intervals chain (plain ndarray).
    binding : int
        ``binding.start`` (1) — chain was produced left-to-right.
        ``binding.end`` (2) — chain was produced right-to-left.
    tuple_mode : int
        ``tuple_mode.lossy``, ``tuple_mode.normal``, or
        ``tuple_mode.redundant``.

    Returns
    -------
    ndarray
        Plain 1-D integer array of boundary-adjusted intervals.
    """
    return core_intervals_tuple(chain, binding, tuple_mode)
