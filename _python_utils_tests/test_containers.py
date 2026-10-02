"""Tests for the container types in ``python_utils.containers``."""

import collections.abc
import copy
import pickle

import pytest

from python_utils import containers

#: A callable that copies a ``UniqueList``, such as ``copy.copy``.
Copier = collections.abc.Callable[
    [containers.UniqueList[int]], containers.UniqueList[int]
]

#: ``UniqueList(1, 2, on_duplicate='raise')`` as pickled by python-utils 4.0.1,
#: which stored the membership set in the instance state.
LEGACY_PICKLES: tuple[bytes, ...] = (
    (
        b'ccopy_reg\n_reconstructor\np0\n(cpython_utils.containers\nUniqueList'
        b'\np1\nc__builtin__\nlist\np2\n(lp3\nI1\naI2\natp4\nRp5\n(dp6\n'
        b'Von_duplicate\np7\nVraise\np8\nsV_set\np9\nc__builtin__\nset\np10\n'
        b'((lp11\nI1\naI2\natp12\nRp13\nsb.'
    ),
    (
        b'\x80\x02cpython_utils.containers\nUniqueList\nq\x00)\x81q\x01(K\x01'
        b'K\x02e}q\x02(X\x0c\x00\x00\x00on_duplicateq\x03X\x05\x00\x00\x00'
        b'raiseq\x04X\x04\x00\x00\x00_setq\x05c__builtin__\nset\nq\x06]q\x07'
        b'(K\x01K\x02e\x85q\x08Rq\tub.'
    ),
    (
        b'\x80\x04\x95^\x00\x00\x00\x00\x00\x00\x00\x8c\x17python_utils.'
        b'containers\x94\x8c\nUniqueList\x94\x93\x94)\x81\x94(K\x01K\x02e}'
        b'\x94(\x8c\x0con_duplicate\x94\x8c\x05raise\x94\x8c\x04_set\x94\x8f'
        b'\x94(K\x01K\x02\x90ub.'
    ),
)


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


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
@pytest.mark.parametrize('index', [0, -2])
def test_unique_list_replace_membership(
    on_duplicate: containers.OnDuplicate, index: int
) -> None:
    """Release the old value after replacing an indexed item."""
    values = containers.UniqueList(1, 2, on_duplicate=on_duplicate)
    values[index] = 3

    assert values == [3, 2]
    assert 1 not in values
    assert 3 in values
    values.append(1)
    assert values == [3, 2, 1]


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
@pytest.mark.parametrize('index', [2, -3])
def test_unique_list_failed_replace_preserves_membership(
    on_duplicate: containers.OnDuplicate, index: int
) -> None:
    """Do not reserve a value when indexed assignment fails."""
    values = containers.UniqueList(1, 2, on_duplicate=on_duplicate)
    with pytest.raises(IndexError):
        values[index] = 3

    assert values == [1, 2]
    assert 3 not in values
    values.append(3)
    assert values == [1, 2, 3]


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
def test_unique_list_replace_same_value(
    on_duplicate: containers.OnDuplicate,
) -> None:
    """Replacing an item with itself keeps membership intact."""
    values = containers.UniqueList(1, 2, on_duplicate=on_duplicate)
    values[0] = 1
    assert values == [1, 2]
    assert 1 in values
    assert 2 in values


def test_unique_list_slice_replace_membership() -> None:
    """Release the old values after replacing a slice."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    values[0:2] = [8, 9]

    assert values == [8, 9, 3]
    assert 1 not in values
    assert 8 in values
    values.append(1)
    assert values == [8, 9, 3, 1]


def test_unique_list_failed_slice_preserves_membership() -> None:
    """Do not reserve values when slice assignment fails."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, 4, on_duplicate='raise'
    )
    with pytest.raises(ValueError, match='extended slice'):
        values[0:4:2] = [8, 9, 10]

    assert values == [1, 2, 3, 4]
    assert 8 not in values
    values.append(8)
    assert values == [1, 2, 3, 4, 8]


def test_unique_list_slice_from_iterator() -> None:
    """Assign a one-shot iterable to a slice without losing its values."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    values[0:2] = iter([8, 9])

    assert values == [8, 9, 3]
    assert 8 in values
    assert 1 not in values


def test_unique_list_slice_reuses_replaced_values() -> None:
    """Allow new slice values that only duplicate the values they replace."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    values[0:2] = (1, 2)
    assert values == [1, 2, 3]

    values[0:2] = [2, 1]
    assert values == [2, 1, 3]

    values[0:2] = [1, 9]
    assert values == [1, 9, 3]
    assert 2 not in values


def test_unique_list_slice_rejects_duplicates() -> None:
    """Reject slice values that repeat themselves or a kept item."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    with pytest.raises(ValueError, match='Duplicate values'):
        values[0:2] = [9, 9]
    with pytest.raises(ValueError, match='Duplicate values'):
        values[0:2] = [3, 9]

    assert values == [1, 2, 3]
    assert 9 not in values


def test_unique_list_extend_ignore() -> None:
    """Skip duplicates while extending and track the new members."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    values.extend(iter([2, 3, 3, 4]))

    assert values == [1, 2, 3, 4]
    assert 3 in values
    values[2] = 5
    assert values == [1, 2, 5, 4]
    assert 3 not in values


@pytest.mark.parametrize('extra', [[3, 1], [3, 3]])
def test_unique_list_extend_raise(extra: list[int]) -> None:
    """Raise on a duplicate before extending with any of the values."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate='raise'
    )
    with pytest.raises(ValueError, match='Duplicate value'):
        values.extend(extra)

    assert values == [1, 2]
    assert 3 not in values
    values.extend([3, 4])
    assert values == [1, 2, 3, 4]


def test_unique_list_iadd() -> None:
    """Keep ``+=`` unique and return the same list."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    original: containers.UniqueList[int] = values
    values += [2, 3]

    assert values is original
    assert values == [1, 2, 3]
    assert 3 in values


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
def test_unique_list_imul_clear(on_duplicate: containers.OnDuplicate) -> None:
    """Empty the list and its membership when multiplying by zero."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate=on_duplicate
    )
    values *= 1
    assert values == [1, 2]

    values *= 0
    assert values == []
    assert 1 not in values
    values *= 2
    assert values == []
    values.append(1)
    assert values == [1]


def test_unique_list_imul_repeat() -> None:
    """Never repeat the items when multiplying in place."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    values *= 3
    assert values == [1, 2]

    strict: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate='raise'
    )
    with pytest.raises(ValueError, match='Duplicate values'):
        strict *= 2
    assert strict == [1, 2]


def test_unique_list_pop() -> None:
    """Release a popped value so that it can be added again."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    assert values.pop() == 3
    assert values.pop(0) == 1
    assert values == [2]
    assert 1 not in values
    assert 3 not in values
    values.append(3)
    assert values == [2, 3]

    with pytest.raises(IndexError):
        values.pop(5)
    assert values == [2, 3]
    assert 2 in values


def test_unique_list_remove() -> None:
    """Release a removed value so that it can be added again."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, 3, on_duplicate='raise'
    )
    values.remove(2)
    assert values == [1, 3]
    assert 2 not in values
    values.append(2)
    assert values == [1, 3, 2]

    with pytest.raises(ValueError):
        values.remove(9)
    assert values == [1, 3, 2]


def test_unique_list_clear() -> None:
    """Release every value when the list is cleared."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate='raise'
    )
    values.clear()
    assert values == []
    assert 1 not in values
    values.extend([2, 1])
    assert values == [2, 1]


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
@pytest.mark.parametrize('protocol', range(pickle.HIGHEST_PROTOCOL + 1))
def test_unique_list_pickle(
    on_duplicate: containers.OnDuplicate, protocol: int
) -> None:
    """Round-trip through pickle with working membership."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate=on_duplicate
    )
    restored: containers.UniqueList[int] = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )

    assert type(restored) is containers.UniqueList
    assert restored == [1, 2]
    assert restored.on_duplicate == on_duplicate
    assert 1 in restored
    restored.append(3)
    assert restored == [1, 2, 3]
    assert 3 not in values


@pytest.mark.parametrize(
    'data', LEGACY_PICKLES, ids=['protocol-0', 'protocol-2', 'protocol-4']
)
def test_unique_list_legacy_pickle(data: bytes) -> None:
    """Load a pickle written by python-utils 4.0.1."""
    restored: containers.UniqueList[int] = pickle.loads(data)

    assert type(restored) is containers.UniqueList
    assert restored == [1, 2]
    assert restored.on_duplicate == 'raise'
    with pytest.raises(ValueError):
        restored.append(1)
    restored.append(3)
    assert restored == [1, 2, 3]


@pytest.mark.parametrize('on_duplicate', ['ignore', 'raise'])
@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_unique_list_copy(
    on_duplicate: containers.OnDuplicate,
    copier: Copier,
) -> None:
    """Copy the items and give the copy its own membership."""
    values: containers.UniqueList[int] = containers.UniqueList(
        1, 2, on_duplicate=on_duplicate
    )
    copied: containers.UniqueList[int] = copier(values)

    assert type(copied) is containers.UniqueList
    assert copied == [1, 2]
    assert copied.on_duplicate == on_duplicate
    copied.append(3)
    assert copied == [1, 2, 3]
    assert values == [1, 2]
    assert 3 not in values
