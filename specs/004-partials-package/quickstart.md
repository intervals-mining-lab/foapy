# Quickstart: foapy.partials

**Date**: 2026-04-19 | **Branch**: `004-partials-package`

## What is foapy.partials?

`foapy.partials` provides the Formal Order Analysis pipeline for **partial sequences** — sequences with gap (empty/skip) positions represented as numpy masked arrays. Unlike `foapy.core`, which operates on dense sequences, and `foapy.ma`, which compresses gaps away before computing intervals, `foapy.partials` preserves gap positions throughout the pipeline and measures interval distances using actual positional indices (gaps count toward distance).

## Installation

`foapy.partials` is part of the `foapy` package — no separate installation.

```python
import foapy.partials as partials
import numpy.ma as ma
import foapy  # for binding, chain_mode, tuple_mode enums
```

## Basic Usage

### 1. Construct a Partial Sequence

```python
import numpy.ma as ma

# Text "INTELLIGENCE" with only letters I, T, G, N kept; others are gaps
X = ma.masked_array(
    list("INTELLIGENCE"),
    mask=[False, True, False, True, True, True, True, False, True, False, True, True]
)
# Non-masked positions: I(0), T(2), G(8), N(10)
```

### 2. Extract the Alphabet

```python
alphabet = partials.alphabet(X)
# array(['I', 'T', 'G', 'N'])  — unique non-masked values, first-appearance order
```

### 3. Compute the Order

```python
order, alphabet = partials.order(X, return_alphabet=True)
# order: masked 1-D array of same length as X
# Non-masked positions: [0, 1, 2, 3]  (I=0, T=1, G=2, N=3)
# Masked positions: same as X
```

### 4. Compute the Intervals Chain

```python
chain = partials.intervals_chain(X, foapy.binding.start, foapy.chain_mode.boundary)
# chain: masked 1-D array of same length as X
# Each non-masked position holds the actual positional distance to the previous
# occurrence of that element (including any gap positions in between)
```

### 5. Apply a Boundary Strategy

```python
# Keep all intervals (normal)
result = partials.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.normal)

# Drop boundary (first-occurrence) intervals — those positions become masked
result = partials.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.lossy)

# Append trailing complementary intervals
result = partials.intervals_tuple(chain, foapy.binding.start, foapy.tuple_mode.redundant)
```

### 6. Access the Non-Masked Intervals

```python
# Extract just the interval values for downstream analysis
interval_values = result.compressed()
```

## Key Differences at a Glance

| | `foapy.core` | `foapy.ma` | `foapy.partials` |
|---|---|---|---|
| Input | Plain 1-D array | Masked 1-D array | Masked 1-D array |
| `order()` output | Plain 1-D array | 2-D masked matrix | Masked 1-D array |
| Gaps in intervals | N/A | Compressed out | Count toward distance |
| Output length | Same as input | Varies by function | Same as input (normal/lossy); n+k (redundant) |

## Plain Array Input

All functions accept plain numpy arrays or Python lists; they are auto-wrapped as fully unmasked masked arrays:

```python
result = partials.order(['a', 'b', 'a', 'c'])  # same as foapy.core.order(['a','b','a','c'])
```

## Enums

`foapy.partials` does not export `binding`, `chain_mode`, or `tuple_mode`. Import them from `foapy`:

```python
import foapy
foapy.binding.start   # or foapy.binding.end
foapy.chain_mode.boundary  # or foapy.chain_mode.cycle
foapy.tuple_mode.normal    # or .lossy or .redundant
```
