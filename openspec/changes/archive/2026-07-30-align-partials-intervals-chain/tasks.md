## 1. Align dimensionality behavior

- [x] 1.1 Change `partials.intervals_chain` to reject normalized arrays whose dimensionality is not exactly one with `Not1DArrayException`.
- [x] 1.2 Add a regression test for scalar/0-D input and retain coverage for multidimensional input, invalid binding, and invalid chain mode.
- [x] 1.3 Run the focused core/partials intervals-chain and pipeline-consistency tests, confirming dense parity and existing masked-gap behavior remain unchanged.

## 2. Publish API documentation and examples

- [x] 2.1 Add `docs/references/partials/intervals_chain.md` using the project's autodoc reference format.
- [x] 2.2 Add the partials intervals-chain page to the `foapy.partials` section in `mkdocs.yml`.
- [x] 2.3 Add or update concise runnable examples covering dense input, masked gaps, output mask preservation, binding, and chain mode, and ensure the documented scalar/error behavior matches the implementation.
- [x] 2.4 Build or validate the documentation and confirm the new reference page is linked and renders successfully.

## 3. Add benchmark coverage

- [x] 3.1 Add `benchmarks/benchmarks/bench_partials_intervals_chain.py` with time and peak-memory suites for lengths 100, 10,000, and 1,000,000.
- [x] 3.2 Include representative dense and masked-gap datasets, both bindings, and both chain modes; apply the existing quick-benchmark skip/timeout conventions for the largest worst cases.
- [x] 3.3 Verify benchmark collection and run a quick benchmark smoke test, confirming calls target `foapy.partials.intervals_chain` and not core or `foapy.ma`.

## 4. Final verification

- [x] 4.1 Run the full test suite with coverage and confirm the changed partials implementation remains covered.
- [x] 4.2 Review the API comparison against `foapy.core.intervals_chain` and confirm proposal requirements, documentation, tests, and benchmark parameters are all satisfied.
