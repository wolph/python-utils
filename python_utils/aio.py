'''
Asyncio equivalents to regular Python functions.

'''
import asyncio
import itertools


async def acount(start=0, step=1, delay=0, stop=None):
    '''Asyncio version of itertools.count()'''
    for item in itertools.count(start, step):  # pragma: no branch
        if stop is not None and item >= stop:
            break

        yield item
        await asyncio.sleep(delay)
