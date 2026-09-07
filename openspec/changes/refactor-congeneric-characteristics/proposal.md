## Why

`foapy.ma` duplicates the congeneric concept now owned by `foapy.congenerics`, and `foapy.characteristics` contains functions that already require grouped/congeneric input, making them misplaced. Consolidating these into `foapy.congenerics.characteristics` aligns the package structure with the actual computational model.

## What Changes

- **New** `foapy.congenerics.characteristics` subpackage added to `foapy.congenerics`
- **Moved** from `foapy.characteristics` → `foapy.congenerics.characteristics` (name unchanged, scalar aggregates over congeneric groups):
  - `descriptive_information`
  - `identifying_information`
  - `regularity`
  - `uniformity`
- **Moved + renamed** from `foapy.characteristics.ma` → `foapy.congenerics.characteristics` (plural names, per-symbol arrays):
  - `arithmetic_mean` → `arithmetic_means`
  - `average_remoteness` → `average_remotenesses`
  - `depth` → `depths`
  - `geometric_mean` → `geometric_means`
  - `identifying_information` → `identifying_informations`
  - `periodicity` → `periodicities`
  - `uniformity` → `uniformities`
  - `volume` → `volumes`
- **BREAKING** `foapy.ma` removed (superseded by `foapy.congenerics`)
- **BREAKING** `foapy.characteristics.ma` removed (superseded by `foapy.congenerics.characteristics`)
- **BREAKING** `foapy.characteristics.descriptive_information`, `.identifying_information`, `.regularity`, `.uniformity` removed from `foapy.characteristics`
- Tests and docs updated throughout; no deprecation cycle

## Capabilities

### New Capabilities

- `congeneric-characteristics`: Per-symbol and aggregate characteristics for congeneric interval decompositions, exposed as `foapy.congenerics.characteristics`

### Modified Capabilities

- `congeneric-decomposition`: Public API extended — `foapy.congenerics` now exposes a `characteristics` subpackage

## Impact

- `src/foapy/ma/` — deleted entirely
- `src/foapy/characteristics/ma/` — deleted entirely
- `src/foapy/characteristics/__init__.py` — removes `descriptive_information`, `identifying_information`, `regularity`, `uniformity` and the `ma` subpackage
- `src/foapy/congenerics/` — gains `characteristics/` subpackage
- `src/foapy/__init__.py` — removes `ma` from `__foapy_submodules__`
- `tests/test_ma_*.py` — deleted (congenerics already tested)
- `tests/test_characteristics/test_ma_*.py` — replaced with `test_congenerics_characteristics/test_*s.py` (plural names)
- `tests/test_characteristics/test_descriptive_information.py`, `test_identifying_information.py`, `test_regularity.py`, `test_uniformity.py` — moved to `test_congenerics_characteristics/`
- Docs: all `foapy.ma` and `foapy.characteristics.ma` references updated
