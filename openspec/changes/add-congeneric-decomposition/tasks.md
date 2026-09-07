## 1. Package scaffolding

- [x] 1.1 Create `src/foapy/congenerics/` package directory
- [x] 1.2 Create `src/foapy/congenerics/__init__.py` re-exporting the six public functions (start empty imports, fill in as each module lands)

## 2. Decomposition core

- [x] 2.1 Implement `src/foapy/congenerics/_sequences.py`: `sequences(S)` using `foapy.partials.order(S, return_alphabet=True)` to scatter `S` into an `(m, l)` masked matrix, one row per alphabet symbol
- [x] 2.2 Handle empty/fully-masked input (`m = 0` rows) and multi-dimensional input (`Not1DArrayException`)
- [x] 2.3 Implement `src/foapy/congenerics/_alphabet.py`: `alphabet(S)` delegating to `foapy.partials.alphabet(S)`
- [x] 2.4 Unit tests for `sequences()` and `alphabet()`: occurrence-per-row correctness, gap propagation, empty/fully-masked input, dimensionality errors, row-label parity with `alphabet()`

## 3. Order stage

- [x] 3.1 Implement `src/foapy/congenerics/_order.py`: `order(S)` computing `CS = sequences(S)` then `foapy.partials.order(CS[j])` per row, stacked into `(m, l)`
- [x] 3.2 Unit tests: every non-masked value is `0`, mask matches `sequences(S)` row-for-row

## 4. Interval chains stage

- [x] 4.1 Implement `src/foapy/congenerics/_intervals_chains.py`: `intervals_chains(S, binding, chain_mode)` applying `foapy.partials.intervals_chain(CS[j], binding, chain_mode)` per row, stacked into `(m, l)`
- [x] 4.2 Validate `binding`/`chain_mode` and raise `ValueError` on invalid values (reuse `foapy.partials.intervals_chain`'s validation or replicate it)
- [x] 4.3 Unit tests: row-wise parity against direct `foapy.partials.intervals_chain` calls, both bindings and chain modes, invalid-argument errors

## 5. Interval tuples stage (padded)

- [x] 5.1 Implement `src/foapy/congenerics/_intervals_tuples.py`: `intervals_tuples(S, binding, chain_mode, tuple_mode)` computing each row's tuple via `foapy.partials.intervals_tuple` on `intervals_chains(S, binding, chain_mode)`'s rows, determine `x = max` row length, right-pad shorter rows with `0`, return `(m, x)` plain `ndarray` of dtype `numpy.intp`
- [x] 5.2 Unit tests: padding correctness (unpadded prefix matches direct per-row calls, trailing values are `0`), rectangular shape, `chain_mode` independently affects results from `tuple_mode`, invalid-argument errors

## 6. Interval distributions stage (globally padded)

- [x] 6.1 Implement `src/foapy/congenerics/_intervals_distributions.py`: `intervals_distributions(S, binding, chain_mode, tuple_mode)` computing each row's distribution via `foapy.core.intervals_distribution` on `intervals_tuples(S, binding, chain_mode, tuple_mode)`'s unpadded row values, determine `y = max` interval value across all rows, right-pad every row to width `y`, return `(m, y)` plain `ndarray` of dtype `numpy.intp`
- [x] 6.2 Unit tests: shared width across rows, zero-padding semantics, correctness against direct per-row `foapy.core.intervals_distribution` calls

## 7. Package finalization

- [x] 7.1 Finalize `src/foapy/congenerics/__init__.py` exports: exactly `sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, `intervals_distributions`
- [x] 7.2 Test that `foapy.congenerics` exposes exactly these six names and none are added at the top-level `foapy` namespace
- [x] 7.3 Run full test suite (`tox -e default`) and lint (`black`/`isort`/`flake8` — `pipx` unavailable in this environment, ran the same tools directly instead)

## 8. Documentation

- [x] 8.1 Fill in the "Add example of congeneric decomposition code" TODO in `docs/fundamentals/ideas/congeneric_decomposition.md` with a runnable `foapy.congenerics` example
- [x] 8.2 Add API reference entries for the six new functions under the docs navigation, following the `foapy.partials` reference pattern

## 9. Benchmarks

- [x] 9.1 Implement `benchmarks/benchmarks/bench_congenerics_sequences.py`: time/peakmem for `foapy.congenerics.sequences`, params `length x case` (Best/DNA/Normal/Worst, reusing `cases.py` helpers), skipping `m`-scales-with-length cases at the largest length
- [x] 9.2 Implement `benchmarks/benchmarks/bench_congenerics_order.py`: same param matrix as 9.1, for `foapy.congenerics.order`
- [x] 9.3 Implement `benchmarks/benchmarks/bench_congenerics_intervals_chains.py`: time/peakmem for `foapy.congenerics.intervals_chains`, params `length x case x binding x chain_mode`, skipping `m`-scales-with-length cases at the largest length
- [x] 9.4 Verify the new benchmark suites are discoverable and runnable: `asv check` builds from the last git commit, not the working tree, so it can't see uncommitted `foapy.congenerics` — verified instead by directly instantiating each Suite class and calling `setup()`/`time_*()` across the full param matrix (all length x case x binding x chain_mode combinations, skips excluded), which exercises the exact code path ASV would run

## 10. Vectorize away per-row Python loops (D3 rewrite)

- [x] 10.1 Derive vectorized formulas for `order`, `intervals_chains`, `intervals_tuples` (all three `tuple_mode`s), `intervals_distributions` from the single-group special case of `foapy.partials`'/`foapy.core`'s algorithms; verify against the original loop-based implementation across randomized trials (bindings x chain_modes x tuple_modes x masked/unmasked/empty inputs) before touching source
- [x] 10.2 Rewrite `_order.py`: drop the per-row loop entirely (`0` at every non-masked position is derivable directly from `sequences(S)`'s mask)
- [x] 10.3 Rewrite `_intervals_chains.py`: add private `_chain_work_frame`/`_from_work_frame` helpers computing the chain via `numpy.maximum.accumulate` along columns across all rows at once; keep the public signature/contract unchanged
- [x] 10.4 Rewrite `_intervals_tuples.py`: add private `_pack_rows` (vectorized ragged pack-left-and-pad via `numpy.cumsum` + fancy-index scatter) reusing `_chain_work_frame`'s boundary flags; keep the public signature/contract unchanged
- [x] 10.5 Rewrite `_intervals_distributions.py`: replace the per-row histogram loop with a single `numpy.add.at` scatter-add across all rows; keep the public signature/contract unchanged
- [x] 10.6 Fix test assertions that compared masked arrays' raw `.data` (including masked filler, which changed from `-1` to `0` and was never part of the public contract) instead of mask-aware comparison
- [x] 10.7 Broaden `intervals_tuples`/`intervals_distributions` test coverage to exercise `tuple_mode.lossy` and `tuple_mode.redundant` (previously only `tuple_mode.normal` was tested — a pre-existing gap the rewrite's coverage report surfaced)
- [x] 10.8 Re-run `tox -e default` and lint (`black`/`isort`/`flake8`) after the rewrite; confirm 100% coverage on every `src/foapy/congenerics/*.py` module

## 11. `alphabet`/`order` take `CS` instead of `S` (D2.1)

- [x] 11.1 Change `_alphabet.py`: `alphabet(CS)` reads each row's single non-masked value directly from `CS` (via `argmax` on `~mask` per row) instead of delegating to `foapy.partials.alphabet(S)`
- [x] 11.2 Change `_order.py`: `order(CS)` reads `CS`'s own mask directly instead of calling `sequences(S)` internally
- [x] 11.3 Update `tests/test_congenerics_alphabet.py`/`test_congenerics_order.py` to compute `CS = sequences(X)` first and pass `CS`; update `test_congenerics_sequences.py`'s cross-check accordingly
- [x] 11.4 Update the docs example (`docs/fundamentals/ideas/congeneric_decomposition.md`) and `benchmarks/benchmarks/bench_congenerics_order.py` to call `alphabet(CS)`/`order(CS)` instead of the raw source
- [x] 11.5 Re-run `tox -e default` and lint; confirm 100% coverage on `_alphabet.py`/`_order.py` under the new contract
