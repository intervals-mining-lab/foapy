import numpy as np
from numpy import ndarray


def intervals_distribution(tuple_result) -> ndarray:
    """
    Compute the frequency distribution of interval values.

    Given the output of :func:`intervals_tuple` (or any 1-D array of strictly
    positive integers), counts how many times each interval value occurs.
    The result is a 1-D array of length ``max(tuple_result)`` where
    ``result[i]`` is the count of interval value ``i + 1``.

    Parameters
    ----------
    tuple_result : array_like
        1-D array of strictly positive integers, typically produced by
        :func:`intervals_tuple`.

    Returns
    -------
    ndarray
        1-D integer array of length ``max(tuple_result)`` (or empty for
        empty input).  ``result[i]`` equals the number of elements in
        *tuple_result* with value ``i + 1``.

    Examples
    --------

    ``` py linenums="1"
    import numpy as np
    from foapy.core import intervals_distribution

    print(intervals_distribution(np.array([1, 2, 2, 4, 2])))
    # [1 3 0 1]

    print(intervals_distribution(np.array([])))
    # []
    ```
    """
    ar = np.asanyarray(tuple_result, dtype=np.intp)

    if ar.size == 0:
        return np.array([], dtype=np.intp)

    return np.bincount(ar - 1).astype(np.intp)
