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

#### Scenario: identifying_information computes weighted-log-mean scalar

``` py linenums="1"
import foapy
import numpy as np

source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
CS = foapy.congenerics.sequences(source)
chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
intervals_grouped = [row[row != 0] for row in tuples]

result = foapy.congenerics.characteristics.identifying_information(intervals_grouped)
print(result)
# 1.299309880536629

result = foapy.congenerics.characteristics.identifying_information(intervals_grouped, dtype=np.longdouble)
print(result)
# 1.2993098805366290618
```

#### Scenario: descriptive_information computes 2^H scalar

``` py linenums="1"
import foapy
import numpy as np

source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
CS = foapy.congenerics.sequences(source)
chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
intervals_grouped = [row[row != 0] for row in tuples]

result = foapy.congenerics.characteristics.descriptive_information(intervals_grouped)
print(result)
# 2.4611112617624173

result = foapy.congenerics.characteristics.descriptive_information(intervals_grouped, dtype=np.longdouble)
print(result)
# 2.4611112617624174427
```

#### Scenario: regularity computes geometric-mean / descriptive-information ratio

``` py linenums="1"
import foapy
import numpy as np

source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
CS = foapy.congenerics.sequences(source)
chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
intervals_grouped = [row[row != 0] for row in tuples]

result = foapy.congenerics.characteristics.regularity(intervals_grouped)
print(result)
# 0.9759306487558016

result = foapy.congenerics.characteristics.regularity(intervals_grouped, dtype=np.longdouble)
print(result)
# 0.97593064875580153104
```

#### Scenario: uniformity computes identifying_information minus average_remoteness

``` py linenums="1"
import foapy
import numpy as np

source = np.array(['a', 'b', 'a', 'c', 'a', 'd'])
CS = foapy.congenerics.sequences(source)
chains = foapy.congenerics.intervals_chains(CS, foapy.binding.start, foapy.chain_mode.boundary)
tuples = foapy.congenerics.intervals_tuples(chains, foapy.binding.start, foapy.tuple_mode.normal)
intervals_grouped = [row[row != 0] for row in tuples]

result = foapy.congenerics.characteristics.uniformity(intervals_grouped)
print(result)
# 0.03514946374976957

result = foapy.congenerics.characteristics.uniformity(intervals_grouped, dtype=np.longdouble)
print(result)
# 0.03514946374976969819
```

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

#### Scenario: volumes returns per-symbol product array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.volumes(X)
print(result)
# [16  9 15]
```

#### Scenario: arithmetic_means returns per-symbol arithmetic mean array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.arithmetic_means(X)
print(result)
# [2.5 2.333 3]
```

#### Scenario: identifying_informations returns per-symbol log2-of-mean array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.identifying_informations(X)
print(result)
# [1.32192809 1.22239242 1.5849625 ]
```

#### Scenario: periodicities returns per-symbol geometric/arithmetic mean ratio array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.periodicities(X)
print(result)
# [0.8        0.8914645  0.82207069]
```

#### Scenario: depths returns per-symbol sum-of-log2 array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.depths(X)
print(result)
# [4.        3.169925  3.9068906]
```

#### Scenario: average_remotenesses returns per-symbol mean-of-log2 array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.average_remotenesses(X)
print(result)
# [1.         1.05664167 1.30229687]
```

#### Scenario: geometric_means returns per-symbol geometric mean array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.geometric_means(X)
print(result)
# [2.         2.08008382 2.46621207]
```

#### Scenario: uniformities returns per-symbol identifying_information minus average_remoteness array

``` py linenums="1"
import foapy

X = []
X.append([1, 1, 4, 4])
X.append([3, 1, 3])
X.append([5, 3, 1])

result = foapy.congenerics.characteristics.uniformities(X)
print(result)
# [0.32192809 0.16575075 0.28266564]
```

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
