from typing import Optional

import numpy as np
from numpy.typing import ArrayLike

from foapy.core._axis_transform import _axis_lanes
from foapy.core._factorize import _normalize_sequence_axis


def _is_valid_intervals_chain_1d(chain: np.ndarray) -> bool:
    """Validate one interval chain; semantic checks will be added later."""
    return True


def is_valid_intervals_chain(chain: ArrayLike, *, axis: Optional[int] = None) -> bool:
    """Return whether every selected-axis lane is a valid interval chain."""
    data = np.asanyarray(chain)

    if data.ndim == 1:
        _normalize_sequence_axis(data, axis)
        return bool(_is_valid_intervals_chain_1d(data))

    _, _, lanes = _axis_lanes(data, axis)
    return bool(all(_is_valid_intervals_chain_1d(lane) for lane in lanes))
