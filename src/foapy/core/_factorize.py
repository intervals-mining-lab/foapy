from typing import Optional, Tuple

import numpy as np
import xxhash
from numpy import ndarray
from numpy.typing import ArrayLike

from foapy.exceptions import Not1DArrayException

try:
    from numpy.lib.array_utils import normalize_axis_index
except ImportError:  # NumPy < 2.0
    from numpy.core.multiarray import normalize_axis_index


_HASH_MIN_RECORD_BYTES = 512


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


def _digest_record(record_bytes: ndarray) -> np.void:
    """Return the XXH3-128 digest for one contiguous byte record."""
    return np.void(xxhash.xxh3_128_digest(record_bytes))


def _digest_records(record_bytes: ndarray) -> ndarray:
    """Return one XXH3-128 digest for every byte record."""
    return np.apply_along_axis(_digest_record, 1, record_bytes)


def _slice_digests(moved: ndarray) -> Optional[ndarray]:
    """Build equality-compatible digest candidates for plain slice dtypes."""
    if moved.dtype.fields is not None or moved.dtype.kind not in "biufcmMSU":
        return None

    if moved[0].nbytes < _HASH_MIN_RECORD_BYTES:
        return None

    sequence_length = moved.shape[0]
    records = np.ascontiguousarray(moved.reshape(sequence_length, -1))

    # NumPy equality considers signed zeroes equal, while their byte strings
    # differ. Normalize only when needed so ordinary arrays remain views.
    if records.dtype.kind == "f":
        signed_zero = (records == 0) & np.signbit(records)
        if np.any(signed_zero):
            records = records.copy()
            records[signed_zero] = 0
    elif records.dtype.kind == "c":
        signed_real_zero = (records.real == 0) & np.signbit(records.real)
        signed_imag_zero = (records.imag == 0) & np.signbit(records.imag)
        if np.any(signed_real_zero) or np.any(signed_imag_zero):
            records = records.copy()
            records.real[signed_real_zero] = 0
            records.imag[signed_imag_zero] = 0

    record_bytes = records.view(np.uint8).reshape(sequence_length, -1)
    return _digest_records(record_bytes)


def _factorize_digest_candidates(
    digests: ndarray, moved: ndarray
) -> Optional[Tuple[ndarray, ndarray]]:
    """Factorize verified digest groups, or signal an exact fallback."""
    sequence_length = digests.size

    # Sorting makes every equal-digest group contiguous. ``unique_mask`` marks
    # the first record in each group; a false value therefore means that this
    # record and its predecessor have the same digest.
    perm = digests.argsort(kind="mergesort")
    sorted_digests = digests[perm]

    unique_mask = np.empty(sequence_length, dtype=bool)
    unique_mask[:1] = True
    unique_mask[1:] = sorted_digests[1:] != sorted_digests[:-1]

    # A digest match is only a candidate equality. Compare every adjacent pair
    # inside an equal-digest group across all fields of the original slices.
    # If a group contains two different slices, at least one adjacent pair is
    # unequal, so this detects a real hash collision without a Python loop.
    repeated = ~unique_mask[1:]
    if np.any(repeated):
        sorted_slices = np.take(moved, perm, axis=0)
        adjacent_equal = np.all(
            sorted_slices[1:] == sorted_slices[:-1],
            axis=tuple(range(1, sorted_slices.ndim)),
        )
        if np.any(repeated & ~adjacent_equal):
            # Returning None discards every hash-derived result. The caller
            # reruns exact NumPy factorization, so collisions cannot merge
            # distinct alphabet elements.
            return None

    alphabet_mask = np.zeros(sequence_length, dtype=bool)
    alphabet_mask[perm[unique_mask]] = True
    power = np.count_nonzero(unique_mask)

    sorted_order = np.cumsum(unique_mask, dtype=np.intp) - 1
    sorted_inverse = np.empty(sequence_length, dtype=np.intp)
    sorted_inverse[perm] = sorted_order

    stable_to_sorted = sorted_inverse[alphabet_mask]
    sorted_to_stable = np.empty(power, dtype=np.intp)
    sorted_to_stable[stable_to_sorted] = np.arange(power, dtype=np.intp)
    order = sorted_to_stable[sorted_inverse]

    return order, alphabet_mask


def _factorize_unique_slices(data: ndarray, axis: int) -> Tuple[ndarray, ndarray]:
    """Factorize slices exactly through NumPy's structured-record path."""
    sorted_alphabet, first_indices, sorted_inverse = np.unique(
        data,
        return_index=True,
        return_inverse=True,
        axis=axis,
    )

    stable_to_sorted = np.argsort(first_indices, kind="stable")
    alphabet = np.take(sorted_alphabet, stable_to_sorted, axis=axis)

    sorted_to_stable = np.empty(first_indices.size, dtype=np.intp)
    sorted_to_stable[stable_to_sorted] = np.arange(first_indices.size, dtype=np.intp)
    order = sorted_to_stable[np.asarray(sorted_inverse).reshape(-1)]

    return order, alphabet


def _stable_factorize(
    X: ArrayLike, axis: Optional[int] = None
) -> Tuple[ndarray, ndarray]:
    """Factorize multidimensional slice elements in first-appearance order."""
    data = np.asanyarray(X)
    normalized_axis = _normalize_sequence_axis(data, axis)

    moved = np.moveaxis(data, normalized_axis, 0)
    sequence_length = moved.shape[0]

    if sequence_length == 0:
        return np.array([], dtype=np.intp), data.copy()

    # With no scalar fields every orthogonal slice is the same empty element.
    if moved[0].size == 0:
        order = np.zeros(sequence_length, dtype=np.intp)
        alphabet = np.take(data, [0], axis=normalized_axis)
        return order, alphabet

    digests = _slice_digests(moved)
    if digests is not None:
        factorization = _factorize_digest_candidates(digests, moved)
        if factorization is not None:
            order, alphabet_mask = factorization
            alphabet = np.compress(alphabet_mask, data, axis=normalized_axis)
            return order, alphabet

    # Unsupported dtypes, equality/byte-semantic mismatches (such as NaNs),
    # and detected XXH3 collisions all take this exact path.
    return _factorize_unique_slices(data, normalized_axis)
