## ADDED Requirements

### Requirement: Partial sequence ordering
The system MUST provide `foapy.partials.order(X, return_alphabet=False)`, accepting a 1-D masked array or a plain sequence treated as fully unmasked, and returning a 1-D masked integer array aligned to `X`. Non-masked positions MUST contain zero-based alphabet indices in first-appearance order, and masked positions MUST remain masked.

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

### Requirement: Partial sequence alphabet extraction
The system MUST provide `foapy.partials.alphabet(X)`, accepting a 1-D masked array or plain sequence and returning a plain 1-D array of unique non-masked values in first-appearance order.

#### Scenario: Masked values are excluded
- **WHEN** `alphabet()` receives `['a', --, 'b', 'a', --]`
- **THEN** it returns `['a', 'b']`

#### Scenario: Fully masked or empty input
- **WHEN** `alphabet()` receives a fully masked or empty 1-D input
- **THEN** it returns an empty plain array

#### Scenario: Multi-dimensional input is rejected
- **WHEN** `alphabet()` receives an input with more than one dimension
- **THEN** it raises `Not1DArrayException`

### Requirement: Position-preserving partial interval chains
The system MUST provide `foapy.partials.intervals_chain(X, binding, chain_mode)`, accepting the raw 1-D masked sequence (or a plain fully unmasked sequence), and returning a same-length masked integer array. Non-masked values MUST contain interval distances calculated from actual source indices; masked positions MUST remain masked.

#### Scenario: Gaps count toward distance
- **WHEN** `intervals_chain()` receives `[--, C, T, C, --, G]` with start binding and boundary mode
- **THEN** it returns `[--, 2, 3, 2, --, 6]`

#### Scenario: Dense input matches core
- **WHEN** `intervals_chain()` receives a 1-D input with no masked positions
- **THEN** its non-masked result equals `foapy.core.intervals_chain()` for the same input and modes

#### Scenario: Fully masked input
- **WHEN** `intervals_chain()` receives a fully masked input
- **THEN** it returns a fully masked array of the same length

#### Scenario: Invalid dimensions or modes
- **WHEN** `intervals_chain()` receives a multi-dimensional input or an unsupported binding or chain mode
- **THEN** it raises `Not1DArrayException` for the dimensionality error or `ValueError` for the invalid mode

### Requirement: Partial interval tuple strategies
The system MUST provide `foapy.partials.intervals_tuple(chain, binding, tuple_mode)`, accepting a 1-D masked interval chain or a plain fully unmasked chain and applying the selected boundary strategy while preserving existing masked positions.

#### Scenario: Normal mode preserves the chain
- **WHEN** `intervals_tuple()` is called with normal mode
- **THEN** it returns the same length, values, and mask as the input chain

#### Scenario: Lossy mode masks boundaries
- **WHEN** `intervals_tuple()` is called with lossy mode
- **THEN** boundary positions are additionally masked, the output length remains unchanged, and existing masked positions remain masked

#### Scenario: Redundant mode appends complementary values
- **WHEN** `intervals_tuple()` is called with redundant mode
- **THEN** it returns a masked array containing the original positions followed by one unmasked trailing complementary value per inferred unique symbol

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
