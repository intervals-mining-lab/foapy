# Migration Guide: From `intervals()` to the Decomposed Pipeline

**Branch**: `003-cleanup-intervals-pipeline` | **Date**: 2026-04-19

## Overview

After this cleanup, `foapy.intervals`, `foapy.mode`, and `foapy.is_valid_intervals_chain` are no longer part of the public API. This guide shows how to update existing code to use the decomposed pipeline.

---

## Step 1: Replace the import

**Before:**
```python
from foapy import intervals, mode, binding
```

**After:**
```python
from foapy import intervals_chain, intervals_tuple, chain_mode, tuple_mode, binding
```

---

## Step 2: Replace the call

Use the mode mapping table to find the correct `chain_mode` + `tuple_mode` pair for each old `mode` value.

### `mode.lossy` → `chain_mode.boundary` + `tuple_mode.lossy`

```python
# Before
result = intervals(X, binding.start, mode.lossy)

# After
result = intervals_tuple(
    intervals_chain(X, binding.start, chain_mode.boundary),
    binding.start,
    tuple_mode.lossy,
)
```

### `mode.normal` → `chain_mode.boundary` + `tuple_mode.normal`

```python
# Before
result = intervals(X, binding.start, mode.normal)

# After
result = intervals_tuple(
    intervals_chain(X, binding.start, chain_mode.boundary),
    binding.start,
    tuple_mode.normal,
)
```

### `mode.cycle` → `chain_mode.cycle` + `tuple_mode.normal`

```python
# Before
result = intervals(X, binding.start, mode.cycle)

# After
result = intervals_tuple(
    intervals_chain(X, binding.start, chain_mode.cycle),
    binding.start,
    tuple_mode.normal,
)
```

### `mode.redundant` → `chain_mode.boundary` + `tuple_mode.redundant`

```python
# Before
result = intervals(X, binding.start, mode.redundant)

# After
result = intervals_tuple(
    intervals_chain(X, binding.start, chain_mode.boundary),
    binding.start,
    tuple_mode.redundant,
)
```

---

## Step 3: Remove `is_valid_intervals_chain` calls

`is_valid_intervals_chain` has been removed (deferred feature). If your code calls it, remove the call. A replacement with a clear specification will be provided in a future release.

---

## New Combinations Available

The decomposed pipeline also enables combinations that were not possible with the old `mode` enum:

| New combination | Meaning |
|----------------|---------|
| `chain_mode.cycle` + `tuple_mode.lossy` | Cyclic chain with boundary intervals dropped |
| `chain_mode.cycle` + `tuple_mode.redundant` | Cyclic chain with both boundary components |

---

## Reference: Fundamentals Documentation

- **`intervals_chain`** — [Intervals Chain](../docs/fundamentals/order/intervals_chain/index.md): bounded and cycled variants
- **`chain_mode`** — [Bounded](../docs/fundamentals/order/intervals_chain/bounded.md) | [Cycled](../docs/fundamentals/order/intervals_chain/cycled.md)
- **`intervals_tuple` / `tuple_mode`** — [Intervals Distribution](../docs/fundamentals/order/intervals_distribution/index.md): lossy, normal, redundant
- **`intervals_distribution`** — [Intervals Distribution index](../docs/fundamentals/order/intervals_distribution/index.md)
