# Feature Specification: Decompose Intervals Pipeline

**Feature Branch**: `002-decompose-intervals-pipeline`
**Created**: 2026-03-28
**Status**: Draft
**Input**: User description: "We need to decompose src/foapy/core/intervals. From order/sequence -> intervals -> characteristics to order/sequence -> intervals_chain -> intervals_tuple -> intervals_distribution -> characteristics. To be consistent with what is described in docs/fundamentals"

## Clarifications

### Session 2026-03-28

- Q: Should `binding(chain)` and `chain_mode(chain)` raise an exception or return a default for an empty chain? → A: Return defaults — `binding.start` for `binding(chain)` and `chain_mode.cycle` for `chain_mode(chain)`.

### Session 2026-04-18

- Q: Should `intervals_tuple` require `binding` as an explicit parameter or infer it from chain structure? → A: Explicit parameter. `intervals_tuple(chain, binding, tuple_mode)` — binding is a required positional argument passed by the caller; the function never infers it from the chain.
- Q: Should US5 (`binding(chain)` callable inference), US7 (`chain_mode(chain)` callable inference), and related FR-015, FR-016, SC-006, SC-007 remain in the spec? → A: Remove them. Callable inference is out of scope — `binding` and `chain_mode` are non-constructable named-constant namespaces; calling them raises `TypeError`.

### Session 2026-04-19

- Q: (No new questions) Applied outstanding spec body cleanup from 2026-04-18 clarifications: removed US5, US7, FR-015, FR-016, SC-006, SC-007; updated FR-007–FR-010 and US4 acceptance scenarios to use the 3-argument `intervals_tuple(chain, b, tuple_mode)`; renumbered FR-018–FR-020 → FR-016–FR-018 and SC-008–SC-010 → SC-006–SC-008; updated Edge Cases, FR-006, SC-001, US5/US6 Why text, and Assumptions to remove callable-inference references.

### Session 2026-03-28 (first pass)

- Q: Should `intervals_chain` return a plain ndarray (with structural detection of binding/chain_mode from values) or a metadata-carrying named tuple? → A: Plain ndarray. The separation of `chain_mode` into `cycle` and `boundary` makes structural detection **mathematically deterministic** — this is the reason for the separation. No named tuple or attached metadata is needed.
- Q: How does `tuple_mode` behave on new combinations (`cycle + lossy`, `cycle + redundant`)? → A: `tuple_mode` works uniformly on any chain by checking whether `i - interval` falls outside `[0, n]`: if so, the interval is a first/last-occurrence (boundary) interval. `lossy` drops all such intervals. `normal` keeps them as-is. `redundant` expands each into two intervals — leading and trailing — with trailing intervals appended to the end of the result in element-appearance order. This definition is independent of `chain_mode`, so all six combinations are valid.
- Q: Does `intervals_chain` accept only the output of `order()` (pre-ordered integer indices) or any raw 1-D sequence? → A: Any raw 1-D sequence (strings, ints, objects) — same as `intervals()` today. No pre-ordering required.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Intervals Chain as a Standalone Step (Priority: P1)

A library user working through the FOA pipeline wants to obtain the raw intervals chain from any 1-D sequence (strings, integers, or any comparable elements). The chain is the n-tuple of distances between equal elements computed according to a specific binding direction and chain construction mode. Today they must call `intervals()` which bundles all steps together. They need `intervals_chain` as a callable step that accepts any raw 1-D sequence, a binding direction, and a chain mode (`cycle` or `boundary`) and returns the raw chain — no pre-ordering via `order()` is required.

**Why this priority**: `intervals_chain` is the foundational intermediate representation described in the fundamentals documentation. The `chain_mode` parameter determines whether the sequence is treated as cyclic or bounded during chain construction — a distinction that was previously conflated inside a single `mode` enum.

**Independent Test**: Can be fully tested by calling `intervals_chain(X, binding, chain_mode)` on a known raw sequence and verifying the returned plain 1-D array matches expected values per the fundamentals documentation — without invoking `intervals_tuple` or `intervals_distribution`.

**Acceptance Scenarios**:

1. **Given** a raw sequence `[b, a, b, c, b]`, `binding.start`, and `chain_mode.boundary`, **When** `intervals_chain` is called, **Then** it returns the raw distances between consecutive equal elements with boundary distances to the start of the sequence for each first occurrence.
2. **Given** the same raw sequence, `binding.end`, and `chain_mode.boundary`, **When** `intervals_chain` is called, **Then** it returns distances computed right-to-left with boundary distances from the end of the sequence.
3. **Given** any sequence and `chain_mode.cycle`, **When** `intervals_chain` is called, **Then** the leading and trailing boundary distances are combined into a single cyclic interval per element as if the sequence were circular.
4. **Given** an empty sequence, **When** `intervals_chain` is called, **Then** it returns an empty result without error.
5. **Given** a sequence where every element is unique, **When** `intervals_chain` is called, **Then** each element's chain contains only its boundary interval.

---

### User Story 2 - Apply Tuple Mode via Intervals Tuple (Priority: P2)

A library user wants to apply a tuple transformation mode (`lossy`, `normal`, or `redundant`) to an already-computed intervals chain to obtain the intervals tuple used as input to characteristics. They need `intervals_tuple` as a standalone callable that accepts a raw chain, the binding direction used to produce it, and a `tuple_mode`.

`tuple_mode` operates by detecting boundary intervals using the explicit `binding` parameter: for `binding.start`, the first-occurrence interval at position `i` satisfies `i - v < 0`; for `binding.end`, the last-occurrence interval satisfies `i + v > n`. The detection is uniform and works identically on chains built with either `chain_mode.boundary` or `chain_mode.cycle`.

- `tuple_mode.lossy`: drops all boundary intervals; interior intervals are kept as-is.
- `tuple_mode.normal`: keeps all intervals as-is (boundary intervals remain in place).
- `tuple_mode.redundant`: replaces each boundary interval with two intervals — the leading distance (from sequence start to first occurrence) and the trailing distance (from last occurrence to sequence end). Trailing intervals are appended to the end of the result in element-appearance order.

**Why this priority**: Explicit `binding` makes the contract of `intervals_tuple` unambiguous and eliminates a hidden dependency on chain structural properties. All six combinations of `chain_mode × tuple_mode` are valid.

**Independent Test**: Can be fully tested by calling `intervals_tuple(chain, binding, tuple_mode)` on a known chain with matching `binding` and verifying the output matches expected per each tuple_mode's definition, without needing `intervals_distribution`.

**Acceptance Scenarios**:

1. **Given** a chain produced by `intervals_chain(X, binding.start, chain_mode.boundary)` and `tuple_mode.lossy`, **When** `intervals_tuple(chain, binding.start, tuple_mode.lossy)` is called, **Then** boundary (first-occurrence) intervals are excluded; interior intervals are kept.
2. **Given** a chain produced by `intervals_chain(X, binding.end, chain_mode.boundary)` and `tuple_mode.lossy`, **When** `intervals_tuple(chain, binding.end, tuple_mode.lossy)` is called, **Then** boundary (last-occurrence) intervals are excluded; interior intervals are kept.
3. **Given** an intervals chain and `tuple_mode.normal`, **When** `intervals_tuple(chain, binding, tuple_mode.normal)` is called with any `binding`, **Then** all intervals are returned as-is with no modification.
4. **Given** a chain produced by `intervals_chain(X, binding.start, chain_mode.boundary)`, **When** `intervals_tuple(chain, binding.start, tuple_mode.normal)` is called, **Then** the result is identical to `intervals(X, binding.start, mode.normal)`.
5. **Given** a chain produced by `intervals_chain(X, binding.start, chain_mode.cycle)`, **When** `intervals_tuple(chain, binding.start, tuple_mode.normal)` is called, **Then** the result is identical to `intervals(X, binding.start, mode.cycle)`.
6. **Given** a chain produced by `intervals_chain(X, binding.start, chain_mode.cycle)`, **When** `intervals_tuple(chain, binding.start, tuple_mode.lossy)` is called, **Then** cyclic boundary intervals are dropped and only interior intervals remain.
7. **Given** an invalid `binding` value, **When** `intervals_tuple` is called, **Then** a `ValueError` is raised with a descriptive message.

---

### User Story 3 - Compute Intervals Distribution from Tuple (Priority: P3)

A library user wants to convert an intervals tuple into its distribution — an array where each index represents an interval length and each value is the count of that length's appearances. This distribution is what characteristics such as `volume`, `depth`, and `arithmetic_mean` operate on. They need `intervals_distribution` as a standalone callable that accepts a tuple and returns the distribution.

**Why this priority**: `intervals_distribution` is the direct input to characteristics calculations as documented in the fundamentals. Exposing it enables users to analyse distribution shapes independently and to compare distributions from different binding or mode combinations.

**Independent Test**: Can be fully tested by calling `intervals_distribution(intervals_tuple)` on a known tuple and verifying the returned count array matches expected values — without invoking any characteristic function.

**Acceptance Scenarios**:

1. **Given** an intervals tuple `[1, 2, 3, 2, 4, 6]`, **When** `intervals_distribution` is called, **Then** it returns an array of length 6 where index `i` holds the count of value `i+1` in the tuple (`[1, 2, 1, 1, 0, 1]`).
2. **Given** an empty intervals tuple, **When** `intervals_distribution` is called, **Then** it returns an empty distribution without error.
3. **Given** a tuple where all intervals are equal, **When** `intervals_distribution` is called, **Then** only one position in the distribution is non-zero.

---

### User Story 4 - Full Pipeline Is Consistent with Existing `intervals()` (Priority: P4)

A library user who currently calls `intervals(sequence, binding, mode)` needs assurance that the decomposed pipeline produces the same result for all existing mode combinations. Specifically, the mapping is:

- `mode.lossy` → `chain_mode.boundary` + `tuple_mode.lossy`
- `mode.normal` → `chain_mode.boundary` + `tuple_mode.normal`
- `mode.cycle` → `chain_mode.cycle` + `tuple_mode.normal`
- `mode.redundant` → `chain_mode.boundary` + `tuple_mode.redundant`

**Why this priority**: Without consistency between the old and new paths, users cannot safely adopt the decomposed API, and existing code using `intervals()` plus characteristics could produce different results.

**Independent Test**: Can be fully tested by comparing `intervals(X, b, m)` output with `intervals_tuple(intervals_chain(X, b, chain_mode), b, tuple_mode)` for all four mode mappings on the same input sequence.

**Acceptance Scenarios**:

1. **Given** any 1-D sequence and `mode.lossy`, **When** `intervals(X, b, mode.lossy)` is called **and** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.lossy)` is called, **Then** both produce identical interval arrays.
2. **Given** any 1-D sequence and `mode.normal`, **When** `intervals(X, b, mode.normal)` is called **and** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.normal)` is called, **Then** both produce identical interval arrays.
3. **Given** any 1-D sequence and `mode.cycle`, **When** `intervals(X, b, mode.cycle)` is called **and** `intervals_tuple(intervals_chain(X, b, chain_mode.cycle), b, tuple_mode.normal)` is called, **Then** both produce identical interval arrays.
4. **Given** any 1-D sequence and `mode.redundant`, **When** `intervals(X, b, mode.redundant)` is called **and** `intervals_tuple(intervals_chain(X, b, chain_mode.boundary), b, tuple_mode.redundant)` is called, **Then** both produce identical interval arrays.

---

### User Story 5 - Validate Whether an Array Is a Valid Intervals Chain (Priority: P3)

A library user receiving an intervals chain from an external source needs to verify that the array satisfies the structural properties of a valid intervals chain before passing it to downstream pipeline steps. They need `is_valid_intervals_chain(chain)` as a standalone callable returning a boolean.

**Why this priority**: Structural validation prevents silent errors when invalid data is passed through the pipeline before calling `intervals_tuple` or other downstream steps.

**Independent Test**: Can be fully tested by calling `is_valid_intervals_chain(array)` on both valid chains and known-invalid arrays and verifying the boolean result.

**Acceptance Scenarios**:

1. **Given** an array produced by `intervals_chain` for any valid sequence, binding, and chain_mode, **When** `is_valid_intervals_chain` is called, **Then** it returns `True`.
2. **Given** an array that violates intervals chain structural constraints (e.g., contains zeros, negative values, or values exceeding sequence length), **When** `is_valid_intervals_chain` is called, **Then** it returns `False`.
3. **Given** an empty array, **When** `is_valid_intervals_chain` is called, **Then** it returns `True`.
4. **Given** a non-1D array, **When** `is_valid_intervals_chain` is called, **Then** it returns `False` without raising an exception.

---

### User Story 6 - Each Pipeline Function Has Tests, Inline Documentation, and Benchmarks (Priority: P3)

A library user adopting the decomposed pipeline needs to understand what each function does, validate it is correct for their use case, and have confidence that it performs acceptably for their data volumes. Each new public function must ship with inline documentation (discoverable via help), a complete test suite, and a performance benchmark.

**Why this priority**: Tests, documentation, and benchmarks are the quality gates that make a library function production-ready. Without them, users cannot assess correctness, understand edge cases, or predict performance for large sequences.

**Independent Test**: Can be fully tested by verifying that each function has inline documentation, that the test suite covers all acceptance scenarios and edge cases for that function independently, and that a benchmark entry exists for each function.

**Acceptance Scenarios**:

1. **Given** any of the new pipeline functions, **When** a user calls the built-in help mechanism on it, **Then** a description of the function, its parameters, return value, exceptions, and at least one usage example are returned.
2. **Given** the test suite for a pipeline function, **When** it is run, **Then** it covers all acceptance scenarios defined in this spec for that function independently, without depending on other pipeline stages.
3. **Given** the benchmark suite, **When** run against typical input sizes (small: ≤100 elements, medium: ≤10,000 elements, large: ≤1,000,000 elements), **Then** it reports execution time for each function at each input size.
4. **Given** a function's test suite, **When** run on edge cases (empty input, single element, all-unique elements, all-identical elements), **Then** every edge case defined in this spec for that function passes.

---

### Edge Cases

- What happens when `intervals_chain` receives a non-1D array? The function must raise `Not1DArrayException`.
- What happens when `intervals_chain` receives an invalid `chain_mode` value? It must raise `ValueError`.
- How does each stage handle a sequence with all identical elements? Every position belongs to one element; the chain forms a single long interval sequence.
- What happens when `intervals_distribution` receives a tuple with a single element? It must return a distribution of length equal to that single interval value.
- How does `intervals_tuple` behave with `tuple_mode.redundant` when an element appears only once in the sequence? Both the leading and trailing boundary intervals must still be included per mode definition.
- What does `is_valid_intervals_chain` do when the chain contains values that could match either chain_mode? It must return a deterministic boolean without ambiguity. The structural distinction is mathematically deterministic: in `chain_mode.cycle`, every element's interval group sums to `n`; in `chain_mode.boundary`, this does not hold for all elements.
- What are the expected benchmark thresholds for very large inputs (≥1,000,000 elements)? Performance is not required to meet a specific target but must be measurable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The library MUST expose `intervals_chain` as a publicly callable function that accepts any raw 1-D sequence (strings, integers, or any comparable elements — no pre-ordering required), a binding direction, and a `chain_mode` value (`cycle` or `boundary`) and returns the raw intervals chain as a **plain 1-D ndarray** (no metadata wrapper). The chain values alone are sufficient to determine binding and chain_mode via structural properties.
- **FR-002**: The library MUST expose `intervals_tuple` as a publicly callable function with signature `intervals_tuple(chain, binding, tuple_mode)`. `binding` MUST be an explicit positional parameter (`binding.start` or `binding.end`) matching the direction used to produce `chain`; the function MUST NOT infer binding from chain structure. It MUST apply `tuple_mode` using `binding` to detect boundary intervals: `lossy` drops them, `normal` keeps them as-is, `redundant` expands each into leading and trailing components with trailing values appended in element-appearance order. All six `chain_mode × tuple_mode` combinations are valid.
- **FR-003**: The library MUST expose `intervals_distribution` as a publicly callable function that accepts an intervals tuple and returns the count distribution of interval lengths.
- **FR-004**: The library MUST expose a `chain_mode` enum with two values: `boundary` (treats sequence as finite and bounded) and `cycle` (treats sequence as circular).
- **FR-005**: The library MUST expose a `tuple_mode` enum with three values: `lossy` (drop boundary intervals), `normal` (keep one boundary interval per element), and `redundant` (include both leading and trailing boundary intervals).
- **FR-006**: `intervals_chain`, `intervals_tuple`, `intervals_distribution`, `is_valid_intervals_chain`, and the `chain_mode` and `tuple_mode` enums MUST all be importable from the top-level `foapy` namespace.
- **FR-007**: The result of composing `intervals_chain(X, b, chain_mode.boundary)` → `intervals_tuple(chain, b, tuple_mode.lossy)` MUST be identical to `intervals(X, b, mode.lossy)`.
- **FR-008**: The result of composing `intervals_chain(X, b, chain_mode.boundary)` → `intervals_tuple(chain, b, tuple_mode.normal)` MUST be identical to `intervals(X, b, mode.normal)`.
- **FR-009**: The result of composing `intervals_chain(X, b, chain_mode.cycle)` → `intervals_tuple(chain, b, tuple_mode.normal)` MUST be identical to `intervals(X, b, mode.cycle)`.
- **FR-010**: The result of composing `intervals_chain(X, b, chain_mode.boundary)` → `intervals_tuple(chain, b, tuple_mode.redundant)` MUST be identical to `intervals(X, b, mode.redundant)`.
- **FR-011**: `intervals_chain` MUST raise `Not1DArrayException` when passed a non-1D array; MUST raise `ValueError` for invalid `binding` or `chain_mode` values.
- **FR-012**: `intervals_tuple` MUST raise `ValueError` for invalid `tuple_mode` values and for `binding` values other than `binding.start` or `binding.end`.
- **FR-013**: The existing `intervals()` function MUST remain available and continue to produce identical results to preserve backward compatibility.
- **FR-014**: `intervals_chain`, `intervals_tuple`, and `intervals_distribution` MUST each have a masked-array equivalent in `foapy.ma` that mirrors the core API behaviour for sequences with missing values.
- **FR-015**: The library MUST expose `is_valid_intervals_chain` as a publicly callable function that accepts any array and returns a boolean indicating whether it satisfies the structural properties of a valid intervals chain, without raising exceptions for invalid input.
- **FR-016**: Every new public function MUST have inline documentation covering: description, parameters, return value, exceptions raised, and at least one usage example.
- **FR-017**: Every new public function MUST have a dedicated test module covering all acceptance scenarios, all applicable binding and chain_mode or tuple_mode combinations, and all edge cases defined in this spec.
- **FR-018**: Every new public function MUST have a performance benchmark covering at least three input sizes: small (≤100 elements), medium (≤10,000 elements), and large (≤1,000,000 elements).

### Key Entities

- **chain_mode enum**: Two values — `boundary` (sequence treated as finite; boundary intervals are distances from sequence edges to first/last occurrence) and `cycle` (sequence treated as circular; leading and trailing boundary distances are summed into a single cyclic interval). Controls how `intervals_chain` builds the chain.
- **tuple_mode enum**: Three values — `lossy` (boundary intervals dropped), `normal` (one boundary interval retained per element), `redundant` (both leading and trailing boundary intervals included). Controls how `intervals_tuple` shapes the tuple from the chain.
- **Intervals Chain**: A plain 1-D ndarray of natural numbers representing distances between equal elements in a sequence; indexed by sequence position; computed from a sequence, a binding direction, and a chain_mode; the values alone are sufficient to determine both binding direction and chain_mode via structural mathematical properties (no attached metadata needed).
- **Intervals Tuple**: The boundary-adjusted form of an intervals chain shaped by tuple_mode; length may differ from the chain depending on tuple_mode (lossy reduces, redundant extends); direct input to distribution calculation.
- **Intervals Distribution**: An array indexed by interval length (1-based) where each value is the count of that length's appearances in the intervals tuple; length equals the maximum interval value in the tuple.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All new functions and enums (`intervals_chain`, `intervals_tuple`, `intervals_distribution`, `chain_mode` enum, `tuple_mode` enum, `is_valid_intervals_chain`) are importable from the top-level `foapy` namespace within a single import statement.
- **SC-002**: For all four old-mode-to-new-mode mappings (lossy, normal, cycle, redundant), the decomposed pipeline produces output identical to `intervals()` for 100% of test cases in the existing test suite.
- **SC-003**: All characteristics that previously accepted `intervals()` output continue to produce the same results when given `intervals_tuple` output for the same input — with zero regressions.
- **SC-004**: The pipeline stages match the mathematical definitions in the fundamentals documentation for 100% of documented examples.
- **SC-005**: Each new function has a dedicated test suite that passes independently (without invoking other pipeline stages), covering all binding × chain_mode or tuple_mode combinations and all edge cases defined in this spec.
- **SC-006**: `is_valid_intervals_chain` returns `True` for all chains produced by `intervals_chain` and `False` for all known-invalid test inputs — with 0 false negatives on valid chains.
- **SC-007**: Every new public function has inline documentation accessible via the built-in help mechanism, containing description, parameters, return value, exceptions, and at least one usage example.
- **SC-008**: A benchmark suite exists that measures execution time for each new function at small, medium, and large input sizes, and the results are reproducible.

## Assumptions

- The existing `intervals()` function is kept in the public API unchanged; it may internally delegate to the new primitives or remain as-is.
- The split of `mode` into `chain_mode` and `tuple_mode` is a new public API addition; it does not remove the existing `mode` enum or break any existing call sites.
- All six `chain_mode × tuple_mode` combinations are valid. `chain_mode.cycle + tuple_mode.lossy` and `chain_mode.cycle + tuple_mode.redundant` are new combinations not possible with the old `mode` enum; their behaviour is defined by the uniform boundary-detection algorithm in `intervals_tuple` (check `i - v` outside `[0, n]`): cyclic intervals satisfy this condition and are treated as boundary intervals subject to the same lossy/redundant rules as bounded boundary intervals.
- Characteristics functions continue to accept intervals tuples directly; `intervals_distribution` is a separate analysis step, not a required intermediary for existing characteristics.
- The masked-array variants for `intervals_chain`, `intervals_tuple`, and `intervals_distribution` are in scope; a `foapy.ma` equivalent for `is_valid_intervals_chain` is out of scope unless the masked chain representation requires special handling.
- The intervals chain (plain ndarray) encodes both binding direction and chain_mode in its values deterministically. For `chain_mode.cycle`, every element's interval group sums to `n` (sequence length); for `chain_mode.boundary`, this does not hold for all elements. This is a **proven mathematical property** resulting from the separation of `chain_mode` into `cycle` and `boundary` — not a heuristic or open question.
- Test conventions follow the existing `CharacteristicsTest`-style base classes and `AssertBatch` helpers where applicable.
- Performance benchmarks use the existing benchmarking infrastructure in `docs/development/benchmarks.md`.
- No breaking changes are made to any existing public API signatures.
