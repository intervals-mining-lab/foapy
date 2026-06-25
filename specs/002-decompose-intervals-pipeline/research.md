# Research: Decompose Intervals Pipeline

**Branch**: `002-decompose-intervals-pipeline` | **Date**: 2026-04-19 (updated)

> **Note**: All implementation decisions have been resolved and the code is in place. Benchmark call-signature bugs in `bench_intervals_tuple.py` and `bench_intervals_distribution.py` remain (see Open Defects in plan.md).

## Decision 1: How binding travels from chain to tuple stage

**Decision**: `intervals_chain` returns a **plain 1-D ndarray**. `binding` is passed as an **explicit parameter** to `intervals_tuple(chain, binding, tuple_mode)`.

**Rationale**: The original plan proposed an `IntervalChain` named tuple to carry `binding` metadata. During implementation it was found that passing `binding` explicitly is simpler (no wrapper type, no metadata unpacking), consistent with the constitution's simplicity principle (V), and keeps `intervals_tuple` a pure function. The named tuple approach was abandoned.

**Alternatives considered**:
- `IntervalChain` named tuple (original plan) — rejected: adds a container type for metadata that callers already have; violates YAGNI; `collections.namedtuple` usage would be a novelty in this codebase.
- Structural detection of binding from chain values — rejected: mathematically unsound for symmetric chains; an open theoretical question per fundamentals documentation.

---

## Decision 2: chain_mode enum design

**Decision**: `chain_mode` class with two integer constants: `chain_mode.boundary = 1` and `chain_mode.cycle = 2`. Pattern mirrors the existing `binding` and `mode` classes.

**Rationale**: Consistent with existing `binding` (start=1, end=2) and `mode` (lossy=1…redundant=4) patterns. Simple class-level integer constants require no import, no metaclass, no enum module, and no runtime overhead. The value assignments are arbitrary; what matters is uniqueness and consistency with the existing pattern.

**Alternatives considered**:
- `enum.IntEnum` — rejected: the project does not use the `enum` module anywhere; introducing it for two new enums would be inconsistent and add a dependency on stdlib enum semantics.
- Reuse `mode.cycle` and a new `mode.boundary` — rejected: this would further entangle the two orthogonal concepts the decomposition is meant to separate.

---

## Decision 3: tuple_mode enum design

**Decision**: `tuple_mode` class with three integer constants: `tuple_mode.lossy = 1`, `tuple_mode.normal = 2`, `tuple_mode.redundant = 3`. Pattern mirrors existing `mode` class.

**Rationale**: Same reasoning as Decision 2. The three values cover all boundary-handling strategies applicable after chain construction. `mode.cycle = 3` from the old enum is NOT included in `tuple_mode` because cycle boundary handling is a chain construction property (chain_mode), not a tuple-shaping property.

**Alternatives considered**:
- Keeping the old `mode` enum and adding a `chain_mode` only — rejected: this leaves tuple-shaping and chain-construction conflated in the same type, defeating the decomposition goal.

---

## Decision 4: Backward compatibility of `intervals()`

**Decision**: `intervals()` is kept unchanged. Internally it may delegate to `intervals_chain` + `intervals_tuple` or remain as a standalone function. The old `mode` enum is kept, with the mapping: `mode.lossy` → `boundary + lossy`, `mode.normal` → `boundary + normal`, `mode.cycle` → `cycle + normal`, `mode.redundant` → `boundary + redundant`.

**Rationale**: Constitution Principle V (Simplicity / YAGNI) and FR-013 both require no breaking changes. The old `mode` enum is retained for backward compatibility. No deprecation shim is introduced; the old and new APIs coexist independently.

---

## Decision 5: Numpy-only implementation (no Python loops)

**Decision**: All array operations in `intervals_chain`, `intervals_tuple`, `intervals_distribution`, and introspection functions MUST use numpy vectorized operations. The existing `intervals.py` implementation already uses `argsort`, boolean masking, and vectorized index arithmetic as the template.

**Rationale**: Constitution Principle IV prohibits Python loops over array elements. The existing `intervals.py` demonstrates the vectorized pattern: `argsort(kind="mergesort")`, `perm[1:] - perm[:-1]` for interior intervals, boolean mask for first/last occurrence detection. These patterns are extended rather than replaced.

**Key numpy patterns to use**:
- `np.argsort(kind="mergesort")` — stable sort for position extraction
- Boolean indexing with `perm[1:] != perm[:-1]` — change detection
- `np.empty` pre-allocation — avoid repeated concatenation
- `np.concatenate` — for redundant mode trailing intervals
- `np.bincount` — for `intervals_distribution` (count occurrences of each interval value)

---

## Decision 6: TDD workflow

**Decision**: For each function, write tests first (failing), then implement to pass, then refactor.

**Test order**:
1. `chain_mode` enum — trivial attribute tests
2. `tuple_mode` enum — trivial attribute tests
3. `intervals_chain` — all scenarios from spec
4. `binding(chain)` — uses `IntervalChain.binding` field
5. `chain_mode(chain)` function — uses `IntervalChain.chain_mode` field
6. `is_valid_intervals_chain` — structural validity checks
7. `intervals_tuple` — all tuple_mode scenarios
8. `intervals_distribution` — count distribution
9. Consistency tests — `intervals()` equivalence for all 4 mode mappings
10. `foapy.ma` variants

**Test structure**: Each new function gets its own test file `tests/test_{function_name}.py` using `unittest.TestCase` and `numpy.testing.assert_array_equal`. No floating-point characteristics involved, so `CharacteristicsTest` helpers are not needed for these tests.

---

## Decision 7: `is_valid_intervals_chain` structural checks

**Decision**: Validates that:
1. Input is 1-D (or 0-D empty)
2. All values are positive integers (≥ 1)
3. All values are ≤ length of the array (no interval can exceed sequence length)
4. The input is an `IntervalChain` named tuple (the primary validity check for pipeline-internal use)

**Rationale**: The named tuple wrapper means that any chain produced by `intervals_chain` is automatically "valid". The structural value checks catch arrays passed by mistake. Returning `False` rather than raising for invalid inputs is per FR-017.

---

## Decision 8: Performance benchmarks location

**Decision**: Benchmarks go in `benchmarks/` at repository root (or `docs/development/benchmarks/` if that directory exists). Each benchmark script measures small (100), medium (10,000), and large (1,000,000) element sequences for each new function.

**Rationale**: The `docs/development/benchmarks.md` page references `./report/index.html`, suggesting benchmarks are run via an external tool (likely `pytest-benchmark` or similar). Until the benchmark infrastructure is confirmed, benchmark scripts will be written as standalone scripts callable independently.
