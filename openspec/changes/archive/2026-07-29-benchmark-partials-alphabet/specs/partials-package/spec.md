## MODIFIED Requirements

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

#### Scenario: Dense input remains compatible with the core function
- **WHEN** `alphabet()` receives a plain or fully unmasked 1-D input
- **THEN** its result equals `foapy.alphabet()` for the same values
