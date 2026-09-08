## 1. Create foapy.congenerics.characteristics subpackage

- [x] 1.1 Create `src/foapy/congenerics/characteristics/` directory with `__init__.py` exporting all congeneric characteristic functions
- [x] 1.2 Move `src/foapy/characteristics/_descriptive_information.py` → `src/foapy/congenerics/characteristics/_descriptive_information.py`; update internal imports (`from foapy.characteristics import identifying_information` → `from foapy.congenerics.characteristics import identifying_information`)
- [x] 1.3 Move `src/foapy/characteristics/_identifying_information.py` → `src/foapy/congenerics/characteristics/_identifying_information.py`; verify no internal imports need updating
- [x] 1.4 Move `src/foapy/characteristics/_regularity.py` → `src/foapy/congenerics/characteristics/_regularity.py`; update internal imports (`from foapy.characteristics import descriptive_information, geometric_mean` → appropriate new paths)
- [x] 1.5 Move `src/foapy/characteristics/_uniformity.py` (the grouped version) → `src/foapy/congenerics/characteristics/_uniformity.py`; update internal imports

## 2. Move and rename characteristics.ma functions to congenerics.characteristics

- [x] 2.1 Copy `src/foapy/characteristics/ma/_arithmetic_mean.py` → `src/foapy/congenerics/characteristics/_arithmetic_means.py`; rename function to `arithmetic_means`; update docstring
- [x] 2.2 Copy `src/foapy/characteristics/ma/_average_remoteness.py` → `src/foapy/congenerics/characteristics/_average_remotenesses.py`; rename function to `average_remotenesses`; update docstring and internal imports
- [x] 2.3 Copy `src/foapy/characteristics/ma/_depth.py` → `src/foapy/congenerics/characteristics/_depths.py`; rename function to `depths`; update docstring and internal imports
- [x] 2.4 Copy `src/foapy/characteristics/ma/_geometric_mean.py` → `src/foapy/congenerics/characteristics/_geometric_means.py`; rename function to `geometric_means`; update docstring and internal imports
- [x] 2.5 Copy `src/foapy/characteristics/ma/_identifying_information.py` → `src/foapy/congenerics/characteristics/_identifying_informations.py`; rename function to `identifying_informations`; update docstring
- [x] 2.6 Copy `src/foapy/characteristics/ma/_periodicity.py` → `src/foapy/congenerics/characteristics/_periodicities.py`; rename function to `periodicities`; update docstring and internal imports
- [x] 2.7 Copy `src/foapy/characteristics/ma/_uniformity.py` → `src/foapy/congenerics/characteristics/_uniformities.py`; rename function to `uniformities`; update docstring and internal imports
- [x] 2.8 Copy `src/foapy/characteristics/ma/_volume.py` → `src/foapy/congenerics/characteristics/_volumes.py`; rename function to `volumes`; update docstring

## 3. Update docstring examples in moved files

- [x] 3.1 In all moved scalar aggregate files, replace `foapy.ma.order` / `foapy.ma.intervals` examples with `foapy.congenerics` pipeline equivalents
- [x] 3.2 In all plural array files, replace `foapy.characteristics.ma.*` import examples with `foapy.congenerics.characteristics.*`

## 4. Update foapy.characteristics package

- [x] 4.1 Remove `descriptive_information`, `identifying_information`, `regularity`, `uniformity` from `src/foapy/characteristics/__init__.py` exports and `__all__`
- [x] 4.2 Delete `src/foapy/characteristics/_descriptive_information.py`, `_identifying_information.py`, `_regularity.py`, `_uniformity.py` (the moved originals)
- [x] 4.3 Delete `src/foapy/characteristics/ma/` directory entirely

## 5. Update foapy.congenerics package

- [x] 5.1 Add `characteristics` to `src/foapy/congenerics/__init__.py` as a lazy-loaded submodule (mirroring how `foapy.__init__.py` exposes submodules)

## 6. Remove foapy.ma package

- [x] 6.1 Delete `src/foapy/ma/` directory entirely
- [x] 6.2 Remove `ma` from `__foapy_submodules__` in `src/foapy/__init__.py`
- [x] 6.3 Remove the `ma` case from `foapy.__getattr__` in `src/foapy/__init__.py`
- [x] 6.4 Remove `ma` from `__all__` and `__dir__` in `src/foapy/__init__.py`

## 7. Update tests — remove foapy.ma tests

- [x] 7.1 Delete `tests/test_ma_order.py`
- [x] 7.2 Delete `tests/test_ma_alphabet.py`
- [x] 7.3 Delete `tests/test_ma_intervals.py`
- [x] 7.4 Delete `tests/test_ma_intervals_chain.py`
- [x] 7.5 Delete `tests/test_ma_intervals_tuple.py`
- [x] 7.6 Delete `tests/test_ma_intervals_distribution.py`
- [x] 7.7 Keep `tests/helpers/ma_intervals.py` — no `foapy.ma` imports; still used by congenerics characteristics tests

## 8. Update tests — migrate characteristics.ma tests

- [x] 8.1 Create `tests/test_congenerics_characteristics/` directory
- [x] 8.2 Move and update `tests/test_characteristics/test_ma_volume.py` → `tests/test_congenerics_characteristics/test_volumes.py`; update import to `from foapy.congenerics.characteristics import volumes`; rename test class/methods to reflect plural name
- [x] 8.3 Move and update `tests/test_characteristics/test_ma_arithmetic_mean.py` → `tests/test_congenerics_characteristics/test_arithmetic_means.py`
- [x] 8.4 Move and update `tests/test_characteristics/test_ma_average_remoteness.py` → `tests/test_congenerics_characteristics/test_average_remotenesses.py`
- [x] 8.5 Move and update `tests/test_characteristics/test_ma_depth.py` → `tests/test_congenerics_characteristics/test_depths.py`
- [x] 8.6 Move and update `tests/test_characteristics/test_ma_geometric_mean.py` → `tests/test_congenerics_characteristics/test_geometric_means.py`
- [x] 8.7 Move and update `tests/test_characteristics/test_ma_identifying_information.py` → `tests/test_congenerics_characteristics/test_identifying_informations.py`
- [x] 8.8 Move and update `tests/test_characteristics/test_ma_periodicity.py` → `tests/test_congenerics_characteristics/test_periodicities.py`
- [x] 8.9 Move and update `tests/test_characteristics/test_ma_uniformity.py` → `tests/test_congenerics_characteristics/test_uniformities.py`

## 9. Update tests — migrate scalar aggregate characteristic tests

- [x] 9.1 Move `tests/test_characteristics/test_descriptive_information.py` → `tests/test_congenerics_characteristics/test_descriptive_information.py`; update import to `from foapy.congenerics.characteristics import descriptive_information`
- [x] 9.2 Move `tests/test_characteristics/test_identifying_information.py` → `tests/test_congenerics_characteristics/test_identifying_information.py`; update import
- [x] 9.3 Move `tests/test_characteristics/test_regularity.py` → `tests/test_congenerics_characteristics/test_regularity.py`; update import
- [x] 9.4 Move `tests/test_characteristics/test_uniformity.py` → `tests/test_congenerics_characteristics/test_uniformity.py`; update import

## 10. Update docs

- [x] 10.1 Search all docs files for `foapy.ma` references and replace with `foapy.congenerics` equivalents
- [x] 10.2 Search all docs files for `foapy.characteristics.ma` references and replace with `foapy.congenerics.characteristics` equivalents (using plural function names)
- [x] 10.3 Update API reference pages for the `characteristics` module to remove moved functions
- [x] 10.4 Add API reference page for `foapy.congenerics.characteristics`

## 11. Verify

- [x] 11.1 Run `tox -e default` — all tests pass (465 passed)
- [x] 11.2 Run `pre-commit run --all-files` — lint passes (isort, black, flake8 all pass)
- [x] 11.3 Verify `import foapy.ma` raises `ModuleNotFoundError` ✓
- [x] 11.4 Verify `from foapy.characteristics import descriptive_information` raises `ImportError` ✓
- [x] 11.5 Verify `import foapy.congenerics.characteristics` succeeds and all 12 functions are accessible ✓

## 12. Remove foapy.ma benchmarks

- [x] 12.1 Delete `benchmarks/benchmarks/bench_ma_alphabet.py`
- [x] 12.2 Delete `benchmarks/benchmarks/bench_ma_intervals.py`
- [x] 12.3 Delete `benchmarks/benchmarks/bench_ma_order.py`
- [x] 12.4 Delete `benchmarks/benchmarks/ma_cases.py`
