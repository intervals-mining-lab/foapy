# foapy

Python library for Formal Order Analysis (FOA) of symbolic sequences.

## What is FOA?

Formal Order Analysis (FOA) studies the structure of symbolic sequences by:

- Mapping a sequence to its order and alphabet (the set of unique symbols in order of first appearance).
- Extracting intervals between repeated occurrences of the same symbol under different boundary modes.
- Quantifying structure with characteristics (e.g., arithmetic/geometric means, volume, average remoteness, depth, descriptive/identifying information, regularity, uniformity).

This enables robust analysis for text, biological sequences, musical motifs, logs, and any categorical time series.

## Features

- **Alphabets and Orders:** Define alphabets and compute orders of sequences.
- **Intervals and Chains:** Extract intervals for multiple binding and boundary modes.
- **Congeneric Decomposition:** Decompose sequences into congeneric components.
- **Mathematical Characteristics:** Arithmetic mean, geometric mean, volume, average remoteness, depth, descriptive and identifying information, regularity, uniformity.
- **Masked-array Support:** FOA on partially observed sequences via `foapy.ma`.
- **Extensive Documentation:** Theory, algorithms, and examples.

## Installation

- From PyPI:

```bash
pip install foapy
```

- From source (with tox workflows):

```bash
git clone https://github.com/intervals-mining-lab/foapy.git
cd foapy
python -m pip install --upgrade pip
python -m pip install tox

# Run tests (isolated env)
tox -e default

# Build distribution artifacts (sdist and wheel)
tox -e build

# Optionally clean build artifacts
tox -e clean
```

## Quick start

Compute order, intervals, and a characteristic:

```python
import foapy

# 1) Order and alphabet
source = ['a', 'b', 'a', 'c', 'd']
order = foapy.order(source)
print(order)  # [0 1 0 2 3]

order_arr, alphabet = foapy.order(source, True)
print(order_arr, alphabet)  # [0 1 0 2 3] ['a' 'b' 'c' 'd']

# 2) Intervals (binding to start, normal mode)
from foapy import binding, mode
intervals = foapy.intervals(['a', 'b', 'a', 'c', 'a', 'd'], binding.start, mode.normal)
print(intervals)  # [1 2 2 3 2 5]

# 3) A characteristic (volume = product of intervals)
val = foapy.characteristics.volume(intervals)
print(val)  # 192
```

Masked arrays (optional):

```python
import numpy as np
import numpy.ma as ma
import foapy

seq = ma.masked_array(['a', 'b', 'a', 'c', 'd'], mask=[0, 1, 0, 0, 0])
order_ma = foapy.ma.order(seq)
intervals_grouped = foapy.ma.intervals(order_ma, foapy.binding.start, foapy.mode.normal)
u = foapy.characteristics.uniformity(intervals_grouped)
print(u)
```

## Project Structure

- **Source Code:** [`./src`](./src)
- **Documentation:** [`./docs`](./docs)
- **Tests:** [`./tests`](./tests)

## Documentation

Online documentation: [intervals-mining-lab.github.io/foapy](https://intervals-mining-lab.github.io/foapy).

The documentation in [`./docs`](./docs) covers fundamentals, algorithms, characteristics, applications, and development notes.

Build and serve the docs locally (via tox):

```bash
# Build docs into docs/_build
tox -e docs

# Serve docs with live-reload for development
tox -e docsserve
```

## Testing

Run the test suite (via tox):

```bash
tox -e default

# Pass arguments to pytest after --, e.g. run a subset:
tox -e default -- -k order -q
```
