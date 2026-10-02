"""Tests for the batching helpers in ``python_utils.generators``."""

import asyncio
import gc
import sys
from types import SimpleNamespace

import pytest

import python_utils
from python_utils import types


@pytest.mark.asyncio
async def test_abatcher() -> None:
    """Group an async count into fixed-size batches."""
    async for batch in python_utils.abatcher(python_utils.acount(stop=9), 3):
        assert len(batch) == 3

    async for batch in python_utils.abatcher(python_utils.acount(stop=2), 3):
        assert len(batch) == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'arrival_times',
    [
        (0, 8, 16, 24, 32, 40, 48, 56, 64, 72),
        (0, 10, 11, 21, 22, 32, 33, 43, 44, 54),
    ],
)
async def test_abatcher_timed(
    monkeypatch: pytest.MonkeyPatch, arrival_times: tuple[int, ...]
) -> None:
    """Group async items into batches by time interval."""
    now: float = 0.0
    monkeypatch.setattr(
        python_utils.generators,
        'time',
        SimpleNamespace(perf_counter=lambda: now),
    )

    async def generator() -> types.AsyncIterator[int]:
        nonlocal now
        item: int
        arrival: int
        for item, arrival in enumerate(arrival_times):
            now = float(arrival)
            yield item

    batches: types.List[types.List[int]] = []
    async for batch in python_utils.abatcher(generator(), interval=10):
        batches.append(batch)

    assert batches == [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9]]
    assert len(batches) == 5


@pytest.mark.asyncio
async def test_abatcher_timed_with_timeout() -> None:
    """Respect timeouts and propagate errors while batching."""

    async def generator() -> types.AsyncIterator[int]:
        """Yield items with sleeps to exercise batch timeouts."""
        # Test if the timeout is respected
        yield 0
        yield 1
        await asyncio.sleep(0.11)

        # Test if the timeout is respected
        yield 2
        yield 3
        await asyncio.sleep(0.11)

        # Test if exceptions are handled correctly
        await asyncio.wait_for(asyncio.sleep(1), timeout=0.05)

        # Test if StopAsyncIteration is handled correctly
        yield 4

    batcher = python_utils.abatcher(generator(), interval=0.1)
    assert await batcher.__anext__() == [0, 1]
    assert await batcher.__anext__() == [2, 3]

    with pytest.raises(asyncio.TimeoutError):
        await batcher.__anext__()

    with pytest.raises(StopAsyncIteration):
        await batcher.__anext__()


async def blocked_generator(
    started: asyncio.Event, closed: types.List[str]
) -> types.AsyncIterator[int]:
    """Yield one item and then wait for an event that never comes."""
    try:
        yield 0
        started.set()
        await asyncio.Event().wait()
    finally:
        closed.append('closed')


@pytest.mark.asyncio
async def test_abatcher_cancels_pending_item_on_close() -> None:
    """Cancel the pending source item when the consumer stops early."""
    closed: types.List[str] = []
    before: types.Set[asyncio.Task[types.Any]] = asyncio.all_tasks()

    # The source never yields a second item, so the interval always ends
    # while that item is still pending. Sleep accuracy does not matter.
    batcher: types.AsyncGenerator[types.List[int], None] = (
        python_utils.abatcher(
            blocked_generator(asyncio.Event(), closed), interval=0.01
        )
    )
    first: types.List[int] = await batcher.__anext__()
    await batcher.aclose()

    assert first == [0]
    assert asyncio.all_tasks() == before
    assert closed == ['closed']


@pytest.mark.asyncio
async def test_abatcher_cancels_pending_item_on_cancellation() -> None:
    """Cancel the pending source item when the consumer is cancelled."""
    started: asyncio.Event = asyncio.Event()
    closed: types.List[str] = []
    before: types.Set[asyncio.Task[types.Any]] = asyncio.all_tasks()

    batcher: types.AsyncGenerator[types.List[int], None] = (
        python_utils.abatcher(blocked_generator(started, closed), batch_size=2)
    )
    consumer: asyncio.Task[types.List[int]] = asyncio.create_task(
        batcher.__anext__()
    )
    await started.wait()
    consumer.cancel()
    with pytest.raises(asyncio.CancelledError):
        await consumer

    assert asyncio.all_tasks() == before
    assert closed == ['closed']


@pytest.mark.asyncio
async def test_abatcher_reports_source_error_during_cancellation() -> None:
    """Report an error that the source raises while it is cancelled."""
    reported: types.List[types.Dict[str, types.Any]] = []
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    loop.set_exception_handler(lambda _, context: reported.append(context))

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield one item, then fail while the next one is cancelled."""
        yield 0
        try:
            await asyncio.Event().wait()
        finally:
            raise RuntimeError('closing failed')

    batcher: types.AsyncGenerator[types.List[int], None] = (
        python_utils.abatcher(generator(), interval=0.01)
    )
    try:
        first: types.List[int] = await batcher.__anext__()
        await batcher.aclose()
    finally:
        loop.set_exception_handler(None)

    assert first == [0]
    assert [str(context['exception']) for context in reported] == [
        'closing failed'
    ]


@pytest.mark.asyncio
async def test_abatcher_accepts_source_that_ends_on_cancellation() -> None:
    """Report nothing for a source that just stops when it is cancelled."""
    reported: types.List[types.Dict[str, types.Any]] = []
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    loop.set_exception_handler(lambda _, context: reported.append(context))

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield one item, then end as soon as the wait is cancelled."""
        yield 0
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            return

    batcher: types.AsyncGenerator[types.List[int], None] = (
        python_utils.abatcher(generator(), interval=0.01)
    )
    try:
        first: types.List[int] = await batcher.__anext__()
        await batcher.aclose()
    finally:
        loop.set_exception_handler(None)

    assert first == [0]
    assert reported == []


def test_abatcher_collected_after_its_loop_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Clean up without an event loop when nothing is on its way."""
    unraisable: types.List[types.Any] = []
    monkeypatch.setattr(sys, 'unraisablehook', unraisable.append)

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield four items without waiting."""
        i: int
        for i in range(4):
            yield i

    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    batcher: types.AsyncGenerator[types.List[int], None] = (
        python_utils.abatcher(generator(), batch_size=2)
    )
    try:
        first: types.List[int] = loop.run_until_complete(batcher.__anext__())
    finally:
        loop.close()

    del batcher
    gc.collect()

    assert first == [0, 1]
    assert unraisable == []


@pytest.mark.asyncio
async def test_abatcher_size_flush_restarts_interval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Restart the interval after a batch that was flushed by its size."""
    now: float = 0.0
    monkeypatch.setattr(
        python_utils.generators,
        'time',
        SimpleNamespace(perf_counter=lambda: now),
    )

    async def generator() -> types.AsyncIterator[int]:
        """Let one item arrive every 4 seconds on the fake clock."""
        nonlocal now
        item: int
        for item in range(12):
            now = 4.0 * (item + 1)
            yield item

    batches: types.List[types.List[int]] = [
        batch
        async for batch in python_utils.abatcher(
            generator(), batch_size=3, interval=10
        )
    ]

    # Three items take 12 seconds, which is past the interval of 10. The size
    # flush takes them and the next item has to start a fresh interval. It
    # may not leave on its own because the old interval ran out.
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]


class FutureIterator:
    """An async iterator that hands out futures instead of coroutines."""

    def __init__(self, stop: int) -> None:
        """Count from zero up to ``stop``, which is excluded."""
        self.current: int = 0
        self.stop: int = stop

    def __aiter__(self) -> 'FutureIterator':
        """Return the iterator itself."""
        return self

    def __anext__(self) -> 'asyncio.Future[int]':
        """Return a finished future with the next number."""
        future: asyncio.Future[int] = (
            asyncio.get_running_loop().create_future()
        )
        if self.current < self.stop:
            future.set_result(self.current)
            self.current += 1
        else:
            future.set_exception(StopAsyncIteration())

        return future


@pytest.mark.asyncio
async def test_abatcher_with_future_returning_iterator() -> None:
    """Batch an iterator whose ``__anext__`` is not a coroutine."""
    batches: types.List[types.List[int]] = [
        batch async for batch in python_utils.abatcher(FutureIterator(5), 2)
    ]

    assert batches == [[0, 1], [2, 3], [4]]


def test_batcher() -> None:
    """Split an iterable into fixed-size batches."""
    batch = []
    for batch in python_utils.batcher(range(9), 3):
        assert len(batch) == 3

    for batch in python_utils.batcher(range(4), 3):
        assert batch is not None

    assert len(batch) == 1
