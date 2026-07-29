## 1. Package setup

- [x] 1.1 Add `src/foapy/partials/` with exports for `order`, `alphabet`, `intervals_chain`, and `intervals_tuple`.
- [x] 1.2 Update `foapy/__init__.py` to lazy-load `foapy.partials` without hoisting its functions.
- [x] 1.3 Add public API and plain-input wrapping tests.

## 2. Ordering and alphabet

- [x] 2.1 Add tests for `partials.order()` covering empty, fully masked, partially masked, unmasked, multi-dimensional, and `return_alphabet` cases.
- [x] 2.2 Implement `partials.order()` by ordering compressed values and remapping indices to original unmasked positions.
- [x] 2.3 Add tests for `partials.alphabet()` covering first-appearance order, masked exclusion, empty/full-mask, unmasked parity, and dimensionality errors.
- [x] 2.4 Implement `partials.alphabet()` using compressed values and core alphabet behavior.

## 3. Position-preserving interval chain

- [x] 3.1 Add tests for boundary and cycle modes, both bindings, repeated values separated by gaps, all-unique, all-masked, empty, invalid modes, and dense parity.
- [x] 3.2 Implement `partials.intervals_chain()` from raw masked input using original source indices and stable value grouping.
- [x] 3.3 Verify output masks and interval values against the documented `[--, C, T, C, --, G]` example.

## 4. Interval tuple strategies

- [x] 4.1 Add tests for normal, lossy, and redundant modes, including existing masks, empty/full-mask chains, invalid modes, and dense parity.
- [x] 4.2 Implement normal mode as a masked copy of the chain.
- [x] 4.3 Implement lossy mode by masking boundary positions detected on the compressed chain without changing output length.
- [x] 4.4 Implement redundant mode by appending unmasked complementary trailing intervals and preserving the original mask.

## 5. Verification and documentation

- [x] 5.1 Add an end-to-end pipeline test covering order, chain, and tuple behavior with and without gaps.
- [x] 5.2 Run the full test suite and confirm existing `core` and `ma` behavior is unchanged.
- [x] 5.3 Run formatting and lint checks for the new package and fix any violations.
- [x] 5.4 Validate the partials quickstart examples and confirm the public API contains exactly the four scoped functions.
