class chain_mode:
    """
    Chain mode enumeration controlling how ``intervals_chain`` handles sequence boundaries.  # noqa: E501

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

    def __new__(cls, *args, **kwargs):
        raise TypeError(cls.__name__ + " cannot be instantiated.")
