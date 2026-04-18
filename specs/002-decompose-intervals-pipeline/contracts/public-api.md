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

**Signature**: `intervals_chain(X, binding: int, chain_mode: int) -> ndarray`

**Parameters**:

| Name       | Type        | Description |
|------------|-------------|-------------|
| X          | array-like (1-D) | Input sequence. Must be 1-dimensional. |
| binding    | int         | `binding.start` (left-to-right) or `binding.end` (right-to-left) |
| chain_mode | int         | `chain_mode.boundary` or `chain_mode.cycle` |

**Returns**: `ndarray[intp, 1-D]` — raw interval chain in original sequence order

**Raises**:
- `Not1DArrayException` — when `X` is not 1-dimensional
- `ValueError` — when `binding` is not `binding.start` or `binding.end`
- `ValueError` — when `chain_mode` is not `chain_mode.boundary` or `chain_mode.cycle`

**Edge cases**:
- Empty `X` → returns `array([], dtype=intp)`

---

## `intervals_tuple(chain, binding, tuple_mode)`

```
foapy.intervals_tuple
foapy.core.intervals_tuple
```

**Signature**: `intervals_tuple(chain: ndarray, binding: int, tuple_mode: int) -> ndarray`

**Parameters**:

| Name       | Type          | Description |
|------------|---------------|-------------|
| chain      | ndarray (1-D) | Output of `intervals_chain` — plain 1-D integer array. |
| binding    | int           | `binding.start` or `binding.end` — must match the binding used to produce `chain`. |
| tuple_mode | int           | `tuple_mode.lossy`, `tuple_mode.normal`, or `tuple_mode.redundant` |

**Returns**: `ndarray[intp, 1-D]` — boundary-adjusted intervals tuple

**Raises**:
- `ValueError` — when `binding` is not `binding.start` or `binding.end`
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

## `is_valid_intervals_chain(chain)`

```
foapy.is_valid_intervals_chain
foapy.core.is_valid_intervals_chain
```

**Signature**: `is_valid_intervals_chain(chain) -> bool`

**Parameters**:

| Name  | Type | Description |
|-------|------|-------------|
| chain | any  | Any value to validate as an interval chain |

**Returns**: `bool` — `True` if `chain` is a valid 1-D array of positive integers where every value ≤ len(chain); `False` otherwise. Never raises.

**Structural validity criteria**:
1. `chain` is a 1-D ndarray (or 1-D array-like convertible to one)
2. All values are positive integers (≥ 1)
3. All values are ≤ len(chain)

---

## `foapy.ma` variants

The following `foapy.ma` equivalents mirror the core API signatures exactly, differing only in that `X` may be a masked array:

- `foapy.ma.intervals_chain(X, binding, chain_mode)` → `ndarray`
- `foapy.ma.intervals_tuple(chain, binding, tuple_mode)` → `ndarray`
- `foapy.ma.intervals_distribution(tuple_result)` → `ndarray`
