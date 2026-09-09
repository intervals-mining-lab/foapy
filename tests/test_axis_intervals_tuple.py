import importlib

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

import foapy
import foapy.core as core
from foapy import binding, tuple_mode
from foapy.core import intervals_tuple
from foapy.core._intervals_chain_validation import is_valid_intervals_chain
from foapy.exceptions import Not1DArrayException

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


CHAINS = {
    binding.start: np.array([[1, 1, 3, 1], [1, 2, 1, 3]]),
    binding.end: np.array([[1, 3, 1, 1], [3, 1, 2, 1]]),
}
EXPECTED = {
    (binding.start, tuple_mode.normal): [[1, 1, 3, 1], [1, 2, 1, 3]],
    (binding.end, tuple_mode.normal): [[1, 3, 1, 1], [3, 1, 2, 1]],
    (binding.start, tuple_mode.lossy): [[1, 1], [1, 3]],
    (binding.end, tuple_mode.lossy): [[1, 1], [1, 3]],
    (binding.start, tuple_mode.redundant): [
        [1, 1, 3, 1, 3, 1],
        [1, 2, 1, 3, 2, 1],
    ],
    (binding.end, tuple_mode.redundant): [
        [1, 1, 3, 1, 3, 1],
        [1, 2, 1, 3, 2, 1],
    ],
}


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_rows_and_columns_are_independent_chains(axis, binding_value, tuple_mode_value):
    rows = CHAINS[binding_value]
    source = rows if axis == 1 else rows.T
    expected_rows = np.array(EXPECTED[(binding_value, tuple_mode_value)])
    expected = expected_rows if axis == 1 else expected_rows.T

    result = intervals_tuple(source, binding_value, tuple_mode_value, axis=axis)

    assert ma.isMaskedArray(result)
    assert_equal(result, ma.masked_array(expected, mask=False))
    assert result.dtype == np.dtype(np.intp)


def _three_dimensional_chains(axis, binding_value):
    lanes = np.stack([CHAINS[binding_value][index % 2] for index in range(6)]).reshape(
        2, 3, 4
    )
    return np.moveaxis(lanes, -1, axis)


def _three_dimensional_expected(axis, binding_value, tuple_mode_value):
    lane_results = np.stack(
        [
            intervals_tuple(
                CHAINS[binding_value][index % 2],
                binding_value,
                tuple_mode_value,
            )
            for index in range(6)
        ]
    ).reshape(2, 3, -1)
    return np.moveaxis(lane_results, -1, axis)


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_3d_axis_replaces_selected_dimension(axis, binding_value, tuple_mode_value):
    source = _three_dimensional_chains(axis, binding_value)
    expected = _three_dimensional_expected(axis, binding_value, tuple_mode_value)

    result = intervals_tuple(source, binding_value, tuple_mode_value, axis=axis)

    assert_equal(result, ma.masked_array(expected, mask=False))
    assert result.shape[axis] == expected.shape[axis]


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source = _three_dimensional_chains(axis, binding.start)

    positive = intervals_tuple(source, binding.start, tuple_mode.redundant, axis=axis)
    negative = intervals_tuple(
        source, binding.start, tuple_mode.redundant, axis=axis - source.ndim
    )

    assert_equal(negative, positive)


@pytest.mark.parametrize(
    "tuple_mode_value,expected",
    [
        (
            tuple_mode.lossy,
            ma.masked_array(
                [[1, 1, 1], [0, 0, 0]],
                mask=[[False, False, False], [True, True, True]],
            ),
        ),
        (
            tuple_mode.redundant,
            ma.masked_array(
                [
                    [1, 1, 1, 1, 1, 0, 0, 0],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                ],
                mask=[
                    [False, False, False, False, False, True, True, True],
                    [False] * 8,
                ],
            ),
        ),
    ],
)
def test_variable_length_results_are_trailing_masked(tuple_mode_value, expected):
    source = np.array([[1, 1, 1, 1], [1, 2, 3, 4]])

    result = intervals_tuple(source, binding.start, tuple_mode_value, axis=1)

    assert_equal(result, expected)


def test_uniform_results_still_return_masked_array():
    result = intervals_tuple(
        CHAINS[binding.start], binding.start, tuple_mode.lossy, axis=1
    )

    assert ma.isMaskedArray(result)
    assert not np.any(ma.getmaskarray(result))


@pytest.mark.parametrize("axis", [None, 0, -1])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_1d_calls_use_direct_plain_array_path(monkeypatch, axis, tuple_mode_value):
    module = importlib.import_module("foapy.core._intervals_tuple")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered multidimensional packing")

    monkeypatch.setattr(module, "_apply_to_axis_lanes", fail)
    source = np.array([1, 1, 3, 1])

    result = intervals_tuple(source, binding.start, tuple_mode_value, axis=axis)

    assert isinstance(result, np.ndarray)
    assert not ma.isMaskedArray(result)
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_empty_1d_input_stays_plain(tuple_mode_value):
    result = intervals_tuple(
        np.array([], dtype=np.intp),
        binding.start,
        tuple_mode_value,
        axis=0,
    )

    assert_array_equal(result, np.array([], dtype=np.intp))
    assert not ma.isMaskedArray(result)


@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_empty_selected_axis_returns_empty_masked_result(tuple_mode_value):
    result = intervals_tuple(
        np.empty((2, 0, 3), dtype=np.intp),
        binding.start,
        tuple_mode_value,
        axis=1,
    )

    assert ma.isMaskedArray(result)
    assert result.shape == (2, 0, 3)


@pytest.mark.parametrize(
    "tuple_mode_value,expected_shape",
    [
        (tuple_mode.normal, (0, 4)),
        (tuple_mode.lossy, (0, 0)),
        (tuple_mode.redundant, (0, 0)),
    ],
)
def test_no_lanes_has_deterministic_shape(tuple_mode_value, expected_shape):
    result = intervals_tuple(
        np.empty((0, 4), dtype=np.intp),
        binding.start,
        tuple_mode_value,
        axis=1,
    )

    assert ma.isMaskedArray(result)
    assert result.shape == expected_shape


def test_multidimensional_input_without_axis_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_tuple(np.ones((2, 2)), binding.start, tuple_mode.normal)


def test_scalar_input_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_tuple(np.array(1), binding.start, tuple_mode.normal, axis=0)


@pytest.mark.parametrize("axis", [-3, 2])
def test_invalid_axis_raises_numpy_axis_error(axis):
    with pytest.raises(AxisError):
        intervals_tuple(np.ones((2, 2)), binding.start, tuple_mode.normal, axis=axis)


def test_validator_is_not_exported():
    assert not hasattr(foapy, "is_valid_intervals_chain")
    assert not hasattr(core, "is_valid_intervals_chain")
    assert "is_valid_intervals_chain" not in foapy.__all__
    assert "is_valid_intervals_chain" not in core.__all__


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_internal_validator_accepts_1d_input(axis):
    assert is_valid_intervals_chain(np.array([9, -2, 0]), axis=axis) is True


def test_internal_validator_aggregates_multidimensional_lanes(monkeypatch):
    module = importlib.import_module("foapy.core._intervals_chain_validation")
    seen = []

    def record(lane):
        seen.append(lane.copy())
        return True

    monkeypatch.setattr(module, "_is_valid_intervals_chain_1d", record)

    assert is_valid_intervals_chain(np.arange(12).reshape(3, 4), axis=1) is True
    assert len(seen) == 3
    assert_array_equal(seen[0], [0, 1, 2, 3])


def test_internal_validator_structural_errors():
    with pytest.raises(Not1DArrayException):
        is_valid_intervals_chain(np.ones((2, 2)))
    with pytest.raises(Not1DArrayException):
        is_valid_intervals_chain(np.array(1), axis=0)
    with pytest.raises(AxisError):
        is_valid_intervals_chain(np.ones((2, 2)), axis=2)


def test_intervals_tuple_rejects_false_validation(monkeypatch):
    module = importlib.import_module("foapy.core._intervals_tuple")
    monkeypatch.setattr(
        module, "is_valid_intervals_chain", lambda *args, **kwargs: False
    )

    with pytest.raises(ValueError, match="Invalid intervals chain"):
        intervals_tuple([1, 1, 1], binding.start, tuple_mode.normal)
