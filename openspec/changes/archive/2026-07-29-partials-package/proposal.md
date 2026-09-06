## Why

FOA currently supports dense sequences and masked-array workflows, but it does not provide a position-preserving pipeline for partial sequences. Researchers need to exclude gap positions from alphabet/order calculations while retaining their original positions when measuring intervals. This change introduces a dedicated `foapy.partials` submodule with semantics designed for that use case.

## What Changes

- Add the `foapy.partials` submodule with exactly four public functions: `order`, `alphabet`, `intervals_chain`, and `intervals_tuple`.
- Accept masked arrays, plain NumPy arrays, and Python sequences; plain inputs are treated as fully unmasked.
- Preserve input masks in positional outputs and return 1-D masked arrays aligned to the source sequence.
- Compute interval distances using full-array positional indices, so masked gaps contribute to distances.
- Support normal, lossy, and redundant tuple boundary strategies while preserving positional meaning.
- Exclude `intervals_distribution` and characteristic functions from this capability.
- Keep the API submodule-scoped (`foapy.partials.order()`); do not hoist these functions to `foapy.*`.

## Capabilities

### New Capabilities

- `partials-package`: Position-preserving FOA operations for partial masked sequences.

### Modified Capabilities

<!-- No existing OpenSpec capabilities are modified. -->

## Impact

- Adds `src/foapy/partials/` and its public exports.
- Updates lazy submodule exposure in `foapy/__init__.py`.
- Adds focused tests for all four functions, gap semantics, edge cases, and parity with `foapy.core` for unmasked inputs.
- No new runtime dependencies; NumPy remains the sole dependency.
