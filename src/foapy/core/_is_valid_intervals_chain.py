import numpy as np


def is_valid_intervals_chain(chain) -> bool:
    """
    Return ``True`` if *chain* is a structurally valid 1-D intervals chain.

    A valid chain satisfies all of the following conditions:

    1. It is a 1-D array-like of integers (or empty).
    2. Every value is strictly positive (``>= 1``).
    3. Every value does not exceed the length of the chain (``<= n``).

    The function never raises; any input that cannot be interpreted as a 1-D
    integer array returns ``False``.

    Parameters
    ----------
    chain : array_like
        The candidate intervals chain to validate.

    Returns
    -------
    bool
        ``True`` if *chain* is a valid 1-D intervals chain, ``False``
        otherwise.

    Examples
    --------

    ``` py linenums="1"
    import numpy as np
    from foapy.core import is_valid_intervals_chain

    print(is_valid_intervals_chain(np.array([1, 2, 2, 4, 2])))  # True
    print(is_valid_intervals_chain(np.array([0, 1, 2])))         # False — zero
    print(is_valid_intervals_chain(np.array([[1, 2], [3, 4]])))  # False — 2-D
    print(is_valid_intervals_chain([]))                           # True — empty
    ```
    """
    try:
        ar = np.asanyarray(chain, dtype=np.intp)
    except (TypeError, ValueError):
        return False

    if ar.ndim != 1:
        return False

    if ar.size == 0:
        return True

    n = ar.size
    return bool(np.all(ar >= 1) and np.all(ar <= n))
