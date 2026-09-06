## Context

`foapy.partials` provides four position-preserving primitives over masked sequences: `order`, `alphabet`, `intervals_chain`, `intervals_tuple`. `intervals_chain` is deliberately position-preserving — it returns a `MaskedArray` aligned to the source `X`, because gap positions still count toward interval distances (a gap between two occurrences of the same symbol increases the measured interval). `intervals_tuple` sits downstream of `intervals_chain` and applies a boundary-handling strategy (`normal` / `lossy` / `redundant`) to produce the final flat sequence of interval values — the thing characteristics eventually consume.

Today `intervals_tuple` inherited the `MaskedArray` representation from `intervals_chain` without needing to: it returns masked filler instead of dropping gaps, which contradicts both `foapy.core.intervals_tuple`'s contract (plain `ndarray`) and the math already documented in `docs/fundamentals/partials_and_congenerics/intervals_distribution.md` (`ID_p(i) = ID(i) | IC_p(i) ∉ {-}` — gaps are excluded from the distribution by definition, not masked within it).

No code in the repo currently imports `foapy.partials.intervals_tuple` (confirmed by grep across `characteristics/` and `characteristics/ma/`), so this is a self-contained fix with no other call sites to update.

## Goals / Non-Goals

**Goals:**
- `intervals_tuple` returns a plain `numpy.ndarray` (dtype `numpy.intp`) in every mode, matching `foapy.core.intervals_tuple`'s return contract.
- Gap/masked positions are dropped from the result entirely — never represented as masked filler.
- `lossy` and `redundant` remain correct in the presence of gaps (gap-adjusted distances, computed via real source positions where required).
- For `binding.end`, output ordering matches `foapy.core.intervals_tuple`'s own convention (right-to-left / reversed-frame) rather than being re-mapped back to left-to-right source order.
- Close the documentation gap between `intervals_chain` (has docstring examples + reference page + nav entry) and `intervals_tuple` (has none).

**Non-Goals:**
- Wiring `foapy.partials` into `foapy.characteristics` — no consumer exists yet, and this proposal does not add one.
- Changing `intervals_chain` or `order`/`alphabet` — their position-preserving `MaskedArray` contract is correct and untouched.
- Preserving backward compatibility with the current `MaskedArray`-returning behavior — this is an intentional breaking change to a function with no known external consumers.

## Decisions

### 1. Return type: plain `ndarray`, not `MaskedArray`

All three modes end by dropping masked positions and returning `np.ndarray` of dtype `np.intp`. This matches `core.intervals_tuple` byte-for-byte in shape/dtype semantics and lets `intervals_tuple`'s output be handed directly to anything written against `core`'s contract (e.g. `characteristics.*`), should that wiring happen later.

**Alternative considered**: keep `MaskedArray` but with all remaining positions unmasked (i.e. `ma.asarray(plain_result)`). Rejected — it adds ceremony (mask bookkeeping) for a type that's guaranteed to never have a `True` in its mask, and it doesn't match `core`'s type at all, which is the actual parity goal.

### 2. `normal` mode: `chain.compressed()`

`core.intervals_tuple`'s `normal` mode ignores `binding` entirely and returns the array unchanged. For partials, "unchanged" now means "the compressed chain" — dropping gaps is the only work `normal` needs to do, since gap-adjusted distances are already baked into the chain values by `intervals_chain`.

### 3. `lossy` mode: delegate to `core.intervals_tuple`

`core`'s boundary test (`value > local_index`, where `local_index` is the element's position within the array being tested) only ever needs the compressed chain and its local index — it never needs a real source position. This holds even with gaps, because gap-adjusted distances are already encoded in the chain values themselves: an interior (non-boundary) interval's value can never exceed the count of elements already seen locally, regardless of how many gaps sit between occurrences in the source. This was verified against `X = [_, C, T, C, _, G]`: compressed chain `[2, 3, 2, 6]`, and the local-index test correctly identifies index 2 (value `2`) as the sole interior interval — the same result the current position-aware implementation produces.

Given that, `lossy` becomes a direct call: `core.intervals_tuple(chain.compressed(), binding, tuple_mode.lossy)`. This is simpler than maintaining a parallel implementation, and it automatically inherits `core`'s ordering convention for `binding.end` (see Decision 4).

**Alternative considered**: keep the existing bespoke lossy implementation (computing boundary compressed-indices, then mapping back through `non_masked_idx` to preserve left-to-right source order). Rejected per Decision 4.

### 4. `binding.end` ordering: match `core`'s reversed-frame convention, not left-to-right source order

`core.intervals_tuple` handles `binding.end` by reversing the array once, running all its logic on the reversed view, and returning the result *without* mapping back to original order. The current partials implementation instead maps every result back through `non_masked_idx` to preserve left-to-right source order — a deliberate divergence from `core`, previously only asserted as sorted-multiset equality in tests (see `test_lossy_binding_end_no_mask_same_values_as_core`).

This proposal aligns partials with `core`'s convention exactly: for `binding.end`, both `lossy` (via delegation) and `redundant` (via explicit `work = compressed[::-1]`) return values in the same reversed frame `core` uses. This is a user-confirmed decision (see conversation): parity with `core`'s exact output, including order, was chosen over preserving left-to-right source order.

**Alternative considered**: keep left-to-right source order for both bindings, treating it as more intuitive for a position-preserving library. Rejected by explicit user choice — exact parity with `core` was preferred over the position-preserving-flavored ordering.

### 5. `redundant` mode: cannot delegate to `core`; must use real source positions and the true domain length

`core.intervals_tuple`'s `redundant` computes trailing (complementary boundary) distances using the array's own length (call it `m`) and local index. That is correct when there are no gaps, but wrong once gaps exist: the trailing distance is measured from the last occurrence of a symbol to the edge of the *true* domain, and that domain includes gap positions.

Verified with a concrete counterexample: `X = [_, C, T, C, _, G]`, true domain length `n_full = 6`, compressed chain `[2, 3, 2, 6]` (`m = 4`). Using `core`'s local-`m`-based formula gives trailing `[3, 2, 1]`. Using the true domain length (`n_full`) and each element's real source position gives trailing `[4, 3, 1]` — the correct, gap-aware answer (matching the same "distance to array edge" convention `intervals_chain`'s own boundary computation already uses).

So `redundant` keeps its current position-aware trailing computation (using `len(chain)` — the true source domain length — and real source positions via `non_masked_idx`), but:
- targets a plain-`ndarray` output instead of masked filler, and
- fixes an existing bug: today, trailing values are computed in the reversed frame for `binding.end` but concatenated onto the *original-order* compressed data, mixing two orderings in one output. The fix computes `work = compressed[::-1] if binding == end else compressed` once, derives trailing distances against that same `work` (using real positions), and returns `concatenate(work, trailing)` — a single consistent frame end to end, matching Decision 4.

### 6. Empty / fully-masked input: empty `ndarray`

Since gaps are now dropped rather than masked, a fully-masked or empty chain has nothing left to return in any mode — `np.array([], dtype=np.intp)`. This mirrors `core.intervals_tuple`'s own empty-input handling (`ar.size == 0` → empty array) and is symmetric with dropping partial gaps.

## Risks / Trade-offs

- **[Risk]** This is a breaking change to a shipped, public function (`foapy.partials.intervals_tuple`) with a documented spec. → **Mitigation**: confirmed via grep that no in-repo code (characteristics or otherwise) calls it yet; the spec delta and CHANGELOG-equivalent (proposal's "BREAKING" markers) make the behavior change explicit for any external consumer.
- **[Risk]** Delegating `lossy` to `core.intervals_tuple` creates a dependency from `partials` on `core`'s internals (the local-index boundary formula). If `core.intervals_tuple`'s algorithm ever changes, `partials.intervals_tuple` changes with it. → **Mitigation**: this is the intended behavior — parity with `core` is the explicit goal (Decision 4), so coupling here is a feature, not incidental.
- **[Trade-off]** Every existing test in `tests/test_partials_intervals_tuple.py` needs rewriting; there's no incremental/compatible path. → Accepted, since the old assertions test the exact masked-array behavior being removed.

## Migration Plan

Not applicable as a runtime migration — there are no known callers to migrate. Implementation sequencing:
1. Rewrite `src/foapy/partials/_intervals_tuple.py` per Decisions 1–6.
2. Rewrite `tests/test_partials_intervals_tuple.py` against the new contract, including an exact-order parity test against `core.intervals_tuple` for `binding.end` (replacing the current sorted-multiset check).
3. Add docstring examples, `docs/references/partials/intervals_tuple.md`, and the `mkdocs.yml` nav entry.
4. Update `openspec/specs/partials-package/spec.md` via this change's spec delta (applied at archive time).

## Open Questions

None outstanding — the ordering question (Decision 4) was resolved with the user before writing this design.
