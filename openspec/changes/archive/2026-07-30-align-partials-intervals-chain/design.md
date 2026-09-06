## Context

`foapy.core.intervals_chain` and `foapy.partials.intervals_chain` intentionally share the same three-argument API and binding/chain-mode model. The partials variant additionally accepts masked input, preserves the full source shape, and computes distances in source coordinates. The current implementation already has focused functional tests, but scalar validation differs, the partials API is absent from the published reference navigation, and no benchmark measures its masked-array workload.

## Goals / Non-Goals

**Goals:**

- Normalize partials dimensionality validation with the core one-dimensional contract.
- Make the partials API reference and examples discoverable through the built documentation.
- Benchmark partials intervals-chain time and peak memory using representative dense and gapped inputs, both bindings, and both chain modes.
- Preserve all existing masked-gap semantics and dense parity with core.

**Non-Goals:**

- Changing the core or `foapy.ma` implementations.
- Changing the partials return representation or its positional gap semantics.
- Adding a new public enum, dependency, or benchmark framework.

## Decisions

1. **Use the same exact dimensionality check as core.** Change the partials check from `ar.ndim > 1` to `ar.ndim != 1`. This makes scalar input raise `Not1DArrayException` before `len()` is called, while retaining rejection of multidimensional arrays.

2. **Add a generated API page rather than duplicating the full contract.** Create `docs/references/partials/intervals_chain.md` using the project's existing autodoc syntax and add it under the existing `foapy.partials` navigation. Keep the detailed gap comparison in the function docstring and/or fundamentals documentation, with runnable examples covering dense and masked input.

3. **Reuse the existing ASV benchmark conventions.** Add a `bench_partials_intervals_chain.py` suite with time and peak-memory methods, the existing 100/10,000/1,000,000 lengths, representative partial datasets, both bindings, and both chain modes. Generate masked inputs during setup so setup cost is excluded from timed calls.

4. **Test behavior at both API and matrix levels.** Add a scalar exception test and retain the existing dense parity, mask preservation, gap-distance, binding, and mode tests. The benchmark suite itself should be importable and expose the complete parameter matrix; performance thresholds are not part of the functional test contract.

## Risks / Trade-offs

- [Risk] Large masked arrays may make the 1,000,000-element worst-case benchmark slow or memory-intensive → Mitigation: follow the existing skip/quick-benchmark conventions and use the same timeout/skip policy as the core suite.
- [Risk] Documentation examples can drift from implementation behavior → Mitigation: use small examples that mirror existing tests and include them in documentation checks where supported.
- [Risk] Changing scalar errors could affect callers relying on the incidental `TypeError` → Mitigation: this is a documented-contract correction; callers should catch the library's dimensionality exception instead.

## Migration Plan

1. Update the partials dimensionality check and add the regression test.
2. Add the API reference, navigation entry, and examples.
3. Add and run the partials benchmark suite, then run the focused and full test suites.
4. Rollback is limited to reverting the change; no data or external service migration is required.

## Open Questions

- Whether the partials benchmark should use only masked inputs or include a no-mask baseline; the design currently includes both through representative partial datasets and a dense case for direct comparison.
