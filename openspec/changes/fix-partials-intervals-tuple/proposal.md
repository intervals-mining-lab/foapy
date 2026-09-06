## Why

`foapy.partials.intervals_tuple` currently returns a `numpy.ma.MaskedArray`, unlike `foapy.core.intervals_tuple`, which returns a plain `numpy.ndarray`. A "tuple" of intervals is, by definition, position-agnostic — the math in `docs/fundamentals/partials_and_congenerics/intervals_distribution.md` defines the distribution as excluding gap (`-`) positions entirely (`ID_p(i) = ID(i) | IC_p(i) ∉ {-}`). Carrying masked filler forward from `intervals_chain` (which is rightly position-preserving, since gap distance matters for measuring intervals) into `intervals_tuple` is the wrong representation for the final flat output, and it also leaves `redundant` mode mixing two different element orderings for `binding.end` in the same result. Fixing this now, before any downstream consumer exists, avoids baking the wrong contract into `foapy.partials`.

## What Changes

- **BREAKING**: `foapy.partials.intervals_tuple` now returns a plain `numpy.ndarray` (dtype `numpy.intp`) in every mode, never a `numpy.ma.MaskedArray`. Masked/gap entries are dropped from the result rather than carried forward as masked filler.
- **BREAKING**: `tuple_mode.normal` now returns `chain.compressed()` instead of a same-length masked copy of the chain.
- **BREAKING**: `tuple_mode.lossy` now delegates to `foapy.core.intervals_tuple` on the compressed chain, returning only the interior (non-boundary) values as a plain array. For `binding.end`, the result is now in core's own right-to-left order rather than being re-mapped to left-to-right source order.
- **BREAKING**: `tuple_mode.redundant` now returns `concatenate(work, trailing)` as a plain array (`work` = compressed chain, reversed for `binding.end`), fixing an ordering inconsistency where the current implementation computes trailing values in the reversed frame but concatenates them onto the original-order array.
- **BREAKING**: Empty or fully-masked input now returns `np.array([], dtype=np.intp)` for every mode, instead of a same-length fully-masked array.
- Add the missing documentation `intervals_chain` already has: runnable docstring examples, `docs/references/partials/intervals_tuple.md`, and a `mkdocs.yml` nav entry under `foapy.partials`.
- Rewrite `tests/test_partials_intervals_tuple.py` against the new `ndarray` contract.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `partials-package`: the "Partial interval tuple strategies" requirement changes from a mask-preserving `MaskedArray` contract to a plain `ndarray` contract, with per-mode semantics updated to drop gaps entirely instead of masking them.

## Impact

- `src/foapy/partials/_intervals_tuple.py` — full reimplementation of the return type and per-mode logic.
- `openspec/specs/partials-package/spec.md` — "Partial interval tuple strategies" requirement rewritten via spec delta.
- `tests/test_partials_intervals_tuple.py` — nearly every test rewritten to assert `ndarray` behavior instead of masked-array behavior.
- `docs/references/partials/intervals_tuple.md` (new file) and `mkdocs.yml` (nav entry) — documentation parity with `intervals_chain`.
- No impact on `foapy.characteristics.*` or `foapy.characteristics.ma.*` — confirmed no existing code imports or calls `foapy.partials.intervals_tuple` (or any other `foapy.partials` function), so this is a self-contained fix with no other downstream consumers today.
