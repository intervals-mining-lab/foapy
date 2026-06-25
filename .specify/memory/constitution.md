<!--
SYNC IMPACT REPORT
==================
Version change: [unversioned template] → 1.0.0
Modified principles: N/A (initial ratification)
Added sections:
  - Core Principles (I–V)
  - Development Workflow
  - Quality Gates
  - Governance
Removed sections: N/A
Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check section already present; gates now concrete
  ✅ .specify/templates/spec-template.md — Success Criteria / Performance Goals align with Principles IV and V
  ✅ .specify/templates/tasks-template.md — Polish phase tasks align with Principles I–IV
  ✅ .specify/templates/constitution-template.md — source template; no changes needed
Deferred TODOs: none
-->

# FoaPy Constitution

## Core Principles

### I. Code Quality

Every module in `src/foapy/` MUST be clean, minimal, and directly purposeful.

- Each function MUST have a single, well-defined responsibility. Multi-responsibility functions MUST be split.
- Public API MUST be free of implementation-internal state; functions MUST be pure where possible.
- No third-party runtime dependency beyond `numpy >= 1.20` may be introduced without explicit approval.
- Code MUST pass `black`, `isort`, and `flake8` (enforced via `pre-commit`) before any merge.
- Complexity MUST be justified in the plan's Complexity Tracking table; unexplained complexity is a
  constitution violation.

**Rationale**: FoaPy is a scientific library; correctness and auditability depend on readable,
minimal code. Dependency creep degrades portability for scientific users who manage environments carefully.

### II. Testing Standards

All behavioral changes MUST be covered by tests before the implementation is merged.

- Tests MUST use `tox -e default` as the canonical test runner; no ad-hoc test invocations substitute.
- Characteristics tests MUST extend `CharacteristicsTest` and use `AssertCase`/`AssertBatch` helpers; plain
  `assert` MUST NOT be used for floating-point comparisons.
- `AssertBatch` MUST cover all `binding × mode` combinations whenever a characteristic depends on
  `binding` or `mode`.
- New core pipeline functions (`order`, `intervals`, `intervals_chain`, `intervals_tuple`) MUST have
  tests for: empty input, single-element input, all-unique symbols, all-same symbol, and at least one
  realistic dataset.
- `foapy.ma` variants MUST include masked-value edge-case tests (fully masked, partially masked,
  no-mask passthrough).

**Rationale**: Numerical libraries silently produce wrong results when floating-point edge cases go
untested. The `CharacteristicsTest` helpers enforce epsilon tolerance uniformly and prevent
test-maintenance drift.

### III. API Consistency

The public API MUST follow a uniform contract across all modules and sub-packages.

- Core functions MUST accept a 1-D array-like `X` as their first positional argument.
- `binding` and `mode` MUST be passed as keyword arguments using the `binding` and `mode` enums; raw
  integer or string literals for these parameters MUST NOT appear in library code.
- `foapy.ma` MUST mirror every public function in `foapy.core` with an identical signature; behavioral
  differences MUST be limited to masked-value handling.
- Exceptions MUST use the project-defined types (`Not1DArrayException`, `InconsistentOrderException`);
  bare `ValueError`/`TypeError` MUST NOT be raised for user-input errors.
- Function return shapes MUST be documented with numpy dtype and dimension annotations in the docstring.

**Rationale**: Library users compose functions across `foapy.core` and `foapy.ma`; inconsistent
signatures force defensive branching in caller code and break the substitution principle.

### IV. Performance Requirements

All computations on sequences MUST use vectorized numpy operations; Python-level loops over array
elements are prohibited.

- Operations on sequences up to length 10 000 MUST complete in < 100 ms on a single CPU core (no GPU
  assumption).
- Memory allocation MUST be O(n) or better in sequence length; hidden quadratic allocations MUST be
  eliminated before merge.
- Performance-sensitive paths (interval extraction, characteristic computation) MUST avoid
  `numpy.vectorize` (which is a disguised Python loop) and MUST prefer `numpy.where`, boolean indexing,
  `numpy.diff`, `numpy.unique`, or equivalent C-backed ufuncs.
- If a vectorized solution genuinely cannot express a required algorithm, a fallback loop MUST be
  documented with a complexity note and flagged in the Complexity Tracking table.

**Rationale**: FoaPy targets research workflows where sequences can be large and many characteristics
are computed in a batch. Python loops at the inner level produce unacceptable runtimes.

### V. Simplicity

The simplest correct implementation MUST be preferred over clever or over-engineered alternatives.

- YAGNI applies: features, parameters, and abstractions not required by the current specification MUST
  NOT be added speculatively.
- Characteristics MUST be thin functions over numpy operations — no base class, no shared mutable state.
- Helper utilities MUST only be extracted when the same logic appears in three or more independent call
  sites; single-use helpers MUST be inlined.
- Backwards-compatibility shims (re-exports, deprecated aliases, unused `_vars`) MUST NOT be added
  unless a versioned deprecation policy is explicitly documented.

**Rationale**: FoaPy is a scientific primitive; downstream code depends on its stability. Unused
abstractions become maintenance burdens and obscure the mathematical intent of the code.

## Development Workflow

Standard commands for all contributors:

| Task | Command |
|------|---------|
| Run full test suite | `tox -e default` |
| Run single test file | `tox -e default -- tests/path/to/test.py -v` |
| Run by keyword | `tox -e default -- -k <keyword> -q` |
| Lint (black, isort, flake8) | `pipx run pre-commit run --all-files --show-diff-on-failure` |
| Build distribution | `tox -e clean,build` |
| Build and serve docs | `tox -e docs && tox -e docsserve` |

All contributors MUST run linting and the full test suite locally before opening a pull request.
CI MUST be green before merge; no exceptions.

## Quality Gates

The following gates MUST pass before any feature branch is merged to `main`:

1. **Lint gate**: `pre-commit` passes with zero violations (black, isort, flake8).
2. **Test gate**: `tox -e default` passes with zero test failures or errors.
3. **Constitution check**: The plan's Constitution Check section has no open violations, or each
   violation is documented with a justification in the Complexity Tracking table.
4. **API consistency check**: Any new public function mirrors the signature contract defined in
   Principle III; `foapy.ma` parity is maintained.
5. **Performance check**: Any new sequence-processing path uses vectorized numpy; no Python loops over
   array elements without a documented justification.

## Governance

This constitution supersedes all other development practices and guidelines for the FoaPy project.
In conflicts between this document and any other guidance, the constitution prevails.

**Amendment procedure**:

1. Propose the amendment as a pull request modifying this file.
2. State the version bump (MAJOR/MINOR/PATCH) and rationale.
3. Update the Sync Impact Report comment at the top of this file.
4. Propagate changes to affected templates (plan, spec, tasks) in the same PR.
5. Obtain at least one maintainer approval before merging.

**Versioning policy**:

- MAJOR: backward-incompatible governance changes (principle removal or redefinition).
- MINOR: new principle or section added, or materially expanded guidance.
- PATCH: clarifications, wording fixes, non-semantic refinements.

**Compliance review**: All PRs MUST verify adherence to the Quality Gates above. Reviewers are
expected to call out constitution violations explicitly; authors are expected to resolve them before
merge, not after.

**Version**: 1.0.0 | **Ratified**: 2026-03-28 | **Last Amended**: 2026-03-28
