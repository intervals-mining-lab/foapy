import numpy as np


def identifying_information(intervals_grouped):
    """
    Calculation identifying information (Amount of Information / Entropy)
     of intervals grouped by element.

    $$H=\\frac {1} {n} * \\sum_{j=1}^{m}{(n_j * \\log_2 \\sum_{i=1}^{n_j} \\frac{\\Delta_{ij}}{n_j})}$$

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
        The identifying information of the input array of intervals_grouped.

    Examples
    --------

    Calculate the identifying information of intervals_grouped of a sequence.

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

    result = foapy.characteristics.identifying_information(intervals_grouped)
    print(result)
    # 1.299309880536629
    ```
    """  # noqa: E501

    total_elements = np.concatenate(intervals_grouped)

    n = len(total_elements)

    identifying_information_values = []

    for interval in intervals_grouped:
        n_j = len(interval)
        if n_j == 0:  # Check for empty interval
            partial_identifying_information = 0
        else:
            average_value = np.sum(interval) / n_j
            log_average = np.log2(average_value)
            partial_identifying_information = n_j / n * log_average

        identifying_information_values.append(partial_identifying_information)

    return np.sum(identifying_information_values)
