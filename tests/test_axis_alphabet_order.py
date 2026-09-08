import importlib

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy.core import alphabet, order
from foapy.exceptions import Not1DArrayException

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


def test_explicit_axis_preserves_stable_scalar_factorization():
    source = np.array(["b", "a", "b", "c"])

    assert_array_equal(alphabet(source, axis=0), ["b", "a", "c"])
    assert_array_equal(order(source, axis=-1), [0, 1, 0, 2])


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_1d_calls_do_not_use_multidimensional_factorizer(monkeypatch, axis):
    alphabet_module = importlib.import_module("foapy.core._alphabet")
    order_module = importlib.import_module("foapy.core._order")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered multidimensional factorization")

    monkeypatch.setattr(alphabet_module, "stable_factorize", fail)
    monkeypatch.setattr(order_module, "stable_factorize", fail)

    source = np.array(["b", "a", "b", "c"])
    assert_array_equal(alphabet(source, axis=axis), ["b", "a", "c"])
    result, result_alphabet = order(source, True, axis=axis)
    assert_array_equal(result, [0, 1, 0, 2])
    assert_array_equal(result_alphabet, ["b", "a", "c"])


@pytest.mark.parametrize(
    ("axis", "expected_order", "expected_alphabet"),
    [
        (
            0,
            [0, 1, 0],
            [["a", "b", "a", "x"], ["c", "d", "c", "y"]],
        ),
        (
            1,
            [0, 1, 0, 2],
            [["a", "b", "x"], ["c", "d", "y"], ["a", "b", "x"]],
        ),
    ],
)
def test_2d_slice_elements(axis, expected_order, expected_alphabet):
    source = np.array(
        [
            ["a", "b", "a", "x"],
            ["c", "d", "c", "y"],
            ["a", "b", "a", "x"],
        ]
    )

    result, result_alphabet = order(source, True, axis=axis)

    assert_array_equal(result, expected_order)
    assert_array_equal(result_alphabet, expected_alphabet)
    assert_array_equal(alphabet(source, axis=axis), result_alphabet)
    assert_array_equal(np.take(result_alphabet, result, axis=axis), source)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_3d_slice_elements_on_every_axis(axis):
    source_alphabet = np.take(np.arange(12).reshape(2, 2, 3), [0, 1], axis=axis)
    source = np.take(source_alphabet, [1, 0, 1], axis=axis)
    expected_alphabet = np.take(source_alphabet, [1, 0], axis=axis)

    result, result_alphabet = order(source, True, axis=axis)

    assert result.shape == (3,)
    assert result.dtype == np.dtype(np.intp)
    assert_array_equal(result, [0, 1, 0])
    assert_array_equal(result_alphabet, expected_alphabet)
    assert_array_equal(np.take(result_alphabet, result, axis=axis), source)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source = np.take(np.arange(12).reshape(2, 2, 3), [1, 0, 1], axis=axis)
    negative_axis = axis - source.ndim

    positive_order, positive_alphabet = order(source, True, axis=axis)
    negative_order, negative_alphabet = order(source, True, axis=negative_axis)

    assert_array_equal(negative_order, positive_order)
    assert_array_equal(negative_alphabet, positive_alphabet)


def test_first_appearance_order_is_not_sorted_order():
    source = np.array([[9, 9], [1, 1], [9, 9], [5, 5]])

    result, result_alphabet = order(source, True, axis=0)

    assert_array_equal(result, [0, 1, 0, 2])
    assert_array_equal(result_alphabet, [[9, 9], [1, 1], [5, 5]])


@pytest.mark.parametrize(
    ("shape", "axis"),
    [((0, 2), 0), ((2, 0), 1), ((2, 0, 3), 1)],
)
def test_empty_sequence_axis(shape, axis):
    source = np.empty(shape, dtype=np.int64)

    result, result_alphabet = order(source, True, axis=axis)

    assert result.shape == (0,)
    assert result.dtype == np.dtype(np.intp)
    assert result_alphabet.shape == shape
    assert result_alphabet.dtype == source.dtype


@pytest.mark.parametrize(("shape", "axis"), [((3, 0), 0), ((0, 3), 1)])
def test_structurally_empty_slices_are_one_repeated_element(shape, axis):
    source = np.empty(shape, dtype=np.float64)

    result, result_alphabet = order(source, True, axis=axis)

    assert_array_equal(result, [0, 0, 0])
    expected_shape = list(shape)
    expected_shape[axis] = 1
    assert result_alphabet.shape == tuple(expected_shape)
    assert_array_equal(np.take(result_alphabet, result, axis=axis), source)


@pytest.mark.parametrize("function", [alphabet, order])
def test_multidimensional_input_without_axis_keeps_legacy_error(function):
    with pytest.raises(Not1DArrayException):
        function(np.array([[1, 2], [3, 4]]))


@pytest.mark.parametrize("function", [alphabet, order])
def test_scalar_input_is_rejected(function):
    with pytest.raises(Not1DArrayException):
        function(np.array(1), axis=0)


@pytest.mark.parametrize("function", [alphabet, order])
@pytest.mark.parametrize("axis", [-3, 2])
def test_out_of_range_axis_raises_numpy_axis_error(function, axis):
    with pytest.raises(AxisError):
        function(np.ones((2, 2)), axis=axis)


def test_numeric_and_string_dtypes_are_preserved():
    numeric = np.array([[2, 1], [3, 4], [2, 1]], dtype=np.int16)
    strings = np.array([["b", "a"], ["c", "d"], ["b", "a"]])

    assert alphabet(numeric, axis=0).dtype == numeric.dtype
    assert alphabet(strings, axis=0).dtype == strings.dtype
