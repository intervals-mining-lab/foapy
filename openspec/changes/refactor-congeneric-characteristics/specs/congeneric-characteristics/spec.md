## ADDED Requirements

### Requirement: congeneric-characteristics subpackage
The system MUST expose `foapy.congenerics.characteristics` as a subpackage accessible via `import foapy.congenerics.characteristics` or `from foapy.congenerics import characteristics`. It MUST NOT promote any characteristic function to the `foapy.congenerics` top-level namespace.

#### Scenario: Subpackage import
- **WHEN** a caller runs `import foapy.congenerics.characteristics`
- **THEN** the import succeeds and the module exposes all congeneric characteristic functions

#### Scenario: No top-level promotion
- **WHEN** a caller inspects `dir(foapy.congenerics)`
- **THEN** individual characteristic function names are not present at the top level

### Requirement: Scalar aggregate characteristics (singular names)
The system MUST provide the following functions in `foapy.congenerics.characteristics`, each accepting `intervals_grouped` (a sequence of 1-D arrays, one per congeneric group) and returning a single scalar. Their mathematical definitions MUST be identical to those previously in `foapy.characteristics`:
- `descriptive_information(intervals_grouped, dtype=None)`
- `identifying_information(intervals_grouped, dtype=None)`
- `regularity(intervals_grouped, dtype=None)`
- `uniformity(intervals_grouped, dtype=None)`

#### Scenario: identifying_information matches former foapy.characteristics result
- **WHEN** `foapy.congenerics.characteristics.identifying_information(intervals_grouped)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.identifying_information(intervals_grouped)` returned before this change

#### Scenario: descriptive_information matches former foapy.characteristics result
- **WHEN** `foapy.congenerics.characteristics.descriptive_information(intervals_grouped)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.descriptive_information(intervals_grouped)` returned before this change

#### Scenario: regularity matches former foapy.characteristics result
- **WHEN** `foapy.congenerics.characteristics.regularity(intervals_grouped)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.regularity(intervals_grouped)` returned before this change

#### Scenario: uniformity matches former foapy.characteristics result
- **WHEN** `foapy.congenerics.characteristics.uniformity(intervals_grouped)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.uniformity(intervals_grouped)` returned before this change

### Requirement: Per-symbol array characteristics (plural names)
The system MUST provide the following functions in `foapy.congenerics.characteristics`, each accepting a sequence of congeneric intervals arrays and returning a 1-D numpy array with one value per congeneric group. Their mathematical definitions MUST be identical to those previously in `foapy.characteristics.ma`:
- `arithmetic_means(intervals, dtype=None)`
- `average_remotenesses(intervals, dtype=None)`
- `depths(intervals, dtype=None)`
- `geometric_means(intervals, dtype=None)`
- `identifying_informations(intervals, dtype=None)`
- `periodicities(intervals, dtype=None)`
- `uniformities(intervals, dtype=None)`
- `volumes(intervals, dtype=None)`

#### Scenario: volumes matches former foapy.characteristics.ma.volume result
- **WHEN** `foapy.congenerics.characteristics.volumes(intervals)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.ma.volume(intervals)` returned before this change

#### Scenario: arithmetic_means matches former foapy.characteristics.ma.arithmetic_mean result
- **WHEN** `foapy.congenerics.characteristics.arithmetic_means(intervals)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.ma.arithmetic_mean(intervals)` returned before this change

#### Scenario: identifying_informations matches former foapy.characteristics.ma.identifying_information result
- **WHEN** `foapy.congenerics.characteristics.identifying_informations(intervals)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.ma.identifying_information(intervals)` returned before this change

#### Scenario: periodicities matches former foapy.characteristics.ma.periodicity result
- **WHEN** `foapy.congenerics.characteristics.periodicities(intervals)` is called
- **THEN** the result is numerically identical to what `foapy.characteristics.ma.periodicity(intervals)` returned before this change

#### Scenario: Per-symbol array has one entry per congeneric group
- **WHEN** any plural characteristic function is called with `m` congeneric interval arrays
- **THEN** it returns a 1-D array of length `m`

### Requirement: Removed packages
The system MUST NOT expose `foapy.ma` or `foapy.characteristics.ma` after this change. Importing either MUST raise `ModuleNotFoundError` (or `ImportError`).

#### Scenario: foapy.ma is no longer importable
- **WHEN** a caller runs `import foapy.ma`
- **THEN** it raises `ModuleNotFoundError`

#### Scenario: foapy.characteristics.ma is no longer importable
- **WHEN** a caller runs `from foapy.characteristics import ma`
- **THEN** it raises `ImportError` or `ModuleNotFoundError`

### Requirement: foapy.characteristics retains only flat-interval functions
The system MUST ensure `foapy.characteristics` exposes exactly `arithmetic_mean`, `average_remoteness`, `depth`, `geometric_mean`, `volume` after this change. The functions `descriptive_information`, `identifying_information`, `regularity`, `uniformity` MUST NOT be importable from `foapy.characteristics`.

#### Scenario: Moved functions are not importable from foapy.characteristics
- **WHEN** a caller runs `from foapy.characteristics import descriptive_information`
- **THEN** it raises `ImportError`

#### Scenario: Flat-interval functions remain in foapy.characteristics
- **WHEN** a caller runs `from foapy.characteristics import volume`
- **THEN** the import succeeds and returns the flat-interval scalar function
