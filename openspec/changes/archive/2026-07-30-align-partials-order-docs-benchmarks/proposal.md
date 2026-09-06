## Why

`foapy.partials.order` is implemented and well covered by tests, but users cannot discover it through the public API reference as they can `foapy.order`. Its docstring also lacks runnable examples and type annotations, and the ASV suite has no partial-order benchmark, leaving an important masked-array pipeline operation without documented or performance-visible parity.

This change makes the intentional interface difference—mask-preserving output—explicit and gives maintainers comparable performance data without changing the function’s behavior.

## What Changes

- Add public API reference documentation for `foapy.partials.order` to the MkDocs navigation.
- Add runnable examples covering plain input, masked input, gap preservation, and `return_alphabet=True`.
- Align `foapy.partials.order`’s public signature metadata with the core function by adding input/flag/return annotations while preserving the callable signature and masked-array result contract.
- Document the contrast between `foapy.order`’s dense ndarray output and `foapy.partials.order`’s position-preserving masked-array output.
- Add ASV time and peak-memory benchmarks for `foapy.partials.order`, including representative unmasked, partially masked, and fully masked cases and scalable input lengths.
- Extend verification as needed to ensure documentation examples and benchmark setup reflect the existing tested semantics.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `partials-package`: require discoverable public documentation, examples, type annotations, and benchmark coverage for `foapy.partials.order` while retaining its existing masked-array behavior.

## Impact

- Documentation: `docs/references/partials/`, `mkdocs.yml`, and potentially the partials fundamentals/quickstart pages.
- API metadata: `src/foapy/partials/_order.py` annotations and docstring only; no behavioral or breaking API changes intended.
- Benchmarks: a new ASV benchmark module under `benchmarks/benchmarks/` and generated benchmark results only if the project workflow records them.
- Tests/CI: documentation examples and benchmark importability may be validated; existing `foapy.order` and `foapy.partials.order` behavior remains unchanged.
