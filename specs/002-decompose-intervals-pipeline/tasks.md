# Tasks: Decompose Intervals Pipeline

**Input**: Design documents from `specs/002-decompose-intervals-pipeline/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Approach**: Python 3.8+ / numpy >= 1.20. All implementation uses vectorised numpy — no Python loops over array elements. Tests cover both `binding.start` and `binding.end` for every scenario category per Constitution Principle II. `binding`, `tuple_mode`, and `chain_mode` are non-constructable named-constant namespaces per Constitution Principles III and V.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US6)

---

## Phase 1: Setup

**Purpose**: Verify baseline before making changes.

- [X] T001 Run `tox -e default` to capture current test baseline
- [X] T002 Run `pre-commit run --all-files` to capture lint baseline

**Checkpoint**: Baseline captured.

---

## Phase 2: Foundational — Enum Namespace Classes (blocking all user stories)

**Purpose**: `chain_mode`, `tuple_mode`, and `binding` must be non-constructable named-constant namespaces before any pipeline functions validate them.

- [X] T003 Add TypeError-raising `__new__` to `binding` in `src/foapy/core/_binding.py`; remove callable-inference docstring; remove unused `numpy` import
- [X] T004 [P] Add TypeError-raising `__new__` to `chain_mode` in `src/foapy/core/_chain_mode.py`; remove callable-inference docstring; remove unused `numpy` import
- [X] T005 [P] Add TypeError-raising `__new__` to `tuple_mode` in `src/foapy/core/_tuple_mode.py`

**Checkpoint**: `binding()`, `chain_mode()`, `tuple_mode()` all raise `TypeError`; class attributes (`binding.start`, `chain_mode.boundary`, etc.) remain accessible as integers.

---

## Phase 3: User Story 4 — Verify non-constructable enums (Priority: P1)

**Goal**: Tests confirm TypeError on construction and that named constants remain intact. Satisfies Constitution Principles III and V (non-constructable named-constant namespaces).

**Independent Test**: `tox -e default -- tests/test_binding_callable.py tests/test_chain_mode_callable.py -v`

### Implementation for User Story 4

- [X] T006 [US4] Replace `tests/test_binding_callable.py` with `TestEnumNamespaceNotConstructable`:
  - `test_binding_not_constructable` — `binding()` raises `TypeError`
  - `test_binding_not_constructable_with_chain` — `binding(np.array(...))` raises `TypeError`
  - `test_binding_not_constructable_with_int` — `binding(1)` raises `TypeError`
  - `test_chain_mode_not_constructable` — `chain_mode()` raises `TypeError`
  - `test_chain_mode_not_constructable_with_arg` — `chain_mode("boundary")` raises `TypeError`
  - `test_tuple_mode_not_constructable` — `tuple_mode()` raises `TypeError`
  - `test_tuple_mode_not_constructable_with_arg` — `tuple_mode(1)` raises `TypeError`
  - `test_binding_constants_accessible` — `binding.start == 1`, `binding.end == 2`
  - `test_chain_mode_constants_accessible` — `chain_mode.boundary == 1`, `chain_mode.cycle == 2`
  - `test_tuple_mode_constants_accessible` — `tuple_mode.lossy == 1`, `.normal == 2`, `.redundant == 3`

- [X] T007 [P] [US4] Replace `tests/test_chain_mode_callable.py` with `TestChainModeNotConstructable`:
  - `test_chain_mode_not_constructable` — `chain_mode()` raises `TypeError`
  - `test_chain_mode_not_constructable_with_chain` — `chain_mode(array)` raises `TypeError`
  - `test_chain_mode_not_constructable_with_string` — `chain_mode("boundary")` raises `TypeError`
  - `test_chain_mode_not_constructable_with_2d_array` — `chain_mode(2d_array)` raises `TypeError`
  - `test_chain_mode_constants_accessible` — `chain_mode.boundary == 1`, `chain_mode.cycle == 2`
  - `test_chain_mode_boundary_usable_in_intervals_chain` — `intervals_chain(X, binding.start, chain_mode.boundary)` succeeds
  - `test_chain_mode_cycle_usable_in_intervals_chain` — `intervals_chain(X, binding.start, chain_mode.cycle)` succeeds
  - `test_cycle_chain_sum_divisible_by_n` — cycle chain sums to multiple of n

- [X] T008 [US4] Run `tox -e default -- tests/test_binding_callable.py tests/test_chain_mode_callable.py -v` — all 18 tests pass

**Checkpoint**: Constitution Principles III and V satisfied — all three enum types raise TypeError on construction; constants accessible.

---

## Phase 4: User Story 2 — Pass `binding` explicitly to `intervals_tuple` (Priority: P1)

**Goal**: `intervals_tuple(chain, binding, tuple_mode)` has validated explicit `binding` parameter, accurate docstring, updated `foapy.ma` variant, and all callers pass `binding` explicitly. Satisfies FR-002, FR-007.

**Independent Test**: `tox -e default -- tests/test_intervals_tuple.py tests/test_ma_intervals_tuple.py -v`

### Implementation for User Story 2

- [X] T009 [US2] Update `src/foapy/core/_intervals_tuple.py`:
  - Add `binding: int` as 2nd positional parameter (between `chain` and `tuple_mode`)
  - Add validation: raise `ValueError` when `binding not in {binding_cls.start, binding_cls.end}`
  - Fix docstring: remove "inferred automatically" sentence; add `binding` to Parameters section
  - Use `binding` parameter to control lossy/redundant boundary detection direction

- [X] T010 [P] [US2] Update `src/foapy/ma/_intervals_tuple.py`:
  - Add `binding: int` as 2nd positional parameter
  - Update delegation call to `core_intervals_tuple(chain, binding, tuple_mode)`

- [X] T011 [P] [US2] Update `tests/test_intervals_tuple.py`:
  - Update all `intervals_tuple(chain, ...)` calls to pass `binding` as 2nd argument

- [X] T012 [P] [US2] Update `tests/test_ma_intervals_tuple.py`:
  - Update all `intervals_tuple(chain, ...)` calls to pass `binding`; add `from foapy import binding` import

- [X] T013 [P] [US2] Update any pipeline-integration calls in `tests/test_intervals_distribution.py` to pass `binding` as 2nd argument

- [X] T014 [US2] Run `tox -e default -- tests/test_intervals_tuple.py tests/test_ma_intervals_tuple.py -v` — all tests pass

**Checkpoint**: `intervals_tuple` has correct 3-arg signature; all callers updated.

---

## Phase 5: User Story 2 (extended) — Symmetric `binding` coverage (Constitution Principle II) (Priority: P1)

**Goal**: Every scenario category has tests for both `binding.start` and `binding.end` across all three `tuple_mode` values. Satisfies Constitution Principle II (both-binding coverage), SC-005.

**Independent Test**: `tox -e default -- tests/test_intervals_tuple.py -v`

### Gaps to fill in `tests/test_intervals_tuple.py`

- [X] T015 [P] [US2] Add `test_lossy_all_unique_end` — `X=[1,2,3,4,5]`, `binding.end`, `tuple_mode.lossy` → `[]`
- [X] T016 [P] [US2] Add `test_lossy_all_identical_end` — `X=["a","a","a"]`, `binding.end`, `tuple_mode.lossy` → `[1, 1]`
- [X] T017 [P] [US2] Add `test_lossy_boundary_end_integers` — `X=[2,4,2,2,4]`, `binding.end`, `tuple_mode.lossy` → `[1, 3, 2]`
- [X] T018 [P] [US2] Add `test_redundant_all_unique_end` — `X=[1,2,3,4,5]`, `binding.end`, `tuple_mode.redundant`
- [X] T019 [P] [US2] Add `test_redundant_all_identical_end` — `X=["a","a","a"]`, `binding.end`, `tuple_mode.redundant` → `[1,1,1,1]`
- [X] T020 [P] [US2] Add `test_empty_normal_end`, `test_empty_lossy_end`, `test_empty_redundant_end` — empty chain with `binding.end` → `[]` for each `tuple_mode`
- [X] T021 [P] [US2] Add `test_lossy_single_element_start` and `test_lossy_single_element_end` — `X=["a"]`, `tuple_mode.lossy` → `[]` for both bindings
- [X] T022 [US2] Run `tox -e default -- tests/test_intervals_tuple.py -v` — all tests pass

**Checkpoint**: Constitution Principle II satisfied — every scenario × binding combination has a test.

---

## Phase 6: User Story 1 — Compose intervals from explicit stages (Priority: P1)

**Goal**: End-to-end pipeline `intervals_chain → intervals_tuple` matches `intervals()` for all `binding × mode` combinations. Satisfies FR-007, FR-008, FR-009, FR-010, FR-013, SC-001, SC-002, SC-003.

**Independent Test**: `tox -e default -- tests/test_pipeline_consistency.py -v`

### Implementation for User Story 1

- [X] T023 [US1] Verify `tests/test_pipeline_consistency.py` covers all four mode-mapping combinations:
  - `mode.lossy` ↔ `chain_mode.boundary` + `tuple_mode.lossy`
  - `mode.normal` ↔ `chain_mode.boundary` + `tuple_mode.normal`
  - `mode.cycle` ↔ `chain_mode.cycle` + `tuple_mode.normal`
  - `mode.redundant` ↔ `chain_mode.boundary` + `tuple_mode.redundant`
  - Both `binding.start` and `binding.end` for each combination

**Checkpoint**: Composed pipeline is consistent with `intervals()` for all modes.

---

## Phase 7: User Story 3 — Apply distribution stage independently (Priority: P2)

**Goal**: `intervals_distribution` is independently callable and tested. Satisfies FR-003, SC-002.

**Independent Test**: `tox -e default -- tests/test_intervals_distribution.py tests/test_ma_intervals_distribution.py -v`

### Implementation for User Story 3

- [X] T024 [US3] Verify `tests/test_intervals_distribution.py` passes — covers known tuple → count array, empty input, uniform intervals
- [X] T025 [P] [US3] Verify `tests/test_ma_intervals_distribution.py` passes

**Checkpoint**: `intervals_distribution` independently verified.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Full suite and lint gate.

- [X] T026 Run `tox -e default` — full test suite must pass with zero failures
- [X] T027 Run `pre-commit run --all-files --show-diff-on-failure` — all black/isort/flake8 checks pass

---

## Phase 9: Delivered Work — Retrospective Task Coverage

**Purpose**: Track FR/SC items implemented but not covered by Phases 1–8 tasks. All code exists; these tasks verify it meets the spec. Satisfies FR-001, FR-011, FR-014, FR-015, FR-016, FR-017, FR-018, SC-004, SC-006, SC-007, SC-008.

### intervals_chain core + ma (FR-001, FR-011, FR-014, SC-005)

- [X] T028 [US1] Verify `tests/test_intervals_chain.py` covers FR-001 and FR-011 acceptance scenarios:
  - `binding.start` and `binding.end` for `chain_mode.boundary` and `chain_mode.cycle`
  - Empty input → `array([], dtype=intp)`
  - Single-element input
  - All-unique symbols
  - All-identical symbols
  - Non-1D input → `Not1DArrayException`
  - Invalid `binding` → `ValueError`
  - Invalid `chain_mode` → `ValueError`
  Run: `tox -e default -- tests/test_intervals_chain.py -v`

- [X] T029 [P] [US1] Verify `tests/test_ma_intervals_chain.py` covers FR-014 acceptance scenarios:
  - Partially masked input
  - Fully masked input → empty chain
  - No-mask passthrough identical to core result
  Run: `tox -e default -- tests/test_ma_intervals_chain.py -v`

### is_valid_intervals_chain (FR-015, SC-006)

- [X] T030 [P] [US5] Verify `tests/test_is_valid_intervals_chain.py` covers FR-015 and SC-006 acceptance scenarios:
  - Valid chains produced by `intervals_chain` → returns `True` (0 false negatives)
  - Contains zero → `False`
  - Contains negative value → `False`
  - Contains value > n → `False`
  - Non-1D array → `False` (no exception)
  - Empty array → `True`
  Run: `tox -e default -- tests/test_is_valid_intervals_chain.py -v`

### Inline documentation (FR-016, SC-007)

- [X] T031 [P] [US6] Verify each new public function docstring contains all required fields per FR-016: description, Parameters, Returns, Raises, and at least one Example. Functions to check:
  - `src/foapy/core/_intervals_chain.py`
  - `src/foapy/core/_intervals_tuple.py`
  - `src/foapy/core/_intervals_distribution.py`
  - `src/foapy/core/_is_valid_intervals_chain.py`
  - `src/foapy/core/_chain_mode.py`
  - `src/foapy/core/_tuple_mode.py`

### Benchmarks (FR-018, SC-008, Constitution IV)

- [X] T032 [US6] Fix `benchmarks/benchmarks/bench_intervals_tuple.py`:
  - Line 27: change `intervals_tuple(self.chain, self.tuple_mode)` → `intervals_tuple(self.chain, binding.start, self.tuple_mode)`
  - Line 30: same fix
  - Add `from foapy import binding` to imports if not present

- [X] T033 [P] [US6] Fix `benchmarks/benchmarks/bench_intervals_distribution.py`:
  - Line 29: change `intervals_tuple(chain, tuple_mode.normal)` → `intervals_tuple(chain, binding.start, tuple_mode.normal)`

- [X] T034 [US6] Verify benchmark suite covers FR-018 (small ≤100, medium ≤10,000, large ≤1,000,000) for `intervals_chain`, `intervals_tuple`, and `intervals_distribution`. Confirm `bench_intervals_chain.py`, `bench_intervals_tuple.py`, `bench_intervals_distribution.py` each define all three input sizes.

### SC-004: Fundamentals documentation alignment

- [X] T035 [P] [US1] Cross-check at least one concrete example from `docs/fundamentals/` against `intervals_chain` and `intervals_tuple` outputs to satisfy SC-004. Document result in a comment in `tests/test_pipeline_consistency.py` or a new `test_fundamentals_examples.py`.

**Checkpoint**: All FRs and SCs have at least one associated task. Benchmark files callable without TypeError.

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
  ↓
Phase 2 (Foundational — enum __new__) ← blocks everything
  ↓
Phase 3 (US4 tests)  ←→  Phase 4 (US2 core)  [independent, can run in parallel]
                               ↓
                         Phase 5 (US2 binding symmetry)
                               ↓
Phase 6 (US1 consistency)  ←→  Phase 7 (US3 distribution)  [independent]
  ↓
Phase 8 (Polish)
  ↓
Phase 9 (Retrospective — FR/SC coverage verification + benchmark fix)
```

### Within-Phase Parallel Groups

- **Phase 2**: T003 ‖ T004 ‖ T005 (different files)
- **Phase 3**: T006 ‖ T007 (different files); T008 sequential after both
- **Phase 4**: T010 ‖ T011 ‖ T012 ‖ T013 (different files); T009 first; T014 last
- **Phase 5**: T015–T021 all parallel (same file — combine into one edit pass); T022 sequential after
- **Phase 6**: T023 sequential
- **Phase 7**: T024 ‖ T025 (different files)
- **Phase 9**: T029 ‖ T030 ‖ T031 ‖ T033 ‖ T034 ‖ T035 (independent); T028 and T032 sequential as needed

---

## Implementation Strategy

### MVP Sequence (P1 stories first)

1. **Phase 2** (T003–T005): Make enums non-constructable — prerequisite for all validation
2. **Phase 3** (T006–T008): Test enum TypeError behavior
3. **Phase 4** (T009–T014): `intervals_tuple` explicit binding + tests
4. **Phase 5** (T015–T022): Symmetric binding coverage (Constitution Principle II)
5. **Phase 6** (T023): Pipeline consistency verification
6. **Phase 7** (T024–T025): Distribution stage verification
7. **Phase 8** (T026–T027): Full suite + lint
8. **Phase 9** (T028–T035): Retrospective FR/SC verification + benchmark bug fix

### Key implementation notes

- **`__new__` pattern**: `def __new__(cls, *args, **kwargs): raise TypeError(cls.__name__ + " cannot be instantiated.")` — class attributes (`start`, `end`, etc.) are unaffected by `__new__` and remain accessible via dot notation
- **Unused imports**: Removing `__new__` from `binding` and `chain_mode` makes `import numpy as np` unused — remove it to avoid flake8 F401
- **FR-010**: No source file calls `binding(chain)` as callable inference — only test files do. Replacing the test files is sufficient; no source code changes needed beyond adding `__new__`
- **`tuple_mode.normal` binding invariance**: For `tuple_mode.normal`, `binding` has no effect on output (chain returned unchanged). FR-002 only requires correct behaviour for `lossy` and `redundant`.
