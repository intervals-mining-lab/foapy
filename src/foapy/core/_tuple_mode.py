class tuple_mode:
    """
    Tuple mode enumeration controlling how ``intervals_tuple`` shapes the boundary
    intervals in an intervals chain into the final intervals tuple.

    Examples
    --------

    ``` py linenums="1"
    import foapy

    print(foapy.tuple_mode.lossy)      # 1
    print(foapy.tuple_mode.normal)     # 2
    print(foapy.tuple_mode.redundant)  # 3
    ```
    """

    lossy: int = 1
    """Drop all boundary intervals (first/last-occurrence distances)."""

    normal: int = 2
    """Keep all intervals as-is (one boundary interval per element)."""

    redundant: int = 3
    """Expand boundary intervals into leading + trailing components."""

    def __new__(cls, *args, **kwargs):
        raise TypeError(cls.__name__ + " cannot be instantiated.")
