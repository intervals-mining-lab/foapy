import importlib

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

from foapy import binding, tuple_mode
from foapy.core import intervals_distribution, intervals_tuple
from foapy.exceptions import Not1DArrayException

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


TUPLES = np.array([[1, 1, 3, 1], [1, 2, 1, 3]])
EXPECTED_ROWS = np.array([[3, 0, 1], [2, 1, 1]])


@pytest.mark.parametrize("axis", [0, 1])
def test_rows_and_columns_have_independent_distributions(axis):
    source = TUPLES if axis == 1 else TUPLES.T
    expected = EXPECTED_ROWS if axis == 1 else EXPECTED_ROWS.T

    result = intervals_distribution(source, axis=axis)

    assert ma.isMaskedArray(result)
    assert_equal(result, ma.masked_array(expected, mask=False))
    assert result.dtype == np.dtype(np.intp)


def _three_dimensional_tuples(axis):
    lanes = np.stack([TUPLES[index % 2] for index in range(6)]).reshape(2, 3, 4)
    return np.moveaxis(lanes, -1, axis)


def _three_dimensional_expected(axis):
    lanes = np.stack([EXPECTED_ROWS[index % 2] for index in range(6)]).reshape(2, 3, 3)
    return np.moveaxis(lanes, -1, axis)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_3d_axis_replaces_selected_dimension(axis):
    source = _three_dimensional_tuples(axis)
    expected = _three_dimensional_expected(axis)

    result = intervals_distribution(source, axis=axis)

    assert_equal(result, ma.masked_array(expected, mask=False))
    assert result.shape[axis] == 3


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source = _three_dimensional_tuples(axis)

    positive = intervals_distribution(source, axis=axis)
    negative = intervals_distribution(source, axis=axis - source.ndim)

    assert_equal(negative, positive)


def test_unequal_maximums_mask_only_trailing_bins():
    source = np.array([[1, 3], [1, 2]])
    expected = ma.masked_array(
        [[1, 0, 1], [1, 1, 0]],
        mask=[[False, False, False], [False, False, True]],
    )

    result = intervals_distribution(source, axis=1)

    assert_equal(result, expected)
    assert result.mask[0, 1] is np.False_
    assert result[0, 1] == 0


def test_masked_tuple_padding_is_excluded():
    source = ma.masked_array(
        [[1, 1, 1, 0], [1, 2, 3, 4]],
        mask=[[False, False, False, True], [False, False, False, False]],
    )
    expected = ma.masked_array(
        [[3, 0, 0, 0], [1, 1, 1, 1]],
        mask=[[False, True, True, True], [False, False, False, False]],
    )

    result = intervals_distribution(source, axis=1)

    assert_equal(result, expected)


def test_fully_masked_lane_is_trailing_masked():
    source = ma.masked_array(
        [[0, 0, 0, 0], [1, 2, 3, 4]],
        mask=[[True, True, True, True], [False, False, False, False]],
    )

    result = intervals_distribution(source, axis=1)

    assert np.all(result.mask[0])
    assert_equal(result[1], [1, 1, 1, 1])


def test_all_empty_lanes_return_empty_selected_axis():
    result = intervals_distribution(np.empty((2, 0), dtype=np.intp), axis=1)

    assert ma.isMaskedArray(result)
    assert result.shape == (2, 0)


@pytest.mark.parametrize("shape,axis", [((0, 4), 1), ((4, 0), 0)])
def test_no_lanes_returns_zero_length_result_axis(shape, axis):
    result = intervals_distribution(np.empty(shape, dtype=np.intp), axis=axis)

    assert ma.isMaskedArray(result)
    assert result.shape == (0, 0)


def test_1d_masked_tuple_excludes_masked_positions():
    source = ma.masked_array([1, 9, 3], mask=[False, True, False])

    result = intervals_distribution(source)

    assert_array_equal(result, [1, 0, 1])
    assert not ma.isMaskedArray(result)


def test_prepared_1d_plain_array_skips_conversion(monkeypatch):
    module = importlib.import_module("foapy.core._intervals_distribution")
    prepared = np.array([1, 1, 3, 1], dtype=np.intp)

    def fail_conversion(*args, **kwargs):
        raise AssertionError("prepared ndarray was converted again")

    monkeypatch.setattr(module.np, "asanyarray", fail_conversion)

    assert module.intervals_distribution(prepared).tolist() == [3, 0, 1]


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_1d_calls_use_direct_plain_array_path(monkeypatch, axis):
    module = importlib.import_module("foapy.core._intervals_distribution")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered multidimensional packing")

    monkeypatch.setattr(module, "_apply_to_axis_lanes", fail)

    result = intervals_distribution(np.array([1, 1, 3, 1]), axis=axis)

    assert_array_equal(result, [3, 0, 1])
    assert not ma.isMaskedArray(result)
    assert result.dtype == np.dtype(np.intp)


def test_multidimensional_input_without_axis_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_distribution(np.ones((2, 2), dtype=np.intp))


def test_scalar_input_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_distribution(np.array(1), axis=0)


@pytest.mark.parametrize("axis", [-3, 2])
def test_invalid_axis_raises_numpy_axis_error(axis):
    with pytest.raises(AxisError):
        intervals_distribution(np.ones((2, 2), dtype=np.intp), axis=axis)


@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
@pytest.mark.parametrize("axis", [0, 1])
def test_axis_tuple_output_composes_with_distribution(tuple_mode_value, axis):
    rows = np.array([[1, 1, 3, 1], [1, 2, 1, 3]])
    source = rows if axis == 1 else rows.T
    tuple_result = intervals_tuple(source, binding.start, tuple_mode_value, axis=axis)

    result = intervals_distribution(tuple_result, axis=axis)

    lane_results = [
        intervals_distribution(intervals_tuple(row, binding.start, tuple_mode_value))
        for row in rows
    ]
    width = max(lane.size for lane in lane_results)
    expected_rows = ma.masked_all((len(lane_results), width), dtype=np.intp)
    for index, lane in enumerate(lane_results):
        expected_rows.data[index, : lane.size] = lane
        expected_rows.mask[index, : lane.size] = False
    expected = expected_rows if axis == 1 else expected_rows.T

    assert_equal(result, expected)
