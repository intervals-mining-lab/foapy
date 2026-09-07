## Context

FOA's theory documents (`docs/fundamentals/congeneric_decomposition/`, `docs/fundamentals/partials_and_congenerics/*/congeneric.md`) define congeneric decomposition mathematically but no code implements it. `foapy.partials` already implements every single-sequence primitive the decomposition's rows need (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`, and `foapy.core.intervals_distribution` for the final stage). The new `foapy.congenerics` package is a thin orchestration layer: decompose once, then map the existing `foapy.partials` primitives across the decomposition's rows.

Key structural fact from the math (`docs/fundamentals/congeneric_decomposition/sequences.md`): given `alphabet(S)` of size `m` and `order(S)` (values `0..m-1`, masked at gaps), row `j` of the decomposition is fully determined — `CS[j, i] = S[i]` where `order(S)[i] == j`, else masked. No new algorithmic work is needed for the decomposition itself beyond a scatter into an `(m, l)` masked matrix.

## Goals / Non-Goals

**Goals:**
- Implement `foapy.congenerics.sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, `intervals_distributions`.
- Keep `intervals_chains`/`intervals_tuples`/`intervals_distributions` independent: each takes the original sequence `S`, not another `congenerics.*` call's output — matching `foapy.core`/`foapy.partials` convention (see D2). `alphabet`/`order` instead take `CS` directly (see D2.1) — they're pure functions of the decomposition itself, per the math's own `alphabet_c(CS)`/Congeneric Order notation.
- Preserve correctness parity: row `j`'s result for any stage MUST equal calling the corresponding `foapy.partials`/`foapy.core` function directly on that row in isolation.

**Non-Goals:**
- Inverse reconstruction (`CS` → `S`). Deferred to a separate change.
- New enums, exceptions, or masked-array primitives — this package only orchestrates existing ones.
- Performance optimization beyond straightforward vectorization; benchmarks establish a baseline, they do not drive algorithmic changes in this change.

## Decisions

### D1: `sequences()` computed via `partials.order`, not independently

`sequences(S)` calls `foapy.partials.order(S, return_alphabet=True)` to get `(order, alphabet)`, then scatters: for each `j`, row `j`'s mask is `order != j` (also masking original gaps), and row `j`'s data is `S` where unmasked. This reuses the already-tested first-appearance/gap semantics instead of reimplementing them.

**Alternative considered**: compute alphabet/order membership directly from `S` inside `sequences()`. Rejected — it would duplicate `foapy.partials.order`'s logic and risk drifting from its gap-handling semantics.

### D2: Downstream stages take raw `S`, internally recompute `CS = sequences(S)`

**Superseded by D2.2.** Original decision: `order()`, `intervals_chains()`, etc. all accept `S` and call `sequences(S)` as their first step, mirroring `foapy.partials.intervals_chain`'s explicit contract ("pass the original sequence, not the order output"). This kept every `congenerics.*` function callable independently and consistent with the rest of the codebase's convention, at the cost of recomputing `sequences(S)` on each call.

**Alternative considered at the time**: accept a precomputed `CS` matrix to avoid recomputation across chained calls. Rejected per explicit user decision — independent-input consistency with the existing pipeline convention was preferred over the reuse optimization. D2.2 later reversed this once the actual recomputation cost (and the fact that most of these stages don't need `CS`'s values, only its mask) became the higher-priority concern.

### D2.1: `alphabet`/`order` are carved out of D2 — they take `CS` directly

Reversing part of D2 per explicit user decision: `alphabet(CS)` and `order(CS)` take the decomposition matrix itself, not `S`. Both are pure functions of `CS`'s shape/mask alone (`alphabet` reads each row's one non-masked value; `order` reads `CS`'s mask directly) — computing them from `S` was equivalent to `alphabet_or_order(sequences(S))` in every case anyway, just with the `sequences()` call hidden inside the function instead of made explicit by the caller. Taking `CS` directly:
- matches the math's own notation (`alphabet_c(CS)`, Congeneric Order defined over `CS`'s rows, not over `S`), and
- avoids a wasted `sequences(S)` recomputation when a caller already has `CS` (e.g., from a prior `sequences()`/`intervals_chains()` call) and only wants its labels or trivial order.

`order(CS, return_alphabet=False)` additionally accepts a `return_alphabet` parameter, mirroring `foapy.core.order`/`foapy.partials.order`'s existing convention: when `True`, it returns `(order, alphabet)` where `alphabet` is `foapy.congenerics.alphabet(CS)`. This was added so `order`'s call signature stays consistent with `core.order`/`partials.order` at every pipeline layer, and because it enables reconstructing `CS` from `(order, alphabet)` alone (row `j`'s values are `alphabet[j]` broadcast across the row, kept wherever `order`/`CS` is non-masked) — documented as a worked example in `order`'s docstring.

**Result at this point**: `sequences`, `alphabet`, `order` operate on/from `CS`; `intervals_chains`, `intervals_tuples`, `intervals_distributions` still operated on `S` per D2, unchanged so far. D2.2 revisits that split.

### D2.2: `intervals_chains`/`intervals_tuples` converge on the D2.1 pattern — they take upstream output directly, not `S`

Extending D2.1's rationale further per explicit user decision, in two steps:

1. **`intervals_chains(CS, binding, chain_mode)`** (was `intervals_chains(S, binding, chain_mode)`): `_chain_work_frame`'s computation only ever reads `~ma.getmaskarray(CS)` — it never touches `CS`'s actual values (every non-masked value in a congeneric row is interchangeable for this purpose). So `CS` may be either `foapy.congenerics.sequences()`'s or `foapy.congenerics.order()`'s output; passing raw `S` and recomputing `sequences(S)` inside was pure waste once this was noticed.
2. **`intervals_tuples(chains, binding, tuple_mode)`** (was `intervals_tuples(S, binding, chain_mode, tuple_mode)`): once `intervals_chains` no longer recomputes `CS`, `intervals_tuples` can take its output (`chains`) directly instead of independently recomputing the whole chain from `CS`/`S`. This also makes `chain_mode` disappear from `intervals_tuples`'s own signature — the chain-mode-specific boundary values are already baked into `chains`'s data, and the mask-derived bookkeeping `intervals_tuples` still needs (first/last occurrence per row) depends only on `chains`'s mask, not on `chain_mode` — so passing `chain_mode` again would be redundant. This finally matches `foapy.partials.intervals_tuple(chain, binding, tuple_mode)`'s own signature exactly (no `chain_mode` there either, for the identical reason).

`intervals_distributions(CS, binding, chain_mode, tuple_mode)` keeps all four parameters (it's the one place `chain_mode` is still needed, to build the chain in the first place) but now takes `CS` instead of `S`, and internally composes `chains = intervals_chains(CS, binding, chain_mode)` then `intervals_tuples(chains, binding, tuple_mode)` rather than recomputing anything itself.

**Result (final)**: only `sequences(S)` takes the raw source sequence. Every other `congenerics.*` function takes the previous stage's output directly — `alphabet`/`order`/`intervals_chains` take `CS`, `intervals_tuples` takes `intervals_chains`'s output, `intervals_distributions` takes `CS` and chains the remaining two stages internally. A caller building the full pipeline computes `CS = sequences(S)` once and threads it (or its downstream outputs) through every subsequent call — no stage recomputes an earlier stage's work.

### D3: Fully vectorized `(m, l)`-native implementation — no per-row Python loop

Superseded an earlier version of this decision (originally: loop over `foapy.partials`/`foapy.core` primitives per row). Every stage is now a batched numpy computation across all `m` rows at once:

- `order(CS)`: no computation at all — every non-masked value is `0` by the Congeneric Order definition, so the result is `ma.masked_array(np.zeros(CS.shape), mask=CS.mask)` (see D2.1 for why this takes `CS` rather than `S`, and for the later-added `return_alphabet` parameter).
- `intervals_chains(CS, binding, chain_mode)`: a congeneric row has exactly one non-empty symbol, so its interval chain reduces to "distance to the previous non-masked column in this row" — computed for every row at once via a shifted running maximum along columns (`numpy.maximum.accumulate(shifted, axis=1)`) instead of calling `foapy.partials.intervals_chain` per row. A private helper `_chain_work_frame` computes this in "work frame" column order (natural for `binding.start`, column-reversed for `binding.end`, matching `foapy.partials`' internal processing frame); its mask-only bookkeeping (`_occurrence_positions`: previous/first/last occurrence per row) is factored out and shared with `intervals_tuples` below (see D2.2 — takes `CS` directly, not `S`, since this bookkeeping only ever reads `CS`'s mask).
- `intervals_tuples(chains, binding, tuple_mode)`: takes `intervals_chains()`'s output directly (see D2.2) and recomputes only the mask-derived bookkeeping it needs (`_occurrence_positions` on `chains`'s mask, converted to work-frame order) — a position is "boundary" iff it's a row's first occurrence in work-frame order, which is exactly what `foapy.partials.intervals_tuple`'s lossy-mode check (`work value > work position`) detects. Ragged per-row results (variable count of kept entries before padding) are packed left and zero-padded via a single vectorized cumulative-count scatter (`_pack_rows`: `numpy.cumsum` for destination columns, then one fancy-indexed assignment) rather than building per-row Python lists.
- `intervals_distributions(CS, binding, chain_mode, tuple_mode)`: composes `intervals_chains(CS, binding, chain_mode)` then `intervals_tuples(chains, binding, tuple_mode)` (see D2.2), then a single vectorized scatter-add (`numpy.add.at` over every row's real tuple entries at once) computes all `m` row-histograms simultaneously, instead of one `foapy.core.intervals_distribution` call per row.

**Why this replaces the original decision**: the initial "loop and delegate" approach optimized for correctness-by-construction (reusing already-tested `foapy.partials`/`foapy.core` logic) over performance, on the assumption that `m` (alphabet size) is usually small enough that per-row Python overhead doesn't matter. The user explicitly asked to remove the loops in favor of numpy-only vectorized code. Before replacing any function, the vectorized formulas were derived by hand from `foapy.partials`' algorithms (a congeneric row is a single-group special case of the general multi-symbol algorithm) and verified against the original loop-based implementation across ~96,000 randomized trials (all `binding` × `chain_mode` × `tuple_mode` combinations, masked and unmasked inputs, empty/edge cases) before being adopted — zero mismatches. Test suites for `intervals_tuples`/`intervals_distributions` were also broadened to actually exercise `tuple_mode.lossy`/`redundant` (a pre-existing gap surfaced by this rewrite: only `tuple_mode.normal` had test coverage before).

**Trade-off accepted**: the vectorized code is meaningfully harder to read than "call the tested primitive per row" — the tuple/distribution stages in particular duplicate algorithmic knowledge that previously lived only in `foapy.partials`/`foapy.core` (see the risk below).

### D4: Padding conventions for ragged stages

- `intervals_tuples`: width `x = max` tuple length across the `m` rows; shorter rows right-padded with `0`. Safe because real interval values are always `>= 1` (per `foapy.partials.intervals_chain`'s contract), so `0` is unambiguous filler.
- `intervals_distributions`: width `y = max` interval value across **all** rows' tuples (a single shared denominator, not a per-row max), so column `i` means "count of interval value `i+1`" consistently across every row. Rows whose own max interval is smaller are right-padded with `0`, which is also the correct semantic value (zero occurrences), not just a filler.

### D5: Module layout mirrors `foapy.partials`

`src/foapy/congenerics/` with one module per function (`_sequences.py`, `_alphabet.py`, `_order.py`, `_intervals_chains.py`, `_intervals_tuples.py`, `_intervals_distributions.py`) and an `__init__.py` re-exporting the six names — same pattern as `src/foapy/partials/__init__.py`.

### D6: Benchmark scope — `sequences`, `order`, `intervals_chains` only

ASV benchmarks (`benchmarks/benchmarks/bench_congenerics_*.py`) are added for `sequences`, `order`, and `intervals_chains`, mirroring exactly which `foapy.partials` functions got benchmarks (`order`, `alphabet`, `intervals_chain` — `intervals_tuple` was left unbenchmarked there too). `alphabet()` is a pure delegate to `foapy.partials.alphabet` with no added cost, so a separate benchmark would only re-measure existing coverage. `intervals_tuples`/`intervals_distributions` are left unbenchmarked in this change for the same reason `foapy.partials.intervals_tuple` was: consistent with existing project convention, not a decision specific to congenerics.

Length/case parameters are scaled down from `foapy.partials`' benchmarks because congenerics' cost is `O(m*l)` (matrix-shaped), not `O(l)`: the `Normal` case (`m ≈ 0.2*l`) and `Worst` case (`m = l`, one row per unique element) are skipped at the largest benchmarked length to avoid multi-gigabyte matrices; `Best` (`m = 1`) and `DNA` (`m = 4`, fixed) stay cheap at any length and are benchmarked at the full range.

**Alternative considered**: reuse `foapy.partials`' exact length range (`up to 50,000,000`). Rejected — at that length, `Normal`/`Worst` cases would allocate matrices with `10^12`+ elements, which is not representative of realistic congenerics usage and would make the benchmark suite impractically slow/memory-heavy.

## Risks / Trade-offs

- **[Risk, resolved by D2.2]** Recomputing `sequences(S)` inside every `congenerics.*` call was `O(m*l)` extra work per call when a caller invoked multiple stages on the same `S`, under D2's original "independent `S` input" contract. → **Resolution**: D2.2 changed `intervals_chains`/`intervals_tuples`/`intervals_distributions` to take the previous stage's output directly instead of `S`, eliminating the redundant recomputation for callers building the full pipeline. The residual cost — `intervals_distributions` still recomputes `intervals_chains`/`intervals_tuples` internally on each call — is inherent to composing three independent stages, not a recomputation of earlier work.
- **[Risk]** `intervals_distributions`' global (cross-row) padding width means adding/removing a row (e.g., a different input `S`) changes the meaning of "row `j`, column `i`" between calls, which could surprise callers comparing distributions across different `S` inputs. → **Mitigation**: document explicitly that the padded width is only stable within a single call's output, not across calls with different `S`.
- **[Risk]** `order()`'s output is mathematically trivial (all non-masked values are `0`). → **Mitigation**: kept per explicit user decision for pipeline-stage consistency; documented as returning the trivial Congeneric Order rather than treated as a bug.
- **[Risk]** (D3, vectorized rewrite) `intervals_tuples`/`intervals_distributions` now duplicate algorithmic knowledge from `foapy.partials.intervals_tuple`/`foapy.core.intervals_distribution` (the boundary-detection and redundant-mode trailing-value formulas) instead of delegating to them — a future change to those algorithms' semantics would need a matching change here, with no shared code to keep them in sync. → **Mitigation**: verified bit-for-bit against the original delegating implementation across ~96,000 randomized trials before the rewrite was adopted; test suites now exercise all three `tuple_mode` values (previously only `normal` had coverage) to catch future divergence.

## Open Questions

None outstanding — all resolved during exploration (see proposal.md and conversation history): ragged-stage padding, `order()` inclusion, and the final input-chaining contract (D2.2 — each stage takes the previous stage's output, not `S`) are settled decisions, not open items.
