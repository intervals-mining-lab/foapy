## MODIFIED Requirements

### Requirement: Dense partial interval chains avoid gap-processing overhead
The system MUST return a `numpy.ma.MaskedArray` from `foapy.partials.intervals_chain()` for plain one-dimensional input, and its values, dtype, binding behavior, and chain-mode behavior MUST equal `foapy.core.intervals_chain()`. Plain one-dimensional input with omitted axis, `axis=0`, or `axis=-1` MUST reuse the core one-dimensional interval-chain calculation without extracting, compressing, or scattering a mask. Masked input MUST retain the existing gap-aware partial calculation.

#### Scenario: Dense one-dimensional input uses core-equivalent calculation
- **WHEN** a plain one-dimensional array is passed for any binding and chain mode
- **THEN** the returned masked array has no masked positions and contains the same `numpy.intp` values as the core interval chain

#### Scenario: Explicit sole axis retains the dense fast path
- **WHEN** plain one-dimensional input is passed with `axis=0` or `axis=-1`
- **THEN** axis validation succeeds and the same core-equivalent calculation is used

#### Scenario: Gapped input retains partial semantics
- **WHEN** a masked one-dimensional input contains gaps
- **THEN** the gaps remain masked and count toward interval distances through the partial interval-chain calculation

### Requirement: Partial interval tuple strategies
The system MUST provide `foapy.partials.intervals_tuple(chain, binding, tuple_mode, *, axis=None)`, accepting a one-dimensional masked interval chain (as produced by `foapy.partials.intervals_chain`), a plain fully unmasked chain, or a multidimensional collection of such chains. One-dimensional input with omitted axis, `axis=0`, or `axis=-1` MUST return a plain one-dimensional `numpy.ndarray` of dtype `numpy.intp` with masked gap positions excluded entirely.

For multidimensional input with an explicit valid axis, every one-dimensional lane along that axis MUST be processed independently. Each lane's masked positions MUST retain their source coordinates while boundary and complementary values are calculated, then MUST be excluded from that lane's tuple result. The system MUST return a `numpy.ma.MaskedArray` of dtype `numpy.intp` with the result dimension replacing the selected input axis, each lane result packed from index zero, and positions after shorter results masked as structural padding. For `binding.end`, each returned lane's order MUST match `foapy.core.intervals_tuple`'s reversed processing frame rather than source left-to-right order.

#### Scenario: Normal mode compresses gaps out
- **WHEN** `intervals_tuple()` is called with `tuple_mode.normal` on a one-dimensional chain containing masked positions
- **THEN** it returns a plain `ndarray` containing only the non-masked chain values, in their original relative order, with no masked positions represented

#### Scenario: Lossy mode drops boundary and gap values together
- **WHEN** `intervals_tuple()` is called with `tuple_mode.lossy`
- **THEN** each processed lane contains only the interior non-boundary values — gap positions and boundary first-occurrence positions are both absent from the lane result
- **AND** for an unmasked chain, the result is identical to `foapy.core.intervals_tuple(chain, binding, tuple_mode.lossy)`, including element order for both `binding.start` and `binding.end`

#### Scenario: Redundant mode appends gap-aware complementary values
- **WHEN** `intervals_tuple()` is called with `tuple_mode.redundant` on a chain containing masked positions
- **THEN** each processed lane contains the compressed gap-free chain values followed by one trailing complementary value per inferred unique symbol
- **AND** each trailing value is computed as the distance from that symbol's last occurrence to the edge of the true lane domain, including gaps, not the compressed element count

#### Scenario: Redundant mode keeps a single consistent order for binding.end
- **WHEN** `intervals_tuple()` is called with `tuple_mode.redundant` and `binding.end` on a chain containing masked positions
- **THEN** both the compressed portion and the trailing portion of each result are expressed in the same reversed processing frame — the compressed portion is not left in original source order while the trailing portion is computed in the reversed frame

#### Scenario: Empty or fully masked one-dimensional input yields an empty array
- **WHEN** `intervals_tuple()` receives an empty one-dimensional chain or a one-dimensional chain that is fully masked, for any `tuple_mode`
- **THEN** it returns `numpy.array([], dtype=numpy.intp)` as a plain array

#### Scenario: Multidimensional lanes are independent
- **WHEN** a multidimensional masked array is passed with an explicit axis
- **THEN** every lane obtained by fixing all orthogonal coordinates is processed independently with the existing partial tuple-mode semantics

#### Scenario: Multidimensional variable lengths use structural masks
- **WHEN** partial lanes produce unequal result lengths
- **THEN** the selected result axis has the longest lane length, every lane is packed from index zero, and only trailing positions after shorter lane results are masked

#### Scenario: Uniform multidimensional lengths remain masked
- **WHEN** every multidimensional lane produces the same tuple length
- **THEN** the result remains a `numpy.ma.MaskedArray` with an entirely false mask

#### Scenario: Three-dimensional axis placement
- **WHEN** input has shape `(A, B, C)` and the longest lane result has length `L`
- **THEN** axes 0, 1, and 2 produce result shapes `(L, B, C)`, `(A, L, C)`, and `(A, B, L)` respectively

#### Scenario: Dense multidimensional input matches core
- **WHEN** a multidimensional partial chain collection has no masked positions
- **THEN** its values and structural masks equal `foapy.core.intervals_tuple()` for the same binding, tuple mode, and axis

#### Scenario: Empty multidimensional lane collections
- **WHEN** all selected lanes are empty or fully masked, or no lanes exist because an orthogonal dimension is zero
- **THEN** the selected output axis has length zero and every orthogonal dimension is preserved

#### Scenario: Axis validation and dimensionality errors
- **WHEN** a multidimensional input omits `axis`, input is scalar, an equivalent negative axis is used, or an explicit axis is out of range
- **THEN** the function respectively raises `Not1DArrayException`, raises `Not1DArrayException`, succeeds with the same result as the positive axis, or raises NumPy's axis error

#### Scenario: Invalid binding or tuple mode
- **WHEN** `intervals_tuple()` receives an unsupported binding or tuple mode
- **THEN** it raises `ValueError`
