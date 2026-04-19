# Contract: partials.intervals_chain

## Signature

```python
foapy.partials.intervals_chain(X, binding: int, chain_mode: int) -> numpy.ma.MaskedArray
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `X` | `array_like` or `numpy.ma.MaskedArray` | Yes | 1-D raw sequence (plain or masked). Masked positions are gaps. Pass the original sequence, not the order output. |
| `binding` | `int` | Yes | `foapy.binding.start` (1) or `foapy.binding.end` (2) |
| `chain_mode` | `int` | Yes | `foapy.chain_mode.boundary` (1) or `foapy.chain_mode.cycle` (2) |

## Returns

| Return | Type | Shape | dtype |
|--------|------|-------|-------|
| `chain` | `numpy.ma.MaskedArray` | `(n,)` | `numpy.intp` |

- `n` = length of input sequence
- Output mask is identical to input mask
- Non-masked positions hold the interval distance as a positive integer
- **Interval distance uses actual positional indices in the full array** (gap positions count toward distance)
- Minimum interval value: 1. Maximum: n.

## Raises

| Exception | Condition |
|-----------|-----------|
| `Not1DArrayException` | Input has more than 1 dimension |
| `ValueError` | `binding` is not `binding.start` or `binding.end` |
| `ValueError` | `chain_mode` is not `chain_mode.boundary` or `chain_mode.cycle` |

## Invariants

- `len(result) == len(X)` always
- `result.mask` equals `ma.getmaskarray(X)` always
- For two non-masked occurrences of the same element at actual positions `i < j`: interval at position `j` = `j - i`
- For the first non-masked occurrence of an element at actual position `p` (binding.start, boundary): interval = `p + 1`
- When `X` has no masked positions: result equals `foapy.core.intervals_chain(X, binding, chain_mode)`

## Key Semantic Difference from `foapy.ma.intervals_chain`

`foapy.ma.intervals_chain` compresses masked elements first, so intervals measure distances in the compressed sequence. `foapy.partials.intervals_chain` uses actual positional indices, so a gap between two occurrences increases the interval distance.

| Sequence | foapy.ma result | foapy.partials result |
|----------|-----------------|-----------------------|
| `[A, --, A]` (binding.start, boundary) | `[1, 1]` (compressed) | `[1, --, 2]` (full array) |

## Examples

```python
import numpy.ma as ma
import foapy
import foapy.partials as partials

X = ma.masked_array(['C', 'T', 'C', 'G'], mask=[False, False, False, False])
chain = partials.intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
# chain: [1, 2, 2, 4]  (same as core — no gaps)

X_partial = ma.masked_array(
    ['_', 'C', 'T', 'C', '_', 'G'],
    mask=[True, False, False, False, True, False]
)
chain = partials.intervals_chain(X_partial, foapy.binding.start, foapy.chain_mode.boundary)
# chain.data at non-masked positions [1,2,3,5]: [2, 3, 2, 6]
# chain.mask: [True, False, False, False, True, False]
```
