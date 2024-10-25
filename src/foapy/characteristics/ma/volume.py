import numpy as np


def volume(intervals):
    """
    Calculation volume of sequence.
    Volume is the product of the elements of the intervals of the sequence.

    Parameters
    ----------
    X: two-dimensional array
        Source array sequence.

    Returns
    -------
    result: array.

    Examples
    --------

    ----1----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [16  3  3]

    ----2----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.normal)
    >>> b
    [16 12  6]

    ----3----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.end,  mode.normal)
    >>> b
    [16 36 30]

    ----4----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.redundant)
    >>> b
    [16 36 30]

    ----5----
    >>> a = ["B", "B", "A", "A", "C", "B", "A", "C", "C", "B"]
    >>> b = volume(X, binding.start, mode.cycle)
    >>> b
    [16 18 18]

    ----6----
    >>> a = ["B", "A"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [1 1]

    ----7----
    >>> a = ["B", "A", "C", "D"]
    >>> b = volume(X, binding.start, mode.lossy)
    >>> b
    [1 1 1 1]
    """

    return np.asanyarray([np.prod(line) for line in intervals])
