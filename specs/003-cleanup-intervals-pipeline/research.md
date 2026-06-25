# Research: Cleanup Intervals Pipeline

**Branch**: `003-cleanup-intervals-pipeline` | **Date**: 2026-04-19

## Summary

This feature is a cleanup/removal task. No new algorithms, patterns, or technologies are introduced. All design decisions are explicit in the spec and derived from the completed 002-decompose-intervals-pipeline work. The research below documents the decisions already made and the key facts discovered by reading the current codebase.

---

## Decision 1: Test-Helper Location for the Retired `intervals()` Functions

**Decision**: Create `tests/helpers/intervals.py` (for `foapy.core.intervals`) and `tests/helpers/ma_intervals.py` (for `foapy.ma.intervals`), both unexported from any public package.

**Rationale**: A dedicated `tests/helpers/` directory is a standard pattern for test utilities that are not part of the library API. Placing them there makes it unambiguous that these functions are test fixtures and prevents accidental re-import from any production code path.

**Alternatives considered**:
- Inline the old logic in `tests/test_pipeline_consistency.py` directly — rejected because the function body is non-trivial and would be duplicated if used in multiple test files.
- Keep a `_intervals_compat.py` shim in `src/foapy/core/` — rejected: the constitution prohibits backwards-compatibility shims (Principle V).

---

## Decision 2: Fate of `tests/test_intervals.py` and `tests/test_ma_intervals.py`

**Decision**: Convert both files in-place: replace `from foapy import intervals, mode` with `from tests.helpers.intervals import intervals` (and the corresponding `mode` shim if needed), so that each existing test case becomes an equivalence assertion between the helper and the decomposed pipeline. No test cases are deleted.

**Rationale**: The spec requires that no previously-present test is silently deleted (FR-004). Converting in-place preserves test coverage intent while making the comparison explicit. The existing `tests/test_pipeline_consistency.py` already covers the same four mappings parametrically, but the original test files also cover detailed edge-case inputs that should not be lost.

**Alternatives considered**:
- Merge everything into `test_pipeline_consistency.py` and delete the original files — rejected because it risks losing specific edge-case inputs that appear in `test_intervals.py` and `test_ma_intervals.py` but not in the parametric file.

---

## Decision 3: Fate of `tests/test_is_valid_intervals_chain.py`

**Decision**: Delete the file outright. No replacement test module is created.

**Rationale**: `is_valid_intervals_chain` is a deferred feature (spec §1). Its stub is being removed; there is nothing for tests to verify. Keeping the test file would reference a non-existent public symbol and cause import errors.

**Alternatives considered**:
- Move to `tests/helpers/` and skip with `pytest.mark.skip` — rejected: a skipped test for a non-existent function adds maintenance noise with zero benefit.

---

## Decision 4: `foapy.ma.intervals` Retirement

**Decision**: `src/foapy/ma/_intervals.py` is moved to `tests/helpers/ma_intervals.py` and removed from `foapy.ma.__init__`. The `tests/test_ma_intervals.py` file is converted to import from the test helper and assert equivalence against `foapy.ma.intervals_tuple(foapy.ma.intervals_chain(...), ...)`.

**Rationale**: The user's spec scopes the removal to `src/foapy/core/_intervals.py` explicitly, but `foapy.ma` mirrors every core change (constitution Principle III: "`foapy.ma` MUST mirror every public function in `foapy.core`"). Since `intervals` is removed from core, it must also be removed from `foapy.ma`.

**Alternatives considered**:
- Keep `foapy.ma.intervals` while removing `foapy.core.intervals` — rejected: Principle III requires mirroring; an asymmetric API would be a constitution violation.

---

## Decision 5: Documentation Structure

**Decision**: Add one reference page per new public name: `intervals_chain.md`, `intervals_tuple.md`, `intervals_distribution.md`, `chain_mode.md`, `tuple_mode.md` under `docs/references/`. Mirror for `foapy.ma` (`ma/intervals_chain.md`, `ma/intervals_tuple.md`, `ma/intervals_distribution.md`). Remove `intervals.md` and `mode.md`. Update `mkdocs.yml` nav accordingly. Each new page uses the `:::foapy.<name>` mkdocstrings directive and links to the corresponding fundamentals section.

**Mapping of public names to fundamentals pages**:

| Public name | Fundamentals link |
|-------------|------------------|
| `intervals_chain` | `fundamentals/order/intervals_chain/` |
| `chain_mode` | `fundamentals/order/intervals_chain/bounded.md` and `fundamentals/order/intervals_chain/cycled.md` |
| `intervals_tuple` | `fundamentals/order/intervals_distribution/` |
| `tuple_mode` | `fundamentals/order/intervals_distribution/lossy.md` and `fundamentals/order/intervals_distribution/redundant.md` |
| `intervals_distribution` | `fundamentals/order/intervals_distribution/index.md` |

**Rationale**: Each reference page is a thin mkdocstrings directive that auto-generates content from docstrings. The fundamentals link anchors the function in its mathematical context.

**Alternatives considered**:
- A single combined page for all five names — rejected: the existing pattern (one page per public symbol) is established in `docs/references/` and must be followed for consistency.

---

## Key Codebase Facts Discovered

- `src/foapy/__init__.py` imports `intervals`, `mode`, and `is_valid_intervals_chain` from `foapy.core`; all three must be removed from this file.
- `src/foapy/core/__init__.py` imports `_intervals`, `_mode`, and `_is_valid_intervals_chain`; all three must be removed.
- `src/foapy/ma/__init__.py` imports `_intervals`; this must be removed.
- `src/foapy/ma/_intervals.py` imports `from foapy import mode as mode_enum`; this dependency on the retired `mode` is another reason to move it out of the production source tree.
- `tests/test_pipeline_consistency.py` already exists and imports `intervals` from `foapy` for comparison; after this cleanup it must import from the test helper instead.
- `docs/references/ma/` currently only has `alphabet.md`, `index.md`, `intervals.md`, `order.md` — no pages yet for `intervals_chain`, `intervals_tuple`, `intervals_distribution`; all three must be added.
- `mkdocs.yml` nav references `references/intervals.md`, `references/mode.md`, and `references/ma/intervals.md`; all three must be replaced.
