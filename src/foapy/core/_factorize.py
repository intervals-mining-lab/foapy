from typing import Optional, Tuple

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.exceptions import Not1DArrayException

try:
    from numpy.lib.array_utils import normalize_axis_index
except ImportError:  # NumPy < 2.0
    from numpy.core.multiarray import normalize_axis_index


def _normalize_sequence_axis(data: ndarray, axis: Optional[int]) -> int:
    """Validate an input sequence and return its normalized sequence axis."""
    if data.ndim == 0:
        raise Not1DArrayException(
            {"message": "Incorrect array form. Expected d1 array, exists 0"}
        )

    if axis is None:
        if data.ndim != 1:
            raise Not1DArrayException(
                {
                    "message": (
                        "Incorrect array form. Expected d1 array, "
                        f"exists {data.ndim}"
                    )
                }
            )
        return 0

    return normalize_axis_index(axis, data.ndim)


def _factorize_1d(data: ndarray) -> Tuple[ndarray, ndarray]:
    """Preserve the original scalar factorization algorithm and semantics."""
    perm = data.argsort(kind="mergesort")

    unique_mask = np.empty(data.shape, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = data[perm[1:]] != data[perm[:-1]]

    alphabet_mask = np.zeros_like(unique_mask)
    alphabet_mask[:1] = True
    alphabet_mask[perm[unique_mask]] = True

    power = np.count_nonzero(unique_mask)

    inverse_perm = np.empty(data.shape, dtype=np.intp)
    inverse_perm[perm] = np.arange(data.shape[0], dtype=np.intp)

    sorted_order = np.cumsum(unique_mask, dtype=np.intp) - 1
    sorted_to_stable = np.empty(power, dtype=np.intp)
    sorted_to_stable[sorted_order[inverse_perm][alphabet_mask]] = np.arange(
        power, dtype=np.intp
    )

    order = sorted_to_stable[sorted_order][inverse_perm]
    return order, data[alphabet_mask]


def stable_factorize(
    X: ArrayLike, axis: Optional[int] = None
) -> Tuple[ndarray, ndarray]:
    """Factorize scalar or orthogonal-slice elements in first-appearance order."""
    data = np.asanyarray(X)
    normalized_axis = _normalize_sequence_axis(data, axis)

    if data.ndim == 1:
        return _factorize_1d(data)

    moved = np.moveaxis(data, normalized_axis, 0)
    sequence_length = moved.shape[0]

    if sequence_length == 0:
        return np.array([], dtype=np.intp), data.copy()

    # With no scalar fields every orthogonal slice is the same empty element.
    if moved[0].size == 0:
        order = np.zeros(sequence_length, dtype=np.intp)
        alphabet = np.take(data, [0], axis=normalized_axis)
        return order, alphabet

    sorted_alphabet, first_indices, sorted_inverse = np.unique(
        data,
        return_index=True,
        return_inverse=True,
        axis=normalized_axis,
    )

    stable_to_sorted = np.argsort(first_indices, kind="stable")
    alphabet = np.take(sorted_alphabet, stable_to_sorted, axis=normalized_axis)

    sorted_to_stable = np.empty(first_indices.size, dtype=np.intp)
    sorted_to_stable[stable_to_sorted] = np.arange(first_indices.size, dtype=np.intp)
    order = sorted_to_stable[np.asarray(sorted_inverse).reshape(-1)]

    return order, alphabet
