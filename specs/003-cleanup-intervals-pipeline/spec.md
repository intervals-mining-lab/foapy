# Feature Specification: Cleanup Intervals Pipeline

**Feature Branch**: `003-cleanup-intervals-pipeline`
**Created**: 2026-04-19
**Status**: Draft
**Input**: User description: "Update 002-decompose-intervals-pipeline. 1. Remove '_is_valid_intervals_chain.py' - we will implement it in future. This is now poorly defined. 2. Remove '_mode.py' - due it is decomposed into tuple_mode and chain_mode. 3. Remove '_intervals.py' from the core package. Move it to tests interval function. Keep intervals related tests to clarify that intervals_chain -> intervals_tuple = intervals in all possible parameters inputs. Keep intervals benchmarks replacing intervals function with composition interval_chain -> intervals_tuple. 4. Update documentation. Remove interval method. Added intervals_chain intervals_tuple intervals_distribution and related mode. Link it related with corresponding foundation subjects."

## Context

This feature finalises the cleanup from **002-decompose-intervals-pipeline**, which added the `intervals_chain`, `intervals_tuple`, and `intervals_distribution` primitives. Now that the decomposed pipeline is implemented, three interim artefacts must be retired and documentation must be updated to reflect the new canonical pipeline.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Public API Contains Only the Decomposed Pipeline (Priority: P1)

A library user looking at the `foapy` public namespace expects to find only `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` for interval-related work. The old `intervals()` function, the unified `mode` enum, and the `is_valid_intervals_chain` stub are no longer part of the public API. Users who relied on `intervals()` can replicate its behaviour with the decomposed pipeline using a mapping that is documented and verified by the test suite.

**Why this priority**: A clean public API with no deprecated or incomplete functions reduces confusion for new adopters and aligns the library surface with the fundamentals documentation. Removing ill-defined stubs prevents users from depending on behaviour that will change.

**Independent Test**: Can be fully tested by importing `foapy` and verifying that `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` are importable; that `intervals`, `mode`, and `is_valid_intervals_chain` are not importable from the top-level namespace; and that any attempt to import the removed names raises `ImportError`.

**Acceptance Scenarios**:

1. **Given** a fresh Python environment, **When** a user imports `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` from `foapy`, **Then** all five names resolve without error.
2. **Given** a fresh Python environment, **When** a user attempts to import `intervals` or `mode` or `is_valid_intervals_chain` from `foapy`, **Then** each raises `ImportError`.
3. **Given** existing code that calls `intervals(X, binding, mode.lossy)`, **When** it is replaced with the documented equivalent `intervals_tuple(intervals_chain(X, binding, chain_mode.boundary), binding, tuple_mode.lossy)`, **Then** the output is identical.

---

### User Story 2 - Pipeline Equivalence Is Verified by the Test Suite (Priority: P1)

A library maintainer and a library user adopting the decomposed pipeline both need assurance that the composition `intervals_chain → intervals_tuple` reproduces the former `intervals()` output for every binding direction and mode combination. This assurance lives in the test suite as a dedicated test module: a test helper provides the `intervals(X, binding, mode)` function for comparison purposes only (it is not part of the public API), and parametrised tests verify equivalence for all four mode mappings across representative inputs.

**Why this priority**: Without automated verification of pipeline equivalence, regressions could silently break characteristics results for users who migrated to the new API. This test module is the executable specification of the mode-mapping contract.

**Independent Test**: Can be fully tested by running the dedicated equivalence test module, which imports `intervals_chain`, `intervals_tuple`, and the test-only `intervals` helper, and asserts identical output for each of the four mode mappings on all parametrised inputs.

**Acceptance Scenarios**:

1. **Given** any 1-D sequence, any binding direction, and `mode.lossy`, **When** the equivalence test runs, **Then** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.lossy)` equals the test-helper `intervals(X, b, mode.lossy)` result.
2. **Given** any 1-D sequence, any binding direction, and `mode.normal`, **When** the equivalence test runs, **Then** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.normal)` equals the test-helper `intervals(X, b, mode.normal)` result.
3. **Given** any 1-D sequence, any binding direction, and `mode.cycle`, **When** the equivalence test runs, **Then** `intervals_tuple(intervals_chain(X, b, chain_mode.cycle), b, tuple_mode.normal)` equals the test-helper `intervals(X, b, mode.cycle)` result.
4. **Given** any 1-D sequence, any binding direction, and `mode.redundant`, **When** the equivalence test runs, **Then** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.redundant)` equals the test-helper `intervals(X, b, mode.redundant)` result.
5. **Given** edge-case inputs (empty sequence, single element, all-unique elements, all-identical elements), **When** the equivalence tests run, **Then** all four mode mappings pass for each edge case.

---

### User Story 3 - Performance Benchmarks Use the Decomposed Pipeline (Priority: P2)

A library user evaluating the performance of interval computation needs benchmark numbers that reflect the public API they will actually call. The benchmarks must measure the composition `intervals_chain → intervals_tuple` rather than the retired `intervals()` function, and must cover all four mode mappings at small, medium, and large input sizes.

**Why this priority**: Benchmarks built on a retired function give misleading performance data. Users comparing throughput across library versions need benchmarks that match the current public API.

**Independent Test**: Can be fully tested by running the benchmark suite and confirming that: no benchmark calls the retired `intervals()` function; each benchmark exercises `intervals_chain` followed by `intervals_tuple`; results are reported for all four mode mappings at the three input sizes.

**Acceptance Scenarios**:

1. **Given** the benchmark suite, **When** it is run, **Then** no benchmark invokes the retired `intervals()` function.
2. **Given** the benchmark suite, **When** it is run for each mode mapping (lossy, normal, cycle, redundant), **Then** execution time is reported at small (≤100 elements), medium (≤10,000 elements), and large (≤1,000,000 elements) input sizes.
3. **Given** the benchmark suite, **When** it is run, **Then** it completes without error and the output is reproducible across runs on the same machine.

---

### User Story 4 - Documentation Describes Only the Decomposed Pipeline (Priority: P2)

A library user reading the documentation wants to learn how to compute intervals for their sequence. The documentation describes `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode`; does not mention `intervals()` as a callable; and links each function and enum to the relevant section in the fundamentals documentation so users understand the mathematical motivation.

**Why this priority**: Documentation that still references a retired function misleads users into calling a function that no longer exists. Linking to the fundamentals section anchors each function in the mathematical theory, reducing support questions.

**Independent Test**: Can be fully tested by reviewing the documentation to confirm: `intervals()` appears only as a historical reference (if at all) rather than a callable API entry; each of the five public names has a documented entry; each entry links to the corresponding foundation subject.

**Acceptance Scenarios**:

1. **Given** the API reference documentation, **When** a user browses it, **Then** `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` each have a documented entry with description, parameters, return value, and an example.
2. **Given** the API reference documentation, **When** a user searches for `intervals()` as a standalone function, **Then** it does not appear as a callable API entry.
3. **Given** each function and enum documentation page, **When** a user reads it, **Then** at least one link leads to the corresponding section in the fundamentals documentation.
4. **Given** the documentation for `chain_mode` and `tuple_mode`, **When** a user reads them, **Then** the difference between the two enums is clearly explained with reference to the pipeline stage each controls.

---

### Edge Cases

- What happens when a user imports `intervals` from `foapy` after this cleanup? The import raises `ImportError`.
- What happens when a user imports `mode` from `foapy` after this cleanup? The import raises `ImportError`.
- What happens when a user imports `is_valid_intervals_chain` from `foapy` after this cleanup? The import raises `ImportError`.
- How does the equivalence test handle sequences with no repeated elements? Each result is an empty array for `lossy` mode and a boundary-only array for other modes; both pipeline paths must agree.
- What if an existing external codebase imports `intervals` directly from `foapy.core`? That import path also breaks; the test-only helper is not re-exported from any public module.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `intervals` function, the unified `mode` enum, and the `is_valid_intervals_chain` stub MUST NOT be importable from the `foapy` top-level namespace after this cleanup; attempting to do so MUST raise `ImportError`.
- **FR-002**: The `intervals` function MUST be moved to a test-only helper module that is not part of the public package; it MUST NOT be re-exported from any public `foapy` module or subpackage.
- **FR-003**: A dedicated test module MUST exist that imports the test-only `intervals` helper and verifies that the four-mode equivalence `intervals_chain → intervals_tuple = intervals` holds for all four mode mappings, all binding directions, and representative edge-case inputs.
- **FR-004**: Every existing test that validated `intervals()` behaviour MUST be converted to: (a) a test verifying the decomposed pipeline (`intervals_chain → intervals_tuple`) produces the same result, or (b) a test using the test-only helper in the dedicated equivalence test module; no test that was previously present MUST be silently deleted.
- **FR-005**: The benchmark suite MUST replace all calls to `intervals()` with the equivalent `intervals_chain → intervals_tuple` composition for the corresponding mode mapping; coverage MUST include all four mode mappings at small, medium, and large input sizes.
- **FR-006**: The `foapy` public namespace MUST continue to export `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` without change.
- **FR-007**: The documentation MUST be updated so that `intervals()` does not appear as an API callable; each of `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, and `tuple_mode` MUST have a documentation entry with description, parameters, return value, and at least one example.
- **FR-008**: Each documentation entry for the five public names MUST contain at least one link to the corresponding section in the fundamentals documentation.
- **FR-009**: The `mode` enum and `is_valid_intervals_chain` stub MUST be removed from the source tree; no orphan file or import reference to either MUST remain.

### Key Entities

- **Test-only `intervals` helper**: The retired `intervals()` function preserved in the test suite solely to drive equivalence comparisons; not importable from any public namespace.
- **Equivalence test module**: A dedicated test file asserting that `intervals_chain → intervals_tuple` matches the test-only `intervals` helper for all four mode mappings across all binding directions and edge-case inputs.
- **Mode mapping table**: The four canonical correspondences — `mode.lossy ↔ chain_mode.boundary + tuple_mode.lossy`, `mode.normal ↔ chain_mode.boundary + tuple_mode.normal`, `mode.cycle ↔ chain_mode.cycle + tuple_mode.normal`, `mode.redundant ↔ chain_mode.boundary + tuple_mode.redundant` — documented and verified by the equivalence test module.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Attempting to import `intervals`, `mode`, or `is_valid_intervals_chain` from `foapy` raises `ImportError` in 100% of test runs after this cleanup.
- **SC-002**: The equivalence test module passes for all four mode mappings, both binding directions, and all edge-case inputs — 0 failures.
- **SC-003**: All characteristics that previously accepted `intervals()` output continue to produce the same results when given `intervals_tuple` output for the same input — zero regressions in the existing characteristics test suite.
- **SC-004**: The benchmark suite runs to completion with no calls to the retired `intervals()` function, covering all four mode mappings at three input sizes.
- **SC-005**: Each of the five public names (`intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, `tuple_mode`) has a documentation entry containing description, parameters, return value, and at least one example with a link to the fundamentals documentation.
- **SC-006**: No orphan import references to `_mode.py`, `_is_valid_intervals_chain.py`, or `_intervals.py` remain anywhere in the source tree or test suite (excluding the test-only helper module itself).

## Assumptions

- The decomposed pipeline (`intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode`, `tuple_mode`) was fully implemented in 002-decompose-intervals-pipeline and is already available; this feature does not add new algorithmic functionality.
- Removing `intervals()` from the public API is a deliberate breaking change for any external caller; there is no deprecation grace period — the function moves directly to a test-only helper.
- The `mode` enum is superseded entirely by `chain_mode` and `tuple_mode`; it is removed from the source tree rather than kept as an alias.
- `is_valid_intervals_chain` is deferred to a future feature with a clearer definition; its stub file is removed rather than left as a placeholder.
- The test-only `intervals` helper retains the original four-mode logic unmodified so that equivalence tests serve as a regression safety net; the helper is not subject to the library's public API stability guarantees.
- Documentation updates cover the `foapy` public API reference pages; the fundamentals documentation pages themselves are already written and only require linking from the function/enum entries.
- Masked-array variants (`foapy.ma`) for the five public names are unchanged by this feature.
- Test conventions continue to follow the existing `CharacteristicsTest`-style base classes and `AssertBatch` helpers where applicable.
