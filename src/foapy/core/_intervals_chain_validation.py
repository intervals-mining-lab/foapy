from typing import Optional

import numpy as np
from numpy.typing import ArrayLike

from foapy.core._axis_transform import _axis_lanes
from foapy.core._factorize import _normalize_sequence_axis


def _are_valid_intervals_chain_lanes(lanes: np.ndarray) -> bool:
    """Validate a prepared lane batch; semantic checks will be added later."""
    return True


def is_valid_intervals_chain(chain: ArrayLike, *, axis: Optional[int] = None) -> bool:
    """Return whether every selected-axis lane is a valid interval chain."""
    if isinstance(chain, np.ndarray) and axis is None and chain.ndim == 1:
        return True

    data = chain if isinstance(chain, np.ndarray) else np.asanyarray(chain)

    if data.ndim == 1:
        if axis is not None:
            _normalize_sequence_axis(data, axis)
        return True

    if data.ndim == 2 and axis in {1, -1}:
        return bool(_are_valid_intervals_chain_lanes(data))

    _, _, lanes = _axis_lanes(data, axis)
    return bool(_are_valid_intervals_chain_lanes(lanes))
