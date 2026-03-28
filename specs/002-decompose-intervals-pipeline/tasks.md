# Tasks: Decompose Intervals Pipeline

**Input**: Design documents from `specs/002-decompose-intervals-pipeline/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Approach**: TDD — write failing tests first, implement to pass, then refactor. No Python loops over array elements; numpy vectorized operations only.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US8)

---

## Phase 1: Setup

**Purpose**: Verify existing test infrastructure works before adding new files.

- [X] T001 Verify `tox -e default` passes on current branch (baseline)
- [X] T002 Verify `pipx run pre-commit run --all-files` passes on current branch (baseline)

---

## Phase 2: Foundational — Enums

**Purpose**: `chain_mode` and `tuple_mode` enums are blocking prerequisites for every pipeline function. Must be complete before any user story work begins.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Write failing tests for `chain_mode` enum attributes in `tests/test_chain_mode.py`
- [X] T004 Implement `chain_mode` enum (`boundary=1`, `cycle=2`) in `src/foapy/core/_chain_mode.py`
- [X] T005 [P] Write failing tests for `tuple_mode` enum attributes in `tests/test_tuple_mode.py`
- [X] T006 [P] Implement `tuple_mode` enum (`lossy=1`, `normal=2`, `redundant=3`) in `src/foapy/core/_tuple_mode.py`
- [X] T007 Run `tox -e default` — T003–T006 tests must pass before proceeding

**Checkpoint**: `chain_mode` and `tuple_mode` enums importable and tested — user story phases can now begin.

---

## Phase 3: User Story 1 — `intervals_chain` (Priority: P1) 🎯 MVP

**Goal**: Expose `intervals_chain(X, binding, chain_mode)` as a standalone callable that accepts any raw 1-D sequence and returns a plain 1-D ndarray of interval values.

**Independent Test**: Call `intervals_chain(X, binding.start, chain_mode.boundary)` on a known sequence; verify returned ndarray matches expected values from the fundamentals documentation — without invoking `intervals_tuple` or `intervals_distribution`.

### Tests for User Story 1 (TDD — write and FAIL before implementing)

- [X] T008 [US1] Write failing tests for `intervals_chain` covering: empty sequence, single element, all-unique elements, all-identical elements, mixed sequence with `binding.start` + `chain_mode.boundary`, `binding.end` + `chain_mode.boundary`, `binding.start` + `chain_mode.cycle`, `binding.end` + `chain_mode.cycle`, non-1D input raises `Not1DArrayException`, invalid binding raises `ValueError`, invalid chain_mode raises `ValueError` — in `tests/test_intervals_chain.py`

### Implementation for User Story 1

- [X] T009 [US1] Implement `intervals_chain(X, binding, chain_mode)` returning plain 1-D ndarray using numpy vectorized ops (`argsort(kind="mergesort")`, boolean masking, index arithmetic) — no Python loops — in `src/foapy/core/_intervals_chain.py`
- [X] T010 [US1] Add numpy-style docstring to `intervals_chain` (description, Parameters, Returns, Raises, Examples) in `src/foapy/core/_intervals_chain.py`
- [X] T011 [US1] Export `intervals_chain` from `src/foapy/core/__init__.py`
- [X] T012 [US1] Run `tox -e default` — all T008 tests must pass

**Checkpoint**: `intervals_chain` is fully functional and independently tested.

---

## Phase 4: User Story 5 — `binding(chain)` (Priority: P2)

**Goal**: Expose `binding(chain)` as a callable that determines binding direction from a plain ndarray chain's structural properties, returning `binding.start` or `binding.end`; returns `binding.start` for empty chain.

**Independent Test**: Call `binding(chain)` on chains produced by `intervals_chain(X, binding.start, ...)` and `intervals_chain(X, binding.end, ...)` and verify returned value matches the original binding direction.

### Tests for User Story 5 (TDD — write and FAIL before implementing)

- [X] T013 [US5] Write failing tests for `binding(chain)` covering: chain from `binding.start`, chain from `binding.end`, empty chain returns `binding.start`, invalid (non-chain) input raises `ValueError` — in `tests/test_binding_callable.py`

### Implementation for User Story 5

- [X] T014 [US5] Implement `binding(chain)` callable form by adding `__new__` to the `binding` class in `src/foapy/core/_binding.py` — structural detection from ndarray values, no Python loops
- [X] T015 [US5] Add numpy-style docstring to `binding(chain)` callable form in `src/foapy/core/_binding.py`
- [X] T016 [US5] Run `tox -e default` — all T013 tests must pass

**Checkpoint**: `binding(chain)` is fully functional and independently tested.

---

## Phase 5: User Story 7 — `chain_mode(chain)` function (Priority: P2)

**Goal**: Expose `chain_mode(chain)` as a callable that determines chain_mode from a plain ndarray chain's structural properties (`chain_mode.cycle` if every element's interval group sums to n; else `chain_mode.boundary`); returns `chain_mode.cycle` for empty chain.

**Independent Test**: Call `chain_mode(chain)` on chains produced with `chain_mode.boundary` and `chain_mode.cycle` and verify returned value matches the original chain_mode.

### Tests for User Story 7 (TDD — write and FAIL before implementing)

- [X] T017 [US7] Write failing tests for `chain_mode(chain)` covering: chain from `chain_mode.boundary`, chain from `chain_mode.cycle`, empty chain returns `chain_mode.cycle`, invalid input raises `ValueError` — in `tests/test_chain_mode_callable.py`

### Implementation for User Story 7

- [X] T018 [US7] Implement `chain_mode(chain)` callable form by extending `chain_mode` class in `src/foapy/core/_chain_mode.py` with `__new__` — structural detection using interval group sum property, no Python loops
- [X] T019 [US7] Add numpy-style docstring to `chain_mode(chain)` callable form in `src/foapy/core/_chain_mode.py`
- [X] T020 [US7] Run `tox -e default` — all T017 tests must pass

**Checkpoint**: `chain_mode(chain)` is fully functional and independently tested.

---

## Phase 6: User Story 2 — `intervals_tuple` (Priority: P2)

**Goal**: Expose `intervals_tuple(chain, tuple_mode)` as a standalone callable that accepts a plain ndarray chain and a tuple_mode, detecting boundary intervals via `i - v` outside `[0, n]` uniformly across all 6 `chain_mode × tuple_mode` combinations.

**Independent Test**: Call `intervals_tuple(chain, tuple_mode)` on a known chain for all three tuple_mode values; verify output matches expected per each mode's definition — without invoking `intervals_distribution`.

### Tests for User Story 2 (TDD — write and FAIL before implementing)

- [X] T021 [US2] Write failing tests for `intervals_tuple` covering: all three `tuple_mode` values, empty chain, all-unique elements, all-identical elements, chains from both `chain_mode.boundary` and `chain_mode.cycle` (all 6 combinations), single-occurrence elements with `tuple_mode.redundant`, invalid `tuple_mode` raises `ValueError` — in `tests/test_intervals_tuple.py`

### Implementation for User Story 2

- [X] T022 [US2] Implement `intervals_tuple(chain, tuple_mode)` using numpy vectorized boundary detection (`i - v` outside `[0, n]` mask), boolean indexing for lossy, `np.concatenate` for redundant trailing intervals — no Python loops — in `src/foapy/core/_intervals_tuple.py`
- [X] T023 [US2] Add numpy-style docstring to `intervals_tuple` in `src/foapy/core/_intervals_tuple.py`
- [X] T024 [US2] Export `intervals_tuple` from `src/foapy/core/__init__.py`
- [X] T025 [US2] Run `tox -e default` — all T021 tests must pass

**Checkpoint**: `intervals_tuple` is fully functional and independently tested.

---

## Phase 7: User Story 6 — `is_valid_intervals_chain` (Priority: P3)

**Goal**: Expose `is_valid_intervals_chain(chain)` returning `True` if the input is a valid plain 1-D ndarray of positive integers where every value ≤ len(chain); returns `False` for all invalid inputs; never raises.

**Independent Test**: Call `is_valid_intervals_chain` on chains produced by `intervals_chain` (expect `True`) and on known-invalid inputs (expect `False`) — independently, without pipeline execution.

### Tests for User Story 6 (TDD — write and FAIL before implementing)

- [X] T026 [US6] Write failing tests for `is_valid_intervals_chain` covering: valid chain returns `True`, empty array returns `True`, array with zeros returns `False`, array with negatives returns `False`, array with value > len(array) returns `False`, non-1D array returns `False` (no exception), non-array returns `False` (no exception) — in `tests/test_is_valid_intervals_chain.py`

### Implementation for User Story 6

- [X] T027 [US6] Implement `is_valid_intervals_chain(chain)` using numpy vectorized checks — no Python loops, never raises — in `src/foapy/core/_is_valid_intervals_chain.py`
- [X] T028 [US6] Add numpy-style docstring to `is_valid_intervals_chain` in `src/foapy/core/_is_valid_intervals_chain.py`
- [X] T029 [US6] Export `is_valid_intervals_chain` from `src/foapy/core/__init__.py`
- [X] T030 [US6] Run `tox -e default` — all T026 tests must pass

**Checkpoint**: `is_valid_intervals_chain` is fully functional and independently tested.

---

## Phase 8: User Story 3 — `intervals_distribution` (Priority: P3)

**Goal**: Expose `intervals_distribution(tuple_result)` as a standalone callable that accepts an intervals tuple and returns the count distribution array (length = max interval value; index i = count of value i+1).

**Independent Test**: Call `intervals_distribution([1, 2, 3, 2, 4, 6])` and verify `[1, 2, 1, 1, 0, 1]` is returned — without invoking any characteristic function.

### Tests for User Story 3 (TDD — write and FAIL before implementing)

- [X] T031 [US3] Write failing tests for `intervals_distribution` covering: known tuple with expected counts, empty tuple returns empty array, all-equal tuple with single non-zero position, single-element tuple — in `tests/test_intervals_distribution.py`

### Implementation for User Story 3

- [X] T032 [US3] Implement `intervals_distribution(tuple_result)` using `np.bincount(tuple_result - 1)` — no Python loops — in `src/foapy/core/_intervals_distribution.py`
- [X] T033 [US3] Add numpy-style docstring to `intervals_distribution` in `src/foapy/core/_intervals_distribution.py`
- [X] T034 [US3] Export `intervals_distribution` from `src/foapy/core/__init__.py`
- [X] T035 [US3] Run `tox -e default` — all T031 tests must pass

**Checkpoint**: `intervals_distribution` is fully functional and independently tested.

---

## Phase 9: User Story 4 — Pipeline Consistency with `intervals()` (Priority: P4)

**Goal**: Verify that all four old-mode-to-new-pipeline mappings produce output identical to `intervals()` for any sequence and binding direction.

**Independent Test**: Compare `intervals(X, b, mode.lossy/normal/cycle/redundant)` output with composed pipeline output for all 4 mappings across a diverse set of test sequences.

### Tests for User Story 4

- [X] T036 [US4] Write pipeline consistency tests comparing `intervals()` vs `intervals_tuple(intervals_chain(X, b, chain_mode), tuple_mode)` for all 4 mode mappings (`lossy`, `normal`, `cycle`, `redundant`) on: empty sequence, single element, all-unique, all-identical, mixed real-world sequences with both `binding.start` and `binding.end` — in `tests/test_pipeline_consistency.py`
- [X] T037 [US4] Run `tox -e default` — all T036 tests must pass

**Checkpoint**: Decomposed pipeline is provably consistent with existing `intervals()` for all supported modes.

---

## Phase 10: User Story 8 — `foapy.ma` Variants, Exports, and Benchmarks (Priority: P3)

**Goal**: Mirror `intervals_chain`, `intervals_tuple`, and `intervals_distribution` in `foapy.ma` for masked-array sequences; wire all new symbols into the top-level `foapy` namespace; add performance benchmarks for each function.

**Independent Test**: Each `foapy.ma` variant can be imported and called on masked arrays independently; all new symbols importable from `foapy` in a single import statement; benchmarks run and report execution times.

### foapy.ma Tests (TDD — write and FAIL before implementing)

- [X] T038 [P] [US8] Write failing tests for `foapy.ma.intervals_chain` covering masked-array sequences (missing values handled correctly) in `tests/test_ma_intervals_chain.py`
- [X] T039 [P] [US8] Write failing tests for `foapy.ma.intervals_tuple` in `tests/test_ma_intervals_tuple.py`
- [X] T040 [P] [US8] Write failing tests for `foapy.ma.intervals_distribution` in `tests/test_ma_intervals_distribution.py`

### foapy.ma Implementation

- [X] T041 [P] [US8] Implement `foapy.ma.intervals_chain` mirroring core API for masked arrays in `src/foapy/ma/_intervals_chain.py`
- [X] T042 [P] [US8] Implement `foapy.ma.intervals_tuple` in `src/foapy/ma/_intervals_tuple.py`
- [X] T043 [P] [US8] Implement `foapy.ma.intervals_distribution` in `src/foapy/ma/_intervals_distribution.py`
- [X] T044 [US8] Export `intervals_chain`, `intervals_tuple`, `intervals_distribution` from `src/foapy/ma/__init__.py`
- [X] T045 [US8] Export all new public symbols (`chain_mode`, `tuple_mode`, `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `binding`, `is_valid_intervals_chain`) from `src/foapy/__init__.py`
- [X] T046 [US8] Run `tox -e default` — all T038–T040 tests must pass

### Benchmarks

- [X] T047 [P] [US8] Add benchmark script measuring `intervals_chain` at n=100, n=10_000, n=1_000_000 in `benchmarks/bench_intervals_chain.py`
- [X] T048 [P] [US8] Add benchmark script for `intervals_tuple` (all tuple_mode values) in `benchmarks/bench_intervals_tuple.py`
- [X] T049 [P] [US8] Add benchmark script for `intervals_distribution` in `benchmarks/bench_intervals_distribution.py`
- [X] T050 [P] [US8] Add full end-to-end pipeline benchmark in `benchmarks/bench_pipeline_full.py`

**Checkpoint**: All foapy.ma variants tested and working; all symbols importable from top-level foapy namespace; benchmark scripts runnable.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final quality gate — linting, formatting, full test suite validation.

- [X] T051 Run `pipx run pre-commit run --all-files --show-diff-on-failure` and fix any black/isort/flake8 issues across all new files
- [X] T052 Run `tox -e default` — full test suite must pass with zero failures or errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — verify baseline immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — **blocks all user story phases**
- **Phase 3 (US1 — intervals_chain)**: Depends on Phase 2 — must complete before US5, US7, US2
- **Phase 4 (US5 — binding)**: Depends on Phase 3 (needs intervals_chain for test generation)
- **Phase 5 (US7 — chain_mode fn)**: Depends on Phase 3 (needs intervals_chain for test generation)
- **Phase 6 (US2 — intervals_tuple)**: Depends on Phase 4 and Phase 5 (needs binding and chain_mode detection)
- **Phase 7 (US6 — is_valid)**: Depends on Phase 3 — can run after US1 in parallel with US2
- **Phase 8 (US3 — intervals_distribution)**: Depends on Phase 6 (takes intervals_tuple output)
- **Phase 9 (US4 — consistency)**: Depends on Phases 6 and 8 (full pipeline needed)
- **Phase 10 (US8 — ma/exports/benchmarks)**: Depends on Phases 6, 7, 8
- **Phase 11 (Polish)**: Depends on all phases complete

### User Story Dependencies

```
Phase 2 (enums)
    └── Phase 3: US1 intervals_chain
            ├── Phase 4: US5 binding(chain)  ──┐
            ├── Phase 5: US7 chain_mode(chain) ─┤
            └── Phase 7: US6 is_valid           │
                         Phase 6: US2 intervals_tuple (depends on US5 + US7)
                             └── Phase 8: US3 intervals_distribution
                                     └── Phase 9: US4 consistency
                                         Phase 10: US8 ma/exports/benchmarks
```

### Within Each User Story

1. Write failing tests (TDD) — verify they FAIL
2. Implement to pass tests — no Python loops, numpy only
3. Add inline docstring
4. Export symbol
5. Run `tox -e default` to confirm pass

---

## Parallel Opportunities

### Phase 2 (Foundational)

```
Parallel: T005 + T006 (tuple_mode tests and implementation alongside T003 + T004 for chain_mode)
```

### Phase 4 + Phase 5 (after Phase 3 complete)

```
Parallel: Phase 4 (US5 binding) and Phase 5 (US7 chain_mode fn) can run simultaneously
```

### Phase 10 (US8 — foapy.ma variants)

```
Parallel: T038+T041 (ma.intervals_chain tests+impl)
          T039+T042 (ma.intervals_tuple tests+impl)
          T040+T043 (ma.intervals_distribution tests+impl)

Parallel: T047, T048, T049, T050 (all benchmark scripts)
```

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Complete Phase 1: Setup baseline
2. Complete Phase 2: `chain_mode` + `tuple_mode` enums
3. Complete Phase 3: `intervals_chain`
4. **STOP and VALIDATE**: `tox -e default` passes; `intervals_chain` importable from `foapy.core`
5. Demo: `intervals_chain(['b','a','b','c','b'], binding.start, chain_mode.boundary)` returns expected chain

### Incremental Delivery

1. MVP (Phase 1–3): `intervals_chain` standalone
2. Add US5+US7 (Phase 4–5): `binding(chain)` + `chain_mode(chain)` introspection
3. Add US2 (Phase 6): `intervals_tuple` — all 6 combinations valid
4. Add US6+US3 (Phase 7–8): `is_valid_intervals_chain` + `intervals_distribution`
5. Add US4 (Phase 9): Consistency proof with existing `intervals()`
6. Add US8 (Phase 10): `foapy.ma` variants + top-level exports + benchmarks
7. Polish (Phase 11): Linting + final suite

---

## Notes

- All implementation tasks: numpy vectorized only — no `for` loops over array elements
- TDD strictly enforced: tests must FAIL before writing any implementation code
- Each `tox -e default` checkpoint must pass before advancing to the next phase
- `intervals()` and old `mode` enum remain completely unchanged throughout
- `binding` and `chain_mode` serve dual roles (enum class + callable) via `__new__` on the class
- Plain ndarray is the return type of `intervals_chain` — no named tuple or metadata wrapper needed; structural detection is mathematically deterministic
