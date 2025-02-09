import numpy as np


def descriptive_information(intervals_grouped):
    """
    Calculation descriptive information of intervals grouped by element.

    $$D=\\prod_{j=1}^{m}{\\left(\\sum_{i=1}^{n_j}{\\frac{\\Delta_{ij}}{n_j}}\\right)^{\\frac{n_j}{n}}}$$

    where \\( m \\) is count of groups (alphabet power), \\( n_j \\) is count of intervals in group \\( j \\),
    \\( \\Delta_{ij} \\) represents an interval at index \\( i \\) in group \\( j \\) and \\( n \\) is total count of intervals across all groups.

    $$n=\\sum_{j=1}^{m}{n_j} $$

    Parameters
    ----------
    intervals_grouped : array_like
        An array of intervals grouped by element

    Returns
    -------
    : float
        The descriptive information of the input array of intervals_grouped.

    Examples
    --------

    Calculate the descriptive information of intervals_grouped of a sequence.

    ``` py linenums="1"
    import foapy

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    order = foapy.ma.order(source)
    print(order)

    #[[0 -- 0 -- 0 --]
    # [-- 1 -- -- -- --]
    # [-- -- -- 2 -- --]
    # [-- -- -- -- -- 3]]

    intervals_grouped = foapy.ma.intervals(order, foapy.binding.start, foapy.mode.normal)

    print(intervals_grouped)
    # [
    #    array([1, 2, 2]),
    #    array([2]),
    #    array([4]),
    #    array([6])
    # ]

    # m = 4
    # n_0 = 3
    # n_1 = 1
    # n_2 = 1
    # n_3 = 1
    # n = 6

    result = foapy.characteristics.descriptive_information(intervals_grouped)
    print(result)
    # 2.4611112617624173
    ```
    """  # noqa: E501
    from foapy.characteristics import identifying_information

    return np.power(2, identifying_information(intervals_grouped))
