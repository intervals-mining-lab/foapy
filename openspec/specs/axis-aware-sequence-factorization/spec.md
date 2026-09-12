# Purpose

Define axis-aware alphabet extraction and sequence ordering for dense arrays while preserving the legacy one-dimensional API.

## Requirements

### Requirement: Core alphabet supports slice elements along an axis
The system MUST provide `foapy.core.alphabet(X, *, axis=None)`. When `axis` is an integer, the function MUST treat the complete orthogonal slice at each position along that axis as one sequence element, return unique slice elements in order of first appearance, preserve the input rank, and replace only the selected axis length with the alphabet size. Both positive and equivalent negative axes MUST produce the same result.

#### Scenario: One-dimensional scalar elements
- **WHEN** `alphabet(['b', 'a', 'b', 'c'], axis=0)` is called
- **THEN** it returns `['b', 'a', 'c']`

#### Scenario: Rows are elements along axis zero
- **WHEN** a two-dimensional input has rows `R0`, `R1`, `R0` and `alphabet(X, axis=0)` is called
- **THEN** it returns the two-row array `R0`, `R1` with shape `(2, X.shape[1])`

#### Scenario: Columns are elements along axis one
- **WHEN** a two-dimensional input has columns `C0`, `C1`, `C0`, `C2` and `alphabet(X, axis=1)` is called
- **THEN** it returns the three columns `C0`, `C1`, `C2` in that order and preserves axis 1 as the alphabet axis

#### Scenario: Planes are elements in a three-dimensional input
- **WHEN** `alphabet()` receives a three-dimensional input and an explicit valid axis
- **THEN** each complete two-dimensional slice indexed along that axis is compared as one element and the result retains all orthogonal dimensions unchanged

#### Scenario: First appearance controls alphabet order
- **WHEN** distinct slice elements have a lexicographic or numeric sort order different from their first occurrence order
- **THEN** the returned alphabet follows first occurrence order rather than sorted order

### Requirement: Core order is the one-dimensional inverse of the alphabet
The system MUST provide `foapy.core.order(X, return_alphabet=False, *, axis=None)`. For an explicit axis, the returned order MUST be a one-dimensional `numpy.intp` array of length `X.shape[axis]`, and each value MUST be the zero-based first-appearance alphabet index of the complete slice at that axis position. When `return_alphabet=True`, the accompanying alphabet MUST equal `foapy.core.alphabet(X, axis=axis)`, and `numpy.take(alphabet, order, axis=axis)` MUST reconstruct the original dense input exactly.

#### Scenario: Repeated rows produce repeated order indices
- **WHEN** a two-dimensional input has rows `R0`, `R1`, `R0` and `order(X, axis=0)` is called
- **THEN** the order is `[0, 1, 0]`

#### Scenario: Repeated columns produce repeated order indices
- **WHEN** a two-dimensional input has columns `C0`, `C1`, `C0`, `C2` and `order(X, axis=1)` is called
- **THEN** the order is `[0, 1, 0, 2]`

#### Scenario: Return alphabet uses the shared factorization
- **WHEN** `order(X, return_alphabet=True, axis=axis)` is called
- **THEN** it returns the same one-dimensional order as `order(X, axis=axis)` and the same alphabet as `alphabet(X, axis=axis)`

#### Scenario: Dense reconstruction
- **WHEN** an order and alphabet are returned for any supported dense input and valid axis
- **THEN** `numpy.take(alphabet, order, axis=axis)` equals the original input in shape, dtype, and values

#### Scenario: Empty sequence axis
- **WHEN** the selected input axis has length zero
- **THEN** order returns an empty `numpy.intp` array and alphabet returns an array whose selected axis has length zero and whose other dimensions match the input

### Requirement: Axis behavior preserves the legacy one-dimensional API
Calls that omit `axis` MUST retain the existing one-dimensional behavior and return types of `foapy.core.alphabet` and `foapy.core.order`. A multidimensional input without an explicit axis MUST continue to raise `Not1DArrayException`; an explicit axis MUST be normalized using NumPy axis conventions, including negative axes, and an out-of-range axis MUST raise NumPy's axis error. Scalar inputs MUST be rejected as non-sequences.

#### Scenario: Existing call without axis remains valid
- **WHEN** an existing caller invokes `alphabet(X)` or `order(X, return_alphabet)` with a one-dimensional input
- **THEN** the result is unchanged from the pre-axis API

#### Scenario: Multidimensional input requires explicit intent
- **WHEN** a multidimensional input is passed without `axis`
- **THEN** the function raises `Not1DArrayException`

#### Scenario: Negative axis is equivalent
- **WHEN** `axis=-1` and its equivalent positive axis select the same dimension
- **THEN** both calls return identical orders and alphabets

#### Scenario: Axis is out of range
- **WHEN** an explicit axis is outside the input dimensionality
- **THEN** the function raises NumPy's axis error

#### Scenario: Scalar input is rejected
- **WHEN** `alphabet()` or `order()` receives a zero-dimensional input
- **THEN** it raises `Not1DArrayException`
