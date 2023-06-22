import asyncio
import time

import python_utils
from python_utils import types


_T = types.TypeVar('_T')


async def abatcher(
    generator: types.Union[
        types.AsyncGenerator[_T, None],
        types.AsyncIterator[_T],
    ],
    batch_size: types.Optional[int] = None,
    interval: types.Optional[types.delta_type] = None,
) -> types.AsyncGenerator[types.List[_T], None]:
    '''
    Asyncio generator wrapper that returns items with a given batch size or
    interval (whichever is reached first).
    '''
    batch: types.List[_T] = []

    assert batch_size or interval, 'Must specify either batch_size or interval'

    # If interval is specified, use it to determine when to yield the batch
    # Alternatively set a really long timeout to keep the code simpler
    if interval:
        interval_s = python_utils.delta_to_seconds(interval)
    else:
        # Set the timeout to 10 years
        interval_s = 60 * 60 * 24 * 365 * 10.0

    next_yield: float = time.perf_counter() + interval_s

    done: types.Set[asyncio.Task[_T]]
    pending: types.Set[asyncio.Task[_T]] = set()

    while True:
        try:
            done, pending = await asyncio.wait(
                pending
                or [
                    asyncio.create_task(
                        types.cast(
                            types.Coroutine[None, None, _T],
                            generator.__anext__(),
                        )
                    ),
                ],
                timeout=interval_s,
                return_when=asyncio.FIRST_COMPLETED,
            )

            if done:
                for result in done:
                    batch.append(result.result())

        except StopAsyncIteration:
            if batch:
                yield batch

            break

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


def batcher(
    iterable: types.Iterable[_T],
    batch_size: int = 10,
) -> types.Generator[types.List[_T], None, None]:
    '''
    Generator wrapper that returns items with a given batch size
    '''
    batch: types.List[_T] = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
