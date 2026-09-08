## Context

FoaPy's congeneric decomposition pipeline (`foapy.congenerics`) was introduced to supersede `foapy.ma`, which implemented the same concept (decomposing a sequence into per-symbol masked arrays) using an older masked-array API. Similarly, `foapy.characteristics` accumulated functions that require grouped/congeneric input (`descriptive_information`, `identifying_information`, `regularity`, `uniformity`) — these were misplaced alongside true flat-interval characteristics.

The result is two sources of confusion:
1. `foapy.ma` and `foapy.congenerics` both model congeneric sequences, creating redundancy
2. `foapy.characteristics` mixes flat-interval functions (input: 1-D array → scalar) with grouped-interval functions (input: list of arrays → scalar)

## Goals / Non-Goals

**Goals:**
- Create `foapy.congenerics.characteristics` as the single home for all congeneric characteristics
- Establish a clear naming convention: singular = scalar aggregate; plural = per-symbol array
- Remove `foapy.ma` and `foapy.characteristics.ma` entirely
- Update tests and docs to reflect the new structure; no deprecation cycle

**Non-Goals:**
- Changing any characteristic's mathematical definition or algorithm
- Adding new characteristics
- Modifying `foapy.core`, `foapy.partials`, or `foapy.characteristics` flat functions (`arithmetic_mean`, `average_remoteness`, `depth`, `geometric_mean`, `volume`)

## Decisions

### 1. `congenerics.characteristics` as a subpackage, not flat exports

**Decision:** `foapy.congenerics.characteristics` is a subpackage (a directory with `__init__.py`), accessed via `import foapy.congenerics.characteristics` or `from foapy.congenerics import characteristics`. Functions are NOT promoted to the `foapy.congenerics` top-level namespace.

**Rationale:** Mirrors the existing `foapy.characteristics` pattern. Keeps `foapy.congenerics`'s top-level namespace focused on the decomposition pipeline (sequences, order, intervals_chains, etc.).

**Alternative considered:** Export everything flat from `foapy.congenerics`. Rejected — it would blur the line between pipeline primitives and analysis functions.

### 2. Singular/plural naming convention

**Decision:** Singular names (`identifying_information`, `uniformity`) for scalar aggregates over all congeneric groups; plural names (`identifying_informations`, `uniformities`) for per-symbol arrays.

**Rationale:** The name alone signals the return type and expected input. A caller importing `volumes` knows they get one value per symbol; importing `volume` from `foapy.characteristics` knows they get a scalar.

**Alternative considered:** Suffix-based names (`identifying_information_array` vs `identifying_information_scalar`). Rejected — verbose and inconsistent with numpy's convention of pluralizing array-returning functions (e.g., `indices`, `values`).

### 3. Clean deletion of `foapy.ma` and `foapy.characteristics.ma`

**Decision:** Delete both packages outright. No deprecation shims, no re-exports.

**Rationale:** These are internal library packages. Backward compatibility is explicitly not required. Deprecation wrappers would leave dead code and confuse future contributors.

**Alternative considered:** Keep `foapy.ma` as a thin alias. Rejected — it would perpetuate confusion about which package models congeneric sequences.

### 4. Internal cross-references in moved functions

**Decision:** Functions moved from `characteristics` to `congenerics.characteristics` update their internal imports. For example, `descriptive_information` currently calls `from foapy.characteristics import identifying_information`; after the move it calls `from foapy.congenerics.characteristics import identifying_information`.

**Rationale:** Avoids circular imports and keeps dependencies within the package boundary.

### 5. Test file placement

**Decision:**
- Top-level `tests/test_ma_*.py` files are deleted (the congenerics package already has full test coverage)
- `tests/test_characteristics/test_ma_*.py` are moved to `tests/test_congenerics_characteristics/` and renamed to match plural function names (e.g., `test_ma_volume.py` → `test_volumes.py`)
- `tests/test_characteristics/test_descriptive_information.py`, `test_identifying_information.py`, `test_regularity.py`, `test_uniformity.py` move to `tests/test_congenerics_characteristics/`

**Rationale:** Mirrors the source structure. Keeps congenerics tests together.

## Risks / Trade-offs

- [Scope] Many files touch this change (source, tests, docs). → Mitigation: implement in a single branch with a full test run before merge.
- [Internal imports] Moved functions may import each other (e.g., `regularity` uses `descriptive_information` and `geometric_mean`). → Mitigation: update all cross-references during the move; verify with `tox -e default` after each group.
- [Docs examples] Docstrings in moved files use `foapy.ma.order` / `foapy.ma.intervals` in their examples. → Mitigation: update examples to use `foapy.congenerics` pipeline as part of the move.
