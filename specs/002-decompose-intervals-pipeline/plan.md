# Implementation Plan: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-03-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-decompose-intervals-pipeline/spec.md`

## Summary

Decompose the monolithic `intervals()` function into four independently callable pipeline stages: `intervals_chain` (builds raw chain from sequence, binding, and chain_mode), `intervals_tuple` (applies tuple_mode boundary handling), `intervals_distribution` (computes count distribution), and characteristics (unchanged). Split the existing `mode` enum into two orthogonal enums: `chain_mode` (`boundary`/`cycle`) and `tuple_mode` (`lossy`/`normal`/`redundant`). Add introspection functions `binding(chain)` and `chain_mode(chain)` and a validator `is_valid_intervals_chain`. All implementations use numpy vectorized operations only (no Python loops), following TDD: tests first, implementation to pass, then refactor.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: numpy >= 1.20 (sole runtime dependency per constitution)
**Storage**: N/A
**Testing**: pytest via `tox -e default`; `unittest.TestCase` + `numpy.testing.assert_array_equal`
**Target Platform**: Any Python 3.8+ environment (cross-platform library)
**Project Type**: Scientific library
**Performance Goals**: Sequences up to length 10,000 MUST complete in < 100ms on a single CPU core (constitution Principle IV)
**Constraints**: No Python loops over array elements; no dependencies beyond numpy; no breaking changes to existing API
**Scale/Scope**: Single flat library; ~10 new source files, ~10 new test files, benchmark scripts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality — single responsibility, pure functions | ✅ PASS | Each new function has a single well-defined responsibility; `IntervalChain` namedtuple is immutable; no mutable state |
| I. Code Quality — no new runtime deps | ✅ PASS | Only `collections.namedtuple` from stdlib; no new third-party packages |
| I. Code Quality — black/isort/flake8 | ✅ PASS | All new code will pass through pre-commit before merge |
| II. Testing — TDD, all behavioral changes covered | ✅ PASS | TDD explicitly required in user input; each function gets its own test file |
| II. Testing — canonical test runner `tox -e default` | ✅ PASS | All tests in `tests/` directory following existing pattern |
| II. Testing — new pipeline functions: empty, single, all-unique, all-same, realistic | ✅ PASS | Required in spec FR-019 and constitution Principle II |
| II. Testing — foapy.ma masked-value edge cases | ✅ PASS | FR-014 and constitution Principle II require this |
| III. API Consistency — 1-D array-like as first arg | ✅ PASS | `intervals_chain(X, binding, chain_mode)` follows the pattern |
| III. API Consistency — binding/mode as keyword args with enums | ✅ PASS | New `chain_mode` and `tuple_mode` enums follow identical pattern to existing `binding` and `mode` |
| III. API Consistency — foapy.ma mirrors foapy.core | ✅ PASS | FR-014 requires ma variants |
| III. API Consistency — project-defined exceptions only | ✅ PASS | `Not1DArrayException` for dimensionality; `ValueError` for invalid enum values (following existing `intervals()` precedent) |
| III. API Consistency — return shapes documented | ✅ PASS | Required in docstrings per FR-018 |
| IV. Performance — vectorized numpy, no Python loops | ✅ PASS | Explicitly required by user input and constitution |
| IV. Performance — <100ms for n≤10,000 | ✅ PASS | New functions are decomposed from existing vectorized `intervals()`; no regression expected |
| V. Simplicity — YAGNI, thin functions | ✅ PASS | Each function does exactly one thing; `IntervalChain` namedtuple is minimal |
| V. Simplicity — no backwards-compat shims | ✅ PASS | Old `mode` enum and `intervals()` are kept unchanged (not shimmed); new enums are additions |

**Naming collision note** (requires justification): `binding` and `chain_mode` serve dual roles (enum class + callable function). This is documented in `contracts/public-api.md`. The pattern using `__new__` on the class body is the minimal approach; no wrapper or rename is introduced.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| `IntervalChain` named tuple as return type (non-plain ndarray) | `binding(chain)` and `chain_mode(chain)` require metadata; fundamentals docs confirm structural detection is an open question | Returning plain ndarray rejected: cannot reliably infer binding/chain_mode from values alone |
| `binding` and `chain_mode` as dual-role symbols (enum + callable) | Users expect `binding(chain)` to return binding; no separate namespace available without breaking API consistency | A separate `get_binding(chain)` symbol was considered but rejected as it introduces an asymmetry with no precedent in the codebase |

## Project Structure

### Documentation (this feature)

```text
specs/002-decompose-intervals-pipeline/
├── plan.md                    # This file
├── research.md                # Phase 0 — decisions and rationale
├── data-model.md              # Phase 1 — entities and type definitions
├── contracts/
│   └── public-api.md          # Phase 1 — function signatures and contracts
└── tasks.md                   # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
src/foapy/core/
├── __init__.py                     # ADD: chain_mode, tuple_mode, intervals_chain,
│                                   #      intervals_tuple, intervals_distribution,
│                                   #      is_valid_intervals_chain exports
├── _chain_mode.py                  # NEW: chain_mode enum class (boundary, cycle)
├── _tuple_mode.py                  # NEW: tuple_mode enum class (lossy, normal, redundant)
├── _interval_chain.py              # NEW: IntervalChain namedtuple definition
├── _intervals_chain.py             # NEW: intervals_chain() implementation
├── _intervals_tuple.py             # NEW: intervals_tuple() implementation
├── _intervals_distribution.py      # NEW: intervals_distribution() implementation
├── _is_valid_intervals_chain.py    # NEW: is_valid_intervals_chain() implementation
├── _binding.py                     # MODIFY: add __new__ to support binding(chain) callable form
├── _mode.py                        # UNCHANGED
└── _intervals.py                   # UNCHANGED (backward compat)

src/foapy/ma/
├── __init__.py                     # ADD: intervals_chain, intervals_tuple,
│                                   #      intervals_distribution exports
├── _intervals_chain.py             # NEW: ma.intervals_chain() implementation
├── _intervals_tuple.py             # NEW: ma.intervals_tuple() implementation
└── _intervals_distribution.py      # NEW: ma.intervals_distribution() implementation

src/foapy/
└── __init__.py                     # ADD: chain_mode, tuple_mode, intervals_chain,
                                    #      intervals_tuple, intervals_distribution,
                                    #      is_valid_intervals_chain to public namespace

tests/
├── test_chain_mode.py              # NEW: chain_mode enum tests
├── test_tuple_mode.py              # NEW: tuple_mode enum tests
├── test_interval_chain.py          # NEW: IntervalChain namedtuple tests
├── test_intervals_chain.py         # NEW: intervals_chain() tests
├── test_intervals_tuple.py         # NEW: intervals_tuple() tests
├── test_intervals_distribution.py  # NEW: intervals_distribution() tests
├── test_is_valid_intervals_chain.py # NEW: is_valid_intervals_chain() tests
├── test_binding_callable.py        # NEW: binding(chain) callable form tests
├── test_chain_mode_callable.py     # NEW: chain_mode(chain) callable form tests
├── test_pipeline_consistency.py    # NEW: old intervals() == new pipeline for all 4 mappings
├── test_ma_intervals_chain.py      # NEW: ma.intervals_chain() tests
├── test_ma_intervals_tuple.py      # NEW: ma.intervals_tuple() tests
└── test_ma_intervals_distribution.py # NEW: ma.intervals_distribution() tests

benchmarks/
├── bench_intervals_chain.py        # NEW: small/medium/large benchmark
├── bench_intervals_tuple.py        # NEW
├── bench_intervals_distribution.py # NEW
└── bench_pipeline_full.py          # NEW: end-to-end pipeline benchmark
```

**Structure Decision**: Single-project layout following the existing `src/foapy/` pattern. New modules follow the `_snake_case.py` naming convention used for all existing core modules. Tests follow `tests/test_{function_name}.py` flat structure matching existing test files.

---

## Implementation Order (TDD)

Each step is: write failing test → implement to pass → refactor.

### Step 1: `chain_mode` and `tuple_mode` enums
- `src/foapy/core/_chain_mode.py`
- `src/foapy/core/_tuple_mode.py`
- Tests: `tests/test_chain_mode.py`, `tests/test_tuple_mode.py`

### Step 2: `IntervalChain` named tuple
- `src/foapy/core/_interval_chain.py`
- Tests: `tests/test_interval_chain.py`

### Step 3: `intervals_chain(X, binding, chain_mode)`
- `src/foapy/core/_intervals_chain.py`
- Key numpy patterns from existing `_intervals.py`:
  - `np.argsort(kind="mergesort")` → stable position sort
  - Boolean mask for first/last occurrence detection
  - For `chain_mode.cycle`: `delta = len(ar) - perm[last_mask]` (cyclic gap)
  - For `chain_mode.boundary`: `delta = 1`
  - `intervals[first_mask] = perm[first_mask] + delta`
  - `intervals[1:] = perm[1:] - perm[:-1]` (interior intervals)
  - `inverse_perm` to put back in sequence order
  - Reverse `ar` and result for `binding.end`
- Returns `IntervalChain(values, binding, chain_mode)`
- Tests: `tests/test_intervals_chain.py`

### Step 4: `binding(chain)` callable and `chain_mode(chain)` callable
- Modify `src/foapy/core/_binding.py`: add `__new__` to `binding` class
- Create `src/foapy/core/_chain_mode.py` with both enum and callable
- Tests: `tests/test_binding_callable.py`, `tests/test_chain_mode_callable.py`

### Step 5: `is_valid_intervals_chain(chain)`
- `src/foapy/core/_is_valid_intervals_chain.py`
- Checks: is `IntervalChain`, 1-D values, all values ≥ 1, all values ≤ len(values)
- Returns bool, never raises
- Tests: `tests/test_is_valid_intervals_chain.py`

### Step 6: `intervals_tuple(chain, tuple_mode)`
- `src/foapy/core/_intervals_tuple.py`
- Extracts `values`, `binding`, `chain_mode` from `IntervalChain`
- Applies boundary handling based on `tuple_mode`:
  - `lossy`: filter out boundary (first-occurrence) intervals via boolean mask; for `chain_mode.cycle`, no filtering needed since cyclic interval is already a valid interior interval
  - `normal`: keep as-is (chain already encodes the correct boundary)
  - `redundant`: append trailing boundary intervals (computed as `n - perm[last_mask]`)
- For `binding.end`: reverse the result
- Tests: `tests/test_intervals_tuple.py`

### Step 7: `intervals_distribution(tuple_result)`
- `src/foapy/core/_intervals_distribution.py`
- Use `np.bincount(tuple_result - 1)` (shift by 1 since values are 1-indexed)
- Returns count array of length `max(tuple_result)`
- Empty input: return `np.array([])`
- Tests: `tests/test_intervals_distribution.py`

### Step 8: Consistency tests
- `tests/test_pipeline_consistency.py`
- Verify all 4 old-mode mappings produce identical output to `intervals()`

### Step 9: Export wiring
- Update `src/foapy/core/__init__.py`
- Update `src/foapy/__init__.py`

### Step 10: `foapy.ma` variants
- `src/foapy/ma/_intervals_chain.py`, `_intervals_tuple.py`, `_intervals_distribution.py`
- Tests: `tests/test_ma_intervals_chain.py`, etc.

### Step 11: Inline documentation
- Add numpy-style docstrings to all new functions (per FR-018)
- Include: description, Parameters, Returns, Raises, Examples sections

### Step 12: Benchmarks
- `benchmarks/bench_intervals_chain.py` etc.
- Measure wall time at n=100, n=10_000, n=1_000_000
- Print results as a simple table

### Step 13: Linting and final validation
- `pipx run pre-commit run --all-files --show-diff-on-failure`
- `tox -e default`
