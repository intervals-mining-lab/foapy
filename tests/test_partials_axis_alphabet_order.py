import importlib

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

from foapy.core import alphabet as core_alphabet
from foapy.core import order as core_order
from foapy.exceptions import Not1DArrayException
from foapy.partials import alphabet, order

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_1d_calls_do_not_use_multidimensional_factorizer(monkeypatch, axis):
    alphabet_module = importlib.import_module("foapy.partials._alphabet")
    order_module = importlib.import_module("foapy.partials._order")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered multidimensional factorization")

    monkeypatch.setattr(alphabet_module, "_stable_partial_factorize", fail)
    monkeypatch.setattr(order_module, "_stable_partial_factorize", fail)

    source = ma.masked_array(["b", "x", "a", "b"], mask=[False, True, False, False])
    assert_array_equal(alphabet(source, axis=axis), ["b", "a"])
    result, result_alphabet = order(source, True, axis=axis)
    assert_equal(result, ma.masked_array([0, 0, 1, 0], mask=source.mask))
    assert_array_equal(result_alphabet, ["b", "a"])


@pytest.mark.parametrize("axis", [0, 1])
def test_plain_2d_input_matches_core(axis):
    source = np.array(
        [
            ["a", "b", "a", "x"],
            ["c", "d", "c", "y"],
            ["a", "b", "a", "x"],
        ]
    )

    result, result_alphabet = order(source, True, axis=axis)

    assert not np.any(ma.getmaskarray(result))
    assert_array_equal(result.compressed(), core_order(source, axis=axis))
    assert_array_equal(result_alphabet, core_alphabet(source, axis=axis))
    assert_array_equal(alphabet(source, axis=axis), result_alphabet)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_whole_slice_gaps_for_3d_inputs(axis):
    dense_alphabet = np.take(np.arange(12).reshape(2, 2, 3), [0, 1], axis=axis)
    source_data = np.take(dense_alphabet, [0, 0, 1, 0], axis=axis)
    source_mask = np.zeros(source_data.shape, dtype=bool)
    gap_index = [slice(None)] * source_data.ndim
    gap_index[axis] = 1
    source_mask[tuple(gap_index)] = True
    source = ma.masked_array(source_data, mask=source_mask)

    result, result_alphabet = order(source, True, axis=axis)

    assert_equal(result, ma.masked_array([0, 0, 1, 0], mask=[0, 1, 0, 0]))
    assert_array_equal(result_alphabet, dense_alphabet)
    assert_array_equal(alphabet(source, axis=axis), dense_alphabet)


def test_masked_first_slice_does_not_control_first_appearance():
    source = ma.masked_array(
        [[1, 1], [3, 3], [1, 1], [2, 2]],
        mask=[[1, 1], [0, 0], [0, 0], [0, 0]],
    )

    result, result_alphabet = order(source, True, axis=0)

    assert_equal(result, ma.masked_array([0, 0, 1, 2], mask=[1, 0, 0, 0]))
    assert_array_equal(result_alphabet, [[3, 3], [1, 1], [2, 2]])


def test_partial_reconstruction_restores_observed_slices_and_gap_mask():
    source = ma.masked_array(
        [[1, 9, 3, 1], [2, 9, 4, 2]],
        mask=[[0, 1, 0, 0], [0, 1, 0, 0]],
    )
    axis = 1

    result, result_alphabet = order(source, True, axis=axis)
    restored_data = np.take(result_alphabet, result.filled(0), axis=axis)
    restored_mask = np.broadcast_to(
        ma.getmaskarray(result).reshape(1, result.size), source.shape
    )
    restored = ma.masked_array(restored_data, mask=restored_mask)

    assert ma.allequal(restored, source)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source_data = np.take(np.arange(12).reshape(2, 2, 3), [0, 1, 0], axis=axis)
    source = ma.masked_array(source_data, mask=False)
    negative_axis = axis - source.ndim

    positive_order, positive_alphabet = order(source, True, axis=axis)
    negative_order, negative_alphabet = order(source, True, axis=negative_axis)

    assert_equal(negative_order, positive_order)
    assert_array_equal(negative_alphabet, positive_alphabet)


def test_fully_masked_input_returns_axis_preserving_empty_alphabet():
    source = ma.masked_array(np.arange(12).reshape(2, 3, 2), mask=True)

    result, result_alphabet = order(source, True, axis=1)

    assert result.shape == (3,)
    assert np.all(ma.getmaskarray(result))
    assert result_alphabet.shape == (2, 0, 2)
    assert not isinstance(result_alphabet, ma.MaskedArray)


def test_empty_sequence_axis_returns_empty_results():
    source = ma.masked_array(np.empty((2, 0, 3)), mask=False)

    result, result_alphabet = order(source, True, axis=1)

    assert result.shape == (0,)
    assert result_alphabet.shape == (2, 0, 3)


def test_empty_orthogonal_dimensions_describe_present_empty_slices():
    source = ma.masked_array(np.empty((3, 0)), mask=False)

    result, result_alphabet = order(source, True, axis=0)

    assert_equal(result, [0, 0, 0])
    assert result_alphabet.shape == (1, 0)


@pytest.mark.parametrize("function", [alphabet, order])
def test_mixed_mask_inside_slice_is_rejected(function):
    source = ma.masked_array([[1, 2], [3, 4]], mask=[[0, 1], [0, 0]])

    with pytest.raises(ValueError, match="wholly masked or wholly unmasked"):
        function(source, axis=0)


@pytest.mark.parametrize("function", [alphabet, order])
def test_multidimensional_input_without_axis_is_rejected(function):
    with pytest.raises(Not1DArrayException):
        function(ma.masked_array([[1, 2], [3, 4]], mask=False))


@pytest.mark.parametrize("function", [alphabet, order])
def test_scalar_input_is_rejected(function):
    with pytest.raises(Not1DArrayException):
        function(ma.masked_array(1), axis=0)


@pytest.mark.parametrize("function", [alphabet, order])
def test_invalid_axis_raises_numpy_axis_error(function):
    with pytest.raises(AxisError):
        function(ma.masked_array([[1, 2], [3, 4]], mask=False), axis=2)
