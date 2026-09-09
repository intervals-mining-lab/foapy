## 1. Core Interval-Chain Implementation

- [x] 1.1 Extract or define a private one-dimensional core interval-chain kernel that preserves the current grouping, binding, boundary, cycle, empty-input, dtype, and return semantics.
- [x] 1.2 Add typed keyword-only `axis=None` support to `foapy.core.intervals_chain` and reuse the shared axis-normalization rules from alphabet/order.
- [x] 1.3 Keep one-dimensional inputs, including explicit `axis=0` and `axis=-1`, on the legacy direct kernel without multidimensional factorization.
- [x] 1.4 Factorize multidimensional slice elements through the established core order path and apply the one-dimensional interval kernel to its equality codes.
- [x] 1.5 Preserve binding and chain-mode validation behavior and verify scalar, missing-axis, and invalid-axis errors use the specified exception types.

## 2. Partial Interval-Chain Implementation

- [x] 2.1 Extract or define a private one-dimensional partial interval-chain kernel that preserves full-domain gap positions and existing binding and chain-mode behavior.
- [x] 2.2 Add typed keyword-only `axis=None` support to `foapy.partials.intervals_chain` using the shared axis-normalization rules.
- [x] 2.3 Keep one-dimensional partial inputs on the legacy direct path, including explicit sole-axis calls.
- [x] 2.4 Convert multidimensional partial slices through `foapy.partials.order` so whole-slice gaps, mixed-mask validation, and equality classes match partial alphabet/order before applying the interval kernel.
- [x] 2.5 Verify gap slices remain masked and count toward occurrence, boundary, and cyclic distances across the complete selected-axis domain.

## 3. Core Tests

- [x] 3.1 Add row- and column-element tests for core interval chains with both bindings and both chain modes, including the specified concrete interval values.
- [x] 3.2 Add three-dimensional and order-code-invariance tests across every valid axis.
- [x] 3.3 Add positive/negative axis equivalence, explicit one-dimensional axis, multidimensional-without-axis, invalid-axis, scalar, and empty selected-axis tests.
- [x] 3.4 Add structurally empty-slice coverage and verify the result remains one-dimensional with `numpy.intp` dtype.
- [x] 3.5 Add a dispatch regression test proving one-dimensional calls do not enter the multidimensional factorization path.

## 4. Partial Tests

- [x] 4.1 Add multidimensional whole-slice gap tests for start/end binding and boundary/cycle modes, checking both interval data and masks.
- [x] 4.2 Add plain and fully unmasked multidimensional parity tests against the core API across valid axes and mode combinations.
- [x] 4.3 Add mixed-mask rejection, fully masked, empty selected-axis, structurally empty-slice, negative-axis, invalid-axis, scalar, and missing-axis tests.
- [x] 4.4 Add a dispatch regression test proving one-dimensional partial calls retain the direct path and existing gap behavior.
- [x] 4.5 Run the existing one-dimensional core, partial, pipeline, tuple, and congeneric suites to confirm compatibility.

## 5. Documentation

- [x] 5.1 Update the core `intervals_chain` signature, annotations, return-shape description, errors, and docstring with runnable row/column axis examples.
- [x] 5.2 Update the partial `intervals_chain` signature, annotations, whole-slice mask rules, selected-axis gap-distance semantics, errors, and docstring with a runnable multidimensional example.
- [x] 5.3 Update relevant fundamental documentation to explain that interval chains remain one-dimensional and compose directly with `intervals_tuple` after slice-as-element processing.
- [x] 5.4 Build the MkDocs site and resolve reference or example failures.

## 6. Benchmarks

- [x] 6.1 Extend the core interval-chain ASV module with deterministic axis benchmarks for representative sequence lengths, record widths, axis placements, bindings, and chain modes.
- [x] 6.2 Extend the partial interval-chain ASV module with deterministic unmasked, whole-slice-gapped, and fully masked axis cases while retaining the existing one-dimensional matrix.
- [x] 6.3 Add both time and peak-memory methods and practical skip/timeout bounds for the new benchmark matrices.
- [x] 6.4 Verify ASV discovery and smoke-run the new cases without changing stored machine-specific benchmark results.

## 7. Final Verification

- [x] 7.1 Run the complete pytest suite and confirm all legacy and axis-aware tests pass.
- [x] 7.2 Run Black, isort, flake8, and `git diff --check` on the completed change.
- [x] 7.3 Run strict OpenSpec validation and confirm every proposal requirement is represented by implementation and verification tasks.
