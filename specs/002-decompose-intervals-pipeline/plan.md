# Implementation Plan: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-decompose-intervals-pipeline/spec.md`

## Summary

Decompose the monolithic `intervals(X, binding, mode)` into three composable pipeline stages: `intervals_chain(X, binding, chain_mode)` → `intervals_tuple(chain, binding, tuple_mode)` → `intervals_distribution(tuple_result)`, plus the `is_valid_intervals_chain` validator and the `chain_mode`/`tuple_mode` enum namespaces. `intervals()` is preserved unchanged for backward compatibility.

**Current state (2026-04-19)**: All core implementations, `foapy.ma` variants, test suites (440 passing), and benchmarks are in place. One open defect remains: `bench_intervals_tuple.py` and `bench_intervals_distribution.py` call `intervals_tuple` with the old 2-argument signature (missing `binding`). These benchmarks will fail at runtime.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: numpy >= 1.20 (sole runtime dependency)
**Storage**: N/A
**Testing**: tox -e default (pytest + coverage)
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Python library
**Performance Goals**: Operations on sequences up to length 10,000 in < 100 ms on a single CPU core (Constitution IV)
**Constraints**: No Python-level loops over array elements; all operations vectorized via numpy
**Scale/Scope**: 1-D sequences up to 1,000,000 elements in benchmark suite

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality — pure functions, no extra deps, passes lint | ✅ PASS | All new functions are pure; no deps beyond numpy; pre-commit passes |
| II. Testing Standards — tox, CharacteristicsTest, all binding×mode combos | ✅ PASS | 440 tests pass; pipeline functions use `assert_array_equal` (not float); all binding × chain_mode × tuple_mode combos covered in `test_pipeline_consistency.py` |
| III. API Consistency — 1-D X first arg, binding/mode as enums, ma mirrors core, project exceptions | ✅ PASS | All signatures follow convention; `foapy.ma` variants mirror core; `Not1DArrayException` and `ValueError` used correctly |
| IV. Performance — vectorized numpy, no Python loops, < 100 ms for n ≤ 10,000 | ✅ PASS | `argsort`, boolean masking, `bincount` used throughout; no Python loops |
| V. Simplicity — YAGNI, no shared state, helpers extracted only at 3+ sites | ✅ PASS | No unnecessary abstractions; `binding`/`chain_mode` inference removed from scope |

**Post-design re-check**: No violations found. No entry in Complexity Tracking required.

## Project Structure

### Documentation (this feature)

```text
specs/002-decompose-intervals-pipeline/
├── plan.md              ✅ This file
├── research.md          ✅ Phase 0 complete (updated 2026-04-19)
├── data-model.md        ✅ Phase 1 complete
├── quickstart.md        ✅ Phase 1 complete
├── contracts/
│   └── public-api.md   ✅ Phase 1 complete
└── tasks.md             (Phase 2 — /speckit.tasks command)
```

### Source Code (repository root)

```text
src/foapy/
├── __init__.py                              ✅ exports all new symbols
├── core/
│   ├── __init__.py                          ✅ exports all new symbols
│   ├── _chain_mode.py                       ✅ enum namespace
│   ├── _tuple_mode.py                       ✅ enum namespace
│   ├── _intervals_chain.py                  ✅ implemented, 100% coverage
│   ├── _intervals_tuple.py                  ✅ implemented, 94% coverage
│   ├── _intervals_distribution.py           ✅ implemented, 100% coverage
│   └── _is_valid_intervals_chain.py         ✅ implemented, 100% coverage
└── ma/
    ├── __init__.py                          ✅ exports intervals_chain/tuple/distribution
    ├── _intervals_chain.py                  ✅ compresses masked array, delegates to core
    ├── _intervals_tuple.py                  ✅ thin wrapper around core
    └── _intervals_distribution.py           ✅ thin wrapper around core

tests/
├── test_chain_mode.py                       ✅
├── test_tuple_mode.py                       ✅
├── test_binding_callable.py                 ✅ verifies TypeError on construction
├── test_chain_mode_callable.py              ✅ verifies TypeError on construction
├── test_intervals_chain.py                  ✅
├── test_intervals_tuple.py                  ✅
├── test_intervals_distribution.py           ✅
├── test_is_valid_intervals_chain.py         ✅
├── test_pipeline_consistency.py             ✅ equivalence with intervals()
├── test_ma_intervals_chain.py               ✅
├── test_ma_intervals_tuple.py               ✅
└── test_ma_intervals_distribution.py        ✅

benchmarks/benchmarks/
├── bench_intervals_chain.py                 ✅ correct 3-arg signature
├── bench_intervals_tuple.py                 ⚠️ BUG: 2-arg intervals_tuple call
└── bench_intervals_distribution.py          ⚠️ BUG: 2-arg intervals_tuple call in setup
```

**Structure Decision**: Single-project layout matching the existing `src/foapy/` layout. New files follow the `_<name>.py` private-module naming convention with public exports via `__init__.py`.

## Open Defects

| # | File | Line | Issue | Fix |
|---|------|------|-------|-----|
| 1 | `benchmarks/benchmarks/bench_intervals_tuple.py` | 27, 30 | `intervals_tuple(self.chain, self.tuple_mode)` — missing `binding` argument | Add `binding.start` as second argument |
| 2 | `benchmarks/benchmarks/bench_intervals_distribution.py` | 29 | `intervals_tuple(chain, tuple_mode.normal)` — missing `binding` argument | Add `binding.start` as second argument |

These benchmarks will raise `TypeError` at runtime. The fix is one line per file.

## Complexity Tracking

> No constitution violations requiring justification.
