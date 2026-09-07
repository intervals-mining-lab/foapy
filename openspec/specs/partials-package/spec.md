# Purpose

Provide position-preserving FOA operations for partial masked sequences: gaps are excluded from alphabet and order calculations, but remain part of the positional coordinate system used for interval measurements.

## Requirements

### Requirement: Partial sequence ordering
The system MUST provide `foapy.partials.order(X, return_alphabet=False)`, accepting a 1-D masked array or a plain sequence treated as fully unmasked, and returning a 1-D masked integer array aligned to `X`. Non-masked positions MUST contain zero-based alphabet indices in first-appearance order, and masked positions MUST remain masked. The public API documentation MUST expose the function, describe its mask-preserving semantics and return modes, and include runnable examples for plain and masked inputs. The function MUST expose annotations for its input, boolean flag, and documented return forms without changing its callable interface.

#### Scenario: Order preserves gaps
- **WHEN** `order()` receives `['a', --, 'b', 'a', --]`
- **THEN** it returns `[0, --, 1, 0, --]` with the same length and mask

#### Scenario: Order returns an alphabet when requested
- **WHEN** `order()` is called with `return_alphabet=True`
- **THEN** it returns the masked order array and a plain alphabet array containing only non-masked unique values in first-appearance order

#### Scenario: Empty or fully masked input
- **WHEN** `order()` receives an empty or fully masked 1-D input
- **THEN** it returns a same-length fully masked order array, and an empty alphabet when requested

#### Scenario: Multi-dimensional input is rejected
- **WHEN** `order()` receives an input with more than one dimension
- **THEN** it raises `Not1DArrayException`

#### Scenario: Public documentation provides runnable examples
- **WHEN** a user opens the generated reference for `foapy.partials.order`
- **THEN** the reference includes examples for plain input, masked input with preserved gaps, and `return_alphabet=True`

#### Scenario: Signature annotations describe the contract
- **WHEN** a caller inspects `foapy.partials.order`
- **THEN** annotations identify the accepted array-like input, boolean `return_alphabet` flag, and masked-array or tuple return forms without requiring different call syntax

#### Scenario: ASV benchmark coverage exists
- **WHEN** the ASV benchmark suite discovers partials benchmarks
- **THEN** it includes time and peak-memory cases for `foapy.partials.order` across scalable input lengths and representative unmasked, partially masked, and fully masked data

### Requirement: Partial sequence alphabet extraction
The system MUST provide `foapy.partials.alphabet(X)`, accepting a 1-D masked array or plain sequence and returning a plain 1-D `numpy.ndarray` of unique non-masked values in first-appearance order. Its public documentation MUST describe masked-value exclusion, empty and fully masked inputs, dimensionality errors, and runnable usage examples. The function MUST expose type annotations for its input and plain-array return value without changing its callable interface.

#### Scenario: Masked values are excluded
- **WHEN** `alphabet()` receives `['a', --, 'b', 'a', --]`
- **THEN** it returns `['a', 'b']` as a plain 1-D array

#### Scenario: First element is masked
- **WHEN** `alphabet()` receives `[--, 'b', 'a']`
- **THEN** it returns `['b', 'a']` and does not treat the masked first position as an alphabet value

#### Scenario: First occurrence is masked and later occurrence is unmasked
- **WHEN** `alphabet()` receives `[--, 'a', 'b', 'a']` where the first `a` position is masked
- **THEN** it returns `['b', 'a']`, ordering values by their first unmasked occurrence

#### Scenario: Fully masked or empty input
- **WHEN** `alphabet()` receives a fully masked or empty 1-D input
- **THEN** it returns an empty plain array

#### Scenario: Multi-dimensional input is rejected
- **WHEN** `alphabet()` receives an input with more than one dimension
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
The system MUST expose exactly `order`, `alphabet`, `intervals_chain`, and `intervals_tuple` from `foapy.partials`, preserve masks through all positional operations, and leave `foapy.core` and `foapy.ma` behavior unchanged.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.partials`
- **THEN** the four partials functions are available from that submodule and are not added as top-level `foapy` functions

#### Scenario: Zero-gap parity across the pipeline
- **WHEN** a caller uses an unmasked input and valid combinations of binding, chain mode, and tuple mode
- **THEN** partials results match the corresponding core results, subject to the documented masked-array representation

#### Scenario: Gap masks survive the pipeline
- **WHEN** a caller passes a partially masked sequence through ordering, interval-chain, and tuple operations
- **THEN** every source gap remains masked in each positional output
