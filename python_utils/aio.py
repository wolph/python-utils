'''
Asyncio equivalents to regular Python functions.

'''
import asyncio
import itertools

from . import types

_N = types.TypeVar('_N', int, float)


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

        yield types.cast(_N, item)
        await asyncio.sleep(delay)
