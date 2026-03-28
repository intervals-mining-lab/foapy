# Public API Contracts: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-03-28

---

## `chain_mode` (enum class)

```
foapy.chain_mode
foapy.core.chain_mode
```

**Attributes**:

| Name     | Type | Value |
|----------|------|-------|
| boundary | int  | 1     |
| cycle    | int  | 2     |

**Errors**: None raised on attribute access.

---

## `tuple_mode` (enum class)

```
foapy.tuple_mode
foapy.core.tuple_mode
```

**Attributes**:

| Name      | Type | Value |
|-----------|------|-------|
| lossy     | int  | 1     |
| normal    | int  | 2     |
| redundant | int  | 3     |

**Errors**: None raised on attribute access.

---

## `intervals_chain(X, binding, chain_mode)`

```
foapy.intervals_chain
foapy.core.intervals_chain
```

**Signature**: `intervals_chain(X, binding: int, chain_mode: int) -> IntervalChain`

**Parameters**:

| Name       | Type        | Description |
|------------|-------------|-------------|
| X          | array-like (1-D) | Input sequence (ordered or raw). Must be 1-dimensional. |
| binding    | int         | `binding.start` (left-to-right) or `binding.end` (right-to-left) |
| chain_mode | int         | `chain_mode.boundary` or `chain_mode.cycle` |

**Returns**: `IntervalChain` named tuple with fields `(values: ndarray[intp, 1-D], binding: int, chain_mode: int)`

**Raises**:
- `Not1DArrayException` — when `X` is not 1-dimensional
- `ValueError` — when `binding` is not `binding.start` or `binding.end`
- `ValueError` — when `chain_mode` is not `chain_mode.boundary` or `chain_mode.cycle`

**Edge cases**:
- Empty `X` → returns `IntervalChain(values=array([]), binding=binding, chain_mode=chain_mode)`

---

## `intervals_tuple(chain, tuple_mode)`

```
foapy.intervals_tuple
foapy.core.intervals_tuple
```

**Signature**: `intervals_tuple(chain: IntervalChain, tuple_mode: int) -> ndarray`

**Parameters**:

| Name       | Type          | Description |
|------------|---------------|-------------|
| chain      | IntervalChain | Output of `intervals_chain`. Carries values, binding, and chain_mode internally. |
| tuple_mode | int           | `tuple_mode.lossy`, `tuple_mode.normal`, or `tuple_mode.redundant` |

**Returns**: `ndarray[intp, 1-D]` — boundary-adjusted intervals tuple

**Raises**:
- `ValueError` — when `tuple_mode` is not a valid `tuple_mode` value

**Edge cases**:
- Empty chain → returns `array([])`

---

## `intervals_distribution(tuple_result)`

```
foapy.intervals_distribution
foapy.core.intervals_distribution
```

**Signature**: `intervals_distribution(tuple_result: ndarray) -> ndarray`

**Parameters**:

| Name         | Type              | Description |
|--------------|-------------------|-------------|
| tuple_result | ndarray (1-D)     | Output of `intervals_tuple` or any 1-D array of positive integers |

**Returns**: `ndarray[intp, 1-D]` of length `max(tuple_result)` where `result[i]` = count of interval value `i+1`

**Edge cases**:
- Empty input → returns `array([])`

---

## `binding(chain)`

```
foapy.binding  ← NOTE: this is a NEW overloaded meaning; existing `binding` is an enum class
```

**Resolution**: `binding` as a callable function and `binding` as an enum class are the same symbol. The callable form accepts an `IntervalChain` argument and returns an int.

**Signature**: `binding(chain: IntervalChain) -> int`

**Parameters**:

| Name  | Type          | Description |
|-------|---------------|-------------|
| chain | IntervalChain | Output of `intervals_chain` |

**Returns**: `int` — `binding.start` or `binding.end`

**Raises**:
- `ValueError` — when `chain` is not an `IntervalChain` instance (or valid equivalent)

---

## `chain_mode(chain)` (function)

```
foapy.chain_mode  ← NOTE: dual role — also an enum class (see above)
```

**Resolution**: `chain_mode` serves both as an enum class (accessed via `.boundary`, `.cycle`) and as a callable function (called with an `IntervalChain` argument).

**Signature**: `chain_mode(chain: IntervalChain) -> int`

**Parameters**:

| Name  | Type          | Description |
|-------|---------------|-------------|
| chain | IntervalChain | Output of `intervals_chain` |

**Returns**: `int` — `chain_mode.boundary` or `chain_mode.cycle`

**Raises**:
- `ValueError` — when `chain` is not an `IntervalChain` instance

---

## `is_valid_intervals_chain(chain)`

```
foapy.is_valid_intervals_chain
foapy.core.is_valid_intervals_chain
```

**Signature**: `is_valid_intervals_chain(chain) -> bool`

**Parameters**:

| Name  | Type | Description |
|-------|------|-------------|
| chain | any  | Any value to validate |

**Returns**: `bool` — `True` if `chain` is an `IntervalChain` with structurally valid `values`; `False` otherwise. Never raises.

**Structural validity criteria**:
1. `chain` is an `IntervalChain` named tuple
2. `chain.values` is a 1-D ndarray
3. All values in `chain.values` are positive integers (≥ 1)
4. All values in `chain.values` are ≤ len(chain.values)

---

## `foapy.ma` variants

The following `foapy.ma` equivalents mirror the core API signatures with identical parameter names and return shapes, differing only in accepting/returning masked arrays:

- `foapy.ma.intervals_chain(X, binding, chain_mode)` → `IntervalChain` (values may be masked)
- `foapy.ma.intervals_tuple(chain, tuple_mode)` → masked ndarray
- `foapy.ma.intervals_distribution(tuple_result)` → masked ndarray

`foapy.ma.binding` and `foapy.ma.chain_mode` (function) delegate to the core versions since `IntervalChain` metadata is not masked.

---

## Naming collision note: `binding` and `chain_mode`

Both `binding` and `chain_mode` have dual roles (enum class + callable function). The implementation resolves this by implementing `__call__` on the class itself:

```python
class binding:
    start: int = 1
    end: int = 2

    def __new__(cls, chain):
        # When called as binding(chain), return chain.binding
        ...
```

This pattern allows `foapy.binding.start` (attribute access) and `foapy.binding(chain)` (callable) to coexist without a naming conflict or separate symbols.
