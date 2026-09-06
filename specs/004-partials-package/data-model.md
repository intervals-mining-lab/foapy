# Data Model: foapy.partials

**Date**: 2026-04-19 | **Branch**: `004-partials-package`

## Entities

### Partial Sequence

A 1-D masked array where each position holds either a symbolic value or a gap marker.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| data | any element type (str, int, …) | 1-D only; multi-dimensional raises `Not1DArrayException` |
| mask | boolean ndarray | `True` = gap position; `False` = present element |
| length `n` | int | ≥ 0 |
| compressed length `m` | int | 0 ≤ m ≤ n |

**Construction**: Accept `numpy.ma.MaskedArray`, plain `numpy.ndarray`, or Python list. Plain inputs are auto-wrapped with no mask (`ma.asarray(X)`).

---

### Partial Order

Output of `partials.order()`. A 1-D masked array of the same length as the Partial Sequence.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| data | `numpy.intp` | alphabet index at non-masked positions; value at masked positions is undefined but always 0 |
| mask | boolean ndarray | Identical to input Partial Sequence mask |
| shape | `(n,)` | Same length as input |
| value range | int | 0 ≤ value < alphabet power (number of unique non-masked elements) |

**Reconstruction**: `partial_order` paired with the `alphabet` array from `return_alphabet=True` allows full reconstruction: `alphabet[partial_order.data[~mask]]` recovers the original non-masked elements.

---

### Partial Intervals Chain

Output of `partials.intervals_chain()`. A 1-D masked array of the same length as the input.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| data | `numpy.intp` | positional interval distance at non-masked positions |
| mask | boolean ndarray | Identical to input chain mask |
| shape | `(n,)` | Same length as input |
| value range | int | 1 ≤ value ≤ n (actual positional distance, including gap positions) |

**Semantics**: For two consecutive non-masked occurrences of the same element at actual positions `i` and `j` (i < j), the interval at position `j` is `j - i`. For the first occurrence at position `p`, the boundary interval is `p + 1` (binding.start, chain_mode.boundary).

---

### Partial Intervals Tuple

Output of `partials.intervals_tuple()`. A 1-D masked array.

| Attribute | Type | Constraints |
|-----------|------|-------------|
| data | `numpy.intp` | boundary-adjusted interval distances |
| mask | boolean ndarray | input mask ∪ additionally masked boundary positions (lossy) |
| shape | `(n,)` for normal and lossy; `(n + k,)` for redundant | n = chain length; k = unique symbol count inferred from chain |

**Mode effects on mask**:
- `tuple_mode.normal`: mask unchanged from input
- `tuple_mode.lossy`: first-occurrence boundary positions additionally masked; output length = n
- `tuple_mode.redundant`: original mask unchanged; k trailing elements appended as unmasked; output length = n + k

## Pipeline Flow

```
Partial Sequence (masked 1-D)
        │
        ▼
  partials.order()
        │  returns Partial Order (masked 1-D, same length)
        ▼
  partials.intervals_chain()
        │  takes raw Partial Sequence (not the order)
        │  returns Partial Intervals Chain (masked 1-D, same length)
        ▼
  partials.intervals_tuple()
        │  returns Partial Intervals Tuple (masked 1-D)
        │  normal/lossy: same length; redundant: n + k length
        ▼
  (downstream characteristics or further analysis)
```

Note: `intervals_chain` accepts the original Partial Sequence (raw symbols), not the order output. This mirrors `foapy.core.intervals_chain` which also operates on raw sequences.
