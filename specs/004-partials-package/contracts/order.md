# Contract: partials.order

## Signature

```python
foapy.partials.order(X, return_alphabet=False) -> numpy.ma.MaskedArray
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `X` | `array_like` or `numpy.ma.MaskedArray` | Yes | 1-D sequence (plain or masked). Masked positions treated as gaps. |
| `return_alphabet` | `bool` | No (default `False`) | If `True`, also return the alphabet of non-masked unique values. |

## Returns

| Mode | Return | Type | Shape | dtype |
|------|--------|------|-------|-------|
| `return_alphabet=False` | `order` | `numpy.ma.MaskedArray` | `(n,)` | `numpy.intp` |
| `return_alphabet=True` | `(order, alphabet)` | `(numpy.ma.MaskedArray, numpy.ndarray)` | `(n,)`, `(p,)` | `numpy.intp`, same as input |

- `n` = length of input sequence
- `p` = number of unique non-masked values (alphabet power)
- Output mask is identical to input mask
- Non-masked positions hold the element's 0-based index in the alphabet (first-appearance order)

## Raises

| Exception | Condition |
|-----------|-----------|
| `Not1DArrayException` | Input has more than 1 dimension |

## Invariants

- `len(result) == len(X)` always
- `result.mask` equals `ma.getmaskarray(X)` always
- When `return_alphabet=True`: `alphabet[result.data[~result.mask]]` reconstructs `X.compressed()`
- When all positions are masked: result is fully masked; alphabet is empty array

## Examples

```python
import numpy.ma as ma
import foapy.partials as partials

X = ma.masked_array(['a', 'b', 'a', 'c'], mask=[False, True, False, False])
result = partials.order(X)
# result.data (at non-masked): [0, 0, 1]
# result.mask: [False, True, False, False]

result, alphabet = partials.order(X, return_alphabet=True)
# alphabet: ['a', 'c']
```
