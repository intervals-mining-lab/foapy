## 1. Core Factorization Contract

- [x] 1.1 Add core alphabet/order tests for stable scalar behavior, two-dimensional row and column elements, three-dimensional elements on every axis, positive/negative axis equivalence, and `return_alphabet` parity.
- [x] 1.2 Add reconstruction and shape tests asserting that order is one-dimensional, alphabet preserves rank and axis placement, and `numpy.take(alphabet, order, axis=axis)` restores dense inputs.
- [x] 1.3 Add core validation and edge-case tests for omitted axes on multidimensional inputs, out-of-range axes, scalar inputs, empty sequence axes, empty orthogonal dimensions, and representative numeric and string dtypes.
- [x] 1.4 Implement a shared private stable-factorization primitive that compares complete orthogonal slices, returns inverse indices in first-appearance order, preserves alphabet dtype and axis placement, and handles empty shapes.
- [x] 1.5 Extend `foapy.core.alphabet` and `foapy.core.order` with the keyword-only `axis` parameter and delegate both functions to the shared primitive without changing omitted-axis one-dimensional behavior.

## 2. Partial Sequence Factorization

- [x] 2.1 Add partial alphabet/order tests for multidimensional plain inputs, fully unmasked arrays, whole-slice gaps on axis 0 and interior/last axes, first-appearance ordering after gaps, positive/negative axes, and core parity.
- [x] 2.2 Add partial reconstruction, empty/fully-gapped input, multidimensional-without-axis, invalid-axis, scalar-input, and mixed-mask rejection tests.
- [x] 2.3 Implement whole-slice mask validation and derive the one-dimensional sequence-position gap mask for any valid explicit axis.
- [x] 2.4 Extend `foapy.partials.alphabet` and `foapy.partials.order` with keyword-only `axis`, factorize present slices through the shared core behavior, preserve the alphabet axis, and scatter inverse indices into the masked one-dimensional order.

## 3. Documentation and Performance Coverage

- [x] 3.1 Update core alphabet/order docstrings and references with the axis model, output-shape rules, one-, two-, and three-dimensional examples, negative-axis behavior, errors, and dense `numpy.take` reconstruction.
- [x] 3.2 Update partial alphabet/order docstrings and references with whole-slice gap rules, mixed-mask errors, return shapes, observed-slice reconstruction, and dense parity.
- [x] 3.3 Update type annotations for all four functions and add or adjust ASV time and peak-memory benchmarks across scalable sequence lengths, multiple element shapes, axis placements, and partial gap patterns.

## 4. Verification

- [x] 4.1 Run the focused core and partials alphabet/order test suites and resolve all regressions.
- [x] 4.2 Run the complete test suite, documentation build/checks, linting, and relevant benchmark discovery or smoke cases.
- [x] 4.3 Verify the final public signatures, legacy positional `return_alphabet` compatibility, public exports, and every dense/partial reconstruction example from the specifications.

## 5. One-Dimensional Performance Restoration

- [x] 5.1 Restore dedicated core one-dimensional paths so `alphabet` does not compute order and `order(..., return_alphabet=False)` does not materialize an alphabet.
- [x] 5.2 Restore dedicated partial one-dimensional paths, including the empty/fully-masked fast path, without invoking multidimensional slice-mask processing.
- [x] 5.3 Add dispatch regression tests and compare representative one-dimensional timings with the pre-axis implementations.

## 6. Experimental Hash Factorization

- [x] 6.1 Replace multidimensional record uniqueness with vectorized 128-bit candidate grouping while retaining exact slice comparison and a collision fallback.
- [x] 6.2 Add equality-semantic and forced-collision tests for the hash factorizer, including signed zero and NaN behavior.
- [x] 6.3 Run the complete tests and compare time and peak allocations against the current axis implementation across element widths and cardinalities.

## 7. XXH3 Hash Experiment

- [x] 7.1 Replace the custom `einsum` fingerprint with XXH3-128 dispatched through `numpy.apply_along_axis`, add the runtime dependency, and preserve exact collision verification.
- [x] 7.2 Run focused and complete correctness checks, then compare time and peak memory against exact record factorization across element widths and cardinalities.

## 8. Internal Factorizer Clarity

- [x] 8.1 Rename the shared helper to `_stable_factorize`, update its private call sites, and document how equal-digest groups are exactly verified before factorization.
- [x] 8.2 Rename the partial shared helper to `_stable_partial_factorize` and update all private call sites and dispatch tests.
