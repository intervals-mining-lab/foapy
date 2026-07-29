# Implementation Plan: foapy.partials Package

**Branch**: `004-partials-package` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-partials-package/spec.md`

## Summary

Add `foapy.partials` — a new sub-package providing FOA pipeline operations for partial sequences (sequences with gap/skip positions represented as numpy masked arrays). Unlike `foapy.ma`, which compresses masked elements before computing intervals, `foapy.partials` preserves gap positions in every output and computes interval distances using actual positional indices in the full array. The package exposes four functions: `order`, `alphabet`, `intervals_chain`, `intervals_tuple`.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: numpy >= 1.20 (sole runtime dependency; no additions)
**Storage**: N/A
**Testing**: tox -e default (pytest); tests mirror `tests/test_ma_*.py` naming pattern
**Target Platform**: Any platform supporting Python 3.8+ and numpy >= 1.20
**Project Type**: Python library sub-package
**Performance Goals**: Sequences up to length 10 000 must complete in < 100 ms on a single CPU core (Constitution Principle IV)
**Constraints**: All operations must be vectorized numpy; no Python loops over array elements; O(n) memory
**Scale/Scope**: 4 source modules + `__init__.py`; 4 test files; 1 `__init__.py` update in `foapy/__init__.py`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality — single responsibility, pure functions, no new deps | ✅ Pass | Each function is a single module; no new runtime deps; pure numpy |
| I. Code Quality — pre-commit (black, isort, flake8) | ✅ Pass | Enforced by existing CI pipeline |
| II. Testing — tox -e default; edge cases for pipeline functions | ✅ Pass | Tests must cover empty, single-element, all-unique, all-same, and realistic datasets; masked-value edge cases required |
| III. API Consistency — `foapy.ma` must mirror `foapy.core` signatures | ⚠️ Note | Constitution says "foapy.ma MUST mirror every public function in foapy.core". `foapy.partials` is a NEW sub-package, not an extension of foapy.ma, so this constraint does not apply. `partials` introduces the same four functions as core with an identical signature contract (masked in, masked out). |
| III. API Consistency — exceptions, docstring shapes | ✅ Pass | Uses `Not1DArrayException`; docstrings document dtype and dimensions |
| IV. Performance — vectorized numpy, < 100 ms for n=10 000 | ✅ Pass | All algorithms are vectorized; see design in Phase 1 |
| V. Simplicity — YAGNI, no base class, extract only at 3+ call sites | ✅ Pass | 4 thin modules; no abstractions beyond what is required |

No violations requiring Complexity Tracking entries.

## Project Structure

### Documentation (this feature)

```text
specs/004-partials-package/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── order.md
│   ├── alphabet.md
│   ├── intervals_chain.md
│   └── intervals_tuple.md
└── tasks.md             # Phase 2 output (/speckit.tasks — not created here)
```

### Source Code (repository root)

```text
src/foapy/
├── __init__.py                  # Add 'partials' to __foapy_submodules__ and __getattr__
├── partials/
│   ├── __init__.py              # Exports: order, alphabet, intervals_chain, intervals_tuple
│   ├── _order.py
│   ├── _alphabet.py
│   ├── _intervals_chain.py
│   └── _intervals_tuple.py

tests/
├── test_partials_order.py
├── test_partials_alphabet.py
├── test_partials_intervals_chain.py
└── test_partials_intervals_tuple.py
```

**Structure Decision**: Single flat package under `src/foapy/partials/`, mirroring `src/foapy/ma/`. Each function in its own private module (`_name.py`), exported via `__init__.py`. Test files follow the existing `test_<subpackage>_<function>.py` naming convention.

## Complexity Tracking

No constitution violations requiring justification.

---

## Phase 0: Research

*No NEEDS CLARIFICATION items in Technical Context. All design decisions derived from codebase analysis and documentation review.*

See [research.md](./research.md) for detailed findings.

---

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md).

### Function Algorithm Designs

#### `partials.order(X, return_alphabet=False)`

```
1. ar = ma.asarray(X)               # auto-wrap plain arrays
2. Validate ar.ndim == 1            # raise Not1DArrayException otherwise
3. mask = ma.getmaskarray(ar)       # boolean mask; False=present, True=gap
4. compressed = ar.compressed()     # non-masked values in original order
5. If compressed is empty:
     return fully masked array of length n (and empty alphabet if requested)
6. order_compressed, alphabet = core.order(compressed, return_alphabet=True)
7. result_data = zeros(n, dtype=intp)
8. result_data[~mask] = order_compressed  # map back to full positions
9. result = ma.masked_array(result_data, mask=mask)
10. Return (result, alphabet) if return_alphabet else result
```

All operations are O(n) and fully vectorized.

#### `partials.alphabet(X)`

```
1. ar = ma.asarray(X)
2. Validate ar.ndim == 1
3. return core.order(ar.compressed(), return_alphabet=True)[1]
   # equivalent: unique non-masked values in first-appearance order
```

Delegates to core after compression; O(n log n).

#### `partials.intervals_chain(X, binding, chain_mode)`

Key distinction from `ma.intervals_chain`: intervals measure **actual positional distance** in the full array (gaps count toward distance), not compressed distance.

```
1. Validate binding and chain_mode values
2. ar = ma.asarray(X)
3. Validate ar.ndim == 1
4. full_mask = ma.getmaskarray(ar)
5. non_masked_idx = np.where(~full_mask)[0]  # actual positions in full array
6. compressed_values = ar.compressed()
7. m = len(compressed_values); n = len(ar)
8. If m == 0: return fully masked array of length n

9. If binding == binding.end:
     # Reverse both positions and values to treat as binding.start
     compressed_values = compressed_values[::-1]
     non_masked_idx = (n - 1 - non_masked_idx)[::-1]

10. Sort compressed_values stably → perm (indices into compressed array)
11. actual_pos = non_masked_idx        # actual positions for each compressed element

12. Build group boundary masks (first_mask, last_mask) over perm:
      same as core: compare consecutive sorted values

13. chain_compressed = empty(m, dtype=intp)
    chain_compressed[1:] = actual_pos[perm[1:]] - actual_pos[perm[:-1]]

14. If chain_mode == cycle:
      delta = n - actual_pos[perm[last_mask]]  # wrap-around distance
    else:
      delta = 1                                 # boundary = 1-indexed from edge

    chain_compressed[first_mask] = actual_pos[perm[first_mask]] + delta

15. Invert perm → result_compressed (restore original order)

16. If binding == binding.end: result_compressed = result_compressed[::-1]

17. result_data = zeros(n, dtype=intp)
    result_data[original_non_masked_idx] = result_compressed
18. Return ma.masked_array(result_data, mask=full_mask)
```

Fully vectorized; same algorithmic structure as `core.intervals_chain` but uses `actual_pos` instead of compressed-array indices.

#### `partials.intervals_tuple(chain, binding, tuple_mode)`

Receives a masked 1-D chain (output of `partials.intervals_chain`). Output length rules:
- `normal`: same length as input, same mask
- `lossy`: same length as input; positions identified as boundary intervals become **additionally masked**
- `redundant`: length increases by k (number of unique symbols inferred from chain); trailing intervals appended as unmasked elements

```
normal(ar_masked):
  return ar_masked.copy()

lossy(ar_masked, binding):
  # Work on compressed chain (positions within compressed array)
  compressed = ar_masked.compressed()
  non_masked_idx = np.where(~ma.getmaskarray(ar_masked))[0]
  If binding == end: reverse compressed and non_masked_idx

  positions = np.arange(len(compressed))
  first_mask = compressed > positions      # boundary detection (same as core)
  boundary_original_idx = non_masked_idx[first_mask if binding==start
                                          else reversed first_mask]

  new_mask = ma.getmaskarray(ar_masked).copy()
  new_mask[boundary_original_idx] = True
  return ma.masked_array(ar_masked.data, mask=new_mask)

redundant(ar_masked, binding):
  compressed = ar_masked.compressed()
  # Apply core redundant on compressed chain
  extended_plain = core.intervals_tuple(compressed, binding, tuple_mode.redundant)
  # The extra trailing intervals are the last (len(extended_plain) - len(compressed)) elements
  k = len(extended_plain) - len(compressed)
  trailing = extended_plain[len(compressed):]
  # Reconstruct masked array: original positions unchanged, trailing appended (unmasked)
  result_data = np.concatenate([ar_masked.data, trailing])
  result_mask = np.concatenate([ma.getmaskarray(ar_masked), np.zeros(k, dtype=bool)])
  return ma.masked_array(result_data, mask=result_mask)
```

### `foapy/__init__.py` Update

Add `'partials'` to `__foapy_submodules__` and add a `__getattr__` branch:

```python
if attr == "partials":
    import foapy.partials as partials
    return partials
```

No functions from `partials` are hoisted to `foapy.*` top-level (same pattern as `foapy.ma`).
