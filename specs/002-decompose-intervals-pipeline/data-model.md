# Data Model: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-03-28

## Entities

### chain_mode (enum class)

| Field    | Type | Value | Description |
|----------|------|-------|-------------|
| boundary | int  | 1     | Sequence is treated as finite and bounded; boundary intervals are distances from sequence edges to first/last occurrence |
| cycle    | int  | 2     | Sequence is treated as circular; leading and trailing boundary distances are summed into a single cyclic interval |

**Validation**: Consumer code MUST check value is in `{chain_mode.boundary, chain_mode.cycle}` before use.

---

### tuple_mode (enum class)

| Field     | Type | Value | Description |
|-----------|------|-------|-------------|
| lossy     | int  | 1     | Boundary intervals (first-occurrence distances) are excluded from the result |
| normal    | int  | 2     | One boundary interval is retained per element as produced by the chain |
| redundant | int  | 3     | Both leading and trailing boundary intervals are included |

**Validation**: Consumer code MUST check value is in `{tuple_mode.lossy, tuple_mode.normal, tuple_mode.redundant}`.

---

### Interval Chain (ndarray)

The return type of `intervals_chain`. A plain 1-D ndarray. `binding` and `chain_mode` are **not** embedded — callers must pass them explicitly to downstream functions.

| Property | Value |
|----------|-------|
| dtype    | intp (platform pointer-sized integer) |
| shape    | (n,) where n = len(X) |
| values   | Positive integers (≥ 1), each ≤ n |

**Structural constraints**:
- 1-D ndarray of positive integers (≥ 1)
- Each value ≤ sequence length (n)
- Length equals the original sequence length

> **Note**: The `IntervalChain` named tuple (original plan) was rejected in favour of this simpler plain ndarray. `binding` travels explicitly as a parameter.

---

### Interval Tuple (ndarray)

The return type of `intervals_tuple`. A plain 1-D ndarray.

| Property | Value |
|----------|-------|
| dtype    | intp (platform pointer-sized integer) |
| shape    | (m,) where m ≤ n for lossy, m = n for normal/cycle, m ≥ n for redundant |
| values   | Positive integers (≥ 1) |

---

### Intervals Distribution (ndarray)

The return type of `intervals_distribution`. A plain 1-D ndarray.

| Property | Value |
|----------|-------|
| dtype    | intp or int64 (count array) |
| shape    | (max_interval_value,) |
| values   | Non-negative integers (counts); distribution[i] = count of interval value (i+1) in the tuple |
| indexing | 0-based; distribution[0] = count of interval length 1 |

**Empty input**: Returns empty ndarray `[]` for empty tuple input.

---

## Old → New Mode Mapping

| Old `mode` value | New `chain_mode` | New `tuple_mode` |
|------------------|------------------|------------------|
| mode.lossy       | chain_mode.boundary | tuple_mode.lossy |
| mode.normal      | chain_mode.boundary | tuple_mode.normal |
| mode.cycle       | chain_mode.cycle    | tuple_mode.normal |
| mode.redundant   | chain_mode.boundary | tuple_mode.redundant |

**New combinations** (not possible with old `mode`):
- `chain_mode.cycle` + `tuple_mode.lossy`
- `chain_mode.cycle` + `tuple_mode.redundant`

---

## State Transitions

```
sequence (1-D array-like)
        │
        ▼ intervals_chain(X, binding, chain_mode) → ndarray
        │   (binding is also passed through by caller)
        ▼ intervals_tuple(chain, binding, tuple_mode) → ndarray
        │
        ▼ intervals_distribution(tuple) → ndarray   [optional utility, not used by intervals()]
        │
        ▼ characteristics(distribution) → scalar
```

The `intervals()` legacy function composes steps 1 and 2 internally, passing `binding` explicitly to both stages. It does not call `intervals_distribution`.
