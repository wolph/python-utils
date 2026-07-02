"""Asyncio equivalents of common synchronous helpers.

These bring ``itertools``-style ergonomics to ``async for``: ``acount`` is an
async counter, while ``acontainer`` and ``adict`` collect an async iterable
into a concrete container.
"""

import asyncio
import collections.abc
import itertools
import typing

#: Numeric type (``int`` or ``float``) produced by ``acount``.
_N = typing.TypeVar('_N', int, float)
#: Element type of the async iterables being consumed.
_T = typing.TypeVar('_T')
#: Key type when collecting an async iterable of pairs into a dict.
_K = typing.TypeVar('_K')
#: Value type when collecting an async iterable of pairs into a dict.
_V = typing.TypeVar('_V')


async def acount(
    start: _N = 0,
    step: _N = 1,
    delay: float = 0,
    stop: _N | None = None,
) -> collections.abc.AsyncIterator[_N]:
    """Async equivalent of ``itertools.count()``.

    Counts from ``start`` in steps of ``step``, sleeping ``delay`` seconds
    between values, and stops once ``stop`` (when given) is reached.

    Args:
        start: First value to yield.
        step: Amount added between successive values.
        delay: Seconds to ``asyncio.sleep`` between yields.
        stop: Exclusive upper bound; ``None`` counts forever.

    Yields:
        The successive counter values.

    >>> async def demo():
    ...     return [i async for i in acount(stop=3)]
    >>> asyncio.run(demo())
    [0, 1, 2]
    """
    for item in itertools.count(start, step):  # pragma: no branch
        if stop is not None and item >= stop:
            break

        yield item
        await asyncio.sleep(delay)


@typing.overload
async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: type[tuple[_T, ...]],
) -> tuple[_T, ...]:
    """Overload: collect the async iterable into a ``tuple``."""


@typing.overload
async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: type[list[_T]] = list,
) -> list[_T]:
    """Overload: collect the async iterable into a ``list`` (the default)."""


@typing.overload
async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: type[set[_T]],
) -> set[_T]:
    """Overload: collect the async iterable into a ``set``."""


async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: collections.abc.Callable[
        [collections.abc.Iterable[_T]], collections.abc.Collection[_T]
    ] = list,
) -> collections.abc.Collection[_T]:
    """
    Asyncio version of list()/set()/tuple()/etc() using an async for loop.

    So instead of doing `[item async for item in iterable]` you can do
    `await acontainer(iterable)`.

    """
    iterable_: collections.abc.AsyncIterable[_T]
    if callable(iterable):
        iterable_ = iterable()
    else:
        iterable_ = iterable

    items: list[_T] = [item async for item in iterable_]

    return container(items)


async def adict(
    iterable: collections.abc.AsyncIterable[tuple[_K, _V]]
    | collections.abc.Callable[
        ..., collections.abc.AsyncIterable[tuple[_K, _V]]
    ],
    container: collections.abc.Callable[
        [collections.abc.Iterable[tuple[_K, _V]]],
        collections.abc.Mapping[_K, _V],
    ] = dict,
) -> collections.abc.Mapping[_K, _V]:
    """
    Asyncio version of dict() using an async for loop.

    So instead of doing `{key: value async for key, value in iterable}` you
    can do `await adict(iterable)`.

    """
    iterable_: collections.abc.AsyncIterable[tuple[_K, _V]]
    if callable(iterable):
        iterable_ = iterable()
    else:
        iterable_ = iterable

    items: list[tuple[_K, _V]] = [item async for item in iterable_]

    return container(items)
