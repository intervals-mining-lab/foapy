import importlib

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain, order
from foapy.exceptions import Not1DArrayException

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


EXPECTED = {
    (binding.start, chain_mode.boundary): [1, 2, 2, 4, 2],
    (binding.start, chain_mode.cycle): [1, 5, 2, 5, 2],
    (binding.end, chain_mode.boundary): [2, 4, 2, 2, 1],
    (binding.end, chain_mode.cycle): [2, 5, 2, 5, 1],
}


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value,chain_mode_value", EXPECTED)
def test_rows_and_columns_are_sequence_elements(axis, binding_value, chain_mode_value):
    rows = np.array([[1, 2], [3, 4], [1, 2], [5, 6], [1, 2]])
    source = rows if axis == 0 else rows.T

    result = intervals_chain(source, binding_value, chain_mode_value, axis=axis)

    assert_array_equal(result, EXPECTED[(binding_value, chain_mode_value)])
    assert result.shape == (5,)
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize("chain_mode_value", [chain_mode.boundary, chain_mode.cycle])
def test_3d_result_matches_interval_chain_of_axis_order(
    axis, binding_value, chain_mode_value
):
    source_alphabet = np.take(np.arange(12).reshape(2, 2, 3), [0, 1], axis=axis)
    source = np.take(source_alphabet, [0, 1, 0, 1, 0], axis=axis)

    result = intervals_chain(source, binding_value, chain_mode_value, axis=axis)
    expected = intervals_chain(
        order(source, axis=axis), binding_value, chain_mode_value
    )

    assert_array_equal(result, expected)
    assert result.shape == (5,)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source = np.take(np.arange(12).reshape(2, 2, 3), [0, 1, 0], axis=axis)
    negative_axis = axis - source.ndim

    positive = intervals_chain(source, binding.start, chain_mode.boundary, axis=axis)
    negative = intervals_chain(
        source, binding.start, chain_mode.boundary, axis=negative_axis
    )

    assert_array_equal(negative, positive)


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_1d_calls_use_legacy_direct_path(monkeypatch, axis):
    module = importlib.import_module("foapy.core._intervals_chain")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered axis factorization")

    monkeypatch.setattr(module, "core_order", fail)
    source = np.array(["b", "a", "b", "c", "b"])

    result = intervals_chain(source, binding.start, chain_mode.boundary, axis=axis)

    assert_array_equal(result, [1, 2, 2, 4, 2])


def test_multidimensional_input_without_axis_keeps_legacy_error():
    with pytest.raises(Not1DArrayException):
        intervals_chain(np.ones((2, 2)), binding.start, chain_mode.boundary)


def test_scalar_input_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_chain(np.array(1), binding.start, chain_mode.boundary, axis=0)


@pytest.mark.parametrize("axis", [-3, 2])
def test_out_of_range_axis_raises_numpy_axis_error(axis):
    with pytest.raises(AxisError):
        intervals_chain(np.ones((2, 2)), binding.start, chain_mode.boundary, axis=axis)


@pytest.mark.parametrize(
    "shape,axis",
    [((0, 2), 0), ((2, 0), 1), ((2, 0, 3), 1)],
)
def test_empty_sequence_axis_returns_empty_intp_chain(shape, axis):
    result = intervals_chain(
        np.empty(shape), binding.start, chain_mode.boundary, axis=axis
    )

    assert result.shape == (0,)
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize("shape,axis", [((4, 0), 0), ((0, 4), 1)])
def test_structurally_empty_slices_are_one_repeated_element(shape, axis):
    result = intervals_chain(
        np.empty(shape), binding.start, chain_mode.boundary, axis=axis
    )

    assert_array_equal(result, [1, 1, 1, 1])
    assert result.dtype == np.dtype(np.intp)
