## Why

`foapy.core.alphabet` and `foapy.core.order` currently reject multidimensional inputs even though an array axis can naturally define the sequence direction and each orthogonal slice can act as one alphabet element. Extending the same factorization model to dense and partial sequences allows structured elements while preserving the defining ability to reconstruct the source from its order and alphabet.

## What Changes

- Add an optional `axis` parameter to `foapy.core.alphabet` and `foapy.core.order`.
- When `axis` is supplied, treat each complete slice indexed along that axis as one sequence element, preserve first-appearance ordering, return a one-dimensional order, and retain the selected axis in the alphabet result.
- Define reconstruction through `numpy.take(alphabet, order, axis=axis)` for dense inputs.
- Add equivalent axis-aware behavior to `foapy.partials.alphabet` and `foapy.partials.order`, excluding fully masked slice positions as gaps and preserving those gaps in the one-dimensional order mask.
- Preserve the existing public behavior for one-dimensional calls that omit `axis`.
- Add tests, documentation, type annotations, and benchmarks for one-, two-, and three-dimensional inputs, all valid positive and negative axes, stable slice ordering, reconstruction, and partial-sequence gaps.

## Capabilities

### New Capabilities

- `axis-aware-sequence-factorization`: Stable core alphabet/order factorization of dense arrays whose sequence elements are complete orthogonal slices along a selected axis.

### Modified Capabilities

- `partials-package`: Extend partial alphabet/order operations from scalar elements in one-dimensional inputs to slice elements along an explicit axis while preserving whole-slice gaps.

## Impact

- Public APIs: `foapy.core.alphabet`, `foapy.core.order`, `foapy.partials.alphabet`, and `foapy.partials.order` gain an optional axis argument.
- Implementation: core stable-uniqueness and inverse-mapping logic must compare complete slices and preserve the selected axis in alphabet output; partials must derive a one-dimensional positional mask from slice masks.
- Tests and benchmarks: existing one-dimensional coverage remains, with new multidimensional, axis-validation, reconstruction, and masked-slice cases.
- Documentation: core and partials API references will describe slice-as-element semantics, shapes, axis placement, and reconstruction.
- Dependencies: no new runtime dependency is expected; the implementation remains based on NumPy.
