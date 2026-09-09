## Why

`alphabet` and `order` can treat complete slices along an explicit axis as sequence elements, but `intervals_chain` still rejects every multidimensional input. Extending the same axis model to dense and partial interval chains completes the sequence-decomposition pipeline without changing existing one-dimensional callers.

## What Changes

- Add a keyword-only `axis` parameter to `foapy.core.intervals_chain` and `foapy.partials.intervals_chain`.
- Treat each complete orthogonal slice along an explicit axis as one sequence element and return one interval value per position on that axis.
- Preserve the existing binding and boundary/cycle semantics in the selected axis coordinate system.
- For partial inputs, treat wholly masked slices as gaps that remain masked and count toward interval distances, and reject partially masked slices.
- Preserve legacy one-dimensional behavior, errors, return types, and the direct one-dimensional performance path when `axis` is omitted or explicitly selects the sole axis.
- Add multidimensional tests, public documentation, and ASV time and peak-memory coverage.

## Capabilities

### New Capabilities

- `axis-aware-interval-chains`: Define slice-as-element interval-chain behavior, axis normalization, output shape, binding and chain-mode semantics, and compatibility with the existing one-dimensional core API.

### Modified Capabilities

- `partials-package`: Extend partial interval chains with explicit-axis slice elements, whole-slice gaps, mixed-mask validation, and dense parity.

## Impact

- Public APIs: `foapy.core.intervals_chain` and `foapy.partials.intervals_chain` gain a keyword-only `axis=None` parameter.
- Core implementation: axis-aware inputs can reuse the established sequence factorization/order semantics before applying the one-dimensional interval kernel.
- Partial implementation: multidimensional mask validation and whole-slice gap handling align with partial `alphabet` and `order`.
- Tests, API docstrings/reference output, fundamental documentation, and ASV benchmark suites require corresponding coverage.
- No new runtime dependency or top-level export is required.
