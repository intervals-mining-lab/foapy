## MODIFIED Requirements

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
