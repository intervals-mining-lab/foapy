# Contract: partials.intervals_tuple

## Signature

```python
foapy.partials.intervals_tuple(chain, binding: int, tuple_mode: int) -> numpy.ma.MaskedArray
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | `array_like` or `numpy.ma.MaskedArray` | Yes | 1-D intervals chain produced by `partials.intervals_chain`. |
| `binding` | `int` | Yes | Must match the binding used to produce `chain`. `foapy.binding.start` (1) or `foapy.binding.end` (2). |
| `tuple_mode` | `int` | Yes | `foapy.tuple_mode.normal` (2), `foapy.tuple_mode.lossy` (1), or `foapy.tuple_mode.redundant` (3) |

## Returns

| `tuple_mode` | Shape | Mask | Description |
|--------------|-------|------|-------------|
| `normal` | `(n,)` | Same as input | Chain returned unchanged |
| `lossy` | `(n,)` | Input mask ∪ boundary positions | Boundary (first-occurrence) intervals additionally masked |
| `redundant` | `(n + k,)` | Input mask + `k` unmasked trailing elements | Trailing complementary boundary intervals appended; `k` = unique symbol count inferred from compressed chain |

- `n` = length of input chain
- `k` = number of unique elements inferred from the compressed chain

## Raises

| Exception | Condition |
|-----------|-----------|
| `ValueError` | `binding` is not `binding.start` or `binding.end` |
| `ValueError` | `tuple_mode` is not a recognised value |

## Invariants

- For `normal`: `result.data == chain.data` and `result.mask == chain.mask`
- For `lossy`: `result.mask[i] == True` whenever `chain.mask[i] == True`; additionally masked at boundary positions
- For `lossy`: `len(result) == len(chain)` always
- For `redundant`: `len(result) == len(chain) + k`; trailing k elements are unmasked
- When `chain` has no masked positions: non-masked values in result equal `foapy.core.intervals_tuple(chain, binding, tuple_mode)`

## Boundary Detection (lossy)

A non-masked element at compressed-array index `i` is a boundary interval if `compressed_chain[i] > i`. This is the same criterion as `foapy.core.intervals_tuple` applied to the compressed sub-sequence.

## Examples

```python
import numpy.ma as ma
import foapy
import foapy.partials as partials

# Partial chain: positions 0 and 4 are gaps
chain = ma.masked_array(
    [0, 2, 3, 2, 0, 6],
    mask=[True, False, False, False, True, False]
)

# normal: unchanged
result = partials.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.normal)
# result: same as chain

# lossy: C's first occurrence at compressed-index 0 has value 2 > 0 → masked
# T's first occurrence at compressed-index 1 has value 3 > 1 → masked
# G's first occurrence at compressed-index 3 has value 6 > 3 → masked
# C's second occurrence at compressed-index 2 has value 2 == 2 → kept
result = partials.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.lossy)
# Only position 3 (C second occurrence) remains unmasked
```
