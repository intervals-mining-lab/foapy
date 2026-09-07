import numpy as np


def regularity(intervals_grouped, dtype=None):
    """
    Calculates regularity of intervals grouped by element of the alphabet.

    $$r= \\sqrt[n]{\\prod_{j=1}^{m} \\frac{
        \\prod_{j=1}^{n_j} \\Delta_{ij}}
        {{\\left(\\frac{1}{n_j}\\sum_{i=1}^{n_j}{\\Delta_{ij}}\\right)^{n_j}}
        }
    }$$

    where \\( m \\) is count of groups (alphabet power), \\( n_j \\) is count of intervals in group \\( j \\),
    \\( \\Delta_{ij} \\) represents an interval at index \\( i \\) in group \\( j \\) and \\( n \\) is total count of intervals across all groups.

    $$ n=\\sum_{j=1}^{m}{n_j} $$

    Parameters
    ----------
    intervals_grouped : array_like
        An array of intervals grouped by element
    dtype : dtype, optional
        The dtype of the output

    Returns
    -------
    : float
        The regularity of the input array of intervals_grouped.

    Examples
    --------

    Calculate the regularity of intervals_grouped of a sequence.

    ``` py linenums="1"
    import foapy
    import numpy as np

    source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
    CS = foapy.congenerics.sequences(source)
    chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
    tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
    intervals_grouped = [row[row != 0] for row in tuples]

    result = foapy.congenerics.characteristics.regularity(intervals_grouped)
    print(result)
    # 0.9759306487558016

    # Improve precision by specifying a dtype.
    result = foapy.congenerics.characteristics.regularity(intervals_grouped, dtype=np.longdouble)
    print(result)
    # 0.97593064875580153104
    ```
    """  # noqa: E501

    from foapy.characteristics import geometric_mean
    from foapy.congenerics.characteristics import descriptive_information

    total_elements = np.concatenate(intervals_grouped)
    g = geometric_mean(total_elements, dtype=dtype)
    D = descriptive_information(intervals_grouped, dtype=dtype)
    return g / D
