# Research: foapy.partials Package

**Date**: 2026-04-19 | **Branch**: `004-partials-package`

## Key Decisions

### 1. `partials.order()` Returns a 1-D Masked Array

**Decision**: Return a masked 1-D array of the same length as input (mask preserved).

**Rationale**: The partial-sequence semantics require output positions to align with input positions so callers can trace which gap position produced which result. `foapy.ma.order()` returns a 2-D matrix (one row per alphabet element) because its purpose is to represent the full occurrence matrix; `foapy.partials.order()` returns a 1-D array because the output is a direct replacement of the input sequence with alphabet indices.

**Alternatives considered**:
- 2-D masked matrix (rejected — not partial-sequence semantics; that is `foapy.ma` territory)
- Plain 1-D ndarray with -1 sentinel for gaps (rejected — forces callers to handle sentinel values; masked arrays are the standard numpy idiom for missing data)

### 2. Gaps Contribute to Interval Distances

**Decision**: In `partials.intervals_chain()`, interval distances are computed using actual positional indices in the full (uncompressed) array, so masked gaps between two occurrences of the same element increase the measured interval.

**Rationale**: This is the defining semantic of partial sequences per the FOA documentation: `[-, C, T, C, -, G]` produces intervals `[-, 2, 3, 2, -, 6]`, where C at position 3 has interval 2 (= 3 - 1), not 1 (which would be the compressed distance).

**Alternatives considered**:
- Compress first, compute intervals on compressed, map back (rejected — this is `foapy.ma` behavior; intervals would be wrong for partial sequences)

### 3. `intervals_tuple.lossy` Masks Rather Than Removes

**Decision**: `tuple_mode.lossy` produces an output of the **same length** as the input chain; positions identified as boundary intervals become additionally masked instead of being dropped.

**Rationale**: Preserving array length maintains positional alignment throughout the pipeline. Callers can always determine which original positions were boundary intervals by inspecting the output mask.

**Alternatives considered**:
- Drop positions and shrink the array (rejected — breaks positional alignment; core behavior is appropriate for plain arrays but not for positionally-indexed masked arrays)

### 4. `intervals_tuple.redundant` Appends Trailing Intervals

**Decision**: `tuple_mode.redundant` appends the k trailing intervals at the end of the array (output length = n + k), delegating to `core.intervals_tuple` on the compressed chain.

**Rationale**: Trailing intervals do not map to any original input position, so they cannot be placed at existing positions. Appending is the only semantically valid option. The output remains a masked array (appended trailing elements are unmasked).

**Alternatives considered**:
- Raise NotImplementedError (rejected — the spec requires all three tuple_modes to be supported)
- Place trailing at masked positions (rejected — conflates interval values with gap positions)

### 5. Plain Array Auto-Wrapping

**Decision**: All four functions call `numpy.ma.asarray(X)` as the first operation, which safely converts plain lists, plain ndarrays, or masked arrays to a masked array with no mask.

**Rationale**: Follows the `foapy.ma.intervals_chain()` pattern (`ma.asarray(X)`) and means callers who already use `foapy.core` don't need to explicitly construct masked arrays.

### 6. No `intervals_distribution` in Scope

**Decision**: `intervals_distribution` is excluded from `foapy.partials`.

**Rationale**: It operates on plain interval counts (frequency histogram), not on positionally-indexed arrays. It works identically on the output of `intervals_tuple` regardless of whether the chain came from core or partials. Users simply call `foapy.intervals_distribution(partials_chain.compressed())` directly.

### 7. Submodule Access Only

**Decision**: `foapy.partials` is exposed as a lazily-loaded submodule (via `__getattr__` in `foapy/__init__.py`); no functions are hoisted to `foapy.*`.

**Rationale**: Mirrors the `foapy.ma` pattern. Avoids naming conflicts with core functions (both packages have `order`, `alphabet`, etc.). Users import the specific sub-package they need.

## Implementation Patterns Reused from Existing Code

| Pattern | Source | Reused In |
|---------|--------|-----------|
| `ma.asarray(X)` auto-wrapping | `foapy/ma/_intervals_chain.py` | All four partials functions |
| `Not1DArrayException` on ndim > 1 | `foapy/core/_intervals_chain.py` | `order`, `intervals_chain` |
| `argsort(kind="mergesort")` for stable sort | `foapy/core/_intervals_chain.py` | `intervals_chain` |
| Boundary first/last group detection via boolean mask | `foapy/core/_intervals_chain.py` | `intervals_chain` |
| Inverse permutation via `inverse_perm[perm] = arange(n)` | `foapy/core/_intervals_chain.py` | `intervals_chain` |
| `ar > positions` boundary detection | `foapy/core/_intervals_tuple.py` | `intervals_tuple` (lossy) |
| Lazy `__getattr__` submodule loading | `foapy/__init__.py` | `foapy/__init__.py` update |
