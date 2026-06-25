"""Asyncio equivalents to regular Python functions."""

import asyncio
import collections.abc
import itertools
import typing

_N = typing.TypeVar('_N', int, float)
_T = typing.TypeVar('_T')
_K = typing.TypeVar('_K')
_V = typing.TypeVar('_V')


async def acount(
    start: _N = 0,
    step: _N = 1,
    delay: float = 0,
    stop: _N | None = None,
) -> collections.abc.AsyncIterator[_N]:
    """Asyncio version of itertools.count()."""
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
) -> tuple[_T, ...]: ...


@typing.overload
async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: type[list[_T]] = list,
) -> list[_T]: ...


@typing.overload
async def acontainer(
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]],
    container: type[set[_T]],
) -> set[_T]: ...


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

    item: _T
    items: list[_T] = []
    async for item in iterable_:  # pragma: no branch
        items.append(item)  # noqa: PERF401

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

    item: tuple[_K, _V]
    items: list[tuple[_K, _V]] = []
    async for item in iterable_:  # pragma: no branch
        items.append(item)  # noqa: PERF401

    return container(items)
