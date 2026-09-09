import importlib

import numpy as np
import numpy.ma as ma
import pytest
from numpy.ma.testutils import assert_equal
from numpy.testing import assert_array_equal

from foapy import binding, chain_mode
from foapy.core import intervals_chain as core_intervals_chain
from foapy.exceptions import Not1DArrayException
from foapy.partials import intervals_chain

try:
    from numpy.exceptions import AxisError
except ImportError:  # NumPy < 1.25
    from numpy import AxisError


EXPECTED_DATA = {
    (binding.start, chain_mode.boundary): [1, 0, 3, 3],
    (binding.start, chain_mode.cycle): [1, 0, 4, 3],
    (binding.end, chain_mode.boundary): [3, 0, 2, 1],
    (binding.end, chain_mode.cycle): [3, 0, 4, 1],
}
EXPECTED_MASK = [False, True, False, False]


def _whole_slice_gap_source(axis):
    data = np.array([[1, 2], [9, 9], [3, 4], [1, 2]])
    mask = np.array([[False, False], [True, True], [False, False], [False, False]])
    if axis == 1:
        data = data.T
        mask = mask.T
    return ma.masked_array(data, mask=mask)


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("binding_value,chain_mode_value", EXPECTED_DATA)
def test_whole_slice_gaps_count_in_all_modes(axis, binding_value, chain_mode_value):
    result = intervals_chain(
        _whole_slice_gap_source(axis),
        binding_value,
        chain_mode_value,
        axis=axis,
    )

    assert_equal(
        result,
        ma.masked_array(
            EXPECTED_DATA[(binding_value, chain_mode_value)],
            mask=EXPECTED_MASK,
        ),
    )
    assert result.dtype == np.dtype(np.intp)


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("binding_value", [binding.start, binding.end])
@pytest.mark.parametrize("chain_mode_value", [chain_mode.boundary, chain_mode.cycle])
def test_plain_multidimensional_input_matches_core(
    axis, binding_value, chain_mode_value
):
    source_alphabet = np.take(np.arange(12).reshape(2, 2, 3), [0, 1], axis=axis)
    source = np.take(source_alphabet, [0, 1, 0, 1, 0], axis=axis)

    result = intervals_chain(source, binding_value, chain_mode_value, axis=axis)
    expected = core_intervals_chain(source, binding_value, chain_mode_value, axis=axis)

    assert not np.any(ma.getmaskarray(result))
    assert_array_equal(result.data, expected)


@pytest.mark.parametrize("axis", [0, 1])
def test_fully_unmasked_multidimensional_input_matches_core(axis):
    rows = np.array([[1, 2], [3, 4], [1, 2], [5, 6]])
    source_data = rows if axis == 0 else rows.T
    source = ma.masked_array(source_data, mask=False)

    result = intervals_chain(source, binding.end, chain_mode.cycle, axis=axis)
    expected = core_intervals_chain(
        source_data, binding.end, chain_mode.cycle, axis=axis
    )

    assert not np.any(ma.getmaskarray(result))
    assert_array_equal(result.data, expected)


def test_mixed_mask_inside_slice_is_rejected():
    source = ma.masked_array([[1, 2], [3, 4]], mask=[[False, True], [False, False]])

    with pytest.raises(ValueError, match="wholly masked or wholly unmasked"):
        intervals_chain(source, binding.start, chain_mode.boundary, axis=0)


def test_fully_masked_axis_returns_fully_masked_chain():
    source = ma.masked_array(np.arange(12).reshape(2, 3, 2), mask=True)

    result = intervals_chain(source, binding.start, chain_mode.boundary, axis=1)

    assert result.shape == (3,)
    assert result.dtype == np.dtype(np.intp)
    assert np.all(ma.getmaskarray(result))


def test_empty_sequence_axis_returns_empty_masked_chain():
    source = ma.masked_array(np.empty((2, 0, 3)), mask=False)

    result = intervals_chain(source, binding.start, chain_mode.boundary, axis=1)

    assert result.shape == (0,)
    assert result.dtype == np.dtype(np.intp)


def test_structurally_empty_slices_are_present_and_equal():
    source = ma.masked_array(np.empty((3, 0)), mask=False)

    result = intervals_chain(source, binding.start, chain_mode.boundary, axis=0)

    assert_equal(result, [1, 1, 1])


def test_negative_axis_matches_positive_axis():
    source = _whole_slice_gap_source(axis=1)

    positive = intervals_chain(source, binding.end, chain_mode.cycle, axis=1)
    negative = intervals_chain(source, binding.end, chain_mode.cycle, axis=-1)

    assert_equal(negative, positive)


@pytest.mark.parametrize("axis", [None, 0, -1])
def test_1d_calls_use_legacy_direct_path(monkeypatch, axis):
    module = importlib.import_module("foapy.partials._intervals_chain")

    def fail(*args, **kwargs):
        pytest.fail("one-dimensional input entered axis factorization")

    monkeypatch.setattr(module, "partial_order", fail)
    source = ma.masked_array(["A", "x", "A"], mask=[False, True, False])

    result = intervals_chain(source, binding.start, chain_mode.boundary, axis=axis)

    assert_equal(result, ma.masked_array([1, 0, 2], mask=[False, True, False]))


def test_multidimensional_input_without_axis_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_chain(
            ma.masked_array([[1, 2], [3, 4]], mask=False),
            binding.start,
            chain_mode.boundary,
        )


def test_scalar_input_is_rejected():
    with pytest.raises(Not1DArrayException):
        intervals_chain(
            ma.masked_array(1),
            binding.start,
            chain_mode.boundary,
            axis=0,
        )


def test_out_of_range_axis_raises_numpy_axis_error():
    with pytest.raises(AxisError):
        intervals_chain(
            ma.masked_array([[1, 2], [3, 4]], mask=False),
            binding.start,
            chain_mode.boundary,
            axis=2,
        )
