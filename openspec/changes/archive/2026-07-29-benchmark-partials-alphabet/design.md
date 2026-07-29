## Context

`foapy.alphabet` has a complete API docstring, generated reference page, and ASV benchmark. `foapy.partials.alphabet` implements the corresponding masked-sequence operation and already has functional tests, but its public documentation and benchmark coverage are incomplete. The existing `partials-package` contract defines the behavior that must remain stable.

## Goals / Non-Goals

**Goals:**

- Give `foapy.partials.alphabet` a typed, discoverable public API with documentation and runnable examples parallel to the core function.
- Add a reference page and MkDocs navigation entry for the partial function.
- Measure partial alphabet time and peak memory for plain, partially masked, and fully masked inputs using ASV conventions already used by the project.
- Add regression tests for masked first occurrences and later unmasked occurrences.

**Non-Goals:**

- Change alphabet ordering, masking semantics, or dense-input parity.
- Replace or merge the existing `foapy.ma.alphabet` benchmarks.
- Introduce a runtime dependency or redesign the partials package.

## Decisions

- **Mirror the core API documentation structure.** Use the same NumPy-style sections and explain the partial-specific rule that masked positions are ignored. Include examples for ordinary input, partial masking, empty/all-masked input, and invalid dimensions.
- **Use explicit NumPy-compatible annotations.** Annotate `X` as an array-like input that can be a masked array and annotate the return as `numpy.ndarray`, matching the actual plain-array result. Keep the runtime API as `alphabet(X)` so this is non-breaking.
- **Add a dedicated reference page.** Create `docs/references/partials/alphabet.md` with the project’s existing `::: foapy.partials.alphabet` directive and add it under a `foapy.partials` section in the References navigation. This keeps partials references grouped and avoids conflating them with `foapy.ma`.
- **Benchmark the partial implementation directly.** Add an ASV module analogous to `bench_alphabet.py`, importing `foapy.partials.alphabet`. Prepare inputs in `setup`, then measure `time_alphabet` and `peakmem_alphabet`. Use deterministic or controlled mask-rate cases so comparisons are meaningful across runs.
- **Cover masked-position regimes.** Benchmark unmasked input for dense parity, representative partial masking, and fully masked input. Reuse the existing length/case approach where practical, but cap or skip large cases when masked-array allocation would make runs impractical.
- **Test the first-occurrence rule explicitly.** Add cases where the first array element is masked and where a value first appears masked but later appears unmasked; expected alphabets must contain only later unmasked values in their unmasked first-appearance order.

## Risks / Trade-offs

- **[Benchmark runtime and memory]** Very large masked arrays can be expensive to construct and compress → apply ASV skip rules and retain small/medium cases for all mask regimes.
- **[Random benchmark noise]** Random input generation can affect repeatability → generate data during setup and use stable seeded generators or deterministic patterns for comparable cases.
- **[Type annotation compatibility]** Older supported Python versions may not support newer typing syntax → use annotations compatible with the project’s declared Python support and existing NumPy conventions.
- **[Documentation directive resolution]** MkDocs autodoc may resolve submodule symbols differently from top-level functions → validate the generated reference page and use the same directive style as existing references.
