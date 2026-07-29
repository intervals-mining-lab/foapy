# Contract: partials.alphabet

## Signature

```python
foapy.partials.alphabet(X) -> numpy.ndarray
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `X` | `array_like` or `numpy.ma.MaskedArray` | Yes | 1-D sequence (plain or masked). Masked positions are excluded. |

## Returns

| Return | Type | Shape | dtype |
|--------|------|-------|-------|
| `alphabet` | `numpy.ndarray` | `(p,)` | Same as input element type |

- `p` = number of unique non-masked values
- Values appear in order of first appearance among non-masked positions
- Returns empty array when all positions are masked or input is empty

## Raises

| Exception | Condition |
|-----------|-----------|
| `Not1DArrayException` | Input has more than 1 dimension |

## Invariants

- `len(result)` equals the number of unique values in `X.compressed()`
- Result is a plain ndarray (not masked), even when input is masked

## Examples

```python
import numpy.ma as ma
import foapy.partials as partials

X = ma.masked_array(['a', 'b', 'a', 'c'], mask=[False, True, False, False])
alphabet = partials.alphabet(X)
# alphabet: ['a', 'c']  (b is masked, c appears after a)
```
