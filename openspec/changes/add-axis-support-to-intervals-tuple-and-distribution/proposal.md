## Why

Axis-aware interval chains can represent multidimensional source slices, but core and partial tuple APIs do not consistently process collections of independent interval chains stored along an arbitrary axis. Partial pipelines additionally need to preserve gap-aware tuple semantics while gaining the same axis placement and variable-length packing behavior as core pipelines. Because the one-dimensional tuple operations can complete in only a few microseconds, provisional validation must not repeat input conversion, axis normalization, or multidimensional lane traversal before the actual transformation.

## What Changes

- Add a keyword-only `axis=None` parameter to core `intervals_tuple` and `intervals_distribution`.
- Add the same keyword-only axis support to `foapy.partials.intervals_tuple`, preserving each masked lane's gap-aware tuple semantics.
- Ensure the masked output of axis-aware `foapy.partials.intervals_tuple` composes directly with the existing top-level and core `intervals_distribution`.
- For multidimensional input, apply the existing one-dimensional operation independently to every lane along the selected axis, following `numpy.apply_along_axis` placement rules.
- Return a masked array for every multidimensional call, replacing the selected axis with the longest lane result and masking the trailing positions of shorter results.
- Keep one-dimensional calls, including explicit `axis=0` and `axis=-1`, on the existing direct path and returning plain arrays.
- Reject multidimensional input without an explicit axis, scalars, and invalid axes consistently with the other axis-aware core APIs.
- Add an internal, non-public `is_valid_intervals_chain(..., axis=None)` hook used by `intervals_tuple`; its provisional one-dimensional validity check always returns `True` so stronger validation can be introduced later without changing the tuple API. Reuse prepared arrays and normalized axes, and validate a complete multidimensional lane batch once before invoking its vectorized tuple kernel.
- Implement multidimensional validation, tuple transformation, distribution counting, and variable-length packing with C-backed NumPy batch operations and no Python iteration in production code.
- Teach axis-aware distributions to ignore masked padding while retaining meaningful zero-frequency bins.
- Add tests, documentation, and ASV time and peak-memory coverage for core and partial one-, two-, and three-dimensional inputs and variable-length lane results.

## Capabilities

### New Capabilities

- `axis-aware-interval-transformations`: Define independent-lane axis processing, shape placement, masked variable-length results, validation integration, and compatibility for core interval tuples and distributions.

### Modified Capabilities

- `partials-package`: Extend the partial interval tuple contract with axis-aware independent lanes and composition with the existing interval distribution API.

## Impact

- Public APIs: core and top-level `intervals_tuple` and `intervals_distribution` gain keyword-only `axis=None` support, and `foapy.partials.intervals_tuple` gains the same axis parameter.
- Core and partial implementation: tuple and distribution logic shares vectorized axis dispatch and masked result packing while retaining direct one-dimensional kernels and partial gap-aware tuple calculations. Core tuple validation reuses input preparation and validates a prepared lane batch once.
- Internal API: a non-exported interval-chain validation helper is introduced and called before each applicable one-dimensional tuple transformation.
- Tests, docstrings, API references, fundamental documentation, and ASV benchmarks require multidimensional core and partial coverage.
- Congeneric APIs, dependencies, public exports, and existing one-dimensional results remain unchanged.
