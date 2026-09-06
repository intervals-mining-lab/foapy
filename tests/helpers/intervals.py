# Test-only helper. Not part of the public foapy API.
# Contains the retired intervals() function and mode enum preserved
# solely for pipeline equivalence tests.
from foapy.core._chain_mode import chain_mode
from foapy.core._intervals_chain import intervals_chain
from foapy.core._intervals_tuple import intervals_tuple
from foapy.core._tuple_mode import tuple_mode


class mode:
    lossy: int = 1
    normal: int = 2
    cycle: int = 3
    redundant: int = 4


def intervals(X, binding: int, mode_value: int):
    valid_modes = [mode.lossy, mode.normal, mode.cycle, mode.redundant]
    if mode_value not in valid_modes:
        raise ValueError(
            {"message": "Invalid mode value. Use mode.lossy,normal,cycle or redundant."}
        )

    if mode_value == mode.normal:
        return intervals_chain(X, binding, chain_mode.boundary)

    if mode_value == mode.cycle:
        return intervals_chain(X, binding, chain_mode.cycle)

    if mode_value == mode.lossy:
        return intervals_tuple(
            intervals_chain(X, binding, chain_mode.boundary), binding, tuple_mode.lossy
        )

    if mode_value == mode.redundant:
        return intervals_tuple(
            intervals_chain(X, binding, chain_mode.boundary),
            binding,
            tuple_mode.redundant,
        )
