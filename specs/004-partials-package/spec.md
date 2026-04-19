# Feature Specification: foapy.partials Package

**Feature Branch**: `004-partials-package`
**Created**: 2026-04-19
**Status**: Draft
**Input**: User description: "Create a new package - foapy.partials. The package should be equivalent to core package but use masked arrays as inputs and outputs."

## Clarifications

### Session 2026-04-19

- Q: Should `foapy.partials` include `intervals_distribution`? → A: No — exclude it; it operates on plain interval counts, not positional structure.
- Q: Should `partials` functions accept plain numpy arrays as input? → A: Yes — auto-wrap plain arrays as fully unmasked masked arrays internally.
- Q: Should `foapy.partials` be accessible as a top-level hoist in `foapy.*`? → A: No — submodule access only (`foapy.partials.order()`), matching the `foapy.ma` pattern.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Extract Order of Partial Sequence (Priority: P1)

A researcher has a symbolic sequence with missing or irrelevant positions (e.g., studying a subset of characters in a text while preserving their original positions). They call `foapy.partials.order()` with a masked 1-D array and receive back a masked 1-D array of the same length, where non-empty positions contain the element's alphabet index and empty positions remain masked.

**Why this priority**: The `order` function is the entry point to the entire FOA pipeline. Without it, no downstream analysis is possible. It also defines the fundamental contract between partials and the core API: 1-D in, 1-D out, gaps preserved.

**Independent Test**: Can be fully tested by calling `partials.order()` on a masked array and verifying the returned masked 1-D array has the correct alphabet indices at non-masked positions and masked values at masked positions.

**Acceptance Scenarios**:

1. **Given** a masked 1-D array `['a', --, 'b', 'a', --]` (positions 1 and 4 masked), **When** `partials.order()` is called, **Then** the result is a masked 1-D array `[0, --, 1, 0, --]` — same length, gap positions remain masked, non-gap positions hold alphabet indices.
2. **Given** a masked 1-D array where all positions are masked, **When** `partials.order()` is called, **Then** the result is a fully masked 1-D array of the same length.
3. **Given** a masked 1-D array with no masked positions, **When** `partials.order()` is called, **Then** the result matches `foapy.core.order()` applied to the same sequence.
4. **Given** a 2-D masked array, **When** `partials.order()` is called, **Then** a `Not1DArrayException` is raised.
5. **Given** `return_alphabet=True`, **When** `partials.order()` is called, **Then** both the masked 1-D order array and the alphabet of non-masked unique values are returned.

---

### User Story 2 - Compute Intervals Chain for Partial Sequence (Priority: P2)

A researcher has a partial order (1-D masked array from `partials.order()`) and wants to compute the intervals chain. They call `foapy.partials.intervals_chain()` and receive a masked 1-D array of the same length, where non-empty positions contain the interval distance (counting actual positional distances including gap positions), and empty positions remain masked.

**Why this priority**: Intervals are the core measurement of FOA. The critical semantic distinction of `foapy.partials` vs `foapy.ma` is that gaps contribute to interval distances — a gap between two occurrences of the same element increases the measured distance.

**Independent Test**: Can be fully tested by calling `partials.intervals_chain()` on a masked order array and verifying that interval values at non-masked positions reflect actual positional distances (including any masked gap positions between occurrences).

**Acceptance Scenarios**:

1. **Given** a partial sequence `[--, C, T, C, --, G]` and its partial order `[--, 0, 1, 0, --, 2]`, **When** `partials.intervals_chain()` is called with `binding.start` and `chain_mode.boundary`, **Then** the result is `[--, 2, 3, 2, --, 6]` — intervals count positional distances including gap positions.
2. **Given** two consecutive non-masked occurrences of the same element with one masked gap between them, **When** `partials.intervals_chain()` is called, **Then** the interval distance is 2 (gap counts as distance), not 1.
3. **Given** a partial order with all non-masked positions, **When** `partials.intervals_chain()` is called, **Then** the result matches `foapy.core.intervals_chain()` applied to the same sequence.
4. **Given** a partial order with all positions masked, **When** `partials.intervals_chain()` is called, **Then** a fully masked 1-D array of the same length is returned.

---

### User Story 3 - Apply Tuple Boundary Strategy to Partial Intervals (Priority: P3)

A researcher has a partial intervals chain and wants to apply a boundary strategy (lossy, normal, or redundant) to produce the final intervals tuple. They call `foapy.partials.intervals_tuple()` and receive a masked 1-D array of the same length with boundary-adjusted interval values.

**Why this priority**: Completes the pipeline to match core's full API. Required for all downstream characteristic computations that depend on boundary-adjusted intervals.

**Independent Test**: Can be tested by verifying that `partials.intervals_tuple()` produces the same boundary adjustments as `foapy.core.intervals_tuple()` for the non-masked positions of an equivalent chain.

**Acceptance Scenarios**:

1. **Given** a partial intervals chain and `tuple_mode.lossy`, **When** `partials.intervals_tuple()` is called, **Then** boundary intervals at non-masked positions are dropped and their positions become masked in the result.
2. **Given** a partial intervals chain and `tuple_mode.normal`, **When** `partials.intervals_tuple()` is called, **Then** the partial structure is preserved and boundary intervals at non-masked positions are retained unchanged.
3. **Given** a partial intervals chain and `tuple_mode.redundant`, **When** `partials.intervals_tuple()` is called, **Then** boundary intervals at non-masked positions are expanded and the output remains a masked 1-D array.

---

### User Story 4 - Extract Alphabet from Partial Sequence (Priority: P4)

A researcher needs to know which unique elements appear in a partial sequence. They call `foapy.partials.alphabet()` with a masked array and receive a plain 1-D array of the unique non-masked elements in order of first appearance.

**Why this priority**: A supporting utility used alongside `order()` and needed for result interpretation.

**Independent Test**: Can be tested by verifying that `partials.alphabet()` returns only unique non-masked values in first-appearance order, ignoring masked positions entirely.

**Acceptance Scenarios**:

1. **Given** a masked array `['a', --, 'b', 'a', --]`, **When** `partials.alphabet()` is called, **Then** the result is `['a', 'b']` — masked positions excluded, first-appearance order preserved.
2. **Given** a fully masked array, **When** `partials.alphabet()` is called, **Then** an empty array is returned.

---

### Edge Cases

- What happens when the partial sequence has only a single unique non-masked element? All intervals reduce to distances from the sequence boundary.
- What happens when adjacent non-masked positions are the same element? Interval distance is 1.
- How does a fully masked sequence propagate through the pipeline? Each stage returns a fully masked output of the same length.
- What happens when a non-masked element appears only once in the sequence? Only the boundary interval exists; under `tuple_mode.lossy` it is dropped.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `foapy.partials.order(X, return_alphabet=False)` MUST accept a masked 1-D array (or plain array, auto-wrapped as fully unmasked) and return a masked 1-D array of the same length, with alphabet indices at non-masked positions and masked values at masked positions.
- **FR-002**: `foapy.partials.order()` MUST raise `Not1DArrayException` when given a multi-dimensional input.
- **FR-003**: `foapy.partials.order()` with `return_alphabet=True` MUST return a tuple of `(masked_order_array, alphabet_array)` where `alphabet_array` contains only the unique non-masked values in first-appearance order.
- **FR-004**: `foapy.partials.intervals_chain(X, binding, chain_mode)` MUST accept a masked 1-D order array (or plain array, auto-wrapped as fully unmasked) and return a masked 1-D array of the same length, where interval distances at non-masked positions reflect actual positional distances including gap positions.
- **FR-005**: `foapy.partials.intervals_chain()` MUST treat masked gap positions as contributing to interval distance, so an element at position i and a matching element at position j with k masked gaps between them produces interval `j - i`.
- **FR-006**: `foapy.partials.intervals_tuple(chain, binding, tuple_mode)` MUST accept a masked 1-D intervals chain (or plain array, auto-wrapped as fully unmasked) and return a masked 1-D array with boundary strategy applied to non-masked positions.
- **FR-007**: `foapy.partials.alphabet(X)` MUST accept a masked 1-D array (or plain array, auto-wrapped as fully unmasked) and return a plain 1-D array of unique non-masked values in first-appearance order.
- **FR-008**: All `foapy.partials` functions MUST preserve the masked positions from input to output — a position that is masked in the input MUST be masked in the output.
- **FR-009**: The `foapy.partials` package MUST expose exactly four functions in its public API: `order`, `alphabet`, `intervals_chain`, `intervals_tuple`. `intervals_distribution` is excluded from scope.
- **FR-010**: When a `foapy.partials` function receives input with no masked positions, its result MUST be equivalent to the corresponding `foapy.core` function applied to the same data (as a plain array).
- **FR-011**: `foapy.partials` MUST be accessible as a submodule (`import foapy.partials` or `foapy.partials.order()`); its functions MUST NOT be hoisted to the `foapy.*` top-level namespace.

### Key Entities

- **Partial Sequence**: A 1-D masked array where masked positions represent empty/skip elements and non-masked positions hold symbolic values.
- **Partial Order**: A masked 1-D array where non-masked positions hold the alphabet index of the corresponding element and masked positions match the input mask.
- **Partial Intervals Chain**: A masked 1-D array of interval distances where non-masked positions hold the distance to the previous (or next) occurrence of the same element, counting positional distance including any gap positions between them.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four functions (`order`, `alphabet`, `intervals_chain`, `intervals_tuple`) are callable via `import foapy.partials` without errors.
- **SC-002**: For any partial sequence with no masked positions, `foapy.partials` produces results identical to `foapy.core` applied to the same plain sequence.
- **SC-003**: 100% of the `foapy.core` test cases pass an equivalent `foapy.partials` test with unmasked arrays, confirming behavioral parity at zero gaps.
- **SC-004**: Gap positions in the input are preserved as masked positions in every output, verified across all four functions.
- **SC-005**: Interval distances computed by `partials.intervals_chain()` correctly reflect actual positional distances (including gaps), verified against known examples from the partials documentation.
- **SC-006**: The package is fully covered by automated tests with the same structure as existing core and ma test suites.

## Assumptions

- The `foapy.partials` package scope is limited to four functions: `order`, `alphabet`, `intervals_chain`, `intervals_tuple`. `intervals_distribution` and all characteristics functions are out of scope for this feature.
- Masked positions represent "empty" or "skip" elements — excluded from alphabet construction and order assignment, but their positions count toward interval distances.
- `foapy.partials.order()` returns a 1-D masked array (not the 2-D matrix returned by `foapy.ma.order()`), which is the defining structural difference between the two packages.
- All four functions auto-wrap plain numpy arrays or Python lists as fully unmasked masked arrays; no explicit `numpy.ma.MaskedArray` construction is required by callers.
- `foapy.partials` is accessible as a submodule only (`foapy.partials.order()`), matching the `foapy.ma` pattern — functions are not hoisted to the `foapy.*` top-level namespace.
- `foapy.partials` does not export `binding`, `chain_mode`, or `tuple_mode` — users import those from `foapy.core`.
- The sole runtime dependency remains `numpy >= 1.20`; no new dependencies are introduced.
