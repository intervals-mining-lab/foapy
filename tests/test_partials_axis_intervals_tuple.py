import importlib
import inspect
from typing import Optional, Union

import numpy as np
import numpy.ma as ma
import pytest
from numpy import ndarray
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal
from numpy.typing import ArrayLike

import foapy
import foapy.partials as partials
from foapy import binding, chain_mode, tuple_mode
from foapy.core import intervals_tuple as core_intervals_tuple
from foapy.exceptions import Not1DArrayException
from foapy.partials import intervals_chain, intervals_tuple

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


SOURCES = ma.masked_array(
    [[0, 9, 1, 0, 9, 2], [9, 0, 0, 1, 0, 9]],
    mask=[
        [False, True, False, False, True, False],
        [True, False, False, False, False, True],
    ],
)

EXPECTED_ROWS = {
    (binding.start, tuple_mode.normal): ma.masked_array(
        [[1, 3, 3, 6], [2, 1, 4, 2]], mask=False
    ),
    (binding.start, tuple_mode.lossy): ma.masked_array(
        [[3, 0], [1, 2]], mask=[[False, True], [False, False]]
    ),
    (binding.start, tuple_mode.redundant): ma.masked_array(
        [[1, 3, 3, 6, 4, 3, 1], [2, 1, 4, 2, 3, 2, 0]],
        mask=[[False] * 7, [False] * 6 + [True]],
    ),
    (binding.end, tuple_mode.normal): ma.masked_array(
        [[3, 4, 3, 1], [1, 2, 3, 2]], mask=False
    ),
    (binding.end, tuple_mode.lossy): ma.masked_array(
        [[3, 0], [2, 1]], mask=[[False, True], [False, False]]
    ),
    (binding.end, tuple_mode.redundant): ma.masked_array(
        [[1, 3, 4, 3, 6, 3, 1], [2, 3, 2, 1, 4, 2, 0]],
        mask=[[False] * 7, [False] * 6 + [True]],
    ),
}


def _chains(binding_value):
    return ma.stack(
        [
            intervals_chain(
                source,
                binding_value,
                chain_mode.boundary,
            )
            for source in SOURCES
        ]
    )


def _pack_rows(results):
    result_length = max((result.size for result in results), default=0)
    packed = ma.masked_all((len(results), result_length), dtype=np.intp)
    for index, result in enumerate(results):
        packed.data[index, : result.size] = result
        packed.mask[index, : result.size] = False
    return packed


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_rows_and_columns_are_independent_partial_chains(
    axis, binding_value, tuple_mode_value
):
    rows = _chains(binding_value)
    source = rows if axis == 1 else rows.T
    expected_rows = EXPECTED_ROWS[(binding_value, tuple_mode_value)]
    expected = expected_rows if axis == 1 else expected_rows.T

    result = intervals_tuple(
        source,
        binding_value,
        tuple_mode_value,
        axis=axis,
    )

    assert ma.isMaskedArray(result)
    assert_equal(result, expected)
    assert result.dtype == np.dtype(np.intp)


def _three_dimensional_chains(axis, binding_value):
    rows = _chains(binding_value)
    lanes = ma.stack([rows[index % 2] for index in range(6)]).reshape(2, 3, 6)
    return np.moveaxis(lanes, -1, axis)


def _three_dimensional_expected(axis, binding_value, tuple_mode_value):
    rows = _chains(binding_value)
    lane_results = [
        intervals_tuple(rows[index % 2], binding_value, tuple_mode_value)
        for index in range(6)
    ]
    packed = _pack_rows(lane_results).reshape(2, 3, -1)
    return np.moveaxis(packed, -1, axis)


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_3d_axis_replaces_selected_dimension(axis, binding_value, tuple_mode_value):
    source = _three_dimensional_chains(axis, binding_value)
    expected = _three_dimensional_expected(axis, binding_value, tuple_mode_value)

    result = intervals_tuple(
        source,
        binding_value,
        tuple_mode_value,
        axis=axis,
    )

    assert_equal(result, expected)
    assert result.shape[axis] == expected.shape[axis]


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_negative_axis_matches_positive_axis(axis):
    source = _three_dimensional_chains(axis, binding.start)

    positive = intervals_tuple(source, binding.start, tuple_mode.redundant, axis=axis)
    negative = intervals_tuple(
        source,
        binding.start,
        tuple_mode.redundant,
        axis=axis - source.ndim,
    )

    assert_equal(negative, positive)


def test_uniform_lengths_still_return_masked_array_with_false_mask():
    result = intervals_tuple(
        _chains(binding.start),
        binding.start,
        tuple_mode.normal,
        axis=1,
    )

    assert ma.isMaskedArray(result)
    assert not np.any(ma.getmaskarray(result))


def test_fully_masked_lane_is_structurally_trailing_masked():
    source = ma.masked_array(
        [[0, 0, 0, 0], [1, 2, 2, 4]],
        mask=[[True] * 4, [False] * 4],
    )

    result = intervals_tuple(
        source,
        binding.start,
        tuple_mode.normal,
        axis=1,
    )

    assert result.shape == (2, 4)
    assert np.all(result.mask[0])
    assert_equal(result[1], [1, 2, 2, 4])


@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_empty_selected_axis_returns_empty_masked_result(tuple_mode_value):
    source = ma.masked_array(np.empty((2, 0, 3)), mask=False)

    result = intervals_tuple(
        source,
        binding.start,
        tuple_mode_value,
        axis=1,
    )

    assert ma.isMaskedArray(result)
    assert result.shape == (2, 0, 3)
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize("shape,axis", [((0, 4), 1), ((4, 0), 0), ((0, 4, 2), 1)])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_absent_lanes_have_zero_length_result_axis(shape, axis, tuple_mode_value):
    source = ma.masked_array(np.empty(shape), mask=False)

    result = intervals_tuple(
        source,
        binding.start,
        tuple_mode_value,
        axis=axis,
    )

    expected_shape = list(shape)
    expected_shape[axis] = 0
    assert ma.isMaskedArray(result)
    assert result.shape == tuple(expected_shape)


@pytest.mark.parametrize("axis", [None, 0, -1])
@pytest.mark.parametrize("masked", [False, True])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_1d_calls_use_direct_plain_array_path(
    monkeypatch, axis, masked, tuple_mode_value
):
    module = importlib.import_module("foapy.partials._intervals_tuple")
    plain = np.array([1, 2, 2, 4, 2], dtype=np.intp)
    source = ma.masked_array(plain, mask=[False, True, False, False, False])
    if not masked:
        source = plain
    expected = intervals_tuple(source, binding.start, tuple_mode_value)

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered multidimensional packing")

    monkeypatch.setattr(module, "_apply_to_axis_lanes", fail)
    result = intervals_tuple(
        source,
        binding.start,
        tuple_mode_value,
        axis=axis,
    )

    assert_array_equal(result, expected)
    assert isinstance(result, np.ndarray)
    assert not ma.isMaskedArray(result)
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_empty_1d_input_stays_plain(tuple_mode_value):
    result = intervals_tuple(
        ma.masked_array([], mask=[], dtype=np.intp),
        binding.start,
        tuple_mode_value,
        axis=0,
    )

    assert_array_equal(result, np.array([], dtype=np.intp))
    assert not ma.isMaskedArray(result)


DENSE_CHAINS = {
    binding.start: np.array([[1, 1, 3, 1], [1, 2, 1, 3]]),
    binding.end: np.array([[1, 3, 1, 1], [3, 1, 2, 1]]),
}


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_dense_multidimensional_input_matches_core(
    axis, binding_value, tuple_mode_value
):
    rows = DENSE_CHAINS[binding_value]
    source = rows if axis == 1 else rows.T

    partial_result = intervals_tuple(
        ma.masked_array(source, mask=False),
        binding_value,
        tuple_mode_value,
        axis=axis,
    )
    core_result = core_intervals_tuple(
        source,
        binding_value,
        tuple_mode_value,
        axis=axis,
    )

    assert_equal(partial_result, core_result)


def test_multidimensional_input_without_axis_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_tuple(
            ma.masked_array([[1, 2], [2, 1]], mask=False),
            binding.start,
            tuple_mode.normal,
        )


def test_scalar_input_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_tuple(
            ma.masked_array(1),
            binding.start,
            tuple_mode.normal,
            axis=0,
        )


@pytest.mark.parametrize("axis", [-3, 2])
def test_invalid_axis_raises_numpy_axis_error(axis):
    with pytest.raises(AxisError):
        intervals_tuple(
            ma.masked_array([[1, 2], [2, 1]], mask=False),
            binding.start,
            tuple_mode.normal,
            axis=axis,
        )


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize(
    "tuple_mode_value", [tuple_mode.normal, tuple_mode.lossy, tuple_mode.redundant]
)
def test_partial_tuple_output_composes_with_existing_distribution(
    axis, binding_value, tuple_mode_value
):
    rows = _chains(binding_value)
    source = rows if axis == 1 else rows.T
    tuple_result = intervals_tuple(
        source,
        binding_value,
        tuple_mode_value,
        axis=axis,
    )

    result = foapy.intervals_distribution(tuple_result, axis=axis)
    lane_results = [
        foapy.intervals_distribution(
            intervals_tuple(row, binding_value, tuple_mode_value)
        )
        for row in rows
    ]
    expected_rows = _pack_rows(lane_results)
    expected = expected_rows if axis == 1 else expected_rows.T

    assert_equal(result, expected)


def test_no_duplicate_partial_distribution_export():
    assert not hasattr(partials, "intervals_distribution")
    assert "intervals_distribution" not in partials.__all__
    assert foapy.intervals_distribution is not None


def test_signature_and_annotations():
    signature = inspect.signature(intervals_tuple)

    assert list(signature.parameters) == ["chain", "binding", "tuple_mode", "axis"]
    assert signature.parameters["chain"].annotation is ArrayLike
    assert signature.parameters["binding"].annotation is int
    assert signature.parameters["tuple_mode"].annotation is int
    assert signature.parameters["axis"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["axis"].annotation == Optional[int]
    assert signature.return_annotation == Union[ndarray, ma.MaskedArray]
