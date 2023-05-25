# pyright: reportIncompatibleMethodOverride=false
import abc
import typing

from . import types

if typing.TYPE_CHECKING:
    import _typeshed  # noqa: F401

#: A type alias for a type that can be used as a key in a dictionary.
KT = types.TypeVar('KT')
#: A type alias for a type that can be used as a value in a dictionary.
VT = types.TypeVar('VT')
#: A type alias for a dictionary with keys of type KT and values of type VT.
DT = types.Dict[KT, VT]
#: A type alias for the casted type of a dictionary key.
KT_cast = types.Optional[types.Callable[..., KT]]
#: A type alias for the casted type of a dictionary value.
VT_cast = types.Optional[types.Callable[..., VT]]
#: A type alias for the hashable values of the `UniqueList`
HT = types.TypeVar('HT', bound=types.Hashable)

# Using types.Union instead of | since Python 3.7 doesn't fully support it
DictUpdateArgs = types.Union[
    types.Mapping[KT, VT],
    types.Iterable[types.Tuple[KT, VT]],
    types.Iterable[types.Mapping[KT, VT]],
    '_typeshed.SupportsKeysAndGetItem[KT, VT]',
]


class CastedDictBase(types.Dict[KT, VT], abc.ABC):
    _key_cast: KT_cast[KT]
    _value_cast: VT_cast[VT]

    def __init__(
        self,
        key_cast: KT_cast[KT] = None,
        value_cast: VT_cast[VT] = None,
        *args: DictUpdateArgs[KT, VT],
        **kwargs: VT,
    ) -> None:
        self._value_cast = value_cast
        self._key_cast = key_cast
        self.update(*args, **kwargs)

    def update(
        self, *args: DictUpdateArgs[types.Any, types.Any], **kwargs: types.Any
    ) -> None:
        if args:
            kwargs.update(*args)

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __setitem__(self, key: types.Any, value: types.Any) -> None:
        if self._key_cast is not None:
            key = self._key_cast(key)

        return super().__setitem__(key, value)


class CastedDict(CastedDictBase[KT, VT]):
    '''
    Custom dictionary that casts keys and values to the specified typing.

    Note that you can specify the types for mypy and type hinting with:
    CastedDict[int, int](int, int)

    >>> d: CastedDict[int, int] = CastedDict(int, int)
    >>> d[1] = 2
    >>> d['3'] = '4'
    >>> d.update({'5': '6'})
    >>> d.update([('7', '8')])
    >>> d
    {1: 2, 3: 4, 5: 6, 7: 8}
    >>> list(d.keys())
    [1, 3, 5, 7]
    >>> list(d)
    [1, 3, 5, 7]
    >>> list(d.values())
    [2, 4, 6, 8]
    >>> list(d.items())
    [(1, 2), (3, 4), (5, 6), (7, 8)]
    >>> d[3]
    4

    # Casts are optional and can be disabled by passing None as the cast
    >>> d = CastedDict()
    >>> d[1] = 2
    >>> d['3'] = '4'
    >>> d.update({'5': '6'})
    >>> d.update([('7', '8')])
    >>> d
    {1: 2, '3': '4', '5': '6', '7': '8'}
    '''

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        if self._value_cast is not None:
            value = self._value_cast(value)

        super().__setitem__(key, value)


class LazyCastedDict(CastedDictBase[KT, VT]):
    '''
    Custom dictionary that casts keys and lazily casts values to the specified
    typing. Note that the values are cast only when they are accessed and
    are not cached between executions.

    Note that you can specify the types for mypy and type hinting with:
    LazyCastedDict[int, int](int, int)

    >>> d: LazyCastedDict[int, int] = LazyCastedDict(int, int)
    >>> d[1] = 2
    >>> d['3'] = '4'
    >>> d.update({'5': '6'})
    >>> d.update([('7', '8')])
    >>> d
    {1: 2, 3: '4', 5: '6', 7: '8'}
    >>> list(d.keys())
    [1, 3, 5, 7]
    >>> list(d)
    [1, 3, 5, 7]
    >>> list(d.values())
    [2, 4, 6, 8]
    >>> list(d.items())
    [(1, 2), (3, 4), (5, 6), (7, 8)]
    >>> d[3]
    4

    # Casts are optional and can be disabled by passing None as the cast
    >>> d = LazyCastedDict()
    >>> d[1] = 2
    >>> d['3'] = '4'
    >>> d.update({'5': '6'})
    >>> d.update([('7', '8')])
    >>> d
    {1: 2, '3': '4', '5': '6', '7': '8'}
    >>> list(d.keys())
    [1, '3', '5', '7']
    >>> list(d.values())
    [2, '4', '6', '8']

    >>> list(d.items())
    [(1, 2), ('3', '4'), ('5', '6'), ('7', '8')]
    >>> d['3']
    '4'
    '''

    def __setitem__(self, key: types.Any, value: types.Any):
        if self._key_cast is not None:
            key = self._key_cast(key)

        super().__setitem__(key, value)

    def __getitem__(self, key: types.Any) -> VT:
        if self._key_cast is not None:
            key = self._key_cast(key)

        value = super().__getitem__(key)

        if self._value_cast is not None:
            value = self._value_cast(value)

        return value

    def items(  # type: ignore
        self,
    ) -> types.Generator[types.Tuple[KT, VT], None, None]:
        if self._value_cast is None:
            yield from super().items()
        else:
            for key, value in super().items():
                yield key, self._value_cast(value)

    def values(self) -> types.Generator[VT, None, None]:  # type: ignore
        if self._value_cast is None:
            yield from super().values()
        else:
            for value in super().values():
                yield self._value_cast(value)


class UniqueList(types.List[HT]):
    '''
    A list that only allows unique values. Duplicate values are ignored by
    default, but can be configured to raise an exception instead.

    >>> l = UniqueList(1, 2, 3)
    >>> l.append(4)
    >>> l.append(4)
    >>> l.insert(0, 4)
    >>> l.insert(0, 5)
    >>> l[1] = 10
    >>> l
    [5, 10, 2, 3, 4]

    >>> l = UniqueList(1, 2, 3, on_duplicate='raise')
    >>> l.append(4)
    >>> l.append(4)
    Traceback (most recent call last):
    ...
    ValueError: Duplicate value: 4
    >>> l.insert(0, 4)
    Traceback (most recent call last):
    ...
    ValueError: Duplicate value: 4
    >>> 4 in l
    True
    >>> l[0]
    1
    >>> l[1] = 4
    Traceback (most recent call last):
    ...
    ValueError: Duplicate value: 4
    '''

    _set: types.Set[HT]

    def __init__(
        self,
        *args: HT,
        on_duplicate: types.Literal['raise', 'ignore'] = 'ignore',
    ):
        self.on_duplicate = on_duplicate
        self._set = set()
        super().__init__()
        for arg in args:
            self.append(arg)

    def insert(self, index: types.SupportsIndex, value: HT) -> None:
        if value in self._set:
            if self.on_duplicate == 'raise':
                raise ValueError('Duplicate value: %s' % value)
            else:
                return

        self._set.add(value)
        super().insert(index, value)

    def append(self, value: HT) -> None:
        if value in self._set:
            if self.on_duplicate == 'raise':
                raise ValueError('Duplicate value: %s' % value)
            else:
                return

        self._set.add(value)
        super().append(value)

    def __contains__(self, item: HT) -> bool:  # type: ignore
        return item in self._set

    @types.overload
    def __setitem__(self, indices: types.SupportsIndex, values: HT) -> None:
        ...

    @types.overload
    def __setitem__(self, indices: slice, values: types.Iterable[HT]) -> None:
        ...

    def __setitem__(
        self,
        indices: types.Union[slice, types.SupportsIndex],
        values: types.Union[types.Iterable[HT], HT],
    ) -> None:
        if isinstance(indices, slice):
            values = types.cast(types.Iterable[HT], values)
            if self.on_duplicate == 'ignore':
                raise RuntimeError(
                    'ignore mode while setting slices introduces ambiguous '
                    'behaviour and is therefore not supported'
                )

            duplicates: types.Set[HT] = set(values) & self._set
            if duplicates and values != list(self[indices]):
                raise ValueError(f'Duplicate values: {duplicates}')

            self._set.update(values)
        else:
            values = types.cast(HT, values)
            if values in self._set and values != self[indices]:
                if self.on_duplicate == 'raise':
                    raise ValueError(f'Duplicate value: {values}')
                else:
                    return

            self._set.add(values)

        super().__setitem__(
            types.cast(slice, indices), types.cast(types.List[HT], values)
        )

    def __delitem__(
        self, index: types.Union[types.SupportsIndex, slice]
    ) -> None:
        if isinstance(index, slice):
            for value in self[index]:
                self._set.remove(value)
        else:
            self._set.remove(self[index])

        super().__delitem__(index)


class SlicableDeque(Generic[T], deque):
    def __getitem__(self, index: Union[int, slice]) -> Union[T, 'SlicableDeque[T]']:
        """
        Return the item or slice at the given index.

        >>> d = SlicableDeque[int]([1, 2, 3, 4, 5])
        >>> d[1:4]
        SlicableDeque([2, 3, 4])

        >>> d = SlicableDeque[str](['a', 'b', 'c'])
        >>> d[-2:]
        SlicableDeque(['b', 'c'])

        """
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return self.__class__(self[i] for i in range(start, stop, step))
        else:
            return super().__getitem__(index)

    def pop(self) -> T:
        """
        Remove and return the rightmost element.

        >>> d = SlicableDeque[float]([1.5, 2.5, 3.5])
        >>> d.pop()
        3.5

        """
        return super().pop()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
