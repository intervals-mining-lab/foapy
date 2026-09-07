## ADDED Requirements

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
The system MUST provide `foapy.congenerics.alphabet(S)`, returning the same `(m,)` plain `numpy.ndarray` as `foapy.partials.alphabet(S)` — the row labels of `foapy.congenerics.sequences(S)`, in first-appearance order.

#### Scenario: Alphabet matches row order
- **WHEN** `alphabet(S)` and `sequences(S)` are called on the same `S`
- **THEN** `alphabet(S)[j]` is the unique non-empty value found in row `j` of `sequences(S)`, for every `j`

### Requirement: Congeneric order per row
The system MUST provide `foapy.congenerics.order(S)`, returning a `numpy.ma.MaskedArray` of shape `(m, l)` where row `j` is `foapy.partials.order(CS[j])` and `CS = foapy.congenerics.sequences(S)`. Per the Congeneric Order definition, every non-masked value in every row MUST be `0` (the sole alphabet index of a single-symbol row).

#### Scenario: Every row's order is degenerate
- **WHEN** `order(S)` is called on any input
- **THEN** every non-masked entry in the result equals `0`, and the mask matches `sequences(S)`'s mask row-for-row

### Requirement: Congeneric interval chains per row
The system MUST provide `foapy.congenerics.intervals_chains(S, binding, chain_mode)`, returning a `numpy.ma.MaskedArray` of shape `(m, l)` where row `j` equals `foapy.partials.intervals_chain(CS[j], binding, chain_mode)` and `CS = foapy.congenerics.sequences(S)`. Invalid `binding` or `chain_mode` values MUST raise `ValueError`, matching `foapy.partials.intervals_chain`.

#### Scenario: Row-wise parity with partials.intervals_chain
- **WHEN** `intervals_chains(S, binding, chain_mode)` is called
- **THEN** row `j` of the result equals `foapy.partials.intervals_chain(foapy.congenerics.sequences(S)[j], binding, chain_mode)` for every `j`

#### Scenario: Invalid binding or chain mode
- **WHEN** `intervals_chains()` receives an unsupported `binding` or `chain_mode`
- **THEN** it raises `ValueError`

### Requirement: Congeneric interval tuples, padded to a common width
The system MUST provide `foapy.congenerics.intervals_tuples(S, binding, chain_mode, tuple_mode)`, returning a plain `numpy.ndarray` of shape `(m, x)` and dtype `numpy.intp`, where `x` is the maximum length across the `m` per-row calls to `foapy.partials.intervals_tuple` on `foapy.congenerics.intervals_chains(S, binding, chain_mode)`'s rows. `chain_mode` and `tuple_mode` MUST be accepted as independent parameters — matching `foapy.partials`, where `intervals_chain` takes `chain_mode` and `intervals_tuple` takes an already-built chain plus `tuple_mode`, so neither parameter can be inferred from the other. Rows shorter than `x` MUST be right-padded with `0`.

#### Scenario: Rows are padded to the widest row
- **WHEN** `intervals_tuples()` produces per-row tuples of differing lengths
- **THEN** the result is a rectangular `(m, x)` array where `x` equals the longest per-row tuple, and shorter rows have trailing `0`s

#### Scenario: Row content matches partials.intervals_tuple before padding
- **WHEN** row `j`'s unpadded tuple has length `k`
- **THEN** the first `k` values of row `j` in the result equal `foapy.partials.intervals_tuple` applied to that row's chain (built with the given `chain_mode`), and the remaining `x - k` values are `0`

#### Scenario: Chain mode changes the result independently of tuple mode
- **WHEN** `intervals_tuples()` is called with the same `binding` and `tuple_mode` but different `chain_mode` values
- **THEN** the underlying per-row chains differ accordingly and the results MAY differ, matching `foapy.partials.intervals_chain`'s `chain_mode` semantics

#### Scenario: Invalid binding, chain mode, or tuple mode
- **WHEN** `intervals_tuples()` receives an unsupported `binding`, `chain_mode`, or `tuple_mode`
- **THEN** it raises `ValueError`

### Requirement: Congeneric interval distributions, padded to a shared global width
The system MUST provide `foapy.congenerics.intervals_distributions(S, binding, chain_mode, tuple_mode)`, returning a plain `numpy.ndarray` of shape `(m, y)` and dtype `numpy.intp`, where `y` is the maximum interval value found across **all** rows of `foapy.congenerics.intervals_tuples(S, binding, chain_mode, tuple_mode)` (a single shared width, not a per-row maximum). Row `j` MUST equal `foapy.core.intervals_distribution` applied to row `j`'s unpadded tuple, right-padded with `0` to width `y`.

#### Scenario: Width is shared across all rows
- **WHEN** two different rows have different maximum interval values
- **THEN** both rows of the result share the same width `y`, equal to the largest interval value found in any row

#### Scenario: Padding value means zero occurrences
- **WHEN** row `j`'s own maximum interval value is smaller than `y`
- **THEN** the trailing columns of row `j` are `0`, correctly representing zero occurrences of those interval values in that row

#### Scenario: Invalid binding, chain mode, or tuple mode
- **WHEN** `intervals_distributions()` receives an unsupported `binding`, `chain_mode`, or `tuple_mode`
- **THEN** it raises `ValueError`

### Requirement: Package boundary
The system MUST expose exactly `sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, and `intervals_distributions` from `foapy.congenerics`. It MUST NOT expose an inverse/reconstruction function in this change, and MUST NOT modify `foapy.core`, `foapy.ma`, or `foapy.partials` behavior.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.congenerics`
- **THEN** exactly the six functions above are available from that submodule and are not added as top-level `foapy` functions

#### Scenario: No inverse function is present
- **WHEN** a caller inspects `foapy.congenerics`'s public API
- **THEN** no reconstruction/inverse function exists in this module

### Requirement: Benchmark coverage for the decomposition and order/chain stages
The benchmark suite MUST measure `foapy.congenerics.sequences`, `foapy.congenerics.order`, and `foapy.congenerics.intervals_chains` for time and peak memory, across multiple input lengths and dataset shapes (at minimum: a single-symbol case, a small fixed alphabet case, and a case where alphabet size scales with input length). Dataset shapes whose row count `m` scales with length MUST be excluded at the largest benchmarked length to keep the suite's memory use bounded.

#### Scenario: Benchmark suite covers sequences, order, and intervals_chains
- **WHEN** the ASV benchmark suite is collected
- **THEN** it includes time and peak-memory benchmarks for `foapy.congenerics.sequences`, `foapy.congenerics.order`, and `foapy.congenerics.intervals_chains`

#### Scenario: Large-alphabet cases are bounded
- **WHEN** the benchmark suite's largest configured input length is exercised
- **THEN** dataset shapes whose alphabet size scales with length are skipped at that length, while fixed-small-alphabet shapes are still exercised
