## Context

`foapy.partials.order` already implements the required position-preserving masked-array behavior and has direct tests. The core function has public API autodoc, runnable examples, annotations, and ASV time/peak-memory benchmarks; the partial counterpart currently has only a minimal docstring, no public reference page or navigation entry, no annotations, and no benchmark module.

The change is documentation and measurement work around an existing API. Its defining behavior must remain unchanged: plain inputs are treated as fully unmasked, masked values are excluded from alphabet construction, and the returned order remains aligned with the source positions.

## Goals / Non-Goals

**Goals:**

- Make `foapy.partials.order` discoverable in generated API documentation.
- Provide examples that show both ordinary and masked usage, including alphabet return behavior.
- Add annotations that describe the accepted input, flag, and masked-array/tuple returns without changing invocation syntax.
- Add representative ASV time and peak-memory measurements for partial order, including mask densities that exercise compressed and remapping paths.
- Keep documentation and benchmark cases consistent with the tested contract.

**Non-Goals:**

- Changing the algorithm, output values, mask propagation, or exception behavior.
- Making `foapy.partials.order` return a plain ndarray for unmasked inputs.
- Renaming or hoisting the function into the top-level `foapy` namespace.
- Adding benchmarks for unrelated partials functions.

## Decisions

1. **Use a dedicated reference page and MkDocs entry.**
   The existing partials alphabet reference establishes the package reference layout. A sibling `docs/references/partials/order.md` will expose the order docstring through the same autodoc mechanism. This is preferable to relying only on the fundamentals page or OpenSpec artifacts, which are not the generated API reference.

2. **Document semantics in the function docstring, with examples based on `numpy.ma`.**
   The docstring will explicitly state that the result is a same-length masked array and that masked source positions are preserved. Examples will use `numpy.ma.masked_array` and inspect both compressed values and masks so users do not mistake masked data payloads for valid order indices.

3. **Add precise annotations without changing the callable interface.**
   Use existing NumPy typing conventions available in the project and annotate the input, boolean flag, and union of the single masked-array result versus the `(masked-array, ndarray)` tuple. The default and parameter order remain exactly `X, return_alphabet=False`; annotations are metadata, not runtime validation.

4. **Mirror the core benchmark dimensions while modeling masks explicitly.**
   Add a `PartialsOrderSuite` with the same scalable lengths and representative data families as the order benchmark. The setup will construct plain/unmasked, partially masked, and fully masked inputs before timing; setup work will not be included in measured methods. Both `time_order` and `peakmem_order` will be provided, with skip rules preventing impractical large masked allocations.

5. **Keep generated benchmark results out of the source change unless the repository workflow requires recording them.**
   The benchmark module is the reproducible source of measurement. Existing stored ASV results are machine-specific; updating them is optional and should follow the project’s normal benchmark-recording process rather than being required for implementation.

## Risks / Trade-offs

- [Type annotation compatibility] NumPy typing syntax can vary across supported Python/NumPy versions → use the project’s declared compatibility range and run the normal test/import checks.
- [Benchmark allocation cost] Large masked arrays can consume substantially more memory than dense arrays → use explicit skip thresholds and keep all allocation in `setup`.
- [Documentation drift] Examples can diverge from implementation semantics → execute the relevant examples or add a documentation validation step in the task verification.
- [Misleading comparability] Partial order has mask-preservation overhead, so it is not directly equivalent to dense order timing → label benchmark cases by mask pattern and describe the comparison as diagnostic, not a performance promise.
