## ADDED Requirements

### Requirement: Interval tuples process independent lanes along an axis
The system MUST provide `foapy.core.intervals_tuple(chain, binding, tuple_mode, *, axis=None)`. When `chain` is multidimensional and `axis` is an integer, every one-dimensional lane obtained by fixing all coordinates outside that axis MUST be processed independently with the existing one-dimensional interval-tuple semantics. The lane result dimensions MUST replace the selected input axis in the same position as `numpy.apply_along_axis`.

#### Scenario: Rows are independent chains
- **WHEN** `intervals_tuple()` receives `[[1, 1, 3, 1], [1, 2, 1, 3]]` with start binding, lossy mode, and `axis=1`
- **THEN** it processes the two rows independently and returns values equivalent to `[[1, 1], [1, 3]]`

#### Scenario: Columns are independent chains
- **WHEN** the same two chains are stored as columns of a shape `(4, 2)` input and `axis=0` is selected
- **THEN** the result values are arranged with the tuple-result dimension at axis 0

#### Scenario: Three-dimensional lanes preserve axis placement
- **WHEN** input has shape `(A, B, C)` and each lane result has length `L`
- **THEN** axes 0, 1, and 2 produce result shapes `(L, B, C)`, `(A, L, C)`, and `(A, B, L)` respectively

### Requirement: Multidimensional interval tuples preserve variable result lengths with masks
Every multidimensional `intervals_tuple()` call MUST return a `numpy.ma.MaskedArray`, even when all lane results have the same length. The selected output axis MUST have the maximum result length across all lanes. Each lane result MUST be packed from index zero in its existing one-dimensional output order, and positions after that lane's result MUST be masked. Data stored under padding masks MUST NOT be treated as interval values.

#### Scenario: Lossy lane lengths differ
- **WHEN** start-boundary chains `[1, 1, 1, 1]` and `[1, 2, 3, 4]` are processed in lossy mode along the row axis
- **THEN** the first result is `[1, 1, 1]`, the second result is empty, the selected output axis has length three, and all three positions of the second row are masked

#### Scenario: Redundant lane lengths differ
- **WHEN** the same chains are processed in redundant mode along the row axis
- **THEN** their results have lengths five and eight, the selected output axis has length eight, and the last three positions of the first row are masked

#### Scenario: Uniform lane lengths still return a masked array
- **WHEN** every multidimensional lane produces the same tuple length
- **THEN** the result is a masked array with an entirely false mask rather than a plain ndarray

#### Scenario: All lane results are empty
- **WHEN** every processed lane produces an empty tuple
- **THEN** the selected output axis has length zero and all orthogonal dimensions are preserved

### Requirement: Interval tuple axis behavior preserves the legacy one-dimensional API
Calls to `intervals_tuple()` with one-dimensional input MUST retain the existing binding, tuple-mode, order, dtype, return type, and empty-input behavior. One-dimensional calls with `axis=0` or `axis=-1` MUST use the direct one-dimensional path and return a plain `numpy.ndarray`. Multidimensional input without an explicit axis MUST raise `Not1DArrayException`; negative axes MUST follow NumPy conventions; an out-of-range axis MUST raise NumPy's axis error; and scalar input MUST raise `Not1DArrayException`.

#### Scenario: Existing one-dimensional call remains unchanged
- **WHEN** a one-dimensional chain is passed without `axis` for any valid binding and tuple mode
- **THEN** its result is identical to the pre-axis API and remains a plain `numpy.ndarray`

#### Scenario: Explicit sole axis matches legacy behavior
- **WHEN** a one-dimensional chain is called with `axis=0` or `axis=-1`
- **THEN** both results equal the call that omits `axis` and remain plain arrays

#### Scenario: Multidimensional input requires an axis
- **WHEN** a multidimensional chain collection is passed without `axis`
- **THEN** `intervals_tuple()` raises `Not1DArrayException`

#### Scenario: Axis validation is consistent
- **WHEN** an explicit axis is negative, out of range, or applied to scalar input
- **THEN** an equivalent negative axis succeeds, an out-of-range axis raises NumPy's axis error, and scalar input raises `Not1DArrayException`

### Requirement: Interval tuple uses an efficient provisional internal chain validator
The implementation MUST provide a non-public `is_valid_intervals_chain(chain, *, axis=None)` helper and MUST NOT export it from `foapy.core` or top-level `foapy`. For one-dimensional input, its provisional content-validity check MUST return `True`. When the helper is called directly with multidimensional input and an explicit axis, it MUST treat each one-dimensional lane along that axis as a chain and return one aggregate Boolean that is true only when every lane passes the one-dimensional check.

`intervals_tuple()` MUST prepare its array representation and normalize its axis no more than once per call. It MUST invoke the validation hook on its prepared one-dimensional input or once on the prepared multidimensional lane matrix before applying the corresponding tuple kernel. Multidimensional validation, transformation, distribution, and variable-length packing MUST use C-backed vectorized NumPy batch operations. Production code MUST NOT use Python loops, comprehensions, generator expressions, `numpy.vectorize`, or `numpy.apply_along_axis`. When the hook reports an invalid lane batch, `intervals_tuple()` MUST raise `ValueError` before transformation begins.

#### Scenario: Provisional one-dimensional validation succeeds
- **WHEN** the internal validator receives any structurally accepted one-dimensional input
- **THEN** it returns the Python Boolean `True`

#### Scenario: Prepared one-dimensional validation stays on the fast path
- **WHEN** `intervals_tuple()` receives a prepared one-dimensional array with omitted or already normalized axis
- **THEN** it consults the validation hook without repeating array conversion or general axis normalization before calling the one-dimensional tuple kernel

#### Scenario: Multidimensional validation aggregates lanes
- **WHEN** the internal validator receives multidimensional input with an explicit valid axis
- **THEN** it applies the provisional check to every lane and returns a single Python Boolean

#### Scenario: Tuple transformation validates a multidimensional batch once
- **WHEN** `intervals_tuple()` processes multidimensional input with an explicit valid axis
- **THEN** the prepared lane matrix is validated once before one vectorized batch tuple kernel runs

#### Scenario: Production axis transformations contain no Python iteration
- **WHEN** the axis transformation, core tuple, core distribution, validation, and partial tuple modules are inspected
- **THEN** they contain no `for`, `while`, comprehension, generator expression, `numpy.vectorize`, or `numpy.apply_along_axis` implementation path

#### Scenario: Validator remains internal
- **WHEN** callers inspect the public members of `foapy` and `foapy.core`
- **THEN** `is_valid_intervals_chain` is not exported

#### Scenario: Tuple transformation consults validation
- **WHEN** the internal validation hook reports `False` for a one-dimensional input or multidimensional lane batch
- **THEN** `intervals_tuple()` raises `ValueError` before applying a tuple mode and returns no partial result

### Requirement: Interval distributions process independent lanes along an axis
The system MUST provide `foapy.core.intervals_distribution(tuple_result, *, axis=None)`. For multidimensional input with an explicit axis, every one-dimensional lane along that axis MUST be distributed independently, and the distribution dimension MUST replace the selected axis. Masked tuple positions MUST be excluded before counting. The result MUST be a `numpy.ma.MaskedArray` whose selected axis has the maximum distribution length across all lanes; shorter distributions MUST be packed from index zero and trailing positions MUST be masked.

#### Scenario: Row distributions
- **WHEN** tuple rows are `[1, 1, 3, 1]` and `[1, 2, 1, 3]` and `axis=1` is selected
- **THEN** the result values are `[[3, 0, 1], [2, 1, 1]]` with the distribution dimension at axis 1

#### Scenario: Masked tuple padding is excluded
- **WHEN** a tuple lane contains masked trailing positions
- **THEN** those positions contribute no counts to its distribution

#### Scenario: Zero-frequency bins remain meaningful
- **WHEN** a lane contains interval values one and three but no value two
- **THEN** its distribution contains an unmasked zero at the value-two bin while only positions beyond the lane's distribution length are masked

#### Scenario: Distribution lengths differ
- **WHEN** multidimensional tuple lanes have different maximum interval values
- **THEN** the selected result axis uses the greatest maximum and positions beyond each shorter lane's maximum are masked

#### Scenario: Empty distribution lanes
- **WHEN** one lane contains no unmasked interval values
- **THEN** its positions are masked across the shared distribution axis, and when every lane is empty the selected output axis has length zero

### Requirement: Interval distribution axis behavior preserves the legacy one-dimensional API
Calls to `intervals_distribution()` with plain one-dimensional input MUST preserve existing counts, `numpy.intp` dtype, empty-input behavior, and plain `numpy.ndarray` return type. One-dimensional calls with `axis=0` or `axis=-1` MUST use the direct path. A one-dimensional masked tuple MUST exclude masked positions and return a plain array. Multidimensional input without an explicit axis, scalar input, and invalid axes MUST follow the same validation rules as axis-aware interval tuples.

#### Scenario: Existing one-dimensional distribution remains unchanged
- **WHEN** a plain one-dimensional tuple is passed without `axis`
- **THEN** its result is identical to the pre-axis API and remains a plain `numpy.ndarray`

#### Scenario: One-dimensional masked tuple is compressed for counting
- **WHEN** a one-dimensional tuple contains masked padding
- **THEN** masked positions are excluded and the returned distribution is a plain array

#### Scenario: Explicit sole axis matches legacy distribution
- **WHEN** a one-dimensional tuple is called with `axis=0` or `axis=-1`
- **THEN** both results equal the call that omits `axis`

#### Scenario: Invalid distribution dimensionality or axis
- **WHEN** multidimensional input omits `axis`, input is scalar, or an explicit axis is out of range
- **THEN** the function raises `Not1DArrayException`, `Not1DArrayException`, or NumPy's axis error respectively

### Requirement: Partial interval tuples process masked chains independently along an axis
The system MUST provide `foapy.partials.intervals_tuple(chain, binding, tuple_mode, *, axis=None)`. For multidimensional input with an explicit axis, every one-dimensional lane along that axis MUST be processed independently with the existing partial interval-tuple semantics. Plain lanes MUST be treated as fully unmasked. Masked positions MUST remain source-coordinate gaps while a lane is processed, including when lossy mode identifies boundary values and redundant mode calculates complementary values from the full selected-axis lane length. The lane result dimension MUST replace the selected input axis.

Every multidimensional call MUST return a `numpy.ma.MaskedArray` of `numpy.intp`, including calls whose lane results have equal lengths. Each gap-free lane result MUST be packed from index zero in its existing output order, and positions after shorter results MUST be masked. Those output masks MUST represent structural padding rather than source gaps.

#### Scenario: Normal mode removes gaps independently
- **WHEN** masked partial chains are processed in normal mode along their shared chain axis
- **THEN** each lane's masked positions are removed independently and the resulting unequal lengths are packed from index zero with trailing masks

#### Scenario: Lossy mode uses each lane's real source positions
- **WHEN** different lanes contain gaps at different selected-axis positions and are processed in lossy mode
- **THEN** boundary values are identified from each lane's original unmasked indices rather than indices in its compressed values

#### Scenario: Redundant mode retains the full lane domain
- **WHEN** a gapped lane is processed in redundant mode
- **THEN** complementary values are calculated against the original selected-axis lane length, including gaps, before its result is structurally packed

#### Scenario: Dense partial tuples match core
- **WHEN** a multidimensional partial chain collection has no masked positions
- **THEN** its partial tuple values and structural masks equal `foapy.core.intervals_tuple()` for the same binding, tuple mode, and axis

#### Scenario: Three-dimensional partial lanes preserve axis placement
- **WHEN** partial chain input has shape `(A, B, C)` and the longest lane result has length `L`
- **THEN** axes 0, 1, and 2 produce shapes `(L, B, C)`, `(A, L, C)`, and `(A, B, L)` respectively

#### Scenario: Empty partial tuple collections
- **WHEN** all selected partial lanes are empty or fully masked, or no lanes exist because an orthogonal dimension is zero
- **THEN** the selected output axis has length zero and every orthogonal dimension is preserved

### Requirement: Partial interval tuple axis behavior preserves its one-dimensional API
One-dimensional calls to `foapy.partials.intervals_tuple()` with omitted axis, `axis=0`, or `axis=-1` MUST use the direct partial kernel and return the existing plain `numpy.ndarray` result. Existing binding, tuple-mode, gap, source-position, ordering, dtype, and empty-input behavior MUST remain unchanged. Multidimensional input without an explicit axis MUST raise `Not1DArrayException`; scalar input MUST raise `Not1DArrayException`; negative axes MUST follow NumPy conventions; and an out-of-range axis MUST raise NumPy's axis error.

#### Scenario: Existing gapped one-dimensional tuple remains unchanged
- **WHEN** a one-dimensional masked chain is passed without `axis` for any valid binding and tuple mode
- **THEN** its result is identical to the pre-axis partial API and remains a plain `numpy.ndarray`

#### Scenario: Explicit sole partial axis matches omitted axis
- **WHEN** a one-dimensional partial chain is called with `axis=0` or `axis=-1`
- **THEN** both results equal the omitted-axis call and remain plain arrays

#### Scenario: Partial tuple dimensionality and axis validation
- **WHEN** multidimensional input omits `axis`, input is scalar, or an explicit axis is out of range
- **THEN** the function raises `Not1DArrayException`, `Not1DArrayException`, or NumPy's axis error respectively

### Requirement: Partial tuple output composes with the existing interval distribution
The existing `foapy.intervals_distribution(tuple_result, *, axis=None)` and `foapy.core.intervals_distribution(tuple_result, *, axis=None)` APIs MUST accept the masked multidimensional output of `foapy.partials.intervals_tuple()`. They MUST exclude structural padding before counting each selected-axis lane while preserving meaningful unmasked zero-frequency bins. The system MUST NOT add a duplicate `foapy.partials.intervals_distribution` API.

#### Scenario: Partial tuple output composes directly with distribution
- **WHEN** the masked multidimensional result of `foapy.partials.intervals_tuple(..., axis=a)` is passed to `foapy.intervals_distribution(..., axis=a)`
- **THEN** structural padding is excluded and every lane's unmasked interval values are counted independently

#### Scenario: Dense partial pipeline matches core
- **WHEN** dense chain collections are transformed with partial and core interval tuples and their results are passed to the existing distribution API
- **THEN** both pipelines produce distributions with identical values, masks, shape, dtype, and return type

#### Scenario: No duplicate partial distribution export
- **WHEN** callers inspect public members of `foapy.partials`
- **THEN** no `intervals_distribution` member is added

### Requirement: Axis-aware interval transformations are documented and benchmarked
The system MUST document independent-lane axis semantics, one-, two-, and three-dimensional shape placement, masked variable-length packing, return-type rules, validation errors, partial gap handling, and core and partial tuple-to-distribution pipelines. The ASV suite MUST include time and peak-memory benchmarks for deterministic core and partial multidimensional tuple inputs across representative lengths, lane counts, axis placements, tuple modes, mask states, and variable-length outputs while retaining legacy one-dimensional coverage.

#### Scenario: Public references explain axis transformations
- **WHEN** a user opens the generated references for core interval tuples and distributions
- **THEN** they include runnable multidimensional examples and explain how the selected axis is replaced and shorter results are masked

#### Scenario: ASV discovers axis transformation benchmarks
- **WHEN** the benchmark suite is collected
- **THEN** it includes deterministic time and peak-memory cases for multidimensional core interval tuples and distributions and partial interval tuples
