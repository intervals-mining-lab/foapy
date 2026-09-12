## 1. Shared Axis Infrastructure and Validation

- [x] 1.1 Add or extract a private lane-application helper that normalizes an axis, presents all one-dimensional lanes as one batch, packs variable-length `numpy.intp` results from index zero, masks trailing positions, and restores the result dimension at the selected axis.
- [x] 1.2 Define deterministic behavior for empty selected axes and absent lanes caused by structurally empty orthogonal dimensions.
- [x] 1.3 Add the internal non-exported `is_valid_intervals_chain(chain, *, axis=None)` helper with an always-true one-dimensional content check and aggregate multidimensional lane validation.
- [x] 1.4 Verify the validator's scalar, missing-axis, negative-axis, and invalid-axis behavior uses the shared normalization contract.
- [x] 1.5 Add an export regression test proving the provisional validator is absent from both `foapy.core` and top-level `foapy`.

## 2. Axis-Aware Interval Tuples

- [x] 2.1 Extract or preserve private one-dimensional normal, lossy, and redundant tuple kernels without changing their binding, order, dtype, or empty-input semantics.
- [x] 2.2 Add typed keyword-only `axis=None` support to `foapy.core.intervals_tuple` and keep one-dimensional omitted-axis, `axis=0`, and `axis=-1` calls on the direct plain-array path.
- [x] 2.3 Invoke the internal interval-chain validator before tuple transformation and raise `ValueError` when it reports false.
- [x] 2.4 Dispatch multidimensional inputs across independent lanes and always return a masked array with the output dimension replacing the selected input axis.
- [x] 2.5 Preserve every lane's existing output order while masking trailing positions for unequal lossy and redundant result lengths.
- [x] 2.6 Preserve binding and tuple-mode validation order and implement specified multidimensional-without-axis, scalar, and invalid-axis errors.

## 3. Axis-Aware Interval Distributions

- [x] 3.1 Extract or preserve a private one-dimensional distribution kernel with legacy plain-array counts, dtype, and empty-input behavior.
- [x] 3.2 Add typed keyword-only `axis=None` support to `foapy.core.intervals_distribution` and retain the direct plain-array path for one-dimensional input.
- [x] 3.3 Accept one-dimensional masked tuple input by excluding masked positions before counting while preserving meaningful unmasked zero-frequency bins.
- [x] 3.4 Dispatch multidimensional inputs across independent lanes and always return a masked array with shorter distributions trailing-masked along the selected axis.
- [x] 3.5 Support negative axes and implement specified missing-axis, scalar, invalid-axis, empty-lane, and structurally empty behavior.
- [x] 3.6 Verify direct composition of axis-aware `intervals_tuple` output into `intervals_distribution` on the same axis.

## 4. Interval Tuple Tests

- [x] 4.1 Add exact row- and column-lane tests for normal, lossy, and redundant modes with both bindings.
- [x] 4.2 Add three-dimensional tests for every valid axis and equivalent negative axes, checking that the output dimension replaces the selected axis.
- [x] 4.3 Add unequal-length tests checking packed values and trailing masks, plus equal-length tests proving multidimensional results remain masked arrays with false masks.
- [x] 4.4 Add one-dimensional compatibility and dispatch tests for omitted axis, axis 0, axis -1, empty input, dtype, and plain-array return type.
- [x] 4.5 Add missing-axis, invalid-axis, scalar, empty selected-axis, and structurally empty orthogonal-dimension tests.
- [x] 4.6 Add validator integration tests proving tuple transformation consults the hook and rejects a monkeypatched false result.

## 5. Interval Distribution Tests

- [x] 5.1 Add exact row- and column-lane distribution tests and three-dimensional shape-placement tests for every valid axis.
- [x] 5.2 Add unequal-maximum tests distinguishing masked trailing bins from valid unmasked zero-frequency bins.
- [x] 5.3 Add masked-input, fully masked lane, all-empty, empty selected-axis, and structurally empty orthogonal-dimension tests.
- [x] 5.4 Add one-dimensional parity and direct-dispatch tests for omitted, positive, and negative sole-axis calls, including plain return type and `numpy.intp` dtype.
- [x] 5.5 Add missing-axis, invalid-axis, and scalar validation tests.
- [x] 5.6 Add multidimensional tuple-to-distribution pipeline tests across tuple modes and representative axes.

## 6. Documentation

- [x] 6.1 Update the core `intervals_tuple` signature, annotations, return types, axis errors, and docstring with runnable two- and three-dimensional lane examples and variable-length masks.
- [x] 6.2 Update the core `intervals_distribution` signature, annotations, masked-input rules, return types, axis errors, and docstring with runnable multidimensional examples.
- [x] 6.3 Update fundamental documentation with the independent-lane model, `(A, B, C)` axis-to-shape mapping, structural-mask semantics, and tuple-to-distribution composition.
- [x] 6.4 Build the MkDocs site and resolve reference or example failures.

## 7. Benchmarks

- [x] 7.1 Extend the interval-tuple ASV module with deterministic multidimensional lane cases across representative lane lengths, lane counts, axis placements, bindings, tuple modes, and uniform or variable result lengths.
- [x] 7.2 Extend the interval-distribution ASV module with deterministic plain and masked multidimensional cases across representative lane lengths, lane counts, and axis placements.
- [x] 7.3 Add time and peak-memory methods with practical quick-mode skips and timeouts while retaining existing one-dimensional benchmark matrices.
- [x] 7.4 Verify ASV discovery and smoke-run the new benchmark cases without changing stored machine-specific results.

## 8. Core Final Verification

- [x] 8.1 Run the existing one-dimensional tuple, distribution, pipeline, partial, and congeneric suites to confirm compatibility.
- [x] 8.2 Run the complete pytest suite and resolve regressions.
- [x] 8.3 Run Black, isort, flake8, and `git diff --check` on the completed change.
- [x] 8.4 Run strict OpenSpec validation and confirm every proposal requirement is represented by implementation and verification tasks.

## 9. Axis-Aware Partial Interval Tuples

- [x] 9.1 Extract the existing partial tuple body into an authoritative one-dimensional kernel that retains each lane's original mask, unmasked indices, and full source-domain length while calculating normal, lossy, and redundant results.
- [x] 9.2 Add typed keyword-only `axis=None` support to `foapy.partials.intervals_tuple` and keep omitted-axis, `axis=0`, and `axis=-1` one-dimensional calls on the direct plain-array path.
- [x] 9.3 Reuse the shared lane dispatcher for multidimensional partial chains while preserving masked lanes until the partial kernel finishes and always returning structurally packed masked arrays.
- [x] 9.4 Implement negative-axis, missing-axis, scalar, invalid-axis, empty selected-axis, fully masked lane, and structurally empty orthogonal-dimension behavior.
- [x] 9.5 Preserve existing binding and tuple-mode validation order, `numpy.intp` dtype, start/end processing frames, and dense parity with the core tuple API.

## 10. Partial Interval Tuple Tests

- [x] 10.1 Add exact row- and column-lane tests for normal, lossy, and redundant modes with both bindings and lane-specific gap positions.
- [x] 10.2 Add three-dimensional tests for every valid axis and equivalent negative axes, checking selected-axis result placement.
- [x] 10.3 Add variable- and uniform-length tests checking structural masks, plus empty, fully masked, and absent-lane shape cases.
- [x] 10.4 Add one-dimensional compatibility and direct-dispatch tests for omitted axis, axis 0, axis -1, plain or masked input, every mode, dtype, order, and empty input.
- [x] 10.5 Add dimensionality and invalid-axis tests and multidimensional dense-parity tests against `foapy.core.intervals_tuple`.
- [x] 10.6 Add gapped partial tuple-to-distribution pipeline tests proving the existing `foapy.intervals_distribution` accepts masked output across tuple modes, bindings, and representative axes.

## 11. Partial Documentation and Benchmarks

- [x] 11.1 Update partial tuple annotations and docstring with axis behavior, input-gap versus output-padding masks, errors, return types, and runnable two- and three-dimensional examples.
- [x] 11.2 Update the partial tuple API reference and fundamental documentation with lane processing, selected-axis shape mapping, gap-aware calculations, structural packing, and dense core parity.
- [x] 11.3 Document direct composition with the existing core and top-level interval distribution APIs and confirm that no duplicate partial distribution API is exported.
- [x] 11.4 Add deterministic ASV time and peak-memory matrices for multidimensional partial tuples across lane lengths, lane counts, axes, bindings, tuple modes, and gap patterns.
- [x] 11.5 Build the MkDocs site, verify ASV discovery, and smoke-run the new partial benchmark cases without saving machine-specific results.

## 12. Final Verification

- [x] 12.1 Run existing partial one-dimensional and pipeline suites to confirm compatibility.
- [x] 12.2 Run the new partial axis suite and complete pytest suite and resolve regressions.
- [x] 12.3 Run Black, isort, flake8, and `git diff --check` on the completed delta.
- [x] 12.4 Run strict OpenSpec validation after the deferred `partials-package` delta spec is generated, and confirm every partial requirement is represented by implementation and verification tasks.

## 13. Validation-Path Performance Follow-Up

- [x] 13.1 Add a fast path to `is_valid_intervals_chain()` for already prepared one-dimensional ndarrays with omitted axis while preserving direct ArrayLike conversion and all scalar, missing-axis, negative-axis, and invalid-axis behavior.
- [x] 13.2 Refactor core `intervals_tuple()` to prepare its input once, normalize any explicit one-dimensional axis once, consult the validation hook, and reuse the prepared array in the one-dimensional tuple kernel.
- [x] 13.3 Remove duplicate multidimensional input preparation and axis normalization from validation while preserving `ValueError` behavior and preventing partial results from escaping.
- [x] 13.4 Extend validator integration and dispatch tests to verify the one-dimensional fast path, validation-before-transformation order, false-result rejection, and absence of duplicate multidimensional preparation.
- [x] 13.5 Re-run the affected legacy one-dimensional and multidimensional ASV tuple benchmarks and confirm validation dispatch no longer creates a material regression against the pre-axis implementation.
- [x] 13.6 Run the focused tuple tests, complete pytest suite, Black, isort, flake8, `git diff --check`, and strict OpenSpec validation.

## 14. Vectorized Lane Processing Follow-Up

- [x] 14.1 Amend mandatory repository guidance to prohibit Python loops, comprehensions, generator expressions, and disguised loop wrappers in production while allowing loops in tests and benchmark setup.
- [x] 14.2 Replace the shared per-lane callback and packing loops with one vectorized batch-dispatch call and NumPy indexed masked packing.
- [x] 14.3 Add vectorized multidimensional kernels for core interval tuples and interval distributions, including aggregate pre-transform validation without duplicate axis normalization.
- [x] 14.4 Add vectorized multidimensional partial interval-tuple kernels that preserve gap coordinates, binding order, variable lengths, and structural masks.
- [x] 14.5 Update dispatch tests for batch validation and add an AST regression test prohibiting Python iteration and disguised loop wrappers in the affected production modules.
- [x] 14.6 Run focused axis and pipeline tests, the complete pytest suite, ASV tuple benchmarks, formatting and lint checks, `git diff --check`, and strict OpenSpec validation.
