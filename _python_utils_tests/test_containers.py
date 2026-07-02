"""Tests for the container types in ``python_utils.containers``."""

import pytest

from python_utils import containers


def test_unique_list_ignore() -> None:
    """Ignore duplicate appends and block duplicate slice sets."""
    a: containers.UniqueList[int] = containers.UniqueList()
    a.append(1)
    a.append(1)
    assert a == [1]

    a = containers.UniqueList(*range(20))
    with pytest.raises(RuntimeError):
        a[10:20:2] = [1, 2, 3, 4, 5]

    a[3] = 5


def test_unique_list_raise() -> None:
    """Raise on duplicates when ``on_duplicate='raise'``."""
    a: containers.UniqueList[int] = containers.UniqueList(
        *range(20), on_duplicate='raise'
    )
    with pytest.raises(ValueError):
        a[10:20:2] = [1, 2, 3, 4, 5]

    a[10:20:2] = [21, 22, 23, 24, 25]
    with pytest.raises(ValueError):
        a[3] = 5

    del a[10]
    del a[5:15]


def test_sliceable_deque() -> None:
    """Support indexing and extended slicing on the deque."""
    d: containers.SliceableDeque[int] = containers.SliceableDeque(range(10))
    assert d[0] == 0
    assert d[-1] == 9
    assert d[1:3] == [1, 2]
    assert d[1:3:2] == [1]
    assert d[1:3:-1] == []
    assert d[3:1] == []
    assert d[3:1:-1] == [3, 2]
    assert d[3:1:-2] == [3]
    with pytest.raises(ValueError):
        assert d[1:3:0]
    assert d[1:3:1] == [1, 2]
    assert d[1:3:2] == [1]
    assert d[1:3:-1] == []


def test_sliceable_deque_pop() -> None:
    """Pop by index and raise ``IndexError`` when out of range."""
    d: containers.SliceableDeque[int] = containers.SliceableDeque(range(10))

    assert d.pop() == 9 == 9
    assert d.pop(0) == 0

    with pytest.raises(IndexError):
        assert d.pop(100)

    with pytest.raises(IndexError):
        assert d.pop(2)

    with pytest.raises(IndexError):
        assert d.pop(-2)


def test_sliceable_deque_eq() -> None:
    """Compare equal to list, tuple, set, and another deque."""
    d: containers.SliceableDeque[int] = containers.SliceableDeque([1, 2, 3])
    assert d == [1, 2, 3]
    assert d == (1, 2, 3)
    assert d == {1, 2, 3}
    assert d == d
    assert d == containers.SliceableDeque([1, 2, 3])
