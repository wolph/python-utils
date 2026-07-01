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
