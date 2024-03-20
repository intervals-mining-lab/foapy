from foapy.alphabet import alphabet

"""Test list of unique array elements"""


def test_string_values():
    assert alphabet(["a", "c", "c", "e", "d", "a"]) == ["a", "c", "e", "d"]


def test_int_values():
    assert alphabet([0, 1, 2, 3, 4]) == [0, 1, 2, 3, 4]


def test_void():
    assert alphabet([]) == []
