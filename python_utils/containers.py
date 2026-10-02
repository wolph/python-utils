"""
This module provides custom container classes with enhanced functionality.

Classes::

    CastedDictBase: Abstract base class for dictionaries that cast keys and
        values.
    CastedDict: Dictionary that casts keys and values to specified types.
    LazyCastedDict: Dictionary that lazily casts values to specified types upon
        access.
    UniqueList: List that only allows unique values, with configurable behavior
        on duplicates.
    SliceableDeque: Deque that supports slicing and enhanced equality checks.

Type Aliases::

    KT: Type variable for dictionary keys.
    VT: Type variable for dictionary values.
    DT: Type alias for a dictionary with keys of type KT and values of type VT.
    KT_cast: Type alias for a callable that casts dictionary keys.
    VT_cast: Type alias for a callable that casts dictionary values.
    HT: Type variable for hashable values in UniqueList.
    T: Type variable for generic types.
    DictUpdateArgs: Union type for arguments that can be used to update a
        dictionary.
    OnDuplicate: Literal type for handling duplicate values in UniqueList.

Usage::

    - CastedDict and LazyCastedDict can be used to create dictionaries with
        automatic type casting.
    - UniqueList ensures all elements are unique and can raise an error on
        duplicates.
    - SliceableDeque extends deque with slicing support and enhanced equality
        checks.

Examples:
    >>> d = CastedDict(int, int)
    >>> d[1] = 2
    >>> d['3'] = '4'
    >>> d.update({'5': '6'})
    >>> d.update([('7', '8')])
    >>> d
    {1: 2, 3: 4, 5: 6, 7: 8}

    >>> l = UniqueList(1, 2, 3)
    >>> l.append(4)
    >>> l.append(4)
    >>> l.insert(0, 4)
    >>> l.insert(0, 5)
    >>> l[1] = 10
    >>> l
    [5, 10, 2, 3, 4]

    >>> d = SliceableDeque([1, 2, 3, 4, 5])
    >>> d[1:4]
    SliceableDeque([2, 3, 4])
"""

# pyright: reportIncompatibleMethodOverride=false
import abc
import collections
import collections.abc
import contextlib
import operator
import typing

if typing.TYPE_CHECKING:
    import _typeshed  # noqa: F401
    import typing_extensions

#: A type alias for a type that can be used as a key in a dictionary.
KT = typing.TypeVar('KT')
#: A type alias for a type that can be used as a value in a dictionary.
VT = typing.TypeVar('VT')
#: A type alias for a dictionary with keys of type KT and values of type VT.
DT = dict[KT, VT]
#: A type alias for the casted type of a dictionary key.
KT_cast = collections.abc.Callable[..., KT] | None
#: A type alias for the casted type of a dictionary value.
VT_cast = collections.abc.Callable[..., VT] | None
#: A type alias for the hashable values of the `UniqueList`
HT = typing.TypeVar('HT', bound=collections.abc.Hashable)
#: A type alias for a regular generic type
T = typing.TypeVar('T')

#: Argument shapes accepted when updating a casted dict: a mapping, an iterable
#: of key/value pairs, or a keys-and-getitem object.
# Kept as `typing.Union` (not PEP 604 `|`): one member is a string forward
# reference, and `|` evaluates its operands eagerly, raising `TypeError` on a
# `str` operand at runtime. `typing.Union` accepts it as a lazy `ForwardRef`.
DictUpdateArgs = typing.Union[
    collections.abc.Mapping[KT, VT],
    collections.abc.Iterable[tuple[KT, VT]],
    '_typeshed.SupportsKeysAndGetItem[KT, VT]',
]

#: Policy for ``UniqueList`` duplicates: silently ``'ignore'`` or ``'raise'``.
OnDuplicate = typing.Literal['ignore', 'raise']

#: Marks the state that ``CastedDictBase.__reduce_ex__`` writes, to tell it
#: apart from the default state of an instance with slots.
_CASTED_DICT_STATE: str = 'python_utils.containers.CastedDictBase'


def _restore_attributes(
    instance: object,
    state: typing.Any,
    inherited: collections.abc.Callable[[typing.Any], None] | None,
) -> None:
    """
    Restores the attributes of an instance from its default pickle state.

    The default state is the instance dictionary, or a tuple of that
    dictionary and the slot values when the class has slots. `pickle` and
    `copy` apply both forms themselves, but only for a class without a
    `__setstate__` of its own.

    A `__setstate__` that follows the calling class in the method resolution
    order gets the state when there is one. It would have received it if the
    calling class did not define `__setstate__`.

    Args:
        instance (object): The instance to restore.
        state (typing.Any): The default state of the instance.
        inherited (Callable[[typing.Any], None] | None): The `__setstate__`
            that follows the calling class, or None without one.
    """
    if inherited is not None:
        inherited(state)
        return

    slots: dict[str, typing.Any] | None = None
    if isinstance(state, tuple):
        state, slots = typing.cast(
            'tuple[dict[str, typing.Any] | None, dict[str, typing.Any]]',
            state,
        )

    if state:
        vars(instance).update(state)

    if slots:
        for name, value in slots.items():
            setattr(instance, name, value)


class CastedDictBase(dict[KT, VT], abc.ABC):
    """
    Abstract base class for dictionaries that cast keys and values.

    Attributes:
        _key_cast (KT_cast[KT]): Callable to cast dictionary keys.
        _value_cast (VT_cast[VT]): Callable to cast dictionary values.

    Methods::

        __init__(key_cast: KT_cast[KT] = None, value_cast: VT_cast[VT] = None,
            *args: DictUpdateArgs[KT, VT], **kwargs: VT) -> None:
            Initializes the dictionary with optional key and value casting
            callables.
        update(*args: DictUpdateArgs[typing.Any, typing.Any],
            **kwargs: typing.Any) -> None:
            Updates the dictionary with the given arguments.
        __setitem__(key: typing.Any, value: typing.Any) -> None:
            Sets the item in the dictionary, casting the key if a key cast
            callable is provided.
    """

    # The casts default to `None` on the class so that a dict which `pickle`
    # created without calling `__init__` can already store items.
    _key_cast: KT_cast[KT] = None
    _value_cast: VT_cast[VT] = None

    def __init__(
        self,
        key_cast: KT_cast[KT] = None,
        value_cast: VT_cast[VT] = None,
        *args: DictUpdateArgs[KT, VT],
        **kwargs: VT,
    ) -> None:
        """
        Initializes the CastedDictBase with optional key and value
        casting callables.

        Args:
            key_cast (KT_cast[KT], optional): Callable to cast
                dictionary keys. Defaults to None.
            value_cast (VT_cast[VT], optional): Callable to cast
                dictionary values. Defaults to None.
            *args (DictUpdateArgs[KT, VT]): Arguments to initialize
                the dictionary.
            **kwargs (VT): Keyword arguments to initialize the
                dictionary.
        """
        self._value_cast = value_cast
        self._key_cast = key_cast
        self.update(*args, **kwargs)

    def update(
        self,
        *args: DictUpdateArgs[typing.Any, typing.Any],
        **kwargs: typing.Any,
    ) -> None:
        """
        Updates the dictionary with the given arguments.

        Args:
            *args (DictUpdateArgs[typing.Any, typing.Any]): Arguments to update
                the dictionary.
            **kwargs (typing.Any): Keyword arguments to update the dictionary.
        """
        # Keyword arguments are applied last so that they win, as they do
        # for `dict.update`.
        positional: dict[typing.Any, typing.Any] = {}
        positional.update(*args)
        for key, value in positional.items():
            self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def setdefault(self, key: typing.Any, default: typing.Any = None) -> VT:
        """
        Stores the default through the casts when the key is missing.

        A default of `None` is stored as `None` without casting it, so that
        `setdefault(key)` works for every value cast.

        Args:
            key (typing.Any): The key to look up, before casting.
            default (typing.Any, optional): The value to store when the key
                is missing. Defaults to None.

        Returns:
            VT: The value that is stored under the key.
        """
        if self._key_cast is not None:
            key = self._key_cast(key)

        if not super().__contains__(key):
            stored: typing.Any = default
            if default is not None:
                stored = self._cast_stored_value(default)

            super().__setitem__(key, stored)

        return super().__getitem__(key)

    def _cast_stored_value(self, value: typing.Any) -> typing.Any:
        """
        Casts a value on its way into the dictionary.

        The base class stores values as they are. A subclass that casts when
        it stores a value overrides this method.

        Args:
            value (typing.Any): The value to store.

        Returns:
            typing.Any: The value as it is stored.
        """
        return value

    def __ior__(  # type: ignore[override, misc]
        self, other: DictUpdateArgs[typing.Any, typing.Any]
    ) -> 'typing_extensions.Self':
        """
        Updates the dictionary in place through the casts, see `update`.

        Args:
            other (DictUpdateArgs[typing.Any, typing.Any]): The items to
                merge into the dictionary.

        Returns:
            typing_extensions.Self: The dictionary itself.
        """
        self.update(other)
        return self

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        """
        Sets the item in the dictionary, casting the key if a key cast
        callable is provided.

        Args:
            key (typing.Any): The key to set in the dictionary.
            value (typing.Any): The value to set in the dictionary.
        """
        if self._key_cast is not None:
            key = self._key_cast(key)

        return super().__setitem__(key, value)

    def __reduce_ex__(self, protocol: typing.SupportsIndex) -> typing.Any:
        """
        Describes the dictionary for `pickle` and `copy` with its raw items.

        By default the items are restored through `__setitem__`. `pickle`
        does that before the casts are back and `copy` does it after, which
        casts every value a second time. The items travel inside the state
        to avoid both.

        The default description is returned unchanged where it already
        works or where other code relies on its form, see the comment below.

        Args:
            protocol (typing.SupportsIndex): The pickle protocol.

        Returns:
            typing.Any: The default description, with the items moved into
                the state for protocol 2 and up.
        """
        reduced: typing.Any = super().__reduce_ex__(protocol)
        if (
            operator.index(protocol) < 2
            or len(self) == 0
            or type(self).__reduce__ is not object.__reduce__
            or type(self).__reduce_ex__ is not _BASE_REDUCE_EX
            or type(self).__setstate__ is not _BASE_SETSTATE
        ):
            # Protocol 0 and 1 restore the items through `dict` itself and
            # an empty dictionary has none. A subclass with its own
            # `__reduce__` describes itself. One with its own `__reduce_ex__`
            # or `__setstate__` expects the default state and items.
            return reduced

        state: tuple[str, typing.Any, dict[KT, VT]] = (
            _CASTED_DICT_STATE,
            reduced[2],
            super().copy(),
        )
        return reduced[0], reduced[1], state, None, None

    def __setstate__(self, state: object) -> None:
        """
        Restores the attributes and the raw items without casting them.

        Args:
            state (object): The state from `__reduce_ex__`, or the default
                state for a pickle that already restored its items.
        """
        parts: tuple[object, ...] = ()
        if isinstance(state, tuple):
            parts = typing.cast('tuple[object, ...]', state)

        # A mixin after this class can have a `__setstate__` of its own.
        inherited: typing.Any = getattr(super(), '__setstate__', None)
        if len(parts) == 3 and parts[0] == _CASTED_DICT_STATE:
            _restore_attributes(self, parts[1], inherited)
            super().update(typing.cast('dict[KT, VT]', parts[2]))
        else:
            _restore_attributes(self, state, inherited)


#: The `__setstate__` that understands the state of
#: `CastedDictBase.__reduce_ex__`. A subclass that replaces it gets the default
#: state.
# Both are taken from the class dictionary. `CastedDictBase[...].__reduce_ex__`
# would be the method of the generic alias itself.
_BASE_SETSTATE: collections.abc.Callable[..., None] = vars(CastedDictBase)[
    '__setstate__'
]
#: The `__reduce_ex__` that writes that state. A subclass that replaces it
#: gets the default description to build on.
_BASE_REDUCE_EX: collections.abc.Callable[..., typing.Any] = vars(
    CastedDictBase
)['__reduce_ex__']


class CastedDict(CastedDictBase[KT, VT]):
    """
    Custom dictionary that casts keys and values to the specified types.

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
    """

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        """Cast ``value`` (if a value cast is set) and store it under ``key``.

        The key itself is cast by ``CastedDictBase.__setitem__`` when a key
        cast is configured.
        """
        super().__setitem__(key, self._cast_stored_value(value))

    def _cast_stored_value(self, value: typing.Any) -> typing.Any:
        """
        Casts a value on its way into the dictionary.

        Args:
            value (typing.Any): The value to store.

        Returns:
            typing.Any: The value, cast when a value cast is set.
        """
        if self._value_cast is not None:
            value = self._value_cast(value)

        return value


class LazyCastedDict(CastedDictBase[KT, VT]):
    """
    Custom dictionary that casts keys and lazily casts values to the specified
    types. Note that the values are cast only when they are accessed and
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
    """

    def __setitem__(self, key: typing.Any, value: typing.Any) -> None:
        """
        Sets the item in the dictionary, casting the key if a key cast
        callable is provided. The value is stored as it is.

        Args:
            key (typing.Any): The key to set in the dictionary.
            value (typing.Any): The value to set in the dictionary.
        """
        # The base class casts the key. Casting it here as well would cast
        # it twice.
        super().__setitem__(key, value)

    def __getitem__(self, key: typing.Any) -> VT:
        """
        Gets the item from the dictionary, casting the value if a value cast
        callable is provided.

        Args:
            key (typing.Any): The key to get from the dictionary.

        Returns:
            VT: The value from the dictionary.
        """
        if self._key_cast is not None:
            key = self._key_cast(key)

        value = super().__getitem__(key)

        if self._value_cast is not None:
            value = self._value_cast(value)

        return value

    def items(  # type: ignore[override]
        self,
    ) -> collections.abc.Generator[tuple[KT, VT], None, None]:
        """
        Returns a generator of the dictionary's items, casting the values if a
        value cast callable is provided.

        Yields:
            Generator[tuple[KT, VT], None, None]: A generator of
                the dictionary's items.
        """
        if self._value_cast is None:
            yield from super().items()
        else:
            for key, value in super().items():
                yield key, self._value_cast(value)

    def values(self) -> collections.abc.Generator[VT, None, None]:  # type: ignore[override]
        """
        Returns a generator of the dictionary's values, casting the values if a
        value cast callable is provided.

        Yields:
            Generator[VT, None, None]: A generator of the dictionary's
                values.
        """
        if self._value_cast is None:
            yield from super().values()
        else:
            for value in super().values():
                yield self._value_cast(value)


class UniqueList(list[HT]):
    """
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

    A value that was removed or replaced can be added again:

    >>> l = UniqueList(1, 2, 3)
    >>> l[0] = 4
    >>> l.pop()
    3
    >>> l.extend([1, 2, 3])
    >>> l
    [4, 2, 1, 3]

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
    """

    _set: set[HT]
    #: The default lives on the class, so that a subclass can set its own
    #: and a list that `pickle` created without `__init__` has one.
    on_duplicate: OnDuplicate = 'ignore'

    def __new__(
        cls, *args: typing.Any, **kwargs: typing.Any
    ) -> 'typing_extensions.Self':
        """
        Creates the list with an empty membership set.

        `pickle` and `copy` create the list through `__new__` and refill it
        through `extend` or `append` without calling `__init__`, so the
        membership set has to exist before `__init__` runs.

        Args:
            *args (typing.Any): Ignored, handled by `__init__`.
            **kwargs (typing.Any): Ignored, handled by `__init__`.

        Returns:
            typing_extensions.Self: The new, empty list.
        """
        instance: typing_extensions.Self = super().__new__(cls)
        instance._set = set()
        return instance

    def __init__(
        self,
        *args: HT,
        on_duplicate: OnDuplicate = 'ignore',
    ):
        """
        Initializes the UniqueList with optional duplicate handling behavior.

        Args:
            *args (HT): Initial values for the list.
            on_duplicate (OnDuplicate, optional): Behavior on duplicates.
                Defaults to 'ignore'.
        """
        self.on_duplicate = on_duplicate
        self._set = set()
        super().__init__()
        for arg in args:
            self.append(arg)

    def __setstate__(self, state: typing.Any) -> None:
        """
        Restores the attributes and rebuilds the membership from the items.

        `copy` restores the attributes before the items and `pickle` restores
        them after the items. A stored membership set is only right in the
        second case, so the set is always derived from the items that are in
        the list at this point.

        Args:
            state (typing.Any): The instance attributes, with the slot values
                when a subclass has slots.
        """
        # A mixin after this class can have a `__setstate__` of its own.
        inherited: typing.Any = getattr(super(), '__setstate__', None)
        _restore_attributes(self, state, inherited)
        self._set = set(self)

    def _release(self, value: HT) -> None:
        """
        Drops a value that left the list from the membership set.

        The set is rebuilt from the list when the value cannot be removed
        from it. That happens when the value changed its hash after it was
        added, and when its `__hash__` or `__eq__` raises.

        The value has left the list by now, so nothing here may raise. When
        the rebuild fails as well the set stays as it is.

        Args:
            value (HT): The value that was removed from the list.
        """
        try:
            self._set.remove(value)
        except Exception:  # noqa: BLE001
            with contextlib.suppress(Exception):
                self._set = set(self)

    def insert(self, index: typing.SupportsIndex, value: HT) -> None:
        """
        Inserts a value at the specified index, ensuring uniqueness.

        Args:
            index (typing.SupportsIndex): The index to insert the value at.
            value (HT): The value to insert.

        Raises:
            ValueError: If the value is a duplicate and `on_duplicate` is set
                to 'raise'.
        """
        if value in self._set:
            if self.on_duplicate == 'raise':
                raise ValueError(f'Duplicate value: {value}')
            else:
                return

        # The membership first, right after the check above. Another thread
        # that inserts the same value in between would get past its own
        # check as well. A failed insert takes the membership back.
        self._set.add(value)
        try:
            super().insert(index, value)
        except BaseException:
            self._set.discard(value)
            raise

    def append(self, value: HT) -> None:
        """
        Appends a value to the list, ensuring uniqueness.

        Args:
            value (HT): The value to append.

        Raises:
            ValueError: If the value is a duplicate and `on_duplicate` is set
                to 'raise'.
        """
        if value in self._set:
            if self.on_duplicate == 'raise':
                raise ValueError(f'Duplicate value: {value}')
            else:
                return

        self._set.add(value)
        super().append(value)

    def extend(self, values: collections.abc.Iterable[HT]) -> None:
        """
        Extends the list with the values that are not in it yet.

        Args:
            values (Iterable[HT]): The values to append.

        Raises:
            ValueError: If `on_duplicate` is set to 'raise' and a value is
                already in the list or occurs more than once in `values`.
                The list is left unchanged in that case.
        """
        new_values: list[HT] = list(values)
        if self.on_duplicate == 'raise':
            duplicates: set[HT] = self._find_duplicates(new_values)
            if duplicates:
                raise ValueError(f'Duplicate values: {duplicates}')

        for value in new_values:
            self.append(value)

    # `list.__iadd__` accepts any iterable while `list.__add__` only accepts
    # a list. Typeshed ignores the same mismatch.
    def __iadd__(  # type: ignore[misc, override]
        self, values: collections.abc.Iterable[HT]
    ) -> 'typing_extensions.Self':
        """
        Extends the list in place, see `extend`.

        Args:
            values (Iterable[HT]): The values to append.

        Returns:
            typing_extensions.Self: The list itself.
        """
        self.extend(values)
        return self

    def __imul__(
        self, value: typing.SupportsIndex
    ) -> 'typing_extensions.Self':
        """
        Multiplies the list in place without ever repeating an item.

        A count below 1 empties the list, as it does for a regular list. A
        count above 1 would repeat every item, so the repeat goes through
        `extend` and follows `on_duplicate`.

        Args:
            value (typing.SupportsIndex): The number of times to repeat.

        Returns:
            typing_extensions.Self: The list itself.

        Raises:
            ValueError: If `on_duplicate` is set to 'raise' and a non-empty
                list is multiplied by more than 1.
        """
        count: int = operator.index(value)
        if count < 1:
            self.clear()
        elif count > 1:
            self.extend(self)

        return self

    def pop(self, index: typing.SupportsIndex = -1) -> HT:
        """
        Removes and returns the item at the given index.

        Args:
            index (typing.SupportsIndex, optional): The index to pop.
                Defaults to the last item.

        Returns:
            HT: The removed item.
        """
        value: HT = super().pop(index)
        self._release(value)
        return value

    def remove(self, value: HT) -> None:
        """
        Removes a value from the list.

        Args:
            value (HT): The value to remove.

        Raises:
            ValueError: If the value is not in the list.
        """
        # One list operation, so that another thread cannot get between
        # finding the value and removing it.
        super().remove(value)
        self._release(value)

    def clear(self) -> None:
        """Removes all items from the list."""
        super().clear()
        self._set.clear()

    def _find_duplicates(
        self,
        values: list[HT],
        replaced: collections.abc.Set[HT] = frozenset(),
    ) -> set[HT]:
        """
        Finds the values that would break uniqueness when added.

        Args:
            values (list[HT]): The values to add.
            replaced (Set[HT], optional): Items that leave the list in the
                same operation, so that adding them again is allowed.

        Returns:
            set[HT]: The values that occur more than once in `values` or
                that are already in the list and not in `replaced`.
        """
        seen: set[HT] = set()
        duplicates: set[HT] = set()
        for value in values:
            if value in seen or (value in self._set and value not in replaced):
                duplicates.add(value)
            seen.add(value)

        return duplicates

    def __contains__(self, item: HT) -> bool:  # type: ignore[override]
        """
        Checks if the list contains the specified item.

        Args:
            item (HT): The item to check for.

        Returns:
            bool: True if the item is in the list, False otherwise.
        """
        try:
            return item in self._set
        except TypeError:
            # An unhashable item cannot be in the set, but it can still be
            # equal to an item in the list.
            return super().__contains__(item)

    @typing.overload
    def __setitem__(self, indices: typing.SupportsIndex, values: HT) -> None:
        """Overload: assign a single value at an integer index."""

    @typing.overload
    def __setitem__(
        self, indices: slice, values: collections.abc.Iterable[HT]
    ) -> None:
        """Overload: assign an iterable of values to a slice."""

    def __setitem__(
        self,
        indices: slice | typing.SupportsIndex,
        values: collections.abc.Iterable[HT] | HT,
    ) -> None:
        """
        Sets the item(s) at the specified index/indices, ensuring uniqueness.

        Args:
            indices (slice | typing.SupportsIndex): The index or
                slice to set the value(s) at.
            values (Iterable[HT] | HT): The value(s) to set.

        Raises:
            RuntimeError: If `on_duplicate` is 'ignore' and setting slices.
            ValueError: If the value(s) are duplicates and `on_duplicate` is
                set to 'raise'.
        """
        if isinstance(indices, slice):
            self._set_slice(
                indices, typing.cast(collections.abc.Iterable[HT], values)
            )
        else:
            self._set_index(indices, typing.cast(HT, values))

    def _set_slice(
        self, indices: slice, values: collections.abc.Iterable[HT]
    ) -> None:
        """
        Replaces a slice of the list and keeps the membership in sync.

        The new values can reuse the items they replace. They cannot repeat
        each other or an item that stays in the list.

        Args:
            indices (slice): The slice to replace.
            values (Iterable[HT]): The values to store.

        Raises:
            RuntimeError: If `on_duplicate` is 'ignore'.
            ValueError: If storing the values would create a duplicate.
        """
        if self.on_duplicate == 'ignore':
            raise RuntimeError(
                'ignore mode while setting slices introduces ambiguous '
                'behaviour and is therefore not supported'
            )

        new_values: list[HT] = list(values)
        old_values: list[HT] = self[indices]
        duplicates: set[HT] = self._find_duplicates(
            new_values, replaced=set(old_values)
        )
        if duplicates:
            raise ValueError(f'Duplicate values: {duplicates}')

        # The membership first, for the same reason as in `insert`.
        fresh: set[HT] = set(new_values).difference(self._set)
        self._set.update(fresh)
        try:
            super().__setitem__(indices, new_values)
        except BaseException:
            self._set.difference_update(fresh)
            raise

        self._set.difference_update(old_values)
        self._set.update(new_values)

    def _set_index(self, index: typing.SupportsIndex, value: HT) -> None:
        """
        Replaces a single item and keeps the membership in sync.

        Args:
            index (typing.SupportsIndex): The index to replace.
            value (HT): The value to store.

        Raises:
            ValueError: If the value is a duplicate of another item and
                `on_duplicate` is set to 'raise'.
        """
        old_value: HT = self[index]
        known: bool = value in self._set
        if known and value != old_value:
            if self.on_duplicate == 'raise':
                raise ValueError(f'Duplicate value: {value}')
            else:
                return

        # The membership first, for the same reason as in `insert`.
        self._set.add(value)
        try:
            super().__setitem__(index, value)
        except BaseException:
            if not known:
                self._set.discard(value)

            raise

        self._release(old_value)
        # The release dropped the member when both values are equal.
        self._set.add(value)

    def __delitem__(self, index: typing.SupportsIndex | slice) -> None:
        """
        Deletes the item(s) at the specified index/indices.

        Args:
            index (typing.SupportsIndex | slice): The index or slice
                to delete the item(s) at.
        """
        removed: list[HT]
        if isinstance(index, slice):
            removed = self[index]
        else:
            removed = [self[index]]

        # The list first, then the membership, like every other mutator.
        super().__delitem__(index)
        for value in removed:
            self._release(value)


# Type hinting `collections.deque` does not work consistently between Python
# runtime, mypy and pyright currently so we have to ignore the errors
class SliceableDeque(typing.Generic[T], collections.deque[T]):
    """
    A deque that supports slicing and enhanced equality checks.

    Methods::

        __getitem__(index: typing.SupportsIndex | slice) ->
            T | 'SliceableDeque[T]':
            Returns the item or slice at the given index.
        __eq__(other: typing.Any) -> bool:
            Checks equality with another object, allowing for comparison with
             lists, tuples, and sets.
        pop(index: int = -1) -> T:
            Removes and returns the item at the given index. Only supports
            index 0 and the last index.
    """

    @typing.overload
    def __getitem__(self, index: typing.SupportsIndex) -> T:
        """Overload: an integer index returns a single item."""

    @typing.overload
    def __getitem__(self, index: slice) -> 'SliceableDeque[T]':
        """Overload: a slice returns a new ``SliceableDeque``."""

    def __getitem__(
        self, index: typing.SupportsIndex | slice
    ) -> T | 'SliceableDeque[T]':
        """
        Return the item or slice at the given index.

        Args:
            index (typing.SupportsIndex | slice): The index or
             slice to retrieve.

        Returns:
            T | 'SliceableDeque[T]': The item or slice at the
            given index.

        Examples:
            >>> d = SliceableDeque[int]([1, 2, 3, 4, 5])
            >>> d[1:4]
            SliceableDeque([2, 3, 4])

            >>> d = SliceableDeque[str](['a', 'b', 'c'])
            >>> d[-2:]
            SliceableDeque(['b', 'c'])
        """
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return self.__class__(self[i] for i in range(start, stop, step))
        else:
            return super().__getitem__(index)

    def __eq__(self, other: typing.Any) -> bool:
        """
        Checks equality with another object, allowing for comparison with
        lists, tuples, and sets.

        Args:
            other (typing.Any): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(other, list):
            return list(self) == other
        elif isinstance(other, tuple):
            return tuple(self) == other
        elif isinstance(other, set):
            try:
                return set(self) == other
            except TypeError:
                # An unhashable item cannot be in a set.
                return False
        else:
            return super().__eq__(other)

    def __ne__(self, other: typing.Any) -> bool:
        """
        Checks inequality as the opposite of `__eq__`.

        `collections.deque` has its own `__ne__`, which does not know about
        the lists, tuples and sets that `__eq__` accepts.

        Args:
            other (typing.Any): The object to compare with.

        Returns:
            bool: False if the objects are equal, True otherwise.
        """
        equal: typing.Any = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented

        return not equal

    def pop(self, index: int = -1) -> T:
        """
        Removes and returns the item at the given index. Only supports index 0
        and the last index.

        Args:
            index (int, optional): The index of the item to remove. Defaults to
            -1.

        Returns:
            T: The removed item.

        Raises:
            IndexError: If the index is not 0 or the last index.

        Examples:
            >>> d = SliceableDeque([1, 2, 3])
            >>> d.pop(0)
            1
            >>> d.pop()
            3
        """
        if index == 0:
            return super().popleft()
        elif index in {-1, len(self) - 1}:
            return super().pop()
        else:
            raise IndexError(
                'Only index 0 and the last index (`N-1` or `-1`) are supported'
            )


if __name__ == '__main__':
    import doctest

    doctest.testmod()
