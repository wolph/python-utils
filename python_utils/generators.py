"""
This module provides generator utilities for batching items from
iterables and async iterables.

Functions:
    abatcher(generator, batch_size=None, interval=None):
        Asyncio generator wrapper that returns items with a given batch
        size or interval (whichever is reached first).

    batcher(iterable, batch_size=10):
        Generator wrapper that returns items with a given batch size.
"""

import asyncio
import collections.abc
import time
import typing

import python_utils
from python_utils import _aliases

#: Element type of the iterables being batched.
_T = typing.TypeVar('_T')


async def _cancel(pending: set[asyncio.Future[_T]]) -> None:
    """Cancel the items that are still on their way and wait for them.

    Args:
        pending: The unfinished futures to cancel. An empty set is fine.
    """
    if not pending:
        # Nothing is on its way. This also covers a batcher that is closed
        # by the garbage collector after its event loop is gone.
        return

    for future in pending:
        future.cancel()

    # Waiting lets the cancellation reach the generator. A cancelled item is
    # of no use to anyone. An error that the generator raises while it is
    # being cancelled is reported to the event loop, because raising it here
    # would replace the cancellation of the consumer.
    outcomes: list[_T | BaseException] = await asyncio.gather(
        *pending, return_exceptions=True
    )
    for outcome in outcomes:
        # A generator that returns when it is cancelled ends its item with
        # `StopAsyncIteration`, which is no failure.
        if isinstance(outcome, Exception) and not isinstance(
            outcome, StopAsyncIteration
        ):
            asyncio.get_running_loop().call_exception_handler(
                {
                    'message': 'abatcher source failed while being cancelled',
                    'exception': outcome,
                }
            )


async def abatcher(
    generator: collections.abc.AsyncGenerator[_T, None]
    | collections.abc.AsyncIterator[_T],
    batch_size: int | None = None,
    interval: _aliases.delta_type | None = None,
) -> collections.abc.AsyncGenerator[list[_T], None]:
    """
    Asyncio generator wrapper that returns items with a given batch size or
    interval (whichever is reached first).

    Stopping early while the next item is still on its way cancels the
    request for it. A source that is an async generator ends at that point.
    A source with nothing on its way stays usable.

    Args:
        generator: The async generator or iterator to batch.
        batch_size (typing.Optional[int], optional): The number of items per
            batch. Defaults to None.
        interval (typing.Optional[_aliases.delta_type], optional): The time
            interval to wait before yielding a batch. Defaults to None.

    Yields:
        collections.abc.AsyncGenerator[list[_T], None]: A generator that yields
        batches of items.
    """
    batch: list[_T] = []

    assert batch_size or interval, 'Must specify either batch_size or interval'

    # If interval is specified, use it to determine when to yield the batch
    # Alternatively set a really long timeout to keep the code simpler
    if interval:
        interval_s = python_utils.delta_to_seconds(interval)
    else:
        # Set the timeout to 10 years
        interval_s = 60 * 60 * 24 * 365 * 10.0

    next_yield: float = time.perf_counter() + interval_s

    done: set[asyncio.Future[_T]]
    pending: set[asyncio.Future[_T]] = set()

    try:
        while True:
            try:
                if not pending:
                    # Store the task before waiting for it. A cancellation
                    # during the wait still finds it in the `finally` below.
                    # `ensure_future` takes every awaitable, where
                    # `create_task` insists on a coroutine.
                    pending = {asyncio.ensure_future(generator.__anext__())}

                done, pending = await asyncio.wait(
                    pending,
                    timeout=interval_s,
                    return_when=asyncio.FIRST_COMPLETED,
                )

                if done:
                    batch.extend(result.result() for result in done)

            except StopAsyncIteration:
                if batch:
                    yield batch

                break

            if batch_size is not None and len(batch) == batch_size:
                yield batch
                batch = []
                # A full batch starts a new interval as well. Otherwise the
                # next item is flushed on its own once the old one ran out.
                next_yield = time.perf_counter() + interval_s

            if interval and batch and time.perf_counter() > next_yield:
                yield batch
                batch = []
                # Always set the next yield time to the current time. If the
                # loop is running slow due to blocking functions we do not
                # want to burst too much
                next_yield = time.perf_counter() + interval_s
    finally:
        # The consumer can stop while the next item is still on its way: an
        # early `break`, `aclose()` or a cancellation. Without this the task
        # keeps running, takes the next item from the generator and nobody
        # ever receives it.
        await _cancel(pending)


def batcher(
    iterable: collections.abc.Iterable[_T],
    batch_size: int = 10,
) -> collections.abc.Generator[list[_T], None, None]:
    """
    Generator wrapper that returns items with a given batch size.

    Args:
        iterable (collections.abc.Iterable[_T]): The iterable to batch.
        batch_size (int, optional): The number of items per batch. Defaults
            to 10.

    Yields:
        collections.abc.Generator[list[_T], None, None]: A generator that
            yields batches of items.
    """
    batch: list[_T] = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch
