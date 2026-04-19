# Tasks: foapy.partials Package

**Input**: Design documents from `/specs/004-partials-package/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: Included — required by Constitution Principle II and SC-006 (full test coverage).

**Organization**: Tasks grouped by user story (4 stories → Phases 3–6), each independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable with other [P] tasks (different files, no dependencies)
- **[Story]**: Maps to user story (US1=order, US2=intervals_chain, US3=intervals_tuple, US4=alphabet)

---

## Phase 1: Setup (Package Skeleton)

**Purpose**: Create the `foapy.partials` package structure and wire it into `foapy`.

- [X] T001 Create `src/foapy/partials/` directory with empty `__init__.py` shell (exports: `order`, `alphabet`, `intervals_chain`, `intervals_tuple` — stubs filled in per story)
- [X] T002 Update `src/foapy/__init__.py`: add `'partials'` to `__foapy_submodules__` set and add `if attr == "partials": import foapy.partials as partials; return partials` branch in `__getattr__`

**Checkpoint**: `import foapy.partials` must not raise `AttributeError`.

---

## Phase 3: User Story 1 — `partials.order()` (Priority: P1) 🎯 MVP

**Goal**: Deliver `partials.order()` — accepts a masked or plain 1-D array, returns a masked 1-D array of the same length with alphabet indices at non-masked positions.

**Independent Test**: `import foapy.partials as p; import numpy.ma as ma; X = ma.masked_array(['a','b','a'], mask=[0,1,0]); r = p.order(X); assert r.shape == (3,) and list(r.compressed()) == [0, 0]`

### Tests for User Story 1

> **Write these tests FIRST; ensure they FAIL before implementing `_order.py`**

- [X] T003 [P] [US1] Write tests for `partials.order` in `tests/test_partials_order.py` covering: empty array, single element, all-unique symbols, all-same symbol, realistic dataset, fully masked, partially masked, no-mask passthrough (result equals `foapy.core.order`), multi-dimensional input raises `Not1DArrayException`, `return_alphabet=True` returns correct alphabet

### Implementation for User Story 1

- [X] T004 [US1] Implement `src/foapy/partials/_order.py`: `ma.asarray` wrap, 1-D validation, `ar.compressed()` + `core.order()` + `result_data[~mask] = order_compressed` + `ma.masked_array(result_data, mask)`, `return_alphabet` branch
- [X] T005 [US1] Export `order` from `src/foapy/partials/__init__.py`

**Checkpoint**: `tox -e default -- tests/test_partials_order.py -v` passes with zero failures.

---

## Phase 4: User Story 2 — `partials.intervals_chain()` (Priority: P2)

**Goal**: Deliver `partials.intervals_chain()` — accepts a masked or plain 1-D raw sequence, returns a masked 1-D array of the same length where interval distances at non-masked positions reflect actual positional distances including gap positions.

**Independent Test**: `X = ma.masked_array(['_','C','T','C','_','G'], mask=[1,0,0,0,1,0]); chain = p.intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary); assert list(chain.compressed()) == [2, 3, 2, 6]`

### Tests for User Story 2

> **Write these tests FIRST; ensure they FAIL before implementing `_intervals_chain.py`**

- [X] T006 [P] [US2] Write tests for `partials.intervals_chain` in `tests/test_partials_intervals_chain.py` covering: empty array, single element, all-unique symbols, all-same symbol, realistic dataset with gaps, fully masked array, partially masked (gaps count toward distance), no-mask passthrough (equals `foapy.core.intervals_chain`), invalid binding raises `ValueError`, invalid chain_mode raises `ValueError`, multi-dimensional input raises `Not1DArrayException`, both `binding.start` and `binding.end`, both `chain_mode.boundary` and `chain_mode.cycle`

### Implementation for User Story 2

- [X] T007 [US2] Implement `src/foapy/partials/_intervals_chain.py`: `ma.asarray` wrap, parameter validation, `non_masked_idx = np.where(~full_mask)[0]`, binding.end reversal, stable argsort on `compressed_values`, group boundary detection (`first_mask`/`last_mask`), `chain_compressed[1:] = actual_pos[perm[1:]] - actual_pos[perm[:-1]]`, boundary intervals using `actual_pos[perm[first_mask]] + delta`, inverse permutation, `ma.masked_array(result_data, mask=full_mask)`
- [X] T008 [US2] Export `intervals_chain` from `src/foapy/partials/__init__.py`

**Checkpoint**: `tox -e default -- tests/test_partials_intervals_chain.py -v` passes with zero failures.

---

## Phase 5: User Story 3 — `partials.intervals_tuple()` (Priority: P3)

**Goal**: Deliver `partials.intervals_tuple()` — applies `normal` / `lossy` / `redundant` boundary strategies to a masked 1-D intervals chain. `lossy` masks boundary positions in-place (same length); `redundant` appends k trailing intervals.

**Independent Test**: `chain = ma.masked_array([0,2,3,2,0,6], mask=[1,0,0,0,1,0]); result = p.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.normal); assert result.shape == (6,) and np.array_equal(result.mask, chain.mask)`

### Tests for User Story 3

> **Write these tests FIRST; ensure they FAIL before implementing `_intervals_tuple.py`**

- [X] T009 [P] [US3] Write tests for `partials.intervals_tuple` in `tests/test_partials_intervals_tuple.py` covering: `tuple_mode.normal` (mask unchanged, values unchanged), `tuple_mode.lossy` (boundary positions additionally masked, output length == input length), `tuple_mode.redundant` (trailing k intervals appended unmasked, output length == n+k), no-mask passthrough for normal/lossy (non-masked values equal `foapy.core.intervals_tuple` result), empty input, fully masked input, invalid binding raises `ValueError`, invalid tuple_mode raises `ValueError`

### Implementation for User Story 3

- [X] T010 [US3] Implement `src/foapy/partials/_intervals_tuple.py`: `ma.asarray` wrap, parameter validation, `normal` (copy), `lossy` (compress → `ar > positions` boundary detection → map boundary indices back to original positions → set `new_mask[boundary_original_idx] = True`), `redundant` (compress → `core.intervals_tuple` with redundant → split plain result at `len(compressed)` → `np.concatenate` with trailing; append unmasked)
- [X] T011 [US3] Export `intervals_tuple` from `src/foapy/partials/__init__.py`

**Checkpoint**: `tox -e default -- tests/test_partials_intervals_tuple.py -v` passes with zero failures.

---

## Phase 6: User Story 4 — `partials.alphabet()` (Priority: P4)

**Goal**: Deliver `partials.alphabet()` — accepts a masked or plain 1-D array, returns a plain 1-D array of unique non-masked values in first-appearance order.

**Independent Test**: `X = ma.masked_array(['a','b','a','c'], mask=[0,1,0,0]); assert list(p.alphabet(X)) == ['a', 'c']`

### Tests for User Story 4

> **Write these tests FIRST; ensure they FAIL before implementing `_alphabet.py`**

- [X] T012 [P] [US4] Write tests for `partials.alphabet` in `tests/test_partials_alphabet.py` covering: empty array, single element, all-unique symbols, all-same symbol, realistic dataset, fully masked (returns empty array), partially masked (masked values excluded), no-mask passthrough (equals `foapy.core.alphabet`), multi-dimensional input raises `Not1DArrayException`

### Implementation for User Story 4

- [X] T013 [US4] Implement `src/foapy/partials/_alphabet.py`: `ma.asarray` wrap, 1-D validation, `_, alphabet = core.order(ar.compressed(), return_alphabet=True); return alphabet`
- [X] T014 [US4] Export `alphabet` from `src/foapy/partials/__init__.py`

**Checkpoint**: `tox -e default -- tests/test_partials_alphabet.py -v` passes with zero failures.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end verification, pipeline consistency, and code quality.

- [X] T015 Add pipeline consistency test in `tests/test_partials_pipeline_consistency.py`: for any plain (unmasked) input, verify `partials.order == core.order`, `partials.intervals_chain == core.intervals_chain`, and `partials.intervals_tuple == core.intervals_tuple` across all binding × chain_mode × tuple_mode combinations
- [X] T016 Run full test suite `tox -e default` and verify zero failures across all tests including existing `foapy.core` and `foapy.ma` tests (no regressions)
- [X] T017 [P] Run linting `pipx run pre-commit run --all-files --show-diff-on-failure` and fix any black/isort/flake8 violations in `src/foapy/partials/`
- [X] T018 [P] Validate quickstart examples from `specs/004-partials-package/quickstart.md` execute without error in a Python REPL

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **User Stories (Phases 3–6)**: Depend on Phase 1 completion; each story is independent of the others
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependency on US2/US3/US4
- **US2 (P2)**: No dependency on US1/US3/US4
- **US3 (P3)**: No dependency on US1/US2/US4
- **US4 (P4)**: No dependency on US1/US2/US3

All four user stories can proceed in parallel after Phase 1 completes.

### Within Each User Story

1. Write tests (T003/T006/T009/T012) → **verify they FAIL**
2. Implement module (T004/T007/T010/T013)
3. Export from `__init__.py` (T005/T008/T011/T014)
4. **Verify tests now PASS**

### Parallel Opportunities

- T003, T006, T009, T012 (test writing) can all run in parallel — different files
- T004, T007, T010, T013 (implementations) can run in parallel — different files, but wait for respective test task first
- T017, T018 (polish) can run in parallel

---

## Parallel Example: After Phase 1

```bash
# All four test tasks can be launched together:
Task T003: "Write tests for partials.order in tests/test_partials_order.py"
Task T006: "Write tests for partials.intervals_chain in tests/test_partials_intervals_chain.py"
Task T009: "Write tests for partials.intervals_tuple in tests/test_partials_intervals_tuple.py"
Task T012: "Write tests for partials.alphabet in tests/test_partials_alphabet.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 3: US1 (T003–T005)
3. **STOP and VALIDATE**: `tox -e default -- tests/test_partials_order.py -v`
4. `import foapy.partials; foapy.partials.order(...)` works end-to-end

### Incremental Delivery

1. Phase 1 → Foundation ready
2. Phase 3 (US1: order) → MVP: partials.order works
3. Phase 4 (US2: intervals_chain) → Full interval pipeline
4. Phase 5 (US3: intervals_tuple) → Complete boundary handling
5. Phase 6 (US4: alphabet) → Full public API complete
6. Phase 7 (Polish) → Test suite green, linting clean

### Parallel Strategy

With one developer, recommended order: T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 → T012 → T013 → T014 → T015 → T016 → T017 → T018

---

## Notes

- [P] tasks operate on different files with no incomplete dependencies
- Each test task must produce failing tests BEFORE the paired implementation task runs
- Constitution Principle IV: all implementations must use vectorized numpy — no Python loops over array elements
- `intervals_chain` accepts the **raw sequence** (not the order output) — mirrors `foapy.core.intervals_chain`
- `intervals_tuple.lossy` preserves array length (masks boundary positions rather than removing them)
- `intervals_tuple.redundant` appends k trailing unmasked elements (output length = n + k)
- `foapy/__init__.py` update (T002) is the only modification to an existing file
