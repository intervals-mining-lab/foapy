## ADDED Requirements

### Requirement: Core interval chains support slice elements along an axis
The system MUST provide `foapy.core.intervals_chain(X, binding, chain_mode, *, axis=None)`. When `axis` is an integer, each complete orthogonal slice indexed along that axis MUST be one sequence element, and the function MUST return a one-dimensional `numpy.intp` array of length `X.shape[axis]` containing one interval value for each slice position. Slice equality MUST match the equality classes produced by `foapy.core.order(X, axis=axis)`.

#### Scenario: Rows are sequence elements
- **WHEN** rows along axis 0 are `R0`, `R1`, `R0`, `R2`, `R0` and start binding with boundary mode is requested
- **THEN** the interval chain is `[1, 2, 2, 4, 2]`

#### Scenario: Columns are sequence elements
- **WHEN** columns along axis 1 are `C0`, `C1`, `C0`, `C2` and start binding with boundary mode is requested
- **THEN** the interval chain is `[1, 2, 2, 4]`

#### Scenario: Three-dimensional slices are sequence elements
- **WHEN** `intervals_chain()` receives a three-dimensional input and any explicit valid axis
- **THEN** it compares each complete two-dimensional slice at a position on that axis as one element and returns one interval value per selected-axis position

#### Scenario: Order-code invariance
- **WHEN** a supported multidimensional dense input is evaluated with axis `a`, binding `b`, and chain mode `m`
- **THEN** its result equals `intervals_chain(order(X, axis=a), b, m)`

### Requirement: Binding and chain mode operate in selected-axis coordinates
For explicit-axis input, the system MUST preserve the existing `binding.start`, `binding.end`, `chain_mode.boundary`, and `chain_mode.cycle` definitions using positions and sequence length from the selected axis. Boundary distances MUST be measured from the corresponding selected-axis edge, and cyclic distances for each equality class MUST wrap across the full selected-axis length.

#### Scenario: End binding reverses the selected-axis frame
- **WHEN** slice elements along the selected axis are `S0`, `S1`, `S0`, `S2`, `S0` and end binding with boundary mode is requested
- **THEN** the interval chain in original axis order is `[2, 4, 2, 2, 1]`

#### Scenario: Cycle mode wraps along the selected axis
- **WHEN** slice elements along the selected axis are `S0`, `S1`, `S0`, `S2`, `S0` and start binding with cycle mode is requested
- **THEN** the interval chain is `[1, 5, 2, 5, 2]`

#### Scenario: Structurally empty slices remain equal
- **WHEN** a nonempty selected axis indexes slices whose orthogonal shape contains zero scalar fields
- **THEN** all such slices belong to one equality class and receive intervals according to their positions on the selected axis

### Requirement: Axis behavior preserves the legacy core API
Calls that omit `axis` MUST retain the existing one-dimensional behavior, output dtype, and validation of `foapy.core.intervals_chain`. One-dimensional calls with `axis=0` or `axis=-1` MUST produce the legacy result. Multidimensional input without an explicit axis MUST raise `Not1DArrayException`; negative axes MUST follow NumPy conventions; an out-of-range axis MUST raise NumPy's axis error; and scalar inputs MUST raise `Not1DArrayException`.

#### Scenario: Existing call without axis remains unchanged
- **WHEN** an existing caller passes a one-dimensional input without `axis`
- **THEN** the result is unchanged from the pre-axis API for every valid binding and chain mode

#### Scenario: Explicit sole axis matches legacy behavior
- **WHEN** a one-dimensional input is called with `axis=0` or `axis=-1`
- **THEN** both results equal the call that omits `axis`

#### Scenario: Multidimensional input requires explicit intent
- **WHEN** a multidimensional input is passed without `axis`
- **THEN** the function raises `Not1DArrayException`

#### Scenario: Negative axis is equivalent
- **WHEN** a negative and equivalent positive axis select the same dimension
- **THEN** both calls return identical interval chains

#### Scenario: Axis is out of range
- **WHEN** an explicit axis is outside the input dimensionality
- **THEN** the function raises NumPy's axis error

#### Scenario: Scalar input is rejected
- **WHEN** `intervals_chain()` receives a zero-dimensional input
- **THEN** it raises `Not1DArrayException`

#### Scenario: Empty sequence axis
- **WHEN** the selected input axis has length zero
- **THEN** the function returns an empty one-dimensional `numpy.intp` array

### Requirement: Axis-aware interval chains are documented and benchmarked
The system MUST document the keyword-only axis, slice-as-element behavior, one-dimensional result shape, reconstruction-pipeline compatibility, and validation errors for core interval chains. The ASV suite MUST include time and peak-memory benchmarks for deterministic multidimensional records across representative sequence lengths, slice widths, and axis placements while retaining legacy one-dimensional coverage.

#### Scenario: Public reference explains axis behavior
- **WHEN** a user opens the generated reference for `foapy.core.intervals_chain`
- **THEN** it includes runnable row or column examples and explains that the returned chain is one-dimensional along the selected axis

#### Scenario: ASV discovers axis benchmarks
- **WHEN** the benchmark suite is collected
- **THEN** it includes deterministic time and peak-memory cases for core interval chains with multidimensional slice elements
