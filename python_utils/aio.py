import asyncio
import itertools


async def acount(start=0, step=1, delay=0):
    '''Asyncio version of itertools.count()'''
    for item in itertools.count(start, step):  # pragma: no branch
        yield item
        await asyncio.sleep(delay)
