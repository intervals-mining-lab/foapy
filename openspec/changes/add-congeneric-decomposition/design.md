## Context

FOA's theory documents (`docs/fundamentals/congeneric_decomposition/`, `docs/fundamentals/partials_and_congenerics/*/congeneric.md`) define congeneric decomposition mathematically but no code implements it. `foapy.partials` already implements every single-sequence primitive the decomposition's rows need (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`, and `foapy.core.intervals_distribution` for the final stage). The new `foapy.congenerics` package is a thin orchestration layer: decompose once, then map the existing `foapy.partials` primitives across the decomposition's rows.

Key structural fact from the math (`docs/fundamentals/congeneric_decomposition/sequences.md`): given `alphabet(S)` of size `m` and `order(S)` (values `0..m-1`, masked at gaps), row `j` of the decomposition is fully determined — `CS[j, i] = S[i]` where `order(S)[i] == j`, else masked. No new algorithmic work is needed for the decomposition itself beyond a scatter into an `(m, l)` masked matrix.

## Goals / Non-Goals

**Goals:**
- Implement `foapy.congenerics.sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, `intervals_distributions`.
- Keep every function's public contract independent: each takes the original sequence `S`, not another `congenerics.*` call's output — matching `foapy.core`/`foapy.partials` convention.
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

`order()`, `intervals_chains()`, etc. all accept `S` and call `sequences(S)` as their first step, mirroring `foapy.partials.intervals_chain`'s explicit contract ("pass the original sequence, not the order output"). This keeps every `congenerics.*` function callable independently and consistent with the rest of the codebase's convention, at the cost of recomputing `sequences(S)` on each call.

**Alternative considered**: accept a precomputed `CS` matrix to avoid recomputation across chained calls. Rejected per explicit user decision — independent-input consistency with the existing pipeline convention was preferred over the reuse optimization. Callers who need to avoid recomputation can call `sequences()` once and process rows with `foapy.partials.*` directly instead of the `congenerics.*` wrappers.

### D3: Fully vectorized `(m, l)`-native implementation — no per-row Python loop

Superseded an earlier version of this decision (originally: loop over `foapy.partials`/`foapy.core` primitives per row). Every stage is now a batched numpy computation across all `m` rows at once:

- `order(S)`: no computation at all — every non-masked value is `0` by the Congeneric Order definition, so the result is `ma.masked_array(np.zeros(CS.shape), mask=CS.mask)`.
- `intervals_chains(S, binding, chain_mode)`: a congeneric row has exactly one non-empty symbol, so its interval chain reduces to "distance to the previous non-masked column in this row" — computed for every row at once via a shifted running maximum along columns (`numpy.maximum.accumulate(shifted, axis=1)`) instead of calling `foapy.partials.intervals_chain` per row. A private helper `_chain_work_frame` computes this in "work frame" column order (natural for `binding.start`, column-reversed for `binding.end`, matching `foapy.partials`' internal processing frame) and is shared with the tuple/distribution stages below.
- `intervals_tuples(S, binding, chain_mode, tuple_mode)`: reuses `_chain_work_frame`'s per-row boundary flags (`is_first_work`) directly — a position is "boundary" iff it's a row's first occurrence in work-frame order, which is exactly what `foapy.partials.intervals_tuple`'s lossy-mode check (`work value > work position`) detects. Ragged per-row results (variable count of kept entries before padding) are packed left and zero-padded via a single vectorized cumulative-count scatter (`_pack_rows`: `numpy.cumsum` for destination columns, then one fancy-indexed assignment) rather than building per-row Python lists.
- `intervals_distributions(S, binding, chain_mode, tuple_mode)`: a single vectorized scatter-add (`numpy.add.at` over every row's real tuple entries at once) computes all `m` row-histograms simultaneously, instead of one `foapy.core.intervals_distribution` call per row.

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

- **[Risk]** Recomputing `sequences(S)` inside every `congenerics.*` call is `O(m*l)` extra work per call when a caller invokes multiple stages on the same `S`. → **Mitigation**: acceptable per D2's explicit "independent `S` input" contract; documented as a known cost, revisit only if profiling shows it matters.
- **[Risk]** `intervals_distributions`' global (cross-row) padding width means adding/removing a row (e.g., a different input `S`) changes the meaning of "row `j`, column `i`" between calls, which could surprise callers comparing distributions across different `S` inputs. → **Mitigation**: document explicitly that the padded width is only stable within a single call's output, not across calls with different `S`.
- **[Risk]** `order()`'s output is mathematically trivial (all non-masked values are `0`). → **Mitigation**: kept per explicit user decision for pipeline-stage consistency; documented as returning the trivial Congeneric Order rather than treated as a bug.
- **[Risk]** (D3, vectorized rewrite) `intervals_tuples`/`intervals_distributions` now duplicate algorithmic knowledge from `foapy.partials.intervals_tuple`/`foapy.core.intervals_distribution` (the boundary-detection and redundant-mode trailing-value formulas) instead of delegating to them — a future change to those algorithms' semantics would need a matching change here, with no shared code to keep them in sync. → **Mitigation**: verified bit-for-bit against the original delegating implementation across ~96,000 randomized trials before the rewrite was adopted; test suites now exercise all three `tuple_mode` values (previously only `normal` had coverage) to catch future divergence.

## Open Questions

None outstanding — all resolved during exploration (see proposal.md and conversation history): ragged-stage padding, `order()` inclusion, and the "independent `S` input" contract are settled decisions, not open items.
