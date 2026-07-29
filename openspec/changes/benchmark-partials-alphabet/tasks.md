## 1. API annotations and documentation

- [x] 1.1 Add compatible input and `numpy.ndarray` return annotations to `foapy.partials.alphabet` without changing its call signature.
- [x] 1.2 Expand the partial alphabet docstring with NumPy-style parameter, return, error, and examples sections covering plain, masked, empty/all-masked, and invalid-dimensional inputs.
- [x] 1.3 Add `docs/references/partials/alphabet.md` and expose it in the `foapy.partials` MkDocs References navigation.
- [x] 1.4 Add or update practical partial-alphabet documentation so the conceptual definition and API examples are linked and consistent.

## 2. Benchmark coverage

- [x] 2.1 Add an ASV benchmark module for `foapy.partials.alphabet` with time and peak-memory measurements.
- [x] 2.2 Define comparable unmasked, partially masked, and fully masked input cases, with setup-time data preparation and safe large-input skip rules.
- [x] 2.3 Verify ASV discovers the new benchmark and document or preserve the existing quick-run workflow if benchmark invocation needs adjustment.

## 3. Tests

- [x] 3.1 Add a test where the first element is masked and later unmasked values form the alphabet.
- [x] 3.2 Add a test where a value’s first occurrence is masked but a later occurrence is unmasked, verifying first-unmasked-appearance ordering.
- [x] 3.3 Add assertions for the annotated/plain-`ndarray` contract and retain dense parity coverage with `foapy.alphabet`.

## 4. Validation

- [x] 4.1 Run the focused partial alphabet and parity tests.
- [x] 4.2 Run documentation build/reference validation and a dry-run or quick ASV discovery for the new benchmark.
- [x] 4.3 Run the broader project test suite and review the final diff for unintended API or documentation changes.
