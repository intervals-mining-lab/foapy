## Context

The core and partial `alphabet` and `order` APIs already define a shared axis model: each complete orthogonal slice at a position on the selected axis is one sequence element, and the resulting order is one-dimensional. `intervals_chain` still contains a separate one-dimensional grouping implementation and rejects multidimensional arrays. The partial version additionally measures distances in the full positional domain so masked gaps count toward every boundary and occurrence distance.

The change spans the core and partial APIs, their validation behavior, documentation, tests, and benchmarks. It must preserve the optimized legacy one-dimensional paths restored during the preceding axis-factorization work.

## Goals / Non-Goals

**Goals:**

- Apply the established slice-as-element axis semantics to core and partial interval chains.
- Return one scalar interval per selected-axis position as a one-dimensional `numpy.intp` chain.
- Preserve all binding, boundary, cycle, and partial gap-distance semantics in selected-axis coordinates.
- Reuse existing order/factorization and one-dimensional interval logic instead of creating another multidimensional equality implementation.
- Preserve legacy one-dimensional behavior and performance characteristics.
- Cover axis behavior with tests, documentation, and deterministic ASV benchmarks.

**Non-Goals:**

- Adding `axis` to `intervals_tuple`; it consumes the one-dimensional chain produced here.
- Changing `foapy.congenerics.intervals_chains`, whose two-dimensional shape has domain-specific row-per-symbol semantics.
- Returning an input-shaped multidimensional interval array.
- Changing supported dtypes, binding values, chain modes, public exports, or dependencies.
- Optimizing the multidimensional factorization machinery beyond what `order` already provides.

## Decisions

### 1. Match the existing keyword-only axis contract

Both functions will expose `intervals_chain(X, binding, chain_mode, *, axis=None)`. An integer axis selects the sequence dimension and each complete orthogonal slice becomes one element. The result is one-dimensional with length `X.shape[axis]`, because a slice represents one sequence position and therefore has one interval value.

This matches `order`, keeps the output directly consumable by `intervals_tuple`, and avoids an ambiguous broadcast of one interval across every scalar in a slice. Returning an input-shaped array was rejected because it would duplicate values and break the current interval pipeline.

### 2. Reduce multidimensional equality to order codes

For multidimensional dense input, core `intervals_chain` will obtain the one-dimensional equality pattern from the established axis-aware order/factorization path, then apply the existing one-dimensional interval algorithm to those integer codes. Interval chains depend only on which sequence positions contain equal elements, not on the original values or the first-appearance labels assigned to equality classes.

The implementation should extract or reuse a private one-dimensional interval kernel so the public function does not need recursive validation. Directly teaching the interval algorithm to compare arbitrary slices was rejected because it would duplicate dtype, hashing, signed-zero, NaN, collision, and axis-placement logic already centralized in factorization.

### 3. Keep one-dimensional inputs on the existing direct path

When the normalized input is one-dimensional, including explicit `axis=0` or `axis=-1`, the function will validate the axis and run the current value-sorting implementation directly. It will not first call multidimensional factorization or `order`.

This preserves the legacy allocation profile and avoids the extra alphabet/inverse work that previously caused measurable one-dimensional regressions.

### 4. Reuse partial order semantics for multidimensional masks

For multidimensional partial input, `foapy.partials.order(X, axis=axis)` will provide a masked one-dimensional equality pattern. It already enforces that each slice is wholly present or wholly masked and excludes masked data from factorization. The existing partial interval kernel will process that masked order while using the full selected-axis length and original gap positions.

Consequently, gap slices remain masked in the result and count toward distances, including leading/trailing boundary distances and cyclic wrap-around. Implementing separate slice-mask validation inside `intervals_chain` was rejected because it could drift from partial alphabet/order behavior.

### 5. Preserve validation and error behavior

Existing binding and chain-mode validation remains authoritative. Axis normalization will reuse the same helper as alphabet/order: multidimensional input without an axis raises `Not1DArrayException`, negative axes normalize normally, out-of-range axes raise NumPy's axis error, and scalar input raises `Not1DArrayException`. Legacy validation order should remain stable where practical.

### 6. Test through invariants and explicit examples

Core axis tests will cover rows, columns, all axes of a three-dimensional input, both bindings, both chain modes, negative and invalid axes, empty sequence axes, structurally empty slices, and legacy one-dimensional dispatch. A central invariant is:

`intervals_chain(X, binding, chain_mode, axis=a) == intervals_chain(order(X, axis=a), binding, chain_mode)`.

Partial tests will cover plain-input parity with core, whole-slice gaps, gap-aware boundary and cycle distances, mixed-mask rejection, fully masked and empty inputs, and axis validation. Benchmark data will be deterministic and will exercise multiple sequence lengths, slice widths, axis placements, and partial mask states while retaining existing one-dimensional suites.

## Risks / Trade-offs

- **[Multidimensional work includes factorization plus interval grouping]** Axis inputs may perform two grouping/sorting stages. → Start with the shared, correctness-oriented design, benchmark it explicitly, and optimize only with evidence while retaining the same contract.
- **[One-dimensional performance regression]** Routing legacy inputs through order would add unnecessary work. → Keep a dedicated direct path and add dispatch tests and benchmark coverage.
- **[Core and partial axis rules drift]** Duplicated normalization or mask handling could produce inconsistent behavior. → Reuse the existing factorization and partial-order helpers and assert dense parity.
- **[Import coupling]** Reusing order from interval modules can introduce accidental package-level cycles. → Import concrete internal modules or lower-level helpers rather than public package initializers.
- **[Noisy benchmark comparisons]** Historical GitHub-runner results can report false regressions. → Use deterministic inputs and interpret base/head performance only when both revisions are measured on the same runner.

## Migration Plan

This is backward-compatible and requires no data migration. Add the optional parameter and internal dispatch, then tests, documentation, and benchmarks. Rollback consists of reverting the axis dispatch and related artifacts; existing three-argument callers remain unaffected throughout.

## Open Questions

None. The scope includes both core and partial interval chains and intentionally leaves tuple and congeneric APIs unchanged.
