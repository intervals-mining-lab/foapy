## 1. Public API documentation

- [x] 1.1 Add `docs/references/partials/order.md` with autodoc for `foapy.partials.order`.
- [x] 1.2 Expand the `foapy.partials.order` docstring with the dense-vs-masked interface contract, return-mode details, and runnable plain/masked examples.
- [x] 1.3 Add the partials order reference page to the `foapy.partials` section of `mkdocs.yml`.
- [x] 1.4 Verify examples and generated documentation build successfully and accurately show mask preservation and alphabet behavior.

## 2. API metadata

- [x] 2.1 Add compatible annotations to `foapy.partials.order` for the input, `return_alphabet` flag, and masked-array/tuple return forms.
- [x] 2.2 Add or update focused tests that inspect the signature/annotations and confirm the existing call syntax and runtime behavior are unchanged.

## 3. ASV benchmarks

- [x] 3.1 Add a `PartialsOrderSuite` benchmark module with the existing order benchmark’s scalable lengths and representative data families.
- [x] 3.2 Prepare unmasked, partially masked, and fully masked inputs in benchmark setup, keeping allocation outside timed methods and applying practical skip thresholds.
- [x] 3.3 Add `time_order` and `peakmem_order` methods and verify ASV discovers/imports all cases.

## 4. Verification

- [x] 4.1 Run the core and partial order tests plus partial pipeline consistency tests.
- [x] 4.2 Run documentation validation/build checks relevant to the new reference page.
- [x] 4.3 Run a quick ASV dry-run for the partial order suite and record any expected environment-specific limitations.
