## Context

Core `alphabet` and `order` currently accept only one-dimensional arrays and implement the same stable factorization separately: alphabet values are unique scalar elements ordered by first appearance, and order values are the inverse indices into that alphabet. Partials compress masked positions, delegate factorization to core, and scatter order values back into a masked one-dimensional result.

The new model generalizes a sequence position from a scalar to a complete orthogonal slice. For input shape `(d0, ..., da, ..., dn)` and sequence axis `a`, there are `da` sequence elements, each with shape `(d0, ..., d(a-1), d(a+1), ..., dn)`. The order therefore remains one-dimensional with length `da`; the alphabet retains the input rank and replaces `da` with the number of unique slices.

The core coupling is expressed by the dense reconstruction invariant:

```python
order_result, alphabet_result = order(X, return_alphabet=True, axis=a)
restored = np.take(alphabet_result, order_result, axis=a)
```

`restored` must equal `X` exactly.

## Goals / Non-Goals

**Goals:**

- Give core and partials alphabet/order one shared, stable factorization model for scalar and slice elements.
- Keep order one-dimensional regardless of input rank.
- Preserve the alphabet axis so `numpy.take` is the inverse operation for dense inputs.
- Preserve existing one-dimensional calls and positional arguments.
- Define partial gaps at the same sequence-position granularity as dense slice elements.
- Cover multidimensional behavior, validation, reconstruction, documentation, and performance with tests and benchmarks.

**Non-Goals:**

- Axis support for interval-chain, interval-tuple, distribution, congeneric, or characteristic functions.
- Applying the one-dimensional function independently to every row or column as `numpy.apply_along_axis` does.
- Ragged batches, padded alphabets, or masked padding.
- Flattening multidimensional input when `axis` is omitted.
- Representing a sequence element whose internal scalar components are only partially present.

## Decisions

### Axis selects a sequence of complete orthogonal slices

Normalize an explicit axis and conceptually move it to the front:

```python
elements = np.moveaxis(X, axis, 0)
```

`elements[i]` is one indivisible alphabet element. Equality means equality of the complete slices, not independent element-wise factorization along multiple one-dimensional lines.

This follows NumPy's record-axis model used by `numpy.unique(..., axis=axis)` and directly supports the reconstruction invariant. The rejected alternative was apply-along-axis semantics, which would produce one order per orthogonal coordinate and ragged alphabets requiring padding.

### A shared private factorization primitive drives both public functions

Implement one internal routine that returns both the one-dimensional inverse order and the stable alphabet. `core.alphabet` selects the alphabet result; `core.order` selects the order and optionally returns the same alphabet. This prevents differences in equality, stable ordering, empty handling, dtype, or axis placement between the coupled APIs.

The routine will move the selected axis to the front for comparison, flatten only the orthogonal dimensions into record fields, group equal records with stable first-occurrence bookkeeping, select original slices for the alphabet, and move the alphabet axis back to its original position. Sorting/grouping must not leak sorted order into the public alphabet.

Using `numpy.apply_along_axis` was rejected because it expresses independent sequences rather than slice elements. Returning `numpy.unique(..., axis=axis)` directly was rejected because its alphabet is sorted rather than ordered by first appearance; it may still inform or support the internal grouping algorithm if its indices and inverse are remapped to stable order without narrowing supported dtypes.

### Axis is keyword-only and omission preserves the legacy contract

Use these signatures:

```python
alphabet(X, *, axis=None)
order(X, return_alphabet=False, *, axis=None)
```

and equivalent signatures in `foapy.partials`. Keeping `return_alphabet` in its current positional slot preserves calls such as `order(X, True)`. Making the new parameter keyword-only avoids interpreting existing boolean arguments as axes.

When `axis is None`, require a one-dimensional input and use axis 0 internally. This preserves current results and multidimensional `Not1DArrayException` behavior. An explicit axis opts into slice elements; negative axes are normalized through NumPy's axis utilities. Zero-dimensional inputs are not sequences and are rejected.

`axis=None` flattening was rejected because it silently changes the existing multidimensional error contract and destroys the distinction between structured slice elements and scalar elements.

### The alphabet retains rank and axis placement; order does not

For input shape `(d0, ..., da, ..., dn)` with `k` unique slice elements:

```text
order.shape    = (da,)
alphabet.shape = (d0, ..., k, ..., dn)
```

Keeping the alphabet axis at `a` makes `np.take(alphabet, order, axis=a)` work uniformly for axis 0, interior axes, and the last axis. Moving the alphabet axis to the front in the public result was rejected because callers would need additional axis metadata or a second move operation to reconstruct the source.

### Partial masks describe whole missing sequence positions

After moving the sequence axis to the front, each slice mask must be uniform: all false means a present slice element and all true means a gap. Mixed masks are rejected with `ValueError`, because a one-dimensional order mask cannot faithfully state that only part of an indivisible element exists and a plain ndarray alphabet cannot preserve component masks.

Partials factorize only present slices through the shared core primitive, scatter their inverse indices into a one-dimensional buffer, and use the whole-slice gap vector as the result mask. The partial alphabet remains a plain ndarray and excludes gaps. For non-gap inputs it has exact parity with core.

Allowing partially masked slice fields was rejected because it would require a masked alphabet, define nontrivial record equality for missing fields, and weaken the simple order/alphabet reconstruction model. Treating any partially masked slice as a total gap was rejected because it silently discards observed data.

### Reconstruction for partials is defined over observed slices

For a nonempty partial alphabet, callers can take with the order's underlying or filled indices and then broadcast the one-dimensional order mask across all orthogonal dimensions. The resulting masked array reconstructs every observed slice and the original whole-slice gap pattern; data stored beneath gaps is intentionally not part of the partial-sequence value.

The documentation will provide a helper-sized example rather than claim that bare `numpy.take` propagates a masked index array across every component of a slice.

## Risks / Trade-offs

- **Slice comparison can allocate a large temporary view or index arrays** → Move axes as views where possible, flatten only for comparison, select alphabet values from the original array, and benchmark time and peak memory across axis placements and record widths.
- **NumPy record uniqueness has dtype-specific limitations** → Preserve the current sortable-value contract, test the currently documented numeric and string inputs, and avoid relying on a narrower helper without a compatible fallback or an explicit error.
- **Mixed masks may be useful as structured records in the future** → Reject them clearly now; a later capability can define masked fields and a masked-alphabet return type without changing whole-slice gap semantics.
- **A keyword-only axis differs from some NumPy signatures** → It protects the established positional `return_alphabet` API and all examples still use the familiar `axis=` spelling.
- **Empty orthogonal dimensions make every non-gap slice structurally empty** → Define and test grouping explicitly so multiple empty slices compare consistently and still satisfy reconstruction shapes.

## Migration Plan

1. Introduce the shared private dense factorization primitive and route existing one-dimensional core calls through it while retaining their tests.
2. Add explicit-axis behavior and reconstruction tests to core alphabet/order.
3. Extend partials mask validation, compression, scattering, and alphabet-axis restoration.
4. Update API documentation and benchmarks.
5. Run the focused suites followed by the full test and documentation checks.

Rollback consists of reverting the optional keyword and generalized helper paths; existing callers require no migration because omitted-axis behavior remains unchanged.

## Open Questions

None. The proposal fixes the axis meaning, output shapes, stable order, reconstruction rule, default behavior, and partial mask granularity.
