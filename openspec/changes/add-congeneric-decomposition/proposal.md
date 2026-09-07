## Why

FOA's documented theory (`docs/fundamentals/congeneric_decomposition/`, `docs/fundamentals/partials_and_congenerics/`) defines *congeneric decomposition* — splitting a sequence into a stack of congeneric sequences (one per alphabet symbol, all other positions empty) — as a first-class analytical technique, reversible and order-preserving. No code implements it today: `foapy.partials` provides the mechanics for a single partial/congeneric sequence (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`), but nothing produces the decomposition itself or runs the pipeline across all of a sequence's congeneric rows at once. Without it, per-symbol interval analysis across a full sequence requires manually looping and re-deriving the congeneric rows by hand.

## What Changes

- Add a new `foapy.congenerics` package implementing the forward decomposition and the full analysis pipeline over it:
  - `sequences(S)` — decomposes `S` into `CS`, an `(m, l)` masked matrix; row `j` holds the `j`-th alphabet symbol (first-appearance order) at its original positions, `-` (masked) elsewhere.
  - `alphabet(S)` — the `(m,)` array of row labels (equivalent to `foapy.partials.alphabet(S)`).
  - `order(S)` — `(m, l)` masked matrix; row `j` is the congeneric order of `CS[j]` (non-empty positions are `1`, per the Congeneric Order definition).
  - `intervals_chains(S, binding, chain_mode)` — `(m, l)` masked matrix; row `j` is `foapy.partials.intervals_chain(CS[j], binding, chain_mode)`.
  - `intervals_tuples(S, binding, chain_mode, tuple_mode)` — `(m, x)` ndarray; row `j` is `foapy.partials.intervals_tuple` on the `j`-th chain (built with `chain_mode`), right-padded with `0` to `x = max` tuple length across rows. `chain_mode` is required alongside `tuple_mode` because they are independent axes in `foapy.partials` (`intervals_chain` takes `chain_mode`; `intervals_tuple` takes an already-built chain plus `tuple_mode`) — `tuple_mode` alone cannot select a chain.
  - `intervals_distributions(S, binding, chain_mode, tuple_mode)` — `(m, y)` ndarray; row `j` is `foapy.partials.intervals_distribution` on the `j`-th tuple, right-padded with `0` to `y = max` interval value across **all** rows (shared width, so columns are comparable across rows).
- Every function takes the original 1-D sequence `S` as input (not another `congenerics.*` function's output), deriving `CS = sequences(S)` internally — matching the existing `foapy.core`/`foapy.partials` convention where each stage is called independently on the source sequence.
- Inverse reconstruction (`CS` → `S`) is explicitly **out of scope** for this change; it will be proposed separately.

## Capabilities

### New Capabilities
- `congeneric-decomposition`: decomposing a sequence into its congeneric-sequence matrix and running the order/intervals-chain/intervals-tuple/intervals-distribution pipeline across all rows at once.

### Modified Capabilities
_None._ This is additive; `foapy.partials` and `foapy.core` are consumed as-is, not changed.

## Impact

- New package: `src/foapy/congenerics/` (mirrors the `src/foapy/partials/` layout: one module per function, `__init__.py` re-exporting the public API).
- New tests: `tests/test_congenerics/` (mirrors `tests/test_partials_*.py` conventions, using `CharacteristicsTest`-style batch assertions where applicable).
- Depends only on `foapy.partials` (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`, `intervals_distribution`) and `foapy.core`'s `binding`/`chain_mode`/`tuple_mode` enums — no new runtime dependency (still `numpy >= 1.20` only).
- Docs: fills in the "Add example of congeneric decomposition code" TODO in `docs/fundamentals/ideas/congeneric_decomposition.md`.
