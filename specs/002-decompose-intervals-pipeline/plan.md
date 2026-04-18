# Implementation Plan: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-04-18 | **Spec**: [spec.md](../../.specify/features/002-decompose-intervals-pipeline/spec.md)
**Input**: Feature specification from `/specs/002-decompose-intervals-pipeline/spec.md`

## Summary

Decompose the monolithic `intervals()` function into three independently callable pipeline stages: `intervals_chain`, `intervals_tuple`, and `intervals_distribution`. The key change is that `intervals_tuple` now takes `binding` as an **explicit** positional parameter instead of inferring it from chain structure. The core implementation is already complete; the remaining work is updating `foapy.ma._intervals_tuple` to accept `binding`, fixing the `intervals_tuple` docstring, adding `binding` validation, and updating all tests to pass `binding` explicitly.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: numpy >= 1.20 (sole runtime dependency per constitution)
**Storage**: N/A
**Testing**: tox -e default (pytest under the hood)
**Target Platform**: Any platform supporting Python 3.8+ and numpy 1.20
**Project Type**: Scientific Python library
**Performance Goals**: Sequences up to length 10,000 in < 100 ms on a single CPU core (Constitution IV)
**Constraints**: Pure vectorised numpy only — no Python loops over array elements; O(n) memory
**Scale/Scope**: Core library primitive used by all characteristic computations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Lint (black, isort, flake8) | ✅ | No style violations expected; enforce via pre-commit |
| Tests (tox -e default) | ⚠️ FAILING | Tests call `intervals_tuple(chain, tuple_mode.x)` — old 2-arg form. Must be updated to pass `binding`. |
| Constitution check | ✅ | No open violations; changes are minimal and targeted |
| API consistency | ⚠️ GAP | `foapy.ma._intervals_tuple` still uses old 2-arg signature; must mirror core |
| Performance | ✅ | All operations are vectorised numpy; no loops introduced |

**No constitution violations to justify in Complexity Tracking.**

## Project Structure

### Documentation (this feature)

```text
specs/002-decompose-intervals-pipeline/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks — not created here)
```

### Source Code (affected files)

```text
src/foapy/
├── core/
│   ├── _intervals_tuple.py    # FIX: update docstring + add binding validation
│   └── _intervals.py          # already delegates correctly — no changes needed
├── ma/
│   └── _intervals_tuple.py    # FIX: add binding param to match core signature

tests/
├── test_intervals_tuple.py    # FIX: add binding arg to every intervals_tuple() call
└── test_ma_intervals_tuple.py # FIX: add binding arg to every intervals_tuple() call
```

## Phase 0: Research

No external unknowns. All decisions are resolved by existing code and constitution.

### Decision Log

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| `binding` as 2nd positional arg (not keyword-only) | Matches `intervals_chain(X, binding, chain_mode)` contract; constitution §III requires uniform positional signature | keyword-only (`*`, binding) — inconsistent with chain |
| Validate `binding` in `intervals_tuple` with ValueError | Constitution §III: raise ValueError for unrecognised enum values | Silent ignore — would hide caller bugs |
| `ma.intervals_tuple` delegates to core with same args | Constitution §III: ma mirrors core signature exactly | Independent implementation — unnecessary complexity |
| `intervals_distribution` is a frequency utility, not a pipeline stage | Current `intervals()` never calls it; it computes value-frequency counts, not per-symbol grouping | Renaming/rearchitecting out of scope; no behaviour change needed |

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md).

### Public API Contracts

See [contracts/](contracts/).

### Quickstart

See [quickstart.md](quickstart.md).

## Complexity Tracking

> No constitution violations requiring justification.
