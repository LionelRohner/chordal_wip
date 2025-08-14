import numpy as np
import pytest
from chordal_wip.scales import rotate_list  # Adjust import as needed


def test_rotate_left():
    arr = [1, 2, 3, 4, 5]
    assert np.array_equal(rotate_list(arr, 1), np.array([2, 3, 4, 5, 1]))
    assert np.array_equal(rotate_list(arr, 2), np.array([3, 4, 5, 1, 2]))
    assert np.array_equal(
        rotate_list(arr, 5), np.array([1, 2, 3, 4, 5])
    )  # Full rotation
    assert np.array_equal(rotate_list(arr, 7), np.array([3, 4, 5, 1, 2]))  # Wrap around


def test_rotate_right():
    arr = [1, 2, 3, 4, 5]
    assert np.array_equal(rotate_list(arr, 1, "right"), np.array([5, 1, 2, 3, 4]))
    assert np.array_equal(rotate_list(arr, 2, "right"), np.array([4, 5, 1, 2, 3]))
    assert np.array_equal(
        rotate_list(arr, 5, "right"), np.array([1, 2, 3, 4, 5])
    )  # Full rotation
    assert np.array_equal(
        rotate_list(arr, 7, "right"), np.array([4, 5, 1, 2, 3])
    )  # Wrap around


def test_rotate_empty():
    assert np.array_equal(rotate_list([], 2), np.array([]))


def test_rotate_single_element():
    assert np.array_equal(rotate_list([1], 3), np.array([1]))
    assert np.array_equal(rotate_list([1], 3, "right"), np.array([1]))


def test_rotate_negative_n():
    arr = [1, 2, 3, 4, 5]
    assert np.array_equal(
        rotate_list(arr, -1), np.array([5, 1, 2, 3, 4])
    )  # Equivalent to right rotation
    assert np.array_equal(rotate_list(arr, -2), np.array([4, 5, 1, 2, 3]))


def test_rotate_non_integer_n():
    with pytest.raises(TypeError):
        rotate_list([1, 2, 3], "not_an_int")


def test_rotate_invalid_dir():
    with pytest.raises(ValueError):  # Or whatever exception you want to raise
        rotate_list([1, 2, 3], 1, "up")
