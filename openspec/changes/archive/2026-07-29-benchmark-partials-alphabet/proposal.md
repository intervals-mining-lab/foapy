## Why

`foapy.partials.alphabet` is behaviorally tested, but it lacks the API-documentation parity, type annotations, benchmark coverage, and edge-case examples already provided for `foapy.alphabet`. This makes the partials API harder to discover and leaves its masked-input performance unmeasured.

## What Changes

- Add an ASV benchmark suite for `foapy.partials.alphabet`, including masked and unmasked inputs and time/peak-memory measurements comparable to the core alphabet benchmark.
- Expand the `foapy.partials.alphabet` docstring with a complete API description and runnable examples, symmetric with `foapy.alphabet` while documenting masked-value semantics.
- Add input and return type annotations to `foapy.partials.alphabet`.
- Add a dedicated `foapy.partials.alphabet` API reference page and expose it in `mkdocs.yml`.
- Add tests covering a masked first element, including a value whose first occurrence is masked and later occurrence is unmasked.
- Preserve the existing dense-input parity and masked-value exclusion behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `partials-package`: Clarify the documented public contract for `foapy.partials.alphabet`, including its documented return type, examples, and masked first-occurrence behavior.

## Impact

- Affected implementation: `src/foapy/partials/_alphabet.py`.
- Affected tests: `tests/test_partials_alphabet.py` and related parity coverage.
- Affected benchmark suite: `benchmarks/benchmarks/` and potentially partial masked-data case generation.
- Affected documentation: API reference pages, partial alphabet documentation, and MkDocs navigation.
- No new runtime dependencies or breaking API changes are expected.
