'''
Asyncio equivalents to regular Python functions.

'''
import asyncio
import itertools

from . import types

_N = types.TypeVar('_N', int, float)
_T = types.TypeVar('_T')


async def acount(
    start: _N = 0,
    step: _N = 1,
    delay: float = 0,
    stop: types.Optional[_N] = None,
) -> types.AsyncIterator[_N]:
    '''Asyncio version of itertools.count()'''
    for item in itertools.count(start, step):  # pragma: no branch
        if stop is not None and item >= stop:
            break

        yield item
        await asyncio.sleep(delay)


async def acontainer(
    iterable: types.Union[
        types.AsyncIterable[_T],
        types.Callable[..., types.AsyncIterable[_T]],
    ],
    container: types.Callable[[types.Iterable[_T]], types.Iterable[_T]] = list,
) -> types.Iterable[_T]:
    '''
    Asyncio version of list()/set()/tuple()/etc() using an async for loop

    So instead of doing `[item async for item in iterable]` you can do
    `await acontainer(iterable)`.

    '''
    iterable_: types.AsyncIterable[_T]
    if callable(iterable):
        iterable_ = iterable()
    else:
        iterable_ = iterable

    item: _T
    items: types.List[_T] = []
    async for item in iterable_:  # pragma: no branch
        items.append(item)

    return container(items)
