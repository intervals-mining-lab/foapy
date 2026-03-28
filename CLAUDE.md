# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FoaPy is a Python library for **Formal Order Analysis (FOA)** — analysis of symbolic sequences by mapping them to their structural order and extracting intervals between repeated symbols. Core dependency: `numpy >= 1.20`.

## Commands

**Run all tests:**
```bash
tox -e default
```

**Run a single test file or test:**
```bash
tox -e default -- tests/test_characteristics/test_volume.py -v
tox -e default -- tests/test_characteristics/test_volume.py::TestVolume::test_dataset_1 -v
```

**Run tests matching a keyword:**
```bash
tox -e default -- -k order -q
```

**Lint (black, isort, flake8):**
```bash
pipx run pre-commit run --all-files --show-diff-on-failure
```

**Build distribution:**
```bash
tox -e clean,build
```

**Build and serve docs:**
```bash
tox -e docs
tox -e docsserve
```

## Architecture

### Core Pipeline (`src/foapy/core/`)

The FOA pipeline works in stages:

1. **`order(X)`** — maps a sequence to integer indices (positions in first-appearance alphabet) and optionally returns the `alphabet`
2. **`intervals(X, binding, mode)`** — extracts intervals (distances between consecutive occurrences of the same symbol) from an ordered sequence

`intervals()` is built from two lower-level primitives:
- **`intervals_chain`** — computes raw interval chains before boundary handling
- **`intervals_tuple`** — applies boundary strategy to produce the final result

### Binding and Mode enums

These two enums control how `intervals()` handles sequence boundaries:

- **`binding`**: `start` (left-to-right) or `end` (right-to-left)
- **`mode`**: `lossy` (drop boundary intervals), `normal` (one boundary), `cycle` (cyclic wrap), `redundant` (both boundaries)

### Characteristics (`src/foapy/characteristics/`)

Each characteristic is a standalone module (e.g., `volume`, `arithmetic_mean`, `depth`, `regularity`) that takes an intervals array and returns a scalar. They share no base class — each is a thin function over numpy operations.

### Masked-Array Support (`src/foapy/ma/`)

`foapy.ma` mirrors the core API for sequences with missing data (numpy masked arrays): `ma.order()`, `ma.alphabet()`, `ma.intervals()`. The `characteristics/ma/` subdirectory provides masked-array variants of each characteristic.

### Exceptions (`src/foapy/exceptions/`)

- `Not1DArrayException` — raised when input is not 1-D
- `InconsistentOrderException` — raised when order/alphabet pair is incompatible

## Test Conventions

Tests are in `tests/`. Characteristics tests share a base class `CharacteristicsTest` (in `tests/test_characteristics/characterisitcs_test.py`) providing `AssertCase()` and `AssertBatch()` helpers. `AssertBatch` verifies results across all `binding × mode` combinations using a nested dict of expected values.

Numerical comparisons use epsilon tolerance — use `AssertCase`/`AssertBatch` rather than plain `assert` for floating-point characteristics.
