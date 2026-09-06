## 1. Implementation

- [x] 1.1 Rewrite `src/foapy/partials/_intervals_tuple.py`: `normal` returns `chain.compressed()` as `ndarray`.
- [x] 1.2 Rewrite `lossy` to delegate to `foapy.core.intervals_tuple(chain.compressed(), binding, tuple_mode.lossy)`.
- [x] 1.3 Rewrite `redundant`: compute `work = compressed[::-1] if binding == binding.end else compressed`; compute trailing distances against `len(chain)` (true source domain length) using real source positions; return `np.concatenate((work, trailing))` as a plain `ndarray`.
- [x] 1.4 Handle empty / fully-masked input: return `np.array([], dtype=np.intp)` for all modes.
- [x] 1.5 Remove now-unused masked-array plumbing (e.g. `_lossy`/`_redundant` helpers' mask bookkeeping) once the above land.

## 2. Tests

- [x] 2.1 Rewrite `tests/test_partials_intervals_tuple.py` empty/fully-masked cases (`test_empty_normal/lossy/redundant`, `test_fully_masked_normal/lossy`) to assert `np.array([], dtype=np.intp)`.
- [x] 2.2 Rewrite `normal` mode tests (`test_normal_preserves_mask`, `test_normal_preserves_values`, `test_normal_binding_end_preserves_mask`) to assert plain-`ndarray` compression behavior instead of mask preservation.
- [x] 2.3 Rewrite `lossy` mode tests (`test_lossy_same_length_as_input`, `test_lossy_masks_boundary_positions`, `test_lossy_original_mask_preserved`, `test_lossy_no_mask_non_boundary_values_kept`) against the new compressed-`ndarray` output.
- [x] 2.4 Rewrite `test_lossy_binding_end_no_mask_same_values_as_core` as an exact-order equality check against `core.intervals_tuple` (replacing the current sorted-multiset comparison).
- [x] 2.5 Rewrite `redundant` mode tests (`test_redundant_length_greater_than_input`, `test_redundant_trailing_elements_unmasked`, `test_redundant_input_portion_mask_unchanged`, `test_redundant_no_mask_matches_core_values`) against the new plain-`ndarray` output, including a masked/gapped case verifying gap-aware trailing distances (e.g. `X = [_, C, T, C, _, G]` → trailing `[4, 3, 1]`, not `[3, 2, 1]`).
- [x] 2.6 Add a `binding.end` + `redundant` + gaps test asserting the compressed and trailing portions share one consistent (reversed) order.
- [x] 2.7 Keep/adapt `test_invalid_binding_raises_value_error`, `test_invalid_tuple_mode_raises_value_error`, `test_plain_array_accepted` for the new return type.
- [x] 2.8 Rewrite `tests/test_partials_pipeline_consistency.py`'s `intervals_tuple` cross-checks (`normal`/`lossy`/`redundant` × core, previously relying on `.compressed()`/`.data` and multiset comparisons) to compare the plain-`ndarray` result directly against `core.intervals_tuple`, now exact for every binding.

## 3. Documentation

- [x] 3.1 Add runnable `Examples` section to the `intervals_tuple` docstring in `src/foapy/partials/_intervals_tuple.py`, following the style of `intervals_chain`'s docstring.
- [x] 3.2 Create `docs/references/partials/intervals_tuple.md` (mirroring `docs/references/partials/intervals_chain.md`).
- [x] 3.3 Add `intervals_tuple` nav entry under the `foapy.partials` section of `mkdocs.yml`.

## 4. Verification

- [x] 4.1 Run `tox -e default` and confirm the full suite passes.
- [x] 4.2 Run `pipx run pre-commit run --all-files --show-diff-on-failure` (black/isort/flake8).
- [x] 4.3 Run `openspec validate fix-partials-intervals-tuple` (or the store-scoped equivalent) before archiving.
