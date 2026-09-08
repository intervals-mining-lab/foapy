from typing import Optional, Tuple

import numpy as np
import numpy.ma as ma
from numpy.typing import ArrayLike

from foapy.core._factorize import _normalize_sequence_axis, stable_factorize


def stable_partial_factorize(
    X: ArrayLike, axis: Optional[int] = None
) -> Tuple[ma.MaskedArray, np.ndarray]:
    """Factorize present slices and preserve whole-slice gaps in the order."""
    data = ma.asarray(X)
    normalized_axis = _normalize_sequence_axis(data, axis)

    moved_mask = np.moveaxis(ma.getmaskarray(data), normalized_axis, 0)
    sequence_length = moved_mask.shape[0]
    field_count = int(np.prod(moved_mask.shape[1:], dtype=np.intp))

    if field_count == 0:
        gap_mask = np.zeros(sequence_length, dtype=bool)
    else:
        slice_masks = moved_mask.reshape(sequence_length, field_count)
        any_masked = slice_masks.any(axis=1)
        all_masked = slice_masks.all(axis=1)

        if np.any(any_masked != all_masked):
            raise ValueError(
                {
                    "message": (
                        "Each slice along axis must be wholly masked or "
                        "wholly unmasked."
                    )
                }
            )

        gap_mask = all_masked

    present = ~gap_mask
    present_data = np.compress(present, data.data, axis=normalized_axis)
    present_order, alphabet = stable_factorize(present_data, axis=normalized_axis)

    result_data = np.zeros(sequence_length, dtype=np.intp)
    result_data[present] = present_order
    result = ma.masked_array(result_data, mask=gap_mask)

    return result, alphabet
