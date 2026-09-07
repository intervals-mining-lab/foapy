# Purpose

Define the public congeneric-sequence decomposition API and its row-wise interval analysis semantics, including bounded benchmark coverage.

## Requirements

### Requirement: Congeneric sequence decomposition
The system MUST provide `foapy.congenerics.sequences(S)`, accepting a 1-D masked or plain sequence and returning `CS`, a `numpy.ma.MaskedArray` of shape `(m, l)` where `m` is the size of `foapy.partials.alphabet(S)` and `l = len(S)`. Row `j` MUST hold `S[i]` at every position `i` where `foapy.partials.order(S)[i] == j`, and MUST be masked everywhere else (including all positions masked in `S`). Rows MUST be ordered by first-appearance of their symbol, matching `foapy.partials.alphabet(S)`'s ordering.

#### Scenario: Decomposition matches per-symbol occurrence
- **WHEN** `sequences()` receives `['a', 'b', 'a', 'c']`
- **THEN** it returns a `(3, 4)` masked matrix whose row 0 is `['a', --, 'a', --]`, row 1 is `[--, 'b', --, --]`, and row 2 is `[--, --, --, 'c']`

#### Scenario: Source gaps remain masked in every row
- **WHEN** `sequences()` receives a partial sequence with masked positions
- **THEN** every row of `CS` is masked at those source positions, in addition to positions not belonging to that row's symbol

#### Scenario: Empty or fully masked input
- **WHEN** `sequences()` receives an empty or fully masked 1-D input
- **THEN** it returns a matrix with `m = 0` rows and `l = len(S)` columns

#### Scenario: Multi-dimensional input is rejected
- **WHEN** `sequences()` receives an input with more than one dimension
- **THEN** it raises `Not1DArrayException`

### Requirement: Congeneric decomposition alphabet
The system MUST provide `foapy.congenerics.alphabet(CS)`, taking `CS` (the output of `foapy.congenerics.sequences`) directly — not the original sequence — and returning an `(m,)` plain `numpy.ndarray` of row labels, per the Alphabet of Congeneric sequences definition: `alphabet(CS)[j]` is row `j`'s single non-masked value.

#### Scenario: Alphabet matches row order
- **WHEN** `alphabet(CS)` is called where `CS = sequences(S)`
- **THEN** `alphabet(CS)[j]` is the unique non-empty value found in row `j` of `CS`, for every `j`

#### Scenario: Empty decomposition
- **WHEN** `alphabet(CS)` is called where `CS` has `m = 0` rows
- **THEN** it returns an empty array

### Requirement: Congeneric order per row
The system MUST provide `foapy.congenerics.order(CS, return_alphabet=False)`, taking `CS` (the output of `foapy.congenerics.sequences`) directly — not the original sequence — and returning a `numpy.ma.MaskedArray` of shape `(m, l)` whose mask matches `CS`'s mask exactly. Per the Congeneric Order definition, every non-masked value MUST be `0` (the sole alphabet index of a single-symbol row). When `return_alphabet=True`, it MUST additionally return `foapy.congenerics.alphabet(CS)`, matching `foapy.core.order`/`foapy.partials.order`'s `return_alphabet` convention.

#### Scenario: Every row's order is degenerate
- **WHEN** `order(CS)` is called where `CS = sequences(S)` for any `S`
- **THEN** every non-masked entry in the result equals `0`, and the mask matches `CS`'s mask exactly

#### Scenario: return_alphabet returns the row labels alongside the order
- **WHEN** `order(CS, True)` is called
- **THEN** it returns a `(order, alphabet)` tuple where `order` is identical to `order(CS, False)` and `alphabet` equals `foapy.congenerics.alphabet(CS)`

#### Scenario: CS is reconstructible from order and alphabet
- **WHEN** `order, alphabet = order(CS, True)` for some `CS`
- **THEN** broadcasting `alphabet[j]` across row `j` and keeping only the positions where `order` (equivalently `CS`) is non-masked reproduces `CS` exactly

### Requirement: Congeneric interval chains per row
The system MUST provide `foapy.congenerics.intervals_chains(CS, binding, chain_mode)`, taking `CS` directly — not the original sequence — and returning a `numpy.ma.MaskedArray` of shape `(m, l)` where row `j` equals `foapy.partials.intervals_chain(CS[j], binding, chain_mode)`. Only `CS`'s mask MUST matter to the result, so `CS` MAY be either `foapy.congenerics.sequences()`'s or `foapy.congenerics.order()`'s output. Invalid `binding` or `chain_mode` values MUST raise `ValueError`, matching `foapy.partials.intervals_chain`.

#### Scenario: Row-wise parity with partials.intervals_chain
- **WHEN** `intervals_chains(CS, binding, chain_mode)` is called where `CS = foapy.congenerics.sequences(S)`
- **THEN** row `j` of the result equals `foapy.partials.intervals_chain(CS[j], binding, chain_mode)` for every `j`

#### Scenario: order()'s output is an equally valid input
- **WHEN** `intervals_chains(CS, binding, chain_mode)` and `intervals_chains(foapy.congenerics.order(CS), binding, chain_mode)` are both called for the same `CS`
- **THEN** the two results are identical

#### Scenario: Invalid binding or chain mode
- **WHEN** `intervals_chains()` receives an unsupported `binding` or `chain_mode`
- **THEN** it raises `ValueError`

### Requirement: Congeneric interval tuples, padded to a common width
The system MUST provide `foapy.congenerics.intervals_tuples(chains, binding, tuple_mode)`, taking `chains` — the output of `foapy.congenerics.intervals_chains` — directly, and returning a plain `numpy.ndarray` of shape `(m, x)` and dtype `numpy.intp`, where `x` is the maximum length across the `m` per-row calls to `foapy.partials.intervals_tuple` on `chains`'s rows. `binding` MUST match the binding used to produce `chains`. Rows shorter than `x` MUST be right-padded with `0`.

#### Scenario: Rows are padded to the widest row
- **WHEN** `intervals_tuples()` produces per-row tuples of differing lengths
- **THEN** the result is a rectangular `(m, x)` array where `x` equals the longest per-row tuple, and shorter rows have trailing `0`s

#### Scenario: Row content matches partials.intervals_tuple before padding
- **WHEN** row `j`'s unpadded tuple has length `k`
- **THEN** the first `k` values of row `j` in the result equal `foapy.partials.intervals_tuple` applied to `chains[j]`, and the remaining `x - k` values are `0`

#### Scenario: Chain mode changes the result via chains, not via a separate parameter
- **WHEN** `intervals_tuples()` is called with the same `binding` and `tuple_mode` but on `chains` built from different `chain_mode` values
- **THEN** the results MAY differ, matching `foapy.partials.intervals_chain`'s `chain_mode` semantics, with `chain_mode` never passed to `intervals_tuples()` directly

#### Scenario: Invalid binding or tuple mode
- **WHEN** `intervals_tuples()` receives an unsupported `binding` or `tuple_mode`
- **THEN** it raises `ValueError`

### Requirement: Congeneric interval distributions, padded to a shared global width
The system MUST provide `foapy.congenerics.intervals_distributions(tuples)`, taking `tuples` — the zero-padded output of `foapy.congenerics.intervals_tuples` — directly and returning a plain `numpy.ndarray` of shape `(m, y)` and dtype `numpy.intp`, where `y` is the maximum nonzero interval value found across **all** rows of `tuples` (a single shared width, not a per-row maximum). Row `j` MUST equal `foapy.core.intervals_distribution` applied to the nonzero values in `tuples[j]`, right-padded with `0` to width `y`. The input's `0` padding MUST be excluded from frequency counts.

#### Scenario: Tuple-stage output is consumed directly
- **WHEN** `tuples = foapy.congenerics.intervals_tuples(chains, binding, tuple_mode)`
- **THEN** `intervals_distributions(tuples)` computes every row's interval distribution without separate `binding`, `chain_mode`, or `tuple_mode` parameters

#### Scenario: Width is shared across all rows
- **WHEN** two different rows have different maximum interval values
- **THEN** both rows of the result share the same width `y`, equal to the largest interval value found in any row

#### Scenario: Input padding is ignored and output padding means zero occurrences
- **WHEN** `tuples[j]` contains right-padding `0`s and row `j`'s own maximum interval value is smaller than `y`
- **THEN** input padding creates no frequency bin, and the trailing columns of output row `j` are `0`, correctly representing zero occurrences of those interval values

#### Scenario: No real interval values
- **WHEN** `tuples` has `m` rows but contains no nonzero interval values
- **THEN** `intervals_distributions(tuples)` returns an `(m, 0)` array of dtype `numpy.intp`

### Requirement: Package boundary
The system MUST expose exactly `sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, `intervals_distributions`, and `characteristics` from `foapy.congenerics`. The `characteristics` entry MUST be the `foapy.congenerics.characteristics` subpackage. `foapy.congenerics` MUST NOT expose an inverse/reconstruction function. `foapy.ma` is removed and MUST NOT be referenced.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.congenerics`
- **THEN** exactly the six pipeline functions plus the `characteristics` subpackage are available, and no individual characteristic functions are added to the `foapy.congenerics` top-level namespace

#### Scenario: No inverse function is present
- **WHEN** a caller inspects `foapy.congenerics`'s public API
- **THEN** no reconstruction/inverse function exists in this module

#### Scenario: characteristics subpackage is accessible
- **WHEN** a caller runs `import foapy.congenerics.characteristics`
- **THEN** the import succeeds and `foapy.congenerics.characteristics` is the congeneric characteristics subpackage

### Requirement: Benchmark coverage for the decomposition and order/chain stages
The benchmark suite MUST measure `foapy.congenerics.sequences`, `foapy.congenerics.order`, and `foapy.congenerics.intervals_chains` for time and peak memory, across multiple input lengths and dataset shapes (at minimum: a single-symbol case, a small fixed alphabet case, and a case where alphabet size scales with input length). Dataset shapes whose row count `m` scales with length MUST be excluded at the largest benchmarked length to keep the suite's memory use bounded.

#### Scenario: Benchmark suite covers sequences, order, and intervals_chains
- **WHEN** the ASV benchmark suite is collected
- **THEN** it includes time and peak-memory benchmarks for `foapy.congenerics.sequences`, `foapy.congenerics.order`, and `foapy.congenerics.intervals_chains`

#### Scenario: Large-alphabet cases are bounded
- **WHEN** the benchmark suite's largest configured input length is exercised
- **THEN** dataset shapes whose alphabet size scales with length are skipped at that length, while fixed-small-alphabet shapes are still exercised
