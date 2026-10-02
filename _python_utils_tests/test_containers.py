"""Tests for the container types in ``python_utils.containers``."""

import collections
import collections.abc
import copy
import dataclasses
import pickle
import typing
import unittest.mock

import pytest

from python_utils import containers

#: A callable that copies a ``UniqueList``, such as ``copy.copy``.
Copier = collections.abc.Callable[
    [containers.UniqueList[int]], containers.UniqueList[int]
]

#: The protocols that can pickle a class with slots. The standard library
#: refuses such a class on protocol 0 and 1.
SLOTS_PROTOCOLS: range = range(2, pickle.HIGHEST_PROTOCOL + 1)

#: A casted dict class, to run a test against both of them.
CastedDictType = type[containers.CastedDictBase[typing.Any, typing.Any]]

#: ``CastedDict(int, int, {'1': '2'})`` and its lazy counterpart as pickled by
#: python-utils 4.0.1. That release could write protocol 2 and up but not read
#: them back.
LEGACY_DICT_PICKLES: tuple[tuple[CastedDictType, bytes], ...] = (
    (
        containers.CastedDict,
        (
            b'ccopy_reg\n_reconstructor\np0\n(cpython_utils.containers\nCastedDict'
            b'\np1\nc__builtin__\ndict\np2\n(dp3\nI1\nI2\nstp4\nRp5\n(dp6\n'
            b'V_value_cast\np7\nc__builtin__\nlong\np8\nsV_key_cast\np9\ng8\nsb.'
        ),
    ),
    (
        containers.CastedDict,
        (
            b'\x80\x02cpython_utils.containers\nCastedDict\nq\x00)\x81q\x01K\x01K'
            b'\x02s}q\x02(X\x0b\x00\x00\x00_value_castq\x03c__builtin__\nlong\nq'
            b'\x04X\t\x00\x00\x00_key_castq\x05h\x04ub.'
        ),
    ),
    (
        containers.CastedDict,
        (
            b'\x80\x04\x95f\x00\x00\x00\x00\x00\x00\x00\x8c\x17python_utils.'
            b'containers\x94\x8c\nCastedDict\x94\x93\x94)\x81\x94K\x01K\x02s}\x94'
            b'(\x8c\x0b_value_cast\x94\x8c\x08builtins\x94\x8c\x03int\x94\x93\x94'
            b'\x8c\t_key_cast\x94h\x08ub.'
        ),
    ),
    (
        containers.LazyCastedDict,
        (
            b'ccopy_reg\n_reconstructor\np0\n(cpython_utils.containers\n'
            b'LazyCastedDict\np1\nc__builtin__\ndict\np2\n(dp3\nI1\nV2\np4\nstp5'
            b'\nRp6\n(dp7\nV_value_cast\np8\nc__builtin__\nlong\np9\nsV_key_cast'
            b'\np10\ng9\nsb.'
        ),
    ),
    (
        containers.LazyCastedDict,
        (
            b'\x80\x04\x95j\x00\x00\x00\x00\x00\x00\x00\x8c\x17python_utils.'
            b'containers\x94\x8c\x0eLazyCastedDict\x94\x93\x94)\x81\x94K\x01K\x02s'
            b'}\x94(\x8c\x0b_value_cast\x94\x8c\x08builtins\x94\x8c\x03int\x94\x93'
            b'\x94\x8c\t_key_cast\x94h\x08ub.'
        ),
    ),
)


def raw_items(
    values: dict[typing.Any, typing.Any],
) -> dict[typing.Any, typing.Any]:
    """Return the items as they are stored, without any cast."""
    return dict[typing.Any, typing.Any].copy(values)


def double(value: int) -> int:
    """Double a value, as a cast that must not be applied twice."""
    return value * 2


class StrictUniqueList(containers.UniqueList[int]):
    """A list that sets its duplicate policy on the class."""

    on_duplicate: containers.OnDuplicate = 'raise'

    def __init__(self, *values: int) -> None:
        """Fill the list without calling ``UniqueList.__init__``."""
        super(containers.UniqueList, self).__init__()
        self._set = set()
        for value in values:
            self.append(value)


class SlottedUniqueList(containers.UniqueList[int]):
    """A list that keeps extra attributes in slots."""

    __slots__ = ('other', 'tag')

    other: str
    tag: str


class SlottedCastedDict(containers.CastedDict[int, int]):
    """A casted dict that keeps an extra attribute in a slot."""

    __slots__ = ('tag',)

    tag: str


class ReducedCastedDict(containers.CastedDict[int, int]):
    """A casted dict that brings its own pickle support."""

    def __reduce__(self) -> tuple[typing.Any, ...]:
        """Rebuild through the constructor."""
        return ReducedCastedDict, (int, int, raw_items(self))


class StampedCastedDict(containers.CastedDict[int, int]):
    """A casted dict that restores its own state, the textbook way."""

    restored: bool = False

    def __setstate__(self, state: typing.Any) -> None:
        """Restore the instance dictionary and leave a mark."""
        vars(self).update(state)
        self.restored = True


class AuditedCastedDict(containers.CastedDict[int, int]):
    """A casted dict that passes the default reduce value through."""

    def __reduce_ex__(self, protocol: typing.SupportsIndex) -> typing.Any:
        """Unpack the five default items and hand them on."""
        function: typing.Any
        arguments: typing.Any
        state: typing.Any
        list_items: typing.Any
        dict_items: typing.Any
        function, arguments, state, list_items, dict_items = (
            super().__reduce_ex__(protocol)
        )
        return function, arguments, state, list_items, dict_items


class BrokenHash:
    """A value that can no longer be hashed once it is broken."""

    def __init__(self) -> None:
        """Start out hashable."""
        self.broken: bool = False

    def __hash__(self) -> int:
        """Raise an error that is not a ``TypeError`` when broken."""
        if self.broken:
            raise ValueError('broken hash')

        return id(self)


class Reconnecting:
    """A mixin that drops a live handle from the state and reopens it."""

    handle: str

    def __getstate__(self) -> dict[str, typing.Any]:
        """Leave the handle out of the state."""
        state: dict[str, typing.Any] = dict(vars(self))
        state.pop('handle', None)
        return state

    def __setstate__(self, state: dict[str, typing.Any]) -> None:
        """Restore the attributes and reopen the handle."""
        vars(self).update(state)
        self.handle = 'reopened'


class ReconnectingCastedDict(containers.CastedDict[int, int], Reconnecting):
    """A casted dict whose ``__setstate__`` comes from a mixin after it."""


class ReconnectingUniqueList(containers.UniqueList[int], Reconnecting):
    """A unique list whose ``__setstate__`` comes from a mixin after it."""


class VersionedCastedDict(containers.CastedDict[int, int]):
    """A casted dict that adds a version to the default reduce state."""

    version: int = 0

    def __reduce_ex__(self, protocol: typing.SupportsIndex) -> typing.Any:
        """Edit the default state, which is the instance dictionary."""
        function: typing.Any
        arguments: typing.Any
        state: typing.Any
        list_items: typing.Any
        dict_items: typing.Any
        function, arguments, state, list_items, dict_items = (
            super().__reduce_ex__(protocol)
        )
        state = {**state, 'version': 2}
        return function, arguments, state, list_items, dict_items


class CountingCast:
    """A key cast that adds one and counts how often it is called."""

    def __init__(self) -> None:
        """Start without any calls."""
        self.calls: int = 0

    def __call__(self, key: int) -> int:
        """Return the key plus one."""
        self.calls += 1
        return key + 1


class BareCastedDict(containers.CastedDict[str, int]):
    """A casted dict without casts that never calls the base constructor."""

    def __init__(self) -> None:
        """Leave the casts at their class defaults."""


@dataclasses.dataclass(unsafe_hash=True)
class Point:
    """A hashable value whose hash changes when it is mutated."""

    x: int


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
    last: int = values.pop()
    first: int = values.pop(0)
    assert (last, first) == (3, 1)
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


def test_unique_list_class_level_on_duplicate() -> None:
    """Honour a duplicate policy that a subclass sets on the class."""
    values: StrictUniqueList = StrictUniqueList(1, 2)

    assert values.on_duplicate == 'raise'
    with pytest.raises(ValueError, match='Duplicate value'):
        values.append(1)
    assert values == [1, 2]


@pytest.mark.parametrize('protocol', SLOTS_PROTOCOLS)
def test_unique_list_slots_pickle(protocol: int) -> None:
    """Keep the slots of a subclass through pickle."""
    values: SlottedUniqueList = SlottedUniqueList(1, 2, on_duplicate='raise')
    values.tag = 'spam'
    values.other = 'eggs'
    restored: SlottedUniqueList = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )

    assert restored == [1, 2]
    assert restored.on_duplicate == 'raise'
    assert (restored.tag, restored.other) == ('spam', 'eggs')
    assert set(vars(restored)) == {'on_duplicate', '_set'}
    restored.append(3)
    assert 3 in restored


@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_unique_list_slots_copy(
    copier: collections.abc.Callable[[SlottedUniqueList], SlottedUniqueList],
) -> None:
    """Keep the slots of a subclass through a copy."""
    values: SlottedUniqueList = SlottedUniqueList(1, 2, on_duplicate='raise')
    values.tag = 'spam'
    values.other = 'eggs'
    copied: SlottedUniqueList = copier(values)

    assert copied == [1, 2]
    assert copied.on_duplicate == 'raise'
    assert (copied.tag, copied.other) == ('spam', 'eggs')
    copied.append(3)
    assert 3 not in values


def test_unique_list_pop_after_hash_change() -> None:
    """Return a popped item even when its hash changed in the list."""
    point: Point = Point(1)
    other: Point = Point(5)
    values: containers.UniqueList[Point] = containers.UniqueList(other, point)
    point.x = 2
    popped: Point = values.pop()

    assert popped is point
    assert values == [other]
    assert point not in values
    assert other in values
    values.append(point)
    assert values == [other, point]


def test_unique_list_replace_after_hash_change() -> None:
    """Replace an item by index even when its hash changed in the list."""
    point: Point = Point(1)
    other: Point = Point(5)
    values: containers.UniqueList[Point] = containers.UniqueList(point)
    point.x = 2
    values[0] = other

    assert values == [other]
    assert point not in values
    assert other in values


def test_unique_list_remove_equal_unhashable() -> None:
    """Release the stored item when an equal, unhashable value removes it."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2, 3)
    values.remove(unittest.mock.ANY)

    assert values == [2, 3]
    assert 1 not in values
    values.append(1)
    assert values == [2, 3, 1]


def test_unique_list_failed_insert_preserves_membership() -> None:
    """Do not reserve a value when the insert itself fails."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    bad_index: typing.Any = 'spam'
    with pytest.raises(TypeError):
        values.insert(bad_index, 3)

    assert values == [1, 2]
    assert 3 not in values
    values.append(3)
    assert values == [1, 2, 3]


def test_unique_list_contains_unhashable() -> None:
    """Answer a membership test for an unhashable value like a list does."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    unhashable: typing.Any = [1]

    assert unhashable not in values
    assert unittest.mock.ANY in values


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
@pytest.mark.parametrize('protocol', range(pickle.HIGHEST_PROTOCOL + 1))
def test_casted_dict_pickle(dict_type: CastedDictType, protocol: int) -> None:
    """Round-trip a casted dict through pickle without casting again."""
    values: containers.CastedDictBase[int, int] = dict_type(int, double)
    values['1'] = 2
    restored: containers.CastedDictBase[int, int] = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )

    assert type(restored) is dict_type
    assert raw_items(restored) == raw_items(values)
    assert restored[1] == values[1]
    restored['3'] = 4
    assert restored[3] == 8


@pytest.mark.parametrize(
    'dict_type,data',
    LEGACY_DICT_PICKLES,
    ids=['strict-0', 'strict-2', 'strict-4', 'lazy-0', 'lazy-4'],
)
def test_casted_dict_legacy_pickle(
    dict_type: CastedDictType, data: bytes
) -> None:
    """Load a pickle written by python-utils 4.0.1."""
    restored: containers.CastedDictBase[int, int] = pickle.loads(data)

    assert type(restored) is dict_type
    assert restored[1] == 2
    restored['3'] = '4'
    assert restored[3] == 4


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_casted_dict_copy(
    dict_type: CastedDictType,
    copier: collections.abc.Callable[
        [containers.CastedDictBase[int, int]],
        containers.CastedDictBase[int, int],
    ],
) -> None:
    """Copy the stored items as they are, without casting them again."""
    values: containers.CastedDictBase[int, int] = dict_type(int, double)
    values['1'] = 2
    copied: containers.CastedDictBase[int, int] = copier(values)

    assert type(copied) is dict_type
    assert raw_items(copied) == raw_items(values)
    assert copied[1] == values[1]
    copied['3'] = 4
    assert copied[3] == 8
    assert 3 not in values


def test_casted_dict_deepcopy_cycle() -> None:
    """Deep-copy a casted dict that contains itself."""
    values: containers.CastedDict[str, typing.Any] = containers.CastedDict(
        str, None
    )
    values['self'] = values
    copied: containers.CastedDict[str, typing.Any] = copy.deepcopy(values)

    assert copied['self'] is copied
    assert copied is not values


@pytest.mark.parametrize('protocol', SLOTS_PROTOCOLS)
def test_casted_dict_slots_pickle(protocol: int) -> None:
    """Keep the slots of a subclass through pickle."""
    values: SlottedCastedDict = SlottedCastedDict(int, int)
    values['1'] = '2'
    values.tag = 'spam'
    restored: SlottedCastedDict = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )

    assert restored == {1: 2}
    assert restored.tag == 'spam'
    restored['3'] = '4'
    assert restored[3] == 4


def test_casted_dict_default_slots_state() -> None:
    """Accept the default state of a class with slots, as 4.0.1 wrote it."""
    values: SlottedCastedDict = SlottedCastedDict.__new__(SlottedCastedDict)
    values.__setstate__(
        ({'_key_cast': int, '_value_cast': int}, {'tag': 'spam'})
    )
    values['1'] = '2'

    assert values == {1: 2}
    assert values.tag == 'spam'


def test_casted_dict_slots_copy() -> None:
    """Keep the slots of a subclass through a copy."""
    values: SlottedCastedDict = SlottedCastedDict(int, int)
    values['1'] = '2'
    values.tag = 'spam'
    copied: SlottedCastedDict = copy.copy(values)

    assert copied == {1: 2}
    assert copied.tag == 'spam'


def test_casted_dict_custom_reduce() -> None:
    """Leave a subclass with its own ``__reduce__`` alone."""
    values: ReducedCastedDict = ReducedCastedDict(int, int)
    values['1'] = '2'
    restored: ReducedCastedDict = pickle.loads(pickle.dumps(values))
    copied: ReducedCastedDict = copy.copy(values)

    assert type(restored) is ReducedCastedDict
    assert restored == copied == {1: 2}


@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_casted_dict_copy_without_attributes(
    copier: collections.abc.Callable[[BareCastedDict], BareCastedDict],
) -> None:
    """Copy a dict whose instance holds no attributes at all."""
    values: BareCastedDict = BareCastedDict()
    values['spam'] = 1
    copied: BareCastedDict = copier(values)

    assert type(copied) is BareCastedDict
    assert copied == {'spam': 1}
    assert vars(copied) == {}


def test_casted_dict_setdefault() -> None:
    """Cast the key and the value that ``setdefault`` stores."""
    values: containers.CastedDict[int, int] = containers.CastedDict(int, int)
    first: int = values.setdefault('1', '2')
    second: int = values.setdefault('1', '9')
    third: int = values.setdefault(1, '9')

    assert (first, second, third) == (2, 2, 2)
    assert raw_items(values) == {1: 2}


def test_casted_dict_setdefault_without_casts() -> None:
    """Behave like ``dict.setdefault`` when there are no casts."""
    values: containers.CastedDict[str, typing.Any] = containers.CastedDict()
    missing: typing.Any = values.setdefault('spam')
    present: typing.Any = values.setdefault('spam', 'eggs')

    assert missing is None
    assert present is None
    assert values == {'spam': None}


def test_lazy_casted_dict_setdefault() -> None:
    """Cast the key that ``setdefault`` stores and keep the value raw."""
    values: containers.LazyCastedDict[int, int] = containers.LazyCastedDict(
        int, int
    )
    values.setdefault('1', '2')
    values.setdefault(1, '9')

    assert raw_items(values) == {1: '2'}
    assert values[1] == 2


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
def test_casted_dict_ior(dict_type: CastedDictType) -> None:
    """Cast what ``|=`` merges in and keep the same dict."""
    values: containers.CastedDictBase[int, int] = dict_type(int, int)
    original: containers.CastedDictBase[int, int] = values
    values |= {'1': '2'}
    values |= [('3', '4')]

    assert values is original
    assert list(values) == [1, 3]
    assert (values[1], values[3]) == (2, 4)


def test_casted_dict_update_keyword_precedence() -> None:
    """Let keyword arguments win over the mapping, like ``dict`` does."""
    plain: dict[str, int] = {'a': 0, 'b': 0}
    plain.update({'a': 1, 'c': 3}, a=2, b=1)
    values: containers.CastedDict[str, int] = containers.CastedDict(
        None, None, {'a': 0, 'b': 0}
    )
    values.update({'a': 1, 'c': 3}, a=2, b=1)
    constructed: containers.CastedDict[str, int] = containers.CastedDict(
        None, None, {'a': 1}, a=2
    )

    assert values == plain
    assert list(values) == list(plain)
    assert constructed == {'a': 2}


def test_casted_dict_update_single_positional() -> None:
    """Reject a second positional argument like ``dict.update`` does."""
    values: containers.CastedDict[int, int] = containers.CastedDict(int, int)
    first: typing.Any = {'1': '2'}
    second: typing.Any = {'3': '4'}

    # The message is the interpreter's own and differs on PyPy.
    with pytest.raises(TypeError, match='update'):
        values.update(first, second)
    assert values == {}


def test_sliceable_deque_ne() -> None:
    """Keep ``!=`` the opposite of ``==`` for every supported type."""
    values: containers.SliceableDeque[int] = containers.SliceableDeque(
        [1, 2, 3]
    )
    equal: list[typing.Any] = [
        [1, 2, 3],
        (1, 2, 3),
        {1, 2, 3},
        collections.deque([1, 2, 3]),
        containers.SliceableDeque([1, 2, 3]),
    ]
    different: list[typing.Any] = [[1, 2], (3, 2, 1), {1, 2}, 'spam', None]

    for other in equal:
        assert (values == other) is True
        assert (values != other) is False
    for other in different:
        assert (values != other) is True
        assert (values == other) is False


def test_sliceable_deque_eq_set_unhashable() -> None:
    """Compare unequal to a set when an item cannot be hashed."""
    values: containers.SliceableDeque[list[int]] = containers.SliceableDeque(
        [[1], [2]]
    )
    other: typing.Any = {1, 2}

    assert (values == other) is False
    assert (values != other) is True


@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_casted_dict_subclass_setstate_copy(
    copier: collections.abc.Callable[[StampedCastedDict], StampedCastedDict],
) -> None:
    """Hand a subclass with its own ``__setstate__`` the default state."""
    values: StampedCastedDict = StampedCastedDict(int, int)
    values['1'] = '2'
    copied: StampedCastedDict = copier(values)

    assert copied == {1: 2}
    assert copied.restored
    copied['3'] = '4'
    assert copied[3] == 4


@pytest.mark.parametrize('protocol', range(pickle.HIGHEST_PROTOCOL + 1))
def test_casted_dict_subclass_setstate_pickle(protocol: int) -> None:
    """Pickle a subclass with its own ``__setstate__`` on every protocol."""
    values: StampedCastedDict = StampedCastedDict(int, int)
    values['1'] = '2'
    restored: StampedCastedDict = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )

    assert restored == {1: 2}
    assert restored.restored


def test_casted_dict_reduce_shape() -> None:
    """Keep the five items of the default reduce value."""
    values: AuditedCastedDict = AuditedCastedDict(int, int)
    values['1'] = '2'
    plain: containers.CastedDict[int, int] = containers.CastedDict(int, int)
    plain['1'] = '2'

    assert len(plain.__reduce_ex__(pickle.HIGHEST_PROTOCOL)) == 5
    assert copy.copy(values) == {1: 2}
    assert pickle.loads(pickle.dumps(values)) == {1: 2}


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
@pytest.mark.parametrize('protocol', range(2, pickle.HIGHEST_PROTOCOL + 1))
def test_casted_dict_empty_pickle_is_default(
    dict_type: CastedDictType, protocol: int
) -> None:
    """Pickle an empty dict in the form that python-utils 4.0.1 can load."""
    values: containers.CastedDictBase[int, int] = dict_type(int, int)
    state: typing.Any = values.__reduce_ex__(protocol)[2]

    assert state == {'_key_cast': int, '_value_cast': int}
    assert pickle.loads(pickle.dumps(values, protocol=protocol)) == {}


def test_unique_list_pop_with_broken_hash() -> None:
    """Return a popped item when no item in the list can be hashed."""
    first: BrokenHash = BrokenHash()
    second: BrokenHash = BrokenHash()
    values: containers.UniqueList[BrokenHash] = containers.UniqueList(
        first, second
    )
    first.broken = True
    second.broken = True
    popped: BrokenHash = values.pop()
    values.remove(first)

    assert popped is second
    assert values == []


def test_unique_list_remove_missing() -> None:
    """Raise the error of ``list.remove`` for a missing value."""
    values: containers.UniqueList[int] = containers.UniqueList(1, 2)
    plain: list[int] = [1, 2]
    with pytest.raises(ValueError) as expected:
        plain.remove(9)
    with pytest.raises(ValueError) as raised:
        values.remove(9)

    assert str(raised.value) == str(expected.value)
    assert values == [1, 2]


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
def test_casted_dict_key_cast_once(dict_type: CastedDictType) -> None:
    """Cast a key exactly once when it is stored."""
    key_cast: CountingCast = CountingCast()
    values: containers.CastedDictBase[int, str] = dict_type(key_cast, None)
    values[1] = 'spam'

    assert raw_items(values) == {2: 'spam'}
    assert key_cast.calls == 1


@pytest.mark.parametrize(
    'dict_type', [containers.CastedDict, containers.LazyCastedDict]
)
def test_casted_dict_setdefault_key_cast_once(
    dict_type: CastedDictType,
) -> None:
    """Cast the key of ``setdefault`` exactly once, found or not."""
    key_cast: CountingCast = CountingCast()
    values: containers.CastedDictBase[int, str] = dict_type(key_cast, None)
    stored: str = values.setdefault(1, 'spam')
    found: str = values.setdefault(1, 'eggs')

    assert (stored, found) == ('spam', 'spam')
    assert raw_items(values) == {2: 'spam'}
    assert key_cast.calls == 2


@pytest.mark.parametrize('value_cast', [int, str])
def test_casted_dict_setdefault_none(
    value_cast: collections.abc.Callable[[typing.Any], typing.Any],
) -> None:
    """Store a missing default as ``None`` without casting it."""
    values: containers.CastedDict[int, typing.Any] = containers.CastedDict(
        int, value_cast
    )
    implicit: typing.Any = values.setdefault('1')
    explicit: typing.Any = values.setdefault('2', None)

    assert implicit is None
    assert explicit is None
    assert raw_items(values) == {1: None, 2: None}


@pytest.mark.parametrize('protocol', [0, pickle.HIGHEST_PROTOCOL])
def test_casted_dict_mixin_setstate(protocol: int) -> None:
    """Run a ``__setstate__`` from a mixin that comes after the dict."""
    values: ReconnectingCastedDict = ReconnectingCastedDict(int, int)
    values['1'] = '2'
    values.handle = 'open'
    restored: ReconnectingCastedDict = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )
    copied: ReconnectingCastedDict = copy.copy(values)

    assert restored == copied == {1: 2}
    assert (restored.handle, copied.handle) == ('reopened', 'reopened')
    copied['3'] = '4'
    assert copied[3] == 4


@pytest.mark.parametrize('protocol', [0, pickle.HIGHEST_PROTOCOL])
def test_unique_list_mixin_setstate(protocol: int) -> None:
    """Run a ``__setstate__`` from a mixin that comes after the list."""
    values: ReconnectingUniqueList = ReconnectingUniqueList(1, 2)
    values.handle = 'open'
    restored: ReconnectingUniqueList = pickle.loads(
        pickle.dumps(values, protocol=protocol)
    )
    copied: ReconnectingUniqueList = copy.copy(values)

    assert restored == copied == [1, 2]
    assert (restored.handle, copied.handle) == ('reopened', 'reopened')
    copied.append(1)
    copied.append(3)
    assert copied == [1, 2, 3]


@pytest.mark.parametrize('copier', [copy.copy, copy.deepcopy])
def test_casted_dict_subclass_reduce_ex_state(
    copier: collections.abc.Callable[
        [VersionedCastedDict], VersionedCastedDict
    ],
) -> None:
    """Give a subclass ``__reduce_ex__`` the default state to work on."""
    values: VersionedCastedDict = VersionedCastedDict(int, int)
    values['1'] = '2'
    copied: VersionedCastedDict = copier(values)
    restored: VersionedCastedDict = pickle.loads(pickle.dumps(values))

    assert copied == restored == {1: 2}
    assert (copied.version, restored.version) == (2, 2)


def test_unique_list_delete_after_hash_change() -> None:
    """Delete an item or a slice even when a hash changed in the list."""
    first: Point = Point(1)
    second: Point = Point(2)
    third: Point = Point(3)
    values: containers.UniqueList[Point] = containers.UniqueList(
        first, second, third
    )
    second.x = 99
    del values[1]

    assert values == [first, third]
    assert second not in values

    third.x = 98
    del values[0:2]

    assert values == []
    values.append(first)
    assert values == [first]
