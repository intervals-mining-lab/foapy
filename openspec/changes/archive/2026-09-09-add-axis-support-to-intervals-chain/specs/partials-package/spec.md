## MODIFIED Requirements

### Requirement: Position-preserving partial interval chains
The system MUST provide `foapy.partials.intervals_chain(X, binding, chain_mode, *, axis=None)`, accepting a masked array or a plain sequence treated as fully unmasked. With no axis, it MUST retain its existing one-dimensional behavior. With an explicit axis, each complete orthogonal slice MUST be one sequence element, a fully masked slice MUST be a gap, and every slice MUST be either wholly masked or wholly unmasked. The result MUST be a one-dimensional masked `numpy.intp` array of length `X.shape[axis]`; non-gap positions MUST contain interval distances calculated from actual selected-axis indices and gap positions MUST remain masked. Gaps MUST count toward occurrence, boundary, and cyclic distances because they remain positions in the selected-axis coordinate system.

#### Scenario: One-dimensional gaps count toward distance
- **WHEN** `intervals_chain()` receives `[--, C, T, C, --, G]` with start binding and boundary mode
- **THEN** it returns `[--, 2, 3, 2, --, 6]`

#### Scenario: Whole masked slices are positional gaps
- **WHEN** multidimensional slices along the selected axis are `S0`, a wholly masked slice, `S1`, and `S0` with start binding and boundary mode
- **THEN** the function returns `[1, --, 3, 3]`

#### Scenario: Cycle mode includes whole-slice gaps
- **WHEN** multidimensional slices along the selected axis are `S0`, a wholly masked slice, `S1`, and `S0` with start binding and cycle mode
- **THEN** the function returns `[1, --, 4, 3]`, using the full selected-axis length of four

#### Scenario: Dense input matches core
- **WHEN** `intervals_chain()` receives a plain or fully unmasked input with any valid explicit axis
- **THEN** its non-masked values equal `foapy.core.intervals_chain()` for the same input, binding, chain mode, and axis

#### Scenario: Fully masked input
- **WHEN** every slice along a nonempty selected axis is wholly masked
- **THEN** the function returns a fully masked one-dimensional array with the selected-axis length

#### Scenario: Empty sequence axis
- **WHEN** the selected input axis has length zero
- **THEN** the function returns an empty one-dimensional masked `numpy.intp` array

#### Scenario: Mixed mask inside one slice is rejected
- **WHEN** any slice along the selected axis contains both masked and unmasked scalar components
- **THEN** `intervals_chain()` raises `ValueError` because the slice does not define one present or absent sequence element

#### Scenario: Multidimensional input without axis is rejected
- **WHEN** `intervals_chain()` receives a multidimensional input without an explicit axis
- **THEN** it raises `Not1DArrayException`

#### Scenario: Negative axis is equivalent
- **WHEN** a negative and equivalent positive axis select the same dimension
- **THEN** both calls return interval chains with identical data and masks

#### Scenario: Invalid axis or scalar input is rejected consistently
- **WHEN** the explicit axis is out of range or the input is zero-dimensional
- **THEN** the function raises NumPy's axis error for the invalid axis or `Not1DArrayException` for the scalar

#### Scenario: Invalid modes are rejected
- **WHEN** `intervals_chain()` receives an unsupported binding or chain mode
- **THEN** it raises `ValueError`

### Requirement: Published partial intervals-chain reference
The documentation MUST publish an API reference for `foapy.partials.intervals_chain` under the `foapy.partials` reference navigation. The reference MUST describe its keyword-only axis, slice-as-element behavior, one-dimensional masked return shape, whole-slice mask rules, source-position gap semantics, errors, and runnable one-dimensional and multidimensional examples.

#### Scenario: Partials API page is discoverable
- **WHEN** a user browses the generated documentation's `foapy.partials` reference section
- **THEN** an `intervals_chain` entry links to the API reference page

#### Scenario: Reference explains gap and axis semantics
- **WHEN** a user reads the partial intervals-chain reference
- **THEN** it explains that wholly masked slices remain masked positions, count toward distances along the selected axis, and differ from compressed semantics

#### Scenario: Reference includes a multidimensional example
- **WHEN** a user reads the partial intervals-chain reference
- **THEN** it includes a runnable example with whole-slice gaps and an explicit axis

### Requirement: Partials intervals-chain benchmark coverage
The benchmark suite MUST measure `foapy.partials.intervals_chain` execution time and peak memory for representative one-dimensional lengths and for deterministic multidimensional records across multiple sequence-axis lengths, slice widths, axis placements, and whole-slice mask states. The matrix MUST retain both bindings and both chain modes, and at least one axis-aware benchmark input MUST contain whole-slice gaps.

#### Scenario: Benchmark suite covers the legacy parameter matrix
- **WHEN** the partials intervals-chain benchmark suite is collected
- **THEN** it retains length, dataset, binding, and chain-mode parameters covering the required one-dimensional sizes and both enum values

#### Scenario: Benchmark suite covers axis inputs
- **WHEN** the partials intervals-chain benchmark suite is collected
- **THEN** it includes time and peak-memory cases parameterized by sequence-axis length, record width, axis placement, whole-slice mask state, binding, and chain mode

#### Scenario: Benchmark exercises whole-slice gap semantics
- **WHEN** an axis-aware partial benchmark invokes `intervals_chain`
- **THEN** at least one case passes a masked multidimensional input with wholly masked slices rather than compressing or preprocessing it outside the timed call

### Requirement: Package boundary and dense parity
The system MUST expose exactly `order`, `alphabet`, `intervals_chain`, and `intervals_tuple` from `foapy.partials`. For one-dimensional inputs and for wholly present slice elements along an explicit axis, partial alphabet, order, and interval-chain results MUST match their corresponding core results, subject to the documented masked-array representation. Existing partial interval behavior and top-level package exports MUST remain unchanged.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.partials`
- **THEN** the four partials functions are available from that submodule and are not added as top-level `foapy` functions

#### Scenario: Zero-gap parity for alphabet and order
- **WHEN** a caller uses a plain or fully unmasked input with any valid explicit axis
- **THEN** the partial alphabet equals the core alphabet and the non-masked values of the partial order equal the core order

#### Scenario: Zero-gap parity for interval chains
- **WHEN** a caller uses a plain or fully unmasked input with any valid explicit axis, binding, and chain mode
- **THEN** the partial interval-chain mask is empty and its values equal the core interval chain

#### Scenario: Existing one-dimensional pipeline parity
- **WHEN** a caller uses an unmasked one-dimensional input and valid combinations of binding, chain mode, and tuple mode
- **THEN** partials results match the corresponding core results, subject to the documented masked-array representation

#### Scenario: Existing interval gap behavior remains unchanged
- **WHEN** a caller passes a one-dimensional partial sequence through ordering, interval-chain, and tuple operations
- **THEN** every source gap retains the behavior documented by the partial interval requirements
