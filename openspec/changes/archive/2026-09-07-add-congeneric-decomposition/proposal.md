## Why

FOA's documented theory (`docs/fundamentals/congeneric_decomposition/`, `docs/fundamentals/partials_and_congenerics/`) defines *congeneric decomposition* — splitting a sequence into a stack of congeneric sequences (one per alphabet symbol, all other positions empty) — as a first-class analytical technique, reversible and order-preserving. No code implements it today: `foapy.partials` provides the mechanics for a single partial/congeneric sequence (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`), but nothing produces the decomposition itself or runs the pipeline across all of a sequence's congeneric rows at once. Without it, per-symbol interval analysis across a full sequence requires manually looping and re-deriving the congeneric rows by hand.

## What Changes

- Add a new `foapy.congenerics` package implementing the forward decomposition and the full analysis pipeline over it:
  - `sequences(S)` — decomposes `S` into `CS`, an `(m, l)` masked matrix; row `j` holds the `j`-th alphabet symbol (first-appearance order) at its original positions, `-` (masked) elsewhere.
  - `alphabet(CS)` — the `(m,)` array of row labels: row `j`'s single non-masked value, per the Alphabet of Congeneric sequences definition. Takes `CS` (the output of `sequences`) directly, not `S`.
  - `order(CS, return_alphabet=False)` — `(m, l)` masked matrix; every non-masked position is `0`, per the Congeneric Order definition. Takes `CS` directly, not `S` — the result is fully determined by `CS`'s mask alone. When `return_alphabet=True`, also returns `alphabet(CS)`, mirroring `foapy.core.order`/`foapy.partials.order`'s own `return_alphabet` convention; `(order, alphabet)` together are sufficient to reconstruct `CS`.
  - `intervals_chains(CS, binding, chain_mode)` — `(m, l)` masked matrix; row `j` is `foapy.partials.intervals_chain(CS[j], binding, chain_mode)`. Takes `CS` directly, not `S` — only `CS`'s mask matters, so `CS` may be either `sequences()`'s or `order()`'s output.
  - `intervals_tuples(chains, binding, tuple_mode)` — `(m, x)` ndarray; row `j` is `foapy.partials.intervals_tuple` on `chains`'s `j`-th row, right-padded with `0` to `x = max` tuple length across rows. Takes `chains` — `intervals_chains()`'s output — directly; `chain_mode` is no longer a separate parameter here since it's already baked into `chains`'s values, and `binding` must match the binding used to produce `chains`.
  - `intervals_distributions(tuples)` — `(m, y)` ndarray; takes `tuples`, the zero-padded output of `intervals_tuples()`, directly. Row `j` is `foapy.core.intervals_distribution` applied to the nonzero values in `tuples[j]`, right-padded with `0` to `y = max` interval value across **all** rows (shared width, so columns are comparable across rows). The binding, chain mode, and tuple mode are already represented in `tuples`, so they are not separate parameters.
- The public API chains stage-to-stage instead of each stage independently recomputing from `S`: only `sequences(S)` takes the raw source sequence. `alphabet`, `order`, and `intervals_chains` take `CS` (`sequences()`'s output, or — for `order`/`intervals_chains`, which only depend on the mask — `order()`'s output too); `intervals_tuples` takes `intervals_chains()`'s output; and `intervals_distributions` takes `intervals_tuples()`'s output. A caller building the full pipeline computes `CS = sequences(S)` once and threads each stage's output into the next, so no stage recomputes an earlier stage's work.
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
