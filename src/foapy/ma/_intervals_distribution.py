from foapy.core._intervals_distribution import (
    intervals_distribution as core_intervals_distribution,
)


def intervals_distribution(tuple_result):
    """
    Compute the frequency distribution of interval values.

    Delegates directly to :func:`foapy.core.intervals_distribution`.

    Parameters
    ----------
    tuple_result : array_like
        1-D array of strictly positive integers.

    Returns
    -------
    ndarray
        1-D integer frequency array.
    """
    return core_intervals_distribution(tuple_result)
