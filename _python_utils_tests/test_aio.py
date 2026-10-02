"""Tests for the async helpers in ``python_utils.aio``."""

import asyncio

import pytest

from python_utils import aio, types


@pytest.mark.asyncio
async def test_acount(monkeypatch: pytest.MonkeyPatch) -> None:
    """Count with a delay between yields until reaching ``stop``."""
    sleeps: types.List[float] = []

    async def mock_sleep(delay: float) -> None:
        """Record each requested delay instead of sleeping."""
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, 'sleep', mock_sleep)

    async for _i in aio.acount(delay=1, stop=3.5):
        pass

    assert len(sleeps) == 4
    assert sum(sleeps) == 4


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'start,step,stop,expected',
    [
        (10, -2, 0, [10, 8, 6, 4, 2]),
        (0, -1, -3, [0, -1, -2]),
        (1.5, -0.5, 0, [1.5, 1.0, 0.5]),
        # Nothing to count when `start` is already past `stop`, in either
        # direction. This is what `range` does as well.
        (0, -1, 5, []),
        (5, 1, 3, []),
        (0, 2, 5, [0, 2, 4]),
    ],
)
async def test_acount_stop_follows_step_direction(
    start: float, step: float, stop: float, expected: types.List[float]
) -> None:
    """Count down to a lower ``stop`` when the step is negative."""
    limit: int = len(expected) + 5
    items: types.List[float] = []
    item: float
    # `acount` is annotated as a plain iterator, closing takes a generator.
    counter: types.AsyncGenerator[float, None] = types.cast(
        types.AsyncGenerator[float, None],
        aio.acount(start=start, step=step, stop=stop),
    )
    async for item in counter:
        items.append(item)
        # A counter that misses its `stop` never ends by itself.
        if len(items) == limit:
            break

    await counter.aclose()

    assert items == expected


@pytest.mark.asyncio
async def test_acontainer() -> None:
    """Collect an async iterable into the requested container."""

    async def async_gen() -> types.AsyncIterable[int]:
        """Yield 1, 2, 3 asynchronously."""
        yield 1
        yield 2
        yield 3

    async def empty_gen() -> types.AsyncIterable[int]:
        """Yield nothing as an async generator."""
        if False:
            yield 1

    assert await aio.acontainer(async_gen) == [1, 2, 3]
    assert await aio.acontainer(async_gen()) == [1, 2, 3]
    assert await aio.acontainer(async_gen, set) == {1, 2, 3}
    assert await aio.acontainer(async_gen(), set) == {1, 2, 3}
    assert await aio.acontainer(async_gen, list) == [1, 2, 3]
    assert await aio.acontainer(async_gen(), list) == [1, 2, 3]
    assert await aio.acontainer(async_gen, tuple) == (1, 2, 3)
    assert await aio.acontainer(async_gen(), tuple) == (1, 2, 3)
    assert await aio.acontainer(empty_gen) == []
    assert await aio.acontainer(empty_gen()) == []
    assert await aio.acontainer(empty_gen, set) == set()
    assert await aio.acontainer(empty_gen(), set) == set()
    assert await aio.acontainer(empty_gen, list) == list()
    assert await aio.acontainer(empty_gen(), list) == list()
    assert await aio.acontainer(empty_gen, tuple) == tuple()
    assert await aio.acontainer(empty_gen(), tuple) == tuple()


@pytest.mark.asyncio
async def test_adict() -> None:
    """Build a dict from an async iterable of key/value pairs."""

    async def async_gen() -> types.AsyncIterable[types.Tuple[int, int]]:
        """Yield key/value pairs asynchronously."""
        yield 1, 2
        yield 3, 4
        yield 5, 6

    async def empty_gen() -> types.AsyncIterable[types.Tuple[int, int]]:
        """Yield no pairs as an async generator."""
        if False:
            yield 1, 2

    assert await aio.adict(async_gen) == {1: 2, 3: 4, 5: 6}
    assert await aio.adict(async_gen()) == {1: 2, 3: 4, 5: 6}
    assert await aio.adict(empty_gen) == {}
    assert await aio.adict(empty_gen()) == {}
