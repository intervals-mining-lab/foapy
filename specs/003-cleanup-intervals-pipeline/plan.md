# Implementation Plan: Cleanup Intervals Pipeline

**Branch**: `003-cleanup-intervals-pipeline` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-cleanup-intervals-pipeline/spec.md`

## Summary

Remove three interim artefacts left over from 002-decompose-intervals-pipeline — the `_is_valid_intervals_chain` stub, the unified `mode` enum, and the `intervals()` core function — so that the public API exposes only the decomposed pipeline (`intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, `tuple_mode`). The retired `intervals()` function is preserved as a test-only helper, existing equivalence tests are kept and expanded, benchmarks are updated to use the decomposed pipeline, and documentation is updated to reflect the new canonical API with links to the fundamentals pages.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: numpy >= 1.20 (sole runtime dependency)
**Storage**: N/A
**Testing**: pytest via `tox -e default`
**Target Platform**: Any platform supporting Python 3.8+ with numpy
**Project Type**: library
**Performance Goals**: No new algorithms; existing performance characteristics are unchanged
**Constraints**: No new runtime dependencies; no breaking changes to the `foapy.ma` subpackage beyond removal of `ma.intervals`
**Scale/Scope**: ~10 source files changed, ~5 test files changed, ~10 documentation files changed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality — single responsibility, no extra deps, passes black/isort/flake8 | PASS | Removal only; no new code with multi-responsibility concerns. No new dependencies. |
| II. Testing Standards — tox canonical runner, AssertBatch for binding×mode, edge cases covered | PASS | Equivalence tests cover all 4 mode mappings × 2 binding directions. Edge cases (empty, single, all-unique, all-same) are required by the spec. Removed test_is_valid_intervals_chain.py is consistent with deferral of that feature. |
| III. API Consistency — uniform contract, `foapy.ma` mirrors core, project-defined exceptions | PASS | Five remaining public names retain their signatures unchanged. `foapy.ma.intervals` is also retired (mirrors core removal). |
| IV. Performance — vectorized numpy, O(n) memory | PASS | No new sequence-processing paths introduced. |
| V. Simplicity — YAGNI, no backwards-compat shims | PASS | `mode` and `is_valid_intervals_chain` are removed rather than aliased. No deprecation shim added. |

**Constitution violations**: None. Complexity Tracking table is not required.

## Project Structure

### Documentation (this feature)

```text
specs/003-cleanup-intervals-pipeline/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output (migration guide)
└── tasks.md             # Phase 2 output (/speckit.tasks - NOT created here)
```

### Source Code (repository root)

Files **removed** from source tree:

```text
src/foapy/core/_is_valid_intervals_chain.py   ← DELETE
src/foapy/core/_mode.py                        ← DELETE
src/foapy/core/_intervals.py                   ← MOVE to test helper
src/foapy/ma/_intervals.py                     ← MOVE to test helper
```

Files **modified** in source tree:

```text
src/foapy/__init__.py                          ← remove intervals, mode, is_valid_intervals_chain imports
src/foapy/core/__init__.py                     ← remove intervals, mode, is_valid_intervals_chain imports
src/foapy/ma/__init__.py                       ← remove intervals import
```

Test helper (new):

```text
tests/helpers/__init__.py                      ← new (empty)
tests/helpers/intervals.py                     ← moved core intervals() function
tests/helpers/ma_intervals.py                  ← moved ma intervals() function
```

Tests **removed**:

```text
tests/test_is_valid_intervals_chain.py         ← DELETE (feature deferred; no replacement needed)
```

Tests **converted** (old tests transformed into equivalence verifiers using test helper):

```text
tests/test_intervals.py                        ← convert: import intervals from helpers, assert vs decomposed pipeline
tests/test_ma_intervals.py                     ← convert: import ma intervals from helpers, assert vs decomposed pipeline
```

Tests **unchanged** (already verifying decomposed pipeline):

```text
tests/test_pipeline_consistency.py             ← already comprehensive; extend with edge cases if missing
tests/test_intervals_chain.py                  ← unchanged
tests/test_intervals_tuple.py                  ← unchanged
tests/test_intervals_distribution.py           ← unchanged
```

Documentation files **removed**:

```text
docs/references/intervals.md                   ← DELETE
docs/references/mode.md                        ← DELETE
docs/references/ma/intervals.md                ← DELETE (or convert to stub pointing to new pages)
```

Documentation files **added**:

```text
docs/references/intervals_chain.md
docs/references/intervals_tuple.md
docs/references/intervals_distribution.md
docs/references/chain_mode.md
docs/references/tuple_mode.md
docs/references/ma/intervals_chain.md          ← already exists? check
docs/references/ma/intervals_tuple.md          ← check/add
docs/references/ma/intervals_distribution.md   ← check/add
```

`mkdocs.yml` nav updated:
- Remove `foapy.intervals`, `foapy.mode`, `ma/intervals.md` entries
- Add `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, `tuple_mode` entries
- Add ma equivalents

**Structure Decision**: Single-project layout. All changes are within the existing `src/foapy/`, `tests/`, and `docs/` directories.

---

## Phase 0: Research

*See [research.md](./research.md).*

---

## Phase 1: Design & Contracts

*See [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md).*
