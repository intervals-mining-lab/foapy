# API Contract: Cleanup Intervals Pipeline

**Branch**: `003-cleanup-intervals-pipeline` | **Date**: 2026-04-19

## Public API Diff

### Removed from `foapy` namespace

```python
# REMOVED — raises ImportError after this change
from foapy import intervals           # was: intervals(X, binding, mode) -> ndarray
from foapy import mode                # was: mode.lossy / mode.normal / mode.cycle / mode.redundant
from foapy import is_valid_intervals_chain  # was: is_valid_intervals_chain(chain) -> bool
```

### Removed from `foapy.ma` namespace

```python
# REMOVED — raises ImportError after this change
from foapy.ma import intervals        # was: intervals(X, binding, mode) -> list[ndarray]
```

### Unchanged in `foapy` namespace

```python
from foapy import intervals_chain      # intervals_chain(X, binding, chain_mode) -> ndarray
from foapy import intervals_tuple      # intervals_tuple(chain, binding, tuple_mode) -> ndarray
from foapy import intervals_distribution  # intervals_distribution(intervals_tuple) -> ndarray
from foapy import chain_mode           # chain_mode.boundary | chain_mode.cycle
from foapy import tuple_mode           # tuple_mode.lossy | tuple_mode.normal | tuple_mode.redundant
from foapy import binding              # binding.start | binding.end
from foapy import order                # order(X) -> ndarray
from foapy import alphabet             # alphabet(X) -> ndarray
```

### Unchanged in `foapy.ma` namespace

```python
from foapy.ma import intervals_chain
from foapy.ma import intervals_tuple
from foapy.ma import intervals_distribution
from foapy.ma import order
from foapy.ma import alphabet
```

---

## Mode Mapping Reference

The following table documents the equivalence between the retired `mode` enum and the decomposed pipeline. This is the contract verified by the equivalence test module.

| Old call | Decomposed equivalent |
|----------|----------------------|
| `intervals(X, b, mode.lossy)` | `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.lossy)` |
| `intervals(X, b, mode.normal)` | `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.normal)` |
| `intervals(X, b, mode.cycle)` | `intervals_tuple(intervals_chain(X, b, chain_mode.cycle), b, tuple_mode.normal)` |
| `intervals(X, b, mode.redundant)` | `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.redundant)` |

---

## Test-Helper Availability

The retired `intervals()` functions are available **only** within the test suite:

```python
# Available in tests ONLY — not a public API
from tests.helpers.intervals import intervals, mode
from tests.helpers.ma_intervals import intervals as ma_intervals
```

These helpers MUST NOT be imported from any production source file.
