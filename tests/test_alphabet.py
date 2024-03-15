from ..src.foapy.alphabet import alphabet


def test_alphabet():
    """Test list of unique array elements"""
    # ----test_1----
    assert alphabet(["a", "c", "c", "e", "d", "a"]) == ["a", "c", "e", "d"]
    # ----test_2----
    assert alphabet([0, 1, 2, 3, 4]) == [0, 1, 2, 3, 4]
    # ----test_3----
    assert alphabet([]) == []
