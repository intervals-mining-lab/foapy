import numpy as np

"""
Implementation of ordered set - alphabet of elements.
Alphabet is list of all unique elements in particular sequence.
Parametres
—--------
X: array
Array to get unique values.

Returns
—-----
result: array.

Examples
—------

"""


def alphabet(X) -> np.ndarray:
    result = []

    for i in X:
        if i not in result:
            result.append(i)

    return result


print("_______1_____")
X = ["a", "c", "c", "e", "d", "a"]
result = alphabet(X)
print(result)


print("_______2_____")
X = [0, 1, 2, 3, 4]
result = alphabet(X)
print(result)


print("_______3_____")
X = []
result = alphabet(X)
print(result)
