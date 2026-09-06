## Why

`foapy.partials.intervals_chain` intentionally mirrors `foapy.intervals_chain` while preserving masked positions, but the two APIs are not fully aligned at their input boundary: scalar input produces a raw `TypeError` in the partials implementation instead of the library's documented `Not1DArrayException`. The partials function also lacks a published API-reference page and dedicated benchmark coverage, making its contract and performance harder to discover and compare with the core implementation.

## What Changes

- Make `foapy.partials.intervals_chain` reject scalar/0-D input with `Not1DArrayException`, matching the core API's one-dimensional input contract.
- Add a published `foapy.partials.intervals_chain` API reference with parameters, return type, masking/gap semantics, errors, and executable examples.
- Ensure the partials documentation explicitly compares its full-array positional distances with core and masked-array behavior.
- Add dedicated time and peak-memory benchmarks for `foapy.partials.intervals_chain`, including masked-gap workloads and the same representative sizes and mode combinations used by the core benchmark.
- Extend tests to cover scalar input, documentation examples/contracts, and the partials benchmark setup/matrix where appropriate.

## Capabilities

### New Capabilities

<!-- No new standalone capability is introduced; this change aligns an existing package API. -->

### Modified Capabilities

- `partials-package`: Require one-dimensional validation behavior consistent with the core intervals-chain API and maintain discoverable documentation/examples for `partials.intervals_chain`.

## Impact

- `src/foapy/partials/_intervals_chain.py` and `tests/test_partials_intervals_chain.py`.
- `docs/references/partials/`, `mkdocs.yml`, and partials fundamentals documentation.
- `benchmarks/benchmarks/` and benchmark result generation.
- The public behavior changes only for scalar/0-D partials input, which will raise the documented library exception instead of an incidental `TypeError`.
