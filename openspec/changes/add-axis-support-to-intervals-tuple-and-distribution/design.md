## Context

`foapy.core.intervals_chain` now converts multidimensional source slices into one one-dimensional interval chain, while core `intervals_tuple` and `intervals_distribution` remain documented as one-dimensional consumers. Separately, users can hold many already-built chains or tuples in an N-dimensional rectangular array and need to transform every one-dimensional lane along a selected axis.

`foapy.partials.intervals_tuple` is also one-dimensional. It differs from the core operation because a masked position is a source gap: normal and lossy modes remove gaps, while redundant mode measures complementary intervals against the full source-domain length, including gaps. Once a partial tuple lane is produced, the existing core and top-level `intervals_distribution` semantics already apply because source gaps have been removed and any remaining masks are structural padding.

The existing tuple modes can produce different result lengths for equal-length input lanes: normal yields `n`, lossy yields `n - k`, and redundant yields `n + k`. Distributions similarly end at each lane's maximum interval value. A normal ndarray therefore cannot preserve every independent result without either rejecting common inputs or introducing a padding convention. The congeneric APIs already demonstrate packed results, but their row-per-symbol meaning is domain-specific and must not be changed by this feature.

## Goals / Non-Goals

**Goals:**

- Apply core interval-tuple and distribution operations independently to one-dimensional lanes along any explicit valid axis.
- Apply partial interval-tuple operations independently to masked lanes without losing gap-aware source positions, and compose their masked output with the existing interval-distribution API.
- Place the variable result dimension at the selected axis position for one-, two-, and three-dimensional inputs.
- Preserve variable lane lengths using trailing masks rather than broadcasting, object arrays, or sentinel values.
- Preserve the direct plain-array behavior of all one-dimensional calls.
- Establish a non-public, axis-aware interval-chain validation hook before defining full semantic validity rules.
- Keep provisional validation off duplicate input-preparation and multidimensional traversal paths.
- Use only C-backed NumPy batch operations in production; Python loops, comprehensions, generator expressions, and disguised loop wrappers are prohibited.
- Cover the behavior in tests, documentation, and deterministic ASV benchmarks.

**Non-Goals:**

- Changing congeneric APIs or adding new partial or top-level exports.
- Treating complete orthogonal slices as single equality elements; that is the axis model of `order` and `intervals_chain`, not this independent-lane transformation.
- Returning ragged object arrays or Python lists.
- Defining substantive interval-chain validity rules in this change.
- Changing binding, tuple-mode, interval-value, or one-dimensional ordering semantics.

## Decisions

### 1. Axis selects independent one-dimensional lanes

For an input with shape `(A, B, C)`, axis 0 processes every `input[:, b, c]`, axis 1 processes every `input[a, :, c]`, and axis 2 processes every `input[a, b, :]`. A lane's result replaces the selected dimension, producing `(L, B, C)`, `(A, L, C)`, or `(A, B, L)` when every lane result has length `L`.

This matches `numpy.apply_along_axis` iteration and dimension placement. Reusing the slice-as-element model from `order` was rejected because tuple and distribution inputs contain scalar interval values; an orthogonal vector is a collection of separate chains, not one interval value.

### 2. Pack variable results into masked arrays

Every multidimensional call returns a `numpy.ma.MaskedArray` of `numpy.intp`. The selected output dimension is the maximum result length across all lanes. Each one-dimensional result is copied to the beginning of its lane in its existing order and all trailing positions are masked. If every lane result is empty, the selected result dimension is zero.

Multidimensional calls always return a masked array, including normal tuple mode and batches whose lane lengths happen to match, so return type never depends on data values. One-dimensional calls always return plain ndarrays. Zero padding without masks was rejected because zero is not an interval value and would require sentinel-aware consumers. Object arrays were rejected because they lose ordinary NumPy shape, dtype, and axis behavior.

When there are no lanes because an orthogonal dimension is zero, normal tuple mode retains its known selected-axis length; variable-length tuple modes and distribution use selected-axis result length zero because no lane result exists from which to derive a maximum.

### 3. Use vectorized shared axis dispatch around batch kernels

The existing one-dimensional kernels remain authoritative for direct calls. Multidimensional calls use vectorized batch kernels instead: a shared helper normalizes the axis once, moves it last, reshapes all orthogonal coordinates into a two-dimensional lane matrix, invokes one batch kernel, reshapes its fixed rectangular masked result, and restores the selected-axis position. The helper preserves masked-array lanes so partial tuple calculations can distinguish gaps from present interval values.

Variable-length packing uses vectorized selection counts, cumulative destination indices, and NumPy advanced assignment into a masked rectangular output. Core and partial tuple modes compute selection masks and complementary values across the complete lane matrix. Distribution uses indexed NumPy accumulation across all valid lane values. Python loops, comprehensions, generator expressions, `numpy.vectorize`, and `numpy.apply_along_axis` were rejected because they execute lane callbacks in Python rather than processing the batch in compiled NumPy operations.

### 4. Preserve the one-dimensional fast and compatibility path

After validating binding and mode values, each core or partial public function prepares its input dimensionality and axis once. A one-dimensional input with omitted axis, axis 0, or axis -1 calls the applicable private one-dimensional kernel directly and returns its legacy plain result. The core tuple path consults its validation hook using that prepared one-dimensional array and does not repeat conversion or axis normalization. Multidimensional input without axis and scalar input raise `Not1DArrayException`; invalid axes use NumPy's axis error through the shared normalization helper.

This avoids masked allocation and iteration overhead for existing callers and gives the currently documented one-dimensional-only contracts explicit multidimensional validation.

### 5. Add an internal axis-aware validation seam

A function named `is_valid_intervals_chain(chain, *, axis=None)` will live in a private core module and will not be imported by `foapy.core` or top-level `foapy`. Its private one-dimensional content check returns the Python Boolean `True` in this change. When called directly with a multidimensional input and explicit axis, it applies that leaf check to every lane and returns `all(...)` as one Boolean. Structural dimensionality and axis errors follow the shared normalization rules. An already prepared one-dimensional ndarray with omitted axis takes a fast path that does not reconvert the input or invoke the general axis normalizer.

`intervals_tuple` calls the validator before transforming a one-dimensional input and raises `ValueError` if it reports false. For multidimensional input, the dispatcher calls the same hook once on the prepared two-dimensional lane batch before invoking the vectorized tuple kernel. A false aggregate result raises `ValueError` before transformation begins. Although the provisional implementation accepts all structurally valid lanes, future checks must evaluate the complete batch with vectorized NumPy operations. Exporting the helper now was rejected because its long-term semantic contract is deliberately unfinished.

### 6. Distributions consume masked tuple padding without losing real zeros

The distribution one-dimensional kernel compresses masked input before counting. Masked tuple positions contribute nothing. Within each returned distribution, zero counts between observed interval values remain ordinary unmasked zeros. Only bins beyond that lane's maximum observed interval are padding and therefore masked in the multidimensional packed result.

This lets `intervals_distribution(intervals_tuple(chains, ..., axis=a), axis=a)` compose directly. A one-dimensional masked tuple also excludes masks and returns a plain ndarray, while existing plain one-dimensional inputs remain unchanged.

### 7. Partial tuple lanes retain source-gap coordinates before structural packing

Each selected-axis lane passed to the partial tuple kernel retains its original length and mask. The kernel compresses gaps only as part of its established tuple-mode semantics. In particular, redundant mode uses the selected-axis lane length and original unmasked indices, so gaps continue to affect boundary and complementary distances independently in every lane.

After a lane is transformed, its output has no source-gap positions. Any masks in the multidimensional packed result are therefore structural trailing padding only. Every multidimensional partial tuple call returns a masked array, even when all lanes have equal output lengths; one-dimensional calls return the existing plain ndarray.

Reusing the core tuple kernel was rejected because compression would discard the real source positions required by partial lossy and redundant modes. Treating masks as aligned output gaps was also rejected because tuple transformation deliberately removes source gaps.

### 8. Partial tuple output composes with the existing distribution API

A partial interval tuple contains ordinary interval values after per-lane gap removal. The existing `foapy.intervals_distribution` and `foapy.core.intervals_distribution` functions therefore remain the sole distribution APIs. They accept the masked output of a multidimensional partial tuple, exclude its structural padding, and preserve meaningful unmasked zero-frequency bins.

For dense inputs, the partial tuple-to-distribution pipeline matches the core pipeline. For gapped inputs, differences arise only in the partial tuple values calculated from real source positions; the existing distribution API then counts those values normally. Adding a duplicate `foapy.partials.intervals_distribution` entry point was rejected because it would have identical behavior and no partial-specific state to preserve.

### 9. Test shapes, masks, dispatch, and composition

Tests will use explicit valid core and partial chains to verify row and column processing, every axis of three-dimensional inputs, negative axes, every tuple mode, varying and uniform result lengths, mask placement, empty lanes, and one-dimensional direct dispatch. Partial tests will include gaps at different lane positions and verify that redundant results use the full selected-axis domain independently per lane. Distribution tests will distinguish real internal zero counts from masked trailing bins and verify that the existing distribution API directly consumes core and partial axis-aware tuple results. Monkeypatch dispatch tests will prove one-dimensional calls do not enter multidimensional packing and multidimensional core tuple calls validate one prepared lane batch before invoking one batch kernel. An AST regression test will reject Python iteration constructs and disguised loop wrappers in the axis transformation production modules.

Benchmarks will retain existing one-dimensional matrices and add deterministic multidimensional core and partial tuple lane matrices for time and peak memory. Documentation will show the apply-along-axis shape rule, partial gap semantics, existing distribution composition, and masked variable-length examples.

## Risks / Trade-offs

- **[Vectorized packing allocates lane-wide index arrays]** → Keep all intermediate arrays linear in the lane matrix size and benchmark representative lane counts and lengths.
- **[Masked outputs add allocation cost even for uniform multidimensional results]** → Accept the predictable return contract and preserve an allocation-free direct one-dimensional path.
- **[Masked padding may be mistaken for partial-sequence gaps]** → Document that masks in core multidimensional tuple/distribution outputs are structural trailing padding, not source positions.
- **[Partial tuple input gaps and output padding use the same mask representation]** → Keep masks on input lanes until the partial kernel completes, then document that masks on packed tuple results are structural padding only.
- **[Future validation can reject inputs accepted by the provisional hook]** → Keep the function non-public and describe the current always-true leaf behavior explicitly.
- **[Batch validation reports only aggregate failure]** → Preserve the existing Boolean validation seam and fail before invoking the batch kernel; richer diagnostics remain a future validator concern.
- **[Future substantive validation can again dominate short tuple operations]** → Reuse prepared lane data and fuse validation with values already calculated by tuple kernels where practical.
- **[Empty orthogonal dimensions provide no result shape sample]** → Define deterministic mode-specific empty shapes and cover them with tests.

## Migration Plan

The change is additive for documented one-dimensional usage. Add the validation and lane-packing helpers, refactor existing algorithms into one-dimensional kernels, then enable core and partial public axis dispatch, documentation, tests, and benchmarks. Rollback consists of removing axis dispatch and helpers; all pre-existing one-dimensional signatures remain call-compatible because `axis` is keyword-only.

## Open Questions

None. Variable-length outputs use trailing masks, multidimensional calls always return masked arrays, and validation remains internal and permissive for this change.
