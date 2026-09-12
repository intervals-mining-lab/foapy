# FoaPy agent instructions

- Production code under `src/foapy/` MUST NOT contain Python iteration constructs: `for`, `while`, comprehensions, or generator expressions. Use C-backed NumPy operations that process complete arrays or batches instead.
- Do not use `numpy.vectorize`, `numpy.apply_along_axis`, or similar wrappers that merely hide Python iteration.
- Python loops are permitted only in tests and benchmark setup code.
- The project constitution in `.specify/memory/constitution.md` is authoritative and must be followed for every change.
