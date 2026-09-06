# Tasks: Cleanup Intervals Pipeline

**Input**: Design documents from `/specs/003-cleanup-intervals-pipeline/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅ quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to
- Exact file paths are included in every description

---

## Phase 1: Setup

**Purpose**: Create the test-helper directory that will house the retired `intervals()` functions. This is a prerequisite for Phases 2+ and must be completed first.

- [x] T001 Create `tests/helpers/__init__.py` as an empty module marker

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Populate the test helpers with the retired `intervals()` functions before any source files are removed. Both helpers must exist before the source removals in US1.

**⚠️ CRITICAL**: US1 source-file deletions must not happen until T002 and T003 are complete.

- [x] T002 Create `tests/helpers/intervals.py`: copy `intervals()` function body verbatim from `src/foapy/core/_intervals.py` and copy `mode` enum definition verbatim from `src/foapy/core/_mode.py`; add module docstring noting this is a test-only helper not part of the public API; ensure all imports are self-contained (no `from foapy import ...` references to the retiring names)
- [x] T003 [P] Create `tests/helpers/ma_intervals.py`: copy `intervals()` function body verbatim from `src/foapy/ma/_intervals.py`; replace `from foapy import mode as mode_enum` with a local import from `tests.helpers.intervals`; add module docstring noting test-only status

**Checkpoint**: Both test helpers in place and importable — source removal can now proceed.

---

## Phase 3: User Story 1 — Public API Contains Only the Decomposed Pipeline (Priority: P1) 🎯 MVP

**Goal**: Remove `intervals`, `mode`, and `is_valid_intervals_chain` from every public namespace so that any attempt to import them from `foapy` raises `ImportError`.

**Independent Test**: `python -c "from foapy import intervals"` raises `ImportError`; `python -c "from foapy import intervals_chain, intervals_tuple, intervals_distribution, chain_mode, tuple_mode"` succeeds.

### Implementation for User Story 1

- [x] T004 [P] [US1] Update `src/foapy/core/__init__.py`: remove the three import lines for `_mode`, `_intervals`, `_is_valid_intervals_chain`; remove `"mode"`, `"intervals"`, `"is_valid_intervals_chain"` from `__all__`
- [x] T005 [P] [US1] Update `src/foapy/__init__.py`: remove `from foapy.core import intervals`, `from foapy.core import mode`, `from foapy.core import is_valid_intervals_chain`; remove all three names from `__all__`; remove `"intervals"`, `"mode"` from the `__dir__` inline set
- [x] T006 [P] [US1] Update `src/foapy/ma/__init__.py`: remove `from ._intervals import intervals`; remove `"intervals"` from `__all__`
- [x] T007 [US1] Delete `src/foapy/core/_is_valid_intervals_chain.py` (after T004 complete)
- [x] T008 [P] [US1] Delete `src/foapy/core/_mode.py` (after T004 complete — parallel with T007)
- [x] T009 [P] [US1] Delete `src/foapy/core/_intervals.py` (after T004 complete — parallel with T007, T008)
- [x] T010 [US1] Delete `src/foapy/ma/_intervals.py` (after T006 complete)
- [x] T011 [P] [US1] Delete `tests/test_is_valid_intervals_chain.py` (no source to import; safe to delete independently)

**Checkpoint**: `from foapy import intervals` raises `ImportError`; `from foapy import intervals_chain, intervals_tuple, intervals_distribution, chain_mode, tuple_mode` succeeds; `tox -e default -- -k "not test_intervals and not test_ma_intervals and not test_pipeline" -q` passes.

---

## Phase 4: User Story 2 — Pipeline Equivalence Is Verified by the Test Suite (Priority: P1)

**Goal**: Convert the three affected test files to import `intervals` from the test helper instead of from `foapy`, so each test case becomes a verified equivalence assertion between the helper and the decomposed pipeline.

**Independent Test**: `tox -e default -- tests/test_intervals.py tests/test_ma_intervals.py tests/test_pipeline_consistency.py -v` passes with zero failures.

### Implementation for User Story 2

- [x] T012 [US2] Update `tests/test_intervals.py`: replace `from foapy import binding, intervals, mode` with `from foapy import binding` and `from tests.helpers.intervals import intervals, mode`; no test case bodies need to change — the helper provides identical behaviour
- [x] T013 [P] [US2] Update `tests/test_ma_intervals.py`: replace `from foapy.ma import intervals` with `from tests.helpers.ma_intervals import intervals`; keep all test bodies unchanged
- [x] T014 [P] [US2] Update `tests/test_pipeline_consistency.py`: replace `from foapy import binding, chain_mode, intervals, mode` with `from foapy import binding, chain_mode` and `from tests.helpers.intervals import intervals, mode`; keep all existing assertions; verify the file already covers all four mode mappings for both binding directions and all edge cases (empty, single-element, all-unique, all-same); add any missing edge-case tests to achieve full coverage

**Checkpoint**: `tox -e default -- tests/test_intervals.py tests/test_ma_intervals.py tests/test_pipeline_consistency.py -v` passes with zero failures.

---

## Phase 5: User Story 3 — Performance Benchmarks Use the Decomposed Pipeline (Priority: P2)

**Goal**: Replace the retired `intervals()` calls in the two benchmark files with the equivalent `intervals_chain → intervals_tuple` composition so that benchmarks measure the current public API.

**Independent Test**: `asv run --quick` (or the equivalent quick-benchmark command) completes with no import errors; no benchmark file contains `from foapy import intervals` or `from foapy.ma import intervals`.

### Implementation for User Story 3

- [x] T015 [US3] Rewrite `benchmarks/benchmarks/bench_intervals.py`: replace `from foapy import intervals` with `from foapy import binding as binding_enum, chain_mode, intervals_chain, intervals_tuple, tuple_mode`; update `IntervalsSuite` so the four `mode` integer params (1–4) map to the correct `(chain_mode, tuple_mode)` pairs in `setup()`; update `time_intervals` and `peakmem_intervals` to call `intervals_tuple(intervals_chain(self.data, self.binding, self.chain_mode), self.binding, self.tuple_mode)`; preserve all `skip_params_if` and `timeout` settings
- [x] T016 [P] [US3] Rewrite `benchmarks/benchmarks/bench_ma_intervals.py`: same pattern as T015 but import from `foapy.ma` for `intervals_chain`, `intervals_tuple`, and update `MaIntervalsSuite` accordingly; preserve all existing skip/timeout settings

**Checkpoint**: Grep `benchmarks/benchmarks/` for `from foapy import intervals` and `from foapy.ma import intervals` returns no results.

---

## Phase 6: User Story 4 — Documentation Describes Only the Decomposed Pipeline (Priority: P2)

**Goal**: Remove retired reference pages, add new pages for the five public names plus their `foapy.ma` mirrors, and update `mkdocs.yml` nav so the documentation reflects the current public API with links to the fundamentals pages.

**Independent Test**: `tox -e docs` builds without errors; no `foapy.intervals` or `foapy.mode` entries appear in the rendered nav.

### Implementation for User Story 4

- [x] T017 [P] [US4] Delete `docs/references/intervals.md` and `docs/references/mode.md`
- [x] T018 [P] [US4] Create `docs/references/intervals_chain.md`: use `:::foapy.intervals_chain` mkdocstrings directive with the same options pattern as `docs/references/binding.md`; add a "See also" link to `fundamentals/order/intervals_chain/index.md` (bounded) and `fundamentals/order/intervals_chain/cycled.md` (cycled)
- [x] T019 [P] [US4] Create `docs/references/intervals_tuple.md`: use `:::foapy.intervals_tuple` directive; add "See also" link to `fundamentals/order/intervals_distribution/index.md`
- [x] T020 [P] [US4] Create `docs/references/intervals_distribution.md`: use `:::foapy.intervals_distribution` directive; add "See also" link to `fundamentals/order/intervals_distribution/index.md`
- [x] T021 [P] [US4] Create `docs/references/chain_mode.md`: use `:::foapy.chain_mode` directive with same options as `docs/references/binding.md`; add "See also" links to `fundamentals/order/intervals_chain/bounded.md` and `fundamentals/order/intervals_chain/cycled.md`
- [x] T022 [P] [US4] Create `docs/references/tuple_mode.md`: use `:::foapy.tuple_mode` directive with same options as `docs/references/binding.md`; add "See also" links to `fundamentals/order/intervals_distribution/lossy.md` and `fundamentals/order/intervals_distribution/redundant.md`
- [x] T023 [P] [US4] Delete `docs/references/ma/intervals.md`; create `docs/references/ma/intervals_chain.md`, `docs/references/ma/intervals_tuple.md`, and `docs/references/ma/intervals_distribution.md` — each using `:::foapy.ma.<name>` directive mirroring the core counterpart format
- [x] T024 [US4] Update `mkdocs.yml` nav References section: remove `"foapy.intervals": references/intervals.md`, `"foapy.mode": references/mode.md`, and `"intervals": references/ma/intervals.md` entries; add entries for `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, `tuple_mode` under core references and their `ma/` mirrors under the ma section

**Checkpoint**: `tox -e docs` builds without warnings or errors; all five new core pages and three new ma pages render correctly.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verify quality gates pass, confirm no orphan references remain, and ensure the codebase is clean.

- [x] T025 Run `tox -e default` and confirm zero test failures; fix any remaining failures before marking complete
- [x] T026 [P] Run `pipx run pre-commit run --all-files --show-diff-on-failure` and fix any lint errors (black, isort, flake8)
- [x] T027 [P] Grep the source tree for orphan references: `grep -r "from foapy import intervals\b\|from foapy.core import intervals\b\|from foapy.ma import intervals\b\|is_valid_intervals_chain\|from foapy import mode\b\|_mode\b\|_intervals\b" src/ tests/ benchmarks/ docs/ --include="*.py" --include="*.md"`; confirm zero results outside `tests/helpers/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS US1 source deletions
- **US1 (Phase 3)**: Depends on Phase 2 (helpers must exist before source is removed)
- **US2 (Phase 4)**: Depends on Phase 2 (helpers) + Phase 3 (source removed; imports changed)
- **US3 (Phase 5)**: Depends on Phase 3 (source removed; `foapy.intervals` no longer importable)
- **US4 (Phase 6)**: Can begin in parallel with Phase 3 (doc files are independent of source)
- **Polish (Phase 7)**: Depends on all prior phases complete

### User Story Dependencies

- **US1 (P1)**: Requires Phase 2 complete; no other story dependency
- **US2 (P1)**: Requires Phase 2 + US1 complete
- **US3 (P2)**: Requires US1 complete; independent of US2
- **US4 (P2)**: Independent of US1/US2/US3 (doc files only); can proceed in parallel from Phase 3 onwards

### Within Each Phase

- T004, T005, T006 in Phase 3 can run in parallel (different files)
- T007, T008, T009 can run in parallel after T004 completes
- T010 runs after T006 completes
- T012, T013, T014 in Phase 4 can run in parallel
- T015, T016 in Phase 5 can run in parallel
- T017–T023 in Phase 6 can all run in parallel; T024 runs after T017–T023

---

## Parallel Example: Phase 3 (US1)

```
# After Phase 2 completes, launch in parallel:
T004: Update src/foapy/core/__init__.py
T005: Update src/foapy/__init__.py
T006: Update src/foapy/ma/__init__.py
T011: Delete tests/test_is_valid_intervals_chain.py

# After T004 completes, launch in parallel:
T007: Delete src/foapy/core/_is_valid_intervals_chain.py
T008: Delete src/foapy/core/_mode.py
T009: Delete src/foapy/core/_intervals.py

# After T006 completes:
T010: Delete src/foapy/ma/_intervals.py
```

## Parallel Example: Phase 6 (US4)

```
# All of these can run in parallel:
T017: Delete docs/references/intervals.md and mode.md
T018: Create docs/references/intervals_chain.md
T019: Create docs/references/intervals_tuple.md
T020: Create docs/references/intervals_distribution.md
T021: Create docs/references/chain_mode.md
T022: Create docs/references/tuple_mode.md
T023: Delete+create docs/references/ma/ files

# After T017–T023 complete:
T024: Update mkdocs.yml nav
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002–T003)
3. Complete Phase 3: US1 (T004–T011)
4. **STOP and VALIDATE**: `python -c "from foapy import intervals"` raises `ImportError`; `from foapy import intervals_chain, intervals_tuple, intervals_distribution, chain_mode, tuple_mode` succeeds
5. Then continue with US2, US3, US4

### Incremental Delivery

1. Phase 1 + 2: Helpers in place
2. Phase 3 (US1): API cleaned → test that removed names raise `ImportError`
3. Phase 4 (US2): Equivalence tests converted → `tox -e default` green
4. Phase 5 (US3): Benchmarks updated → no `intervals` import in benchmarks
5. Phase 6 (US4): Docs updated → `tox -e docs` green
6. Phase 7: Polish → all quality gates pass

---

## Notes

- **[P]** tasks touch different files and have no dependencies on incomplete tasks in the same phase
- `tests/helpers/` is accessible as a Python package only within the test suite; it is never imported from `src/`
- The `mode` enum values map to `chain_mode + tuple_mode` as documented in `contracts/api-changes.md`
- Commit logical groups: helpers, init updates, source deletions, test conversions, benchmarks, docs, polish
- Run `tox -e default -- -k <test_name> -v` after each phase to catch regressions early
