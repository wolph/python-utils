'''
Asyncio equivalents to regular Python functions.

'''
import asyncio
import itertools

from . import types


async def acount(
    start: float = 0,
    step: float = 1,
    delay: float = 0,
    stop: types.Optional[float] = None,
) -> types.AsyncIterator[float]:
    '''Asyncio version of itertools.count()'''
    for item in itertools.count(start, step):  # pragma: no branch
        if stop is not None and item >= stop:
            break

        yield item
        await asyncio.sleep(delay)
