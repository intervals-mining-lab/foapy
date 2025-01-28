import numpy as np


def identifying_information(intervals):
    """
    Calculation identifying_information of sequence .

    Identifying Information (Amount of Information / Entropy)
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

    partial_identifying_information - partial identifying_information
    for the current uniform interval.

    """
    total_elements = np.concatenate(intervals)

    length_uniform_sequence = len(total_elements)

    identifying_information_values = []

    for interval in intervals:
        if len(interval) == 0:  # Check for empty interval
            partial_identifying_information = 0
        else:
            proportion = len(interval) / length_uniform_sequence

            if len(interval) == 0:  # Check for empty interval
                average_value = 0
            else:
                average_value = np.sum(interval) / len(interval)

            if average_value == 0:  # Check for zero mean
                log_average = 0
            else:
                log_average = np.log2(average_value)

            partial_identifying_information = proportion * log_average

        identifying_information_values.append(partial_identifying_information)

    return np.sum(identifying_information_values)
