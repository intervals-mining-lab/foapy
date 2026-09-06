import numpy.ma as ma

from foapy.core._intervals_chain import intervals_chain as core_intervals_chain


def intervals_chain(X, binding: int, chain_mode: int):
    """
    Compute an intervals chain from a masked 1-D sequence.

    Masked (missing) values in *X* are skipped; intervals are computed over
    the compressed sequence of unmasked elements only.

    Parameters
    ----------
    X : masked_array
        1-D masked array.  Masked positions are treated as absent elements.
    binding : int
        ``binding.start`` or ``binding.end``.
    chain_mode : int
        ``chain_mode.boundary`` or ``chain_mode.cycle``.

    Returns
    -------
    ndarray
        Plain 1-D integer array (same as :func:`foapy.core.intervals_chain`
        applied to the compressed, unmasked sub-sequence).

    Raises
    ------
    Not1DArrayException
        When the underlying compressed sequence is not 1-dimensional.
    ValueError
        When ``binding`` or ``chain_mode`` is invalid.
    """
    ar = ma.asarray(X)
    compressed = ar.compressed()
    return core_intervals_chain(compressed, binding, chain_mode)
