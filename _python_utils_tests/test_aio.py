import asyncio

import pytest

from python_utils import types
from python_utils.aio import acontainer, acount, adict


@pytest.mark.asyncio
async def test_acount(monkeypatch: pytest.MonkeyPatch):
    sleeps: types.List[float] = []

    async def mock_sleep(delay: float):
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, 'sleep', mock_sleep)

    async for _i in acount(delay=1, stop=3.5):
        pass

    assert len(sleeps) == 4
    assert sum(sleeps) == 4


@pytest.mark.asyncio
async def test_acontainer():
    async def async_gen():
        yield 1
        yield 2
        yield 3

    async def empty_gen():
        if False:
            yield 1

    assert await acontainer(async_gen) == [1, 2, 3]
    assert await acontainer(async_gen()) == [1, 2, 3]
    assert await acontainer(async_gen, set) == {1, 2, 3}
    assert await acontainer(async_gen(), set) == {1, 2, 3}
    assert await acontainer(async_gen, list) == [1, 2, 3]
    assert await acontainer(async_gen(), list) == [1, 2, 3]
    assert await acontainer(async_gen, tuple) == (1, 2, 3)
    assert await acontainer(async_gen(), tuple) == (1, 2, 3)
    assert await acontainer(empty_gen) == []
    assert await acontainer(empty_gen()) == []
    assert await acontainer(empty_gen, set) == set()
    assert await acontainer(empty_gen(), set) == set()
    assert await acontainer(empty_gen, list) == list()
    assert await acontainer(empty_gen(), list) == list()
    assert await acontainer(empty_gen, tuple) == tuple()
    assert await acontainer(empty_gen(), tuple) == tuple()


@pytest.mark.asyncio
async def test_adict():
    async def async_gen():
        yield 1, 2
        yield 3, 4
        yield 5, 6

    async def empty_gen():
        if False:
            yield 1, 2

    assert await adict(async_gen) == {1: 2, 3: 4, 5: 6}
    assert await adict(async_gen()) == {1: 2, 3: 4, 5: 6}
    assert await adict(empty_gen) == {}
    assert await adict(empty_gen()) == {}
