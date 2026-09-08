# Purpose

Provide position-preserving FOA operations for partial masked sequences: gaps are excluded from alphabet and order calculations, but remain part of the positional coordinate system used for interval measurements.

## Requirements

### Requirement: Partial sequence ordering
The system MUST provide `foapy.partials.order(X, return_alphabet=False, *, axis=None)`, accepting a masked array or a plain sequence treated as fully unmasked. With no axis, it MUST retain its existing one-dimensional behavior. With an explicit axis, each complete orthogonal slice MUST be one sequence element, a fully masked slice MUST be a gap, and every slice MUST be either wholly masked or wholly unmasked. The result MUST be a one-dimensional masked integer array of length `X.shape[axis]`; non-gap positions MUST contain zero-based alphabet indices in first-appearance order and gap positions MUST remain masked. When requested, the alphabet MUST be a plain array of the unique non-gap slices, retain the selected axis, and equal `foapy.partials.alphabet(X, axis=axis)`. The public API documentation and annotations MUST describe both call modes, shapes, return forms, mask rules, and reconstruction of observed slices.

#### Scenario: One-dimensional order preserves gaps
- **WHEN** `order()` receives `['a', --, 'b', 'a', --]`
- **THEN** it returns `[0, --, 1, 0, --]` with the same length and mask

#### Scenario: Whole masked slices are gaps
- **WHEN** a multidimensional partial input contains slice `S0`, a wholly masked slice, `S1`, and `S0` along the selected axis
- **THEN** order returns `[0, --, 1, 0]`

#### Scenario: Order returns an axis-preserving alphabet when requested
- **WHEN** multidimensional `order()` is called with `return_alphabet=True` and an explicit axis
- **THEN** it returns the one-dimensional masked order and a plain alphabet array containing only unique non-gap slices in first-appearance order, with the alphabet dimension at the selected axis

#### Scenario: Observed slices can be reconstructed
- **WHEN** the returned alphabet is indexed along the selected axis by the unmasked order values
- **THEN** every non-gap source slice is reconstructed exactly and broadcasting the order mask across the orthogonal dimensions restores the source gap mask

#### Scenario: Empty or fully masked input
- **WHEN** `order()` receives an empty or fully masked input with a valid sequence axis
- **THEN** it returns a same-axis-length fully masked order array and an axis-preserving empty alphabet when requested

#### Scenario: Mixed mask inside one slice is rejected
- **WHEN** any slice along the selected axis contains both masked and unmasked scalar components
- **THEN** `order()` raises `ValueError` because the slice does not define one present or absent sequence element

#### Scenario: Multidimensional input without axis is rejected
- **WHEN** `order()` receives an input with more than one dimension and no explicit axis
- **THEN** it raises `Not1DArrayException`

#### Scenario: Public documentation provides runnable examples
- **WHEN** a user opens the generated reference for `foapy.partials.order`
- **THEN** the reference includes runnable examples for plain input, one-dimensional gaps, multidimensional whole-slice gaps, `return_alphabet=True`, and reconstruction

#### Scenario: Signature annotations describe the contract
- **WHEN** a caller inspects `foapy.partials.order`
- **THEN** annotations identify the accepted array-like input, boolean `return_alphabet` flag, optional integer axis, and masked-array or tuple return forms

#### Scenario: ASV benchmark coverage exists
- **WHEN** the ASV benchmark suite discovers partials benchmarks
- **THEN** it includes time and peak-memory cases for `foapy.partials.order` across scalable sequence-axis lengths and representative one-dimensional, multidimensional, unmasked, partially gapped, and fully gapped data

### Requirement: Partial sequence alphabet extraction
The system MUST provide `foapy.partials.alphabet(X, *, axis=None)`, accepting a masked array or plain sequence. With no axis, it MUST retain its existing one-dimensional behavior. With an explicit axis, each complete orthogonal slice MUST be one sequence element, fully masked slices MUST be excluded as gaps, and every slice MUST be either wholly masked or wholly unmasked. The function MUST return a plain `numpy.ndarray` containing unique non-gap slices in first-appearance order, preserving the input rank and replacing only the selected axis length with the alphabet size. Its public documentation and annotations MUST describe masked-slice exclusion, axis and shape behavior, empty and fully masked inputs, validation errors, and runnable examples.

#### Scenario: One-dimensional masked values are excluded
- **WHEN** `alphabet()` receives `['a', --, 'b', 'a', --]`
- **THEN** it returns `['a', 'b']` as a plain one-dimensional array

#### Scenario: Fully masked multidimensional slices are excluded
- **WHEN** slices along the selected axis are `S0`, a wholly masked slice, `S1`, and `S0`
- **THEN** `alphabet()` returns `S0`, `S1` as a plain array with the selected axis reduced to length two

#### Scenario: First slice is masked
- **WHEN** the first slice is wholly masked and later non-gap slices are `S1`, `S0`
- **THEN** the alphabet is `S1`, `S0` and the masked first position does not affect first-appearance order

#### Scenario: First occurrence is masked and later occurrence is unmasked
- **WHEN** data under a wholly masked slice equals a later non-gap slice
- **THEN** only the later non-gap occurrence introduces that slice into the alphabet

#### Scenario: Fully masked or empty input
- **WHEN** `alphabet()` receives a fully masked input or an input whose selected axis is empty
- **THEN** it returns a plain array with length zero on the selected axis and all orthogonal dimensions preserved

#### Scenario: Mixed mask inside one slice is rejected
- **WHEN** any slice along the selected axis contains both masked and unmasked scalar components
- **THEN** `alphabet()` raises `ValueError`

#### Scenario: Multidimensional input without axis is rejected
- **WHEN** `alphabet()` receives a multidimensional input without an explicit axis
- **THEN** it raises `Not1DArrayException`

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

### Requirement: Partial interval tuple strategies
The system MUST provide `foapy.partials.intervals_tuple(chain, binding, tuple_mode)`, accepting a 1-D masked interval chain (as produced by `foapy.partials.intervals_chain`) or a plain fully unmasked chain, and returning a plain 1-D `numpy.ndarray` of dtype `numpy.intp` with masked (gap) positions excluded entirely. The function MUST NOT return a `numpy.ma.MaskedArray`. For `binding.end`, the returned order MUST match `foapy.core.intervals_tuple`'s own ordering convention (the reversed processing frame), not the source array's left-to-right order.

#### Scenario: Normal mode compresses gaps out
- **WHEN** `intervals_tuple()` is called with `tuple_mode.normal` on a chain containing masked positions
- **THEN** it returns a plain `ndarray` containing only the non-masked chain values, in their original relative order, with no masked positions represented

#### Scenario: Lossy mode drops boundary and gap values together
- **WHEN** `intervals_tuple()` is called with `tuple_mode.lossy`
- **THEN** it returns a plain `ndarray` containing only the interior (non-boundary) values of the compressed chain — gap positions and boundary (first-occurrence) positions are both absent from the result
- **AND** for an unmasked chain, the result is identical to `foapy.core.intervals_tuple(chain, binding, tuple_mode.lossy)`, including element order for both `binding.start` and `binding.end`

#### Scenario: Redundant mode appends gap-aware complementary values
- **WHEN** `intervals_tuple()` is called with `tuple_mode.redundant` on a chain containing masked positions
- **THEN** it returns a plain `ndarray` containing the compressed (gap-free) chain values followed by one trailing complementary value per inferred unique symbol
- **AND** each trailing value is computed as the distance from that symbol's last occurrence to the edge of the true source domain (`len(chain)`, gaps included), not the compressed element count

#### Scenario: Redundant mode keeps a single consistent order for binding.end
- **WHEN** `intervals_tuple()` is called with `tuple_mode.redundant` and `binding.end` on a chain containing masked positions
- **THEN** both the compressed portion and the trailing portion of the result are expressed in the same reversed processing frame — the compressed portion is not left in original source order while the trailing portion is computed in the reversed frame

#### Scenario: Empty or fully masked input yields an empty array
- **WHEN** `intervals_tuple()` receives an empty chain or a chain that is fully masked, for any `tuple_mode`
- **THEN** it returns `numpy.array([], dtype=numpy.intp)`

#### Scenario: Invalid binding or tuple mode
- **WHEN** `intervals_tuple()` receives an unsupported binding or tuple mode
- **THEN** it raises `ValueError`

### Requirement: Package boundary and dense parity
The system MUST expose exactly `order`, `alphabet`, `intervals_chain`, and `intervals_tuple` from `foapy.partials`. For one-dimensional inputs and for wholly present slice elements along an explicit axis, partial alphabet/order results MUST match their corresponding core results, subject to the documented masked-order representation. Existing partial interval behavior and top-level package exports MUST remain unchanged.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.partials`
- **THEN** the four partials functions are available from that submodule and are not added as top-level `foapy` functions

#### Scenario: Zero-gap parity for alphabet and order
- **WHEN** a caller uses a plain or fully unmasked input with any valid explicit axis
- **THEN** the partial alphabet equals the core alphabet and the non-masked values of the partial order equal the core order

#### Scenario: Existing one-dimensional pipeline parity
- **WHEN** a caller uses an unmasked one-dimensional input and valid combinations of binding, chain mode, and tuple mode
- **THEN** partials results match the corresponding core results, subject to the documented masked-array representation

#### Scenario: Existing interval gap behavior remains unchanged
- **WHEN** a caller passes a one-dimensional partial sequence through ordering, interval-chain, and tuple operations
- **THEN** every source gap retains the behavior documented by the partial interval requirements
