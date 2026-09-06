# Data Model: Cleanup Intervals Pipeline

**Branch**: `003-cleanup-intervals-pipeline` | **Date**: 2026-04-19

## Overview

This feature removes entities from the public API rather than adding them. The only new structural entity introduced is the **test helper module** that houses the retired `intervals()` function.

---

## Retired Entities (removed from public API)

| Entity | Current location | Disposition |
|--------|-----------------|-------------|
| `intervals(X, binding, mode)` | `src/foapy/core/_intervals.py` | Moved to `tests/helpers/intervals.py` |
| `intervals` (ma variant) | `src/foapy/ma/_intervals.py` | Moved to `tests/helpers/ma_intervals.py` |
| `mode` enum | `src/foapy/core/_mode.py` | Deleted; superseded by `chain_mode` + `tuple_mode` |
| `is_valid_intervals_chain(chain)` | `src/foapy/core/_is_valid_intervals_chain.py` | Deleted; feature deferred |

---

## New Entity: Test Helper Module

### `tests/helpers/intervals.py`

Purpose: Provides the retired `intervals(X, binding, mode)` function for use by the equivalence test suite only. Not importable from any `foapy` package path.

**Contents**:
- The `intervals()` function body moved verbatim from `src/foapy/core/_intervals.py`
- The `mode` enum class moved verbatim from `src/foapy/core/_mode.py` (needed as a local dependency)
- All imports are self-contained within the helpers directory; no `from foapy import mode` references

**Invariants**:
- Not re-exported from `tests/__init__.py` or any `foapy` init file
- Used only by `tests/test_intervals.py`, `tests/test_ma_intervals.py`, and `tests/test_pipeline_consistency.py`

### `tests/helpers/ma_intervals.py`

Purpose: Provides the retired `foapy.ma.intervals(X, binding, mode)` function for equivalence testing of the ma subpackage.

**Contents**:
- The `intervals()` function body moved verbatim from `src/foapy/ma/_intervals.py`
- Local copy of `mode` enum (or imported from `tests/helpers/intervals.py`)

---

## Remaining Public Entities (unchanged)

These entities retain their current definitions and are listed here for completeness.

| Entity | Module | Description |
|--------|--------|-------------|
| `intervals_chain(X, binding, chain_mode)` | `foapy.core` / `foapy` | Computes raw interval chain from any 1-D sequence |
| `intervals_tuple(chain, binding, tuple_mode)` | `foapy.core` / `foapy` | Applies tuple transformation mode to a chain |
| `intervals_distribution(intervals_tuple)` | `foapy.core` / `foapy` | Computes count distribution of interval lengths |
| `chain_mode` enum (`boundary`, `cycle`) | `foapy.core` / `foapy` | Controls chain construction strategy |
| `tuple_mode` enum (`lossy`, `normal`, `redundant`) | `foapy.core` / `foapy` | Controls boundary-interval handling |
| `binding` enum (`start`, `end`) | `foapy.core` / `foapy` | Controls left-to-right vs right-to-left direction |
| `order(X)` | `foapy.core` / `foapy` | Maps sequence to integer order indices |
| `alphabet(X)` | `foapy.core` / `foapy` | Returns first-appearance alphabet of sequence |
| All `foapy.ma` variants | `foapy.ma` | `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `order`, `alphabet` |
