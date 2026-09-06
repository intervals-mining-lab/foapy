## MODIFIED Requirements

### Requirement: Position-preserving partial interval chains
The system MUST provide `foapy.partials.intervals_chain(X, binding, chain_mode)`, accepting the raw 1-D masked sequence (or a plain fully unmasked sequence), and returning a same-length masked integer array. Non-masked values MUST contain interval distances calculated from actual source indices; masked positions MUST remain masked. Inputs whose normalized array dimensionality is not exactly one MUST raise `Not1DArrayException`.

#### Scenario: Gaps count toward distance
- **WHEN** `intervals_chain()` receives `[--, C, T, C, --, G]` with start binding and boundary mode
- **THEN** it returns `[--, 2, 3, 2, --, 6]`

#### Scenario: Dense input matches core
- **WHEN** `intervals_chain()` receives a 1-D input with no masked positions
- **THEN** its non-masked result equals `foapy.core.intervals_chain()` for the same input and modes

#### Scenario: Fully masked input
- **WHEN** `intervals_chain()` receives a fully masked input
- **THEN** it returns a fully masked array of the same length

#### Scenario: Scalar input is rejected consistently
- **WHEN** `intervals_chain()` receives a scalar or other 0-D input
- **THEN** it raises `Not1DArrayException`, matching `foapy.core.intervals_chain()`

#### Scenario: Multidimensional input or invalid modes are rejected
- **WHEN** `intervals_chain()` receives a multi-dimensional input or an unsupported binding or chain mode
- **THEN** it raises `Not1DArrayException` for the dimensionality error or `ValueError` for the invalid mode

## ADDED Requirements

### Requirement: Published partial intervals-chain reference
The documentation MUST publish an API reference for `foapy.partials.intervals_chain` under the `foapy.partials` reference navigation. The reference MUST describe its shared signature, masked-array return type, mask preservation, source-position gap semantics, errors, and at least one runnable dense or masked example.

#### Scenario: Partials API page is discoverable
- **WHEN** a user browses the generated documentation's `foapy.partials` reference section
- **THEN** an `intervals_chain` entry links to the API reference page

#### Scenario: Reference explains the semantic difference
- **WHEN** a user reads the partials intervals-chain reference
- **THEN** it explains that masked positions remain in the output and count toward distances, and distinguishes this from the dense/core and compressed `foapy.ma` behavior

### Requirement: Partials intervals-chain benchmark coverage
The benchmark suite MUST measure `foapy.partials.intervals_chain` execution time and peak memory for representative input lengths of 100, 10,000, and 1,000,000, with both bindings and both chain modes. At least one benchmark input MUST contain masked gaps.

#### Scenario: Benchmark suite covers the parameter matrix
- **WHEN** the partials intervals-chain benchmark suite is collected
- **THEN** it exposes length, dataset, binding, and chain-mode parameters covering the required sizes and both enum values

#### Scenario: Benchmark exercises masked semantics
- **WHEN** the benchmark invokes the partials intervals-chain methods on a gapped dataset
- **THEN** it passes a masked input and measures the function call rather than silently benchmarking the core or compressed implementation
