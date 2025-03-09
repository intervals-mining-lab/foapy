import numpy as np


def volume(intervals, dtype=None):
    """
    Calculates average geometric value of intervals lengths.

    $$ V=\\prod_{i=1}^{n} \\Delta_{i}$$

    where \\( \\Delta_{i} \\) represents each interval and \\( n \\)
    is the total number of intervals.

    Parameters
    ----------
    intervals : array_like
        An array of intervals
    dtype : dtype, optional
        The dtype of the output.

    Returns
    -------
    : float
        The volume of the input array of intervals.

    Examples
    --------

    Calculate the geometric mean of intervals of a sequence.

    ``` py linenums="1"
    import foapy

    source = ['a', 'b', 'a', 'c', 'a', 'd']
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)
    result = foapy.characteristics.volume(intervals)
    print(result)
    # 192
    ```

    Improve precision and avoid overflow by specifying a dtype.

    ``` py linenums="1"
    import foapy
    import numpy as np

    alphabet = np.arange(0, 200)
    source = np.random.choice(alphabet, 1000)
    intervals = foapy.intervals(source, foapy.binding.start, foapy.mode.normal)

    result_A = foapy.characteristics.volume(intervals)
    result_B = foapy.characteristics.volume(intervals, dtype=np.float128)
    print(result_A)
    # 0
    print(result_B)
    # 5.0039140361650821106e+1951
    ```

    """  # noqa: W605

    return np.prod(intervals, dtype=dtype)
