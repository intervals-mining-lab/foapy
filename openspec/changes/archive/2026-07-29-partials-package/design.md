## Context

`foapy.core` operates on dense sequences, while `foapy.ma` provides masked-array helpers whose interval calculations compress masked positions. Partial-sequence analysis needs a third behavior: masked positions must be excluded from alphabet and order assignment but remain part of the positional coordinate system used for intervals.

The change adds a small subpackage under `src/foapy/partials/`, reusing established `foapy.core` algorithms where dense behavior is equivalent and following the lazy submodule pattern used by `foapy.ma`.

## Goals / Non-Goals

**Goals:**

- Provide `order`, `alphabet`, `intervals_chain`, and `intervals_tuple` for 1-D partial sequences.
- Preserve masks and source-position alignment in masked outputs.
- Count masked gaps in interval distances.
- Preserve parity with `foapy.core` when inputs contain no masked positions.
- Cover edge cases and public API behavior with automated tests.

**Non-Goals:**

- Adding `intervals_distribution` or characteristic functions to `foapy.partials`.
- Changing existing `foapy.core` or `foapy.ma` semantics.
- Hoisting partials functions into the top-level `foapy` namespace.
- Adding runtime dependencies.

## Decisions

### Use 1-D masked outputs aligned to the input

`partials.order()` returns one alphabet index per source position, unlike `foapy.ma.order()`’s occurrence matrix. All positional transformations retain the original length except redundant tuple mode, which appends complementary trailing values.

### Auto-wrap plain inputs

Each function begins by converting its input with NumPy masked-array semantics. Plain lists and arrays therefore behave as fully unmasked inputs without requiring callers to construct a masked array explicitly.

### Compute intervals from the raw masked sequence

`partials.intervals_chain()` accepts the original masked sequence, not the order output. It collects non-masked values and their original indices, computes repeated-symbol distances in those original coordinates, and maps results back to the full array. This makes a gap between positions `i` and `j` contribute to the distance `j - i`.

### Reuse dense algorithms only after removing gaps

`order()` and `alphabet()` can delegate their compressed values to the corresponding core behavior, then map order values back to unmasked source positions. `intervals_tuple()` uses compressed-chain boundary detection for lossy mode and dense complementary-boundary calculation for redundant mode, while retaining the partial mask contract.

### Preserve invalid-input behavior and enum contracts

Multi-dimensional sequence inputs raise `Not1DArrayException`. Binding, chain-mode, and tuple-mode values are validated against the existing `foapy` enum constants and invalid values raise `ValueError`.

### Public API is submodule-only

`foapy.partials` is added to the package’s lazy submodule loader. Its four functions are exported from `foapy.partials.__init__`, but no function is added directly to `foapy.*`.

## Risks / Trade-offs

- [Risk] Stable grouping and remapping for arbitrary NumPy dtypes can diverge from core behavior → Mitigation: reuse core ordering where possible and use stable sorting for interval grouping.
- [Risk] Redundant mode changes output length and no longer maps one-to-one to source positions → Mitigation: append only the complementary trailing values and document that these appended positions are unmasked and synthetic.
- [Risk] The source material inconsistently describes `intervals_chain()` as accepting a partial order in one user-story paragraph → Mitigation: make the normative contract explicit: it accepts the raw masked sequence; use the original-position example in tests and documentation.
- [Risk] Existing core/ma behavior could regress through package wiring → Mitigation: run the full test suite and add explicit zero-gap parity tests.
