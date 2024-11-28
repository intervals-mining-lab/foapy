import numpy as np


def entropy(intervals):
    """
    Calculation entropy of sequence.

    Entropy (Amount of Information / Amount of identifying information)
    characteristic for given intervals.

    -----

    param name = "intervals" (sequence of intervals).

    -----

    total_elements - сombine all intervals into one array.

    -----

    length_uniform_sequence - total number of intervals in the sequence.

    -----

    proportion - share of elements of the current interval from the total number.

    -----

    average_value - arithmetic mean of elements in a uniform interval.

    -----

    log_average - logarithm of the arithmetic mean to base 2.

    -----

    partial_entropy - partial entropy for the current uniform interval.

    """
    total_elements = np.concatenate(intervals)

    length_uniform_sequence = len(total_elements)

    entropy_values = []

    for interval in intervals:

        proportion = len(interval) / length_uniform_sequence

        average_value = np.sum(interval) / len(interval)

        log_average = np.log2(average_value)

        partial_entropy = proportion * log_average

        entropy_values.append(partial_entropy)

    return np.sum(entropy_values)
