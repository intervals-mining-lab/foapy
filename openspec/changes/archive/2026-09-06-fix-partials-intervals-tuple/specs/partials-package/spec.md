## MODIFIED Requirements

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
