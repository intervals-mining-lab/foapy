# Quickstart: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-04-18

## Overview

The intervals pipeline is decomposed into three independently callable stages:

1. `intervals_chain(X, binding, chain_mode)` → raw chain (1-D ndarray)
2. `intervals_tuple(chain, binding, tuple_mode)` → boundary-adjusted tuple (1-D ndarray)
3. `intervals_distribution(tuple_result)` → frequency histogram (1-D ndarray, utility)

`intervals()` remains as a convenience wrapper composing stages 1 and 2.

## Using the decomposed pipeline

```python
import foapy
from foapy.core import intervals_chain, intervals_tuple, chain_mode, tuple_mode

X = ['b', 'a', 'b', 'c', 'b']

# Stage 1: raw chain
chain = intervals_chain(X, foapy.binding.start, chain_mode.boundary)
# chain = [1, 2, 2, 4, 2]

# Stage 2: apply boundary strategy — binding must be passed explicitly
result_normal   = intervals_tuple(chain, foapy.binding.start, tuple_mode.normal)
# [1, 2, 2, 4, 2]

result_lossy    = intervals_tuple(chain, foapy.binding.start, tuple_mode.lossy)
# [2, 2]

result_redundant = intervals_tuple(chain, foapy.binding.start, tuple_mode.redundant)
# [1, 2, 2, 4, 2, 4, 2, 1]  (sorted order varies)
```

## Equivalence with `intervals()`

```python
import foapy
from foapy.core import intervals_chain, intervals_tuple, chain_mode, tuple_mode

X = ['b', 'a', 'b', 'c', 'b']

# These are equivalent:
foapy.intervals(X, foapy.binding.start, foapy.mode.lossy)
intervals_tuple(intervals_chain(X, foapy.binding.start, chain_mode.boundary),
                foapy.binding.start, tuple_mode.lossy)

foapy.intervals(X, foapy.binding.start, foapy.mode.redundant)
intervals_tuple(intervals_chain(X, foapy.binding.start, chain_mode.boundary),
                foapy.binding.start, tuple_mode.redundant)
```

## Mode mapping: old `mode` → new stages

| `intervals()` mode  | `chain_mode`         | `tuple_mode`         |
|---------------------|----------------------|----------------------|
| `mode.normal`       | `chain_mode.boundary`| `tuple_mode.normal`  |
| `mode.lossy`        | `chain_mode.boundary`| `tuple_mode.lossy`   |
| `mode.cycle`        | `chain_mode.cycle`   | `tuple_mode.normal`  |
| `mode.redundant`    | `chain_mode.boundary`| `tuple_mode.redundant` |

## Key rule: pass `binding` explicitly to `intervals_tuple`

`binding` is **not** inferred from chain values. Always pass the same `binding` that was used with `intervals_chain`:

```python
# Correct
chain = intervals_chain(X, foapy.binding.end, chain_mode.boundary)
result = intervals_tuple(chain, foapy.binding.end, tuple_mode.lossy)

# Wrong — binding mismatch produces incorrect boundary detection
result = intervals_tuple(chain, foapy.binding.start, tuple_mode.lossy)
```

## Open benchmark defects

Two benchmark files call `intervals_tuple` with the old 2-argument signature and will fail at runtime. See Open Defects in [plan.md](./plan.md).

| File | Fix |
|------|-----|
| `benchmarks/benchmarks/bench_intervals_tuple.py` | Add `binding.start` as second argument |
| `benchmarks/benchmarks/bench_intervals_distribution.py` | Add `binding.start` as second argument in setup |
