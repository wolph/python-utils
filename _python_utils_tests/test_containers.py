import pytest

from python_utils import containers


def test_unique_list_ignore():
    a = containers.UniqueList()
    a.append(1)
    a.append(1)
    assert a == [1]

    a = containers.UniqueList(*range(20))
    with pytest.raises(RuntimeError):
        a[10:20:2] = [1, 2, 3, 4, 5]

    a[3] = 5


def test_unique_list_raise():
    a = containers.UniqueList(*range(20), on_duplicate='raise')
    with pytest.raises(ValueError):
        a[10:20:2] = [1, 2, 3, 4, 5]

    a[10:20:2] = [21, 22, 23, 24, 25]
    with pytest.raises(ValueError):
        a[3] = 5

    del a[10]
    del a[5:15]
