import numpy as np


class chain_mode:
    """
    Chain mode enumeration controlling how ``intervals_chain`` handles sequence boundaries.  # noqa: E501

    When used as a callable ``chain_mode(chain)``, infers the chain mode from the
    structural properties of the intervals chain:

    - ``chain_mode.cycle``: every element's interval group sums to ``n``
    - ``chain_mode.boundary``: not all element groups sum to ``n``

    The detection works by first inferring the binding direction (start vs end) from
    the chain, normalising to a ``binding.start`` perspective, then counting first
    occurrences and verifying the group-sum property.

    For an empty chain, returns ``chain_mode.cycle`` by convention.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    print(foapy.chain_mode.boundary)  # 1
    print(foapy.chain_mode.cycle)     # 2
    ```
    """

    boundary: int = 1
    """Sequence treated as finite; boundary intervals are distances to sequence edges."""  # noqa: E501

    cycle: int = 2
    """Sequence treated as circular; leading and trailing gaps are combined."""

    def __new__(cls, chain):
        """
        Infer the chain mode from the structural properties of a plain 1-D ndarray chain.  # noqa: E501

        Uses the group-sum property: in ``chain_mode.cycle``, every element's interval
        group sums to ``n`` (sequence length), so the total chain sum equals ``n``
        multiplied by the number of unique elements. In ``chain_mode.boundary`` the sum
        is smaller.

        The binding direction is inferred first (``chain[-1] == 1`` implies
        ``binding.end``) so the chain can be normalised before counting first
        occurrences.

        Parameters
        ----------
        chain : array_like
            A 1-D intervals chain produced by ``intervals_chain``.

        Returns
        -------
        int
            ``chain_mode.cycle`` or ``chain_mode.boundary``.
        """
        ar = np.asanyarray(chain, dtype=np.intp).ravel()
        if ar.size == 0:
            return cls.cycle

        n = int(ar.size)

        # Normalise to binding.start perspective so that first-occurrence intervals
        # appear at positions where chain[i] > i (pred = i - chain[i] < 0).
        work = ar[::-1].copy() if (ar[-1] == 1 and ar[0] != 1) else ar

        positions = np.arange(n, dtype=np.intp)
        k = int(np.sum(work > positions))  # number of unique elements
        total = int(np.sum(work))

        if k > 0 and total == n * k:
            return cls.cycle
        return cls.boundary
