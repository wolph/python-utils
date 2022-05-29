import asyncio
import time

import python_utils
from python_utils import types


async def abatcher(
    generator: types.AsyncGenerator,
    batch_size: types.Optional[int] = None,
    interval: types.Optional[types.delta_type] = None,
):
    '''
    Asyncio generator wrapper that returns items with a given batch size or
    interval (whichever is reached first).
    '''
    batch: list = []

    assert batch_size or interval, 'Must specify either batch_size or interval'

    if interval:
        interval_s = python_utils.delta_to_seconds(interval)
        next_yield = time.perf_counter() + interval_s
    else:
        interval_s = 0
        next_yield = 0

    while True:
        try:
            if interval_s:
                item = await asyncio.wait_for(
                    generator.__anext__(), interval_s
                )
            else:
                item = await generator.__anext__()
        except (StopAsyncIteration, asyncio.TimeoutError):
            if batch:
                yield batch
            break
        else:
            batch.append(item)

        if batch_size is not None and len(batch) == batch_size:
            yield batch
            batch = []

        if interval and batch and time.perf_counter() > next_yield:
            yield batch
            batch = []
            # Always set the next yield time to the current time. If the
            # loop is running slow due to blocking functions we do not
            # want to burst too much
            next_yield = time.perf_counter() + interval_s


def batcher(iterable, batch_size):
    '''
    Generator wrapper that returns items with a given batch size
    '''
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
