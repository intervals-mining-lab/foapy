## MODIFIED Requirements

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
