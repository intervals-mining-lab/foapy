## MODIFIED Requirements

### Requirement: Package boundary
The system MUST expose exactly `sequences`, `alphabet`, `order`, `intervals_chains`, `intervals_tuples`, `intervals_distributions`, and `characteristics` from `foapy.congenerics`. The `characteristics` entry MUST be the `foapy.congenerics.characteristics` subpackage. `foapy.congenerics` MUST NOT expose an inverse/reconstruction function. `foapy.ma` is removed and MUST NOT be referenced.

#### Scenario: Submodule-only access
- **WHEN** a caller imports `foapy.congenerics`
- **THEN** exactly the six pipeline functions plus the `characteristics` subpackage are available, and no individual characteristic functions are added to the `foapy.congenerics` top-level namespace

#### Scenario: No inverse function is present
- **WHEN** a caller inspects `foapy.congenerics`'s public API
- **THEN** no reconstruction/inverse function exists in this module

#### Scenario: characteristics subpackage is accessible
- **WHEN** a caller runs `import foapy.congenerics.characteristics`
- **THEN** the import succeeds and `foapy.congenerics.characteristics` is the congeneric characteristics subpackage
