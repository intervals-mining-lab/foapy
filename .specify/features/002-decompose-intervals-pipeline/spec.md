# Feature Specification: Decompose Intervals Pipeline

**Feature Branch**: `002-decompose-intervals-pipeline`
**Created**: 2026-04-18
**Status**: Draft
**Input**: User description: "Decompose the intervals pipeline into chain/tuple/distribution stages; intervals_tuple should have binding as an explicit input parameter instead of inferring it from the chain structure. tuple_mode, binding and chain_mode should not have constructors."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Compose intervals from explicit stages (Priority: P1)

A library user who needs fine-grained control over interval extraction calls `intervals_chain`, `intervals_tuple`, and `intervals_distribution` as separate, independently composable functions rather than going through the single monolithic `intervals()` entry-point.

**Why this priority**: The pipeline decomposition is the core deliverable of this feature. All downstream user stories depend on the stages being independently callable.

**Independent Test**: Call `intervals_chain` followed by `intervals_tuple` with matching `binding` and verify the result equals the output of the combined `intervals()` function for the same inputs.

**Acceptance Scenarios**:

1. **Given** a sequence `X`, **When** a user calls `intervals_chain(X, binding.start, chain_mode.boundary)` and passes the result to `intervals_tuple(chain, binding.start, tuple_mode.normal)`, **Then** the output matches `intervals(X, binding.start, mode.normal)`.
2. **Given** a sequence `X`, **When** a user calls each stage independently with `binding.end`, **Then** the composed output matches the monolithic `intervals()` call with the same `binding`.
3. **Given** an empty sequence `X`, **When** any stage is called, **Then** each stage returns an empty array without error.

---

### User Story 2 - Pass binding explicitly to intervals_tuple (Priority: P1)

A library user calls `intervals_tuple(chain, binding, tuple_mode)` passing `binding` as an explicit argument, not relying on the function to infer it from chain structure.

**Why this priority**: Explicit `binding` makes the contract of `intervals_tuple` unambiguous and eliminates a hidden dependency on chain structural properties. It is a prerequisite for correctness of `lossy` and `redundant` modes.

**Independent Test**: Call `intervals_tuple` with `binding.start` and `binding.end` on the same chain and confirm the outputs differ correctly for `lossy` and `redundant` modes.

**Acceptance Scenarios**:

1. **Given** a chain produced by `intervals_chain(X, binding.start, chain_mode.boundary)`, **When** `intervals_tuple(chain, binding.start, tuple_mode.lossy)` is called, **Then** boundary (first-occurrence) intervals are removed.
2. **Given** a chain produced by `intervals_chain(X, binding.end, chain_mode.boundary)`, **When** `intervals_tuple(chain, binding.end, tuple_mode.lossy)` is called, **Then** boundary (last-occurrence) intervals are removed.
3. **Given** a chain and `tuple_mode.normal`, **When** `intervals_tuple` is called with any `binding`, **Then** the chain is returned unchanged (binding has no effect in normal mode).
4. **Given** an invalid `binding` value, **When** `intervals_tuple` is called, **Then** a `ValueError` is raised with a descriptive message.

---

### User Story 3 - Apply distribution stage independently (Priority: P2)

A library user calls `intervals_distribution(tuple_result)` to convert a flat intervals tuple into a grouped per-symbol distribution.

**Why this priority**: Completing the three-stage decomposition enables users to inspect intermediate representations for research purposes.

**Independent Test**: Call all three stages in sequence on a known sequence and verify the final distribution matches `intervals()` output.

**Acceptance Scenarios**:

1. **Given** an intervals tuple, **When** `intervals_distribution` is called, **Then** the result is a list/array of per-symbol interval arrays matching the grouped output of `intervals()`.
2. **Given** an empty tuple, **When** `intervals_distribution` is called, **Then** an empty distribution is returned.

---

### User Story 4 - Enum namespaces are not constructable (Priority: P1)

A library user who reads the API documentation or explores the library in an interactive session understands that `binding`, `tuple_mode`, and `chain_mode` are constant namespaces — not classes to be instantiated. Attempting to construct an instance of any of these raises an error, preventing accidental misuse.

**Why this priority**: Allowing construction of `binding()`, `tuple_mode()`, or `chain_mode()` gives users a false impression that these objects carry instance state or support callable inference of values. Removing the constructor makes the API contract unambiguous: only the named constants (`binding.start`, `binding.end`, etc.) are valid values to pass to pipeline functions.

**Independent Test**: Attempt to call `binding()`, `tuple_mode()`, and `chain_mode()` as constructors and confirm each raises `TypeError`. Confirm that the named constants (`binding.start`, `binding.end`, `tuple_mode.lossy`, etc.) are still accessible and hold their expected integer values.

**Acceptance Scenarios**:

1. **Given** a library user calls `binding()` with no arguments, **Then** a `TypeError` is raised indicating the type cannot be instantiated.
2. **Given** a library user calls `tuple_mode()` with no arguments, **Then** a `TypeError` is raised indicating the type cannot be instantiated.
3. **Given** a library user calls `chain_mode()` with no arguments, **Then** a `TypeError` is raised indicating the type cannot be instantiated.
4. **Given** a library user accesses `binding.start`, `binding.end`, `tuple_mode.lossy`, `tuple_mode.normal`, `tuple_mode.redundant`, `chain_mode.boundary`, `chain_mode.cycle`, **Then** each returns its expected integer constant without error.
5. **Given** code that previously relied on `binding(chain)` to infer binding direction from a chain, **Then** that code must be updated to pass `binding` explicitly — the callable inference path no longer exists.

---

### Edge Cases

- Empty sequence: all three stages return empty outputs without raising.
- Single-element sequence: chain has length 1; `lossy` mode yields empty array; `redundant` mode yields two intervals.
- All-same symbol: chain consists of uniform intervals; all modes produce correct results.
- All-unique symbols: only boundary intervals exist; `lossy` mode yields empty array.
- `binding.end` through full pipeline: reversed-direction chain processed correctly at every stage.
- Attempting to instantiate `binding`, `tuple_mode`, or `chain_mode` raises `TypeError`; the constants themselves remain accessible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `intervals_chain(X, binding, chain_mode)` MUST accept a 1-D sequence and return a plain 1-D integer array (the raw interval chain) without applying any boundary strategy.
- **FR-002**: `intervals_tuple(chain, binding, tuple_mode)` MUST accept `binding` as an explicit positional parameter and MUST NOT infer binding direction from chain structure.
- **FR-003**: `intervals_tuple` MUST use the `binding` parameter to correctly handle `tuple_mode.lossy` (drop first-occurrence intervals for `binding.start`, last-occurrence for `binding.end`) and `tuple_mode.redundant` (append complementary boundary intervals in the correct direction).
- **FR-004**: `intervals_distribution(chain)` MUST convert a flat interval tuple into a grouped per-symbol list of interval arrays matching the output contract of the existing `intervals()` function.
- **FR-005**: The monolithic `intervals(X, binding, mode)` MUST delegate internally to `intervals_chain`, `intervals_tuple`, and `intervals_distribution` and MUST produce identical results to the pre-decomposition implementation for all `binding × mode` combinations.
- **FR-006**: All three stage functions MUST be exported from `foapy.core` and accessible as public API.
- **FR-007**: Each stage function MUST validate its inputs and raise `ValueError` (with a descriptive message dict) for unrecognised enum values, and `Not1DArrayException` where applicable.
- **FR-008**: Tests for `intervals_tuple` MUST cover both `binding.start` and `binding.end` for every scenario category: empty chain, all-unique elements, all-identical elements, single-element sequence, and mixed sequences — for all three `tuple_mode` values (`normal`, `lossy`, `redundant`).
- **FR-009**: `binding`, `tuple_mode`, and `chain_mode` MUST NOT be constructable — calling any of them as a constructor (e.g., `binding()`) MUST raise `TypeError`. They function solely as named-constant namespaces.
- **FR-010**: Any existing code path that relied on calling `binding(chain)` to infer the binding direction from chain structure MUST be replaced with an explicit `binding` argument passed by the caller. The callable-inference behaviour is removed entirely.

### Key Entities

- **intervals_chain**: Converts a raw sequence into a flat integer chain; parameterised by `binding` and `chain_mode`.
- **intervals_tuple**: Applies a boundary strategy to a chain; parameterised by `binding` and `tuple_mode`.
- **intervals_distribution**: Groups a flat tuple into per-symbol interval arrays; stateless transformation.
- **binding**: Named-constant namespace controlling left-to-right (`start`) vs right-to-left (`end`) extraction direction. Not constructable.
- **tuple_mode**: Named-constant namespace selecting `normal`, `lossy`, or `redundant` boundary handling. Not constructable.
- **chain_mode**: Named-constant namespace selecting `boundary` or `cycle` treatment of sequence edges. Not constructable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All existing `binding × mode` test combinations pass without modification after the decomposition, confirming zero behavioural regression.
- **SC-002**: Each of the three stage functions (`intervals_chain`, `intervals_tuple`, `intervals_distribution`) is independently callable and testable without invoking the other stages.
- **SC-003**: Calling `intervals_tuple` with an incorrect `binding` value (e.g., the wrong direction for a given chain) produces a result that differs from the correct result, confirming that `binding` is actively used rather than ignored.
- **SC-004**: The full test suite (`tox -e default`) passes with zero failures after the changes.
- **SC-005**: Every `intervals_tuple` test scenario (all-unique, all-identical, single-element, mixed, empty) has a corresponding test case for both `binding.start` and `binding.end`, confirming symmetric coverage of the binding dimension.
- **SC-006**: Calling `binding()`, `tuple_mode()`, and `chain_mode()` as constructors each raises `TypeError`, verified by dedicated tests. Named constants (`binding.start`, `binding.end`, `tuple_mode.lossy`, etc.) continue to return their expected integer values unchanged.

## Assumptions

- The `binding` parameter in `intervals_tuple` takes the same constant values (`binding.start`, `binding.end`) as in `intervals_chain`; no new values are introduced.
- `intervals_distribution` receives a chain/tuple whose grouping metadata is derivable from the original sequence structure already embedded in the chain values; no separate symbol-map argument is required.
- The monolithic `intervals()` function is retained as a convenience wrapper and is not removed.
- `foapy.ma` variants of the decomposed stages are out of scope for this feature (to be addressed separately if needed).
- The three namespace objects (`binding`, `tuple_mode`, `chain_mode`) are the sole change scope for FR-009/FR-010; other callable or class objects in the library are unaffected by this requirement.
