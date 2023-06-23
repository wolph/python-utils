import asyncio

import pytest

import python_utils
from python_utils import types


@pytest.mark.asyncio
async def test_abatcher():
    async for batch in python_utils.abatcher(python_utils.acount(stop=9), 3):
        assert len(batch) == 3

    async for batch in python_utils.abatcher(python_utils.acount(stop=2), 3):
        assert len(batch) == 2


@pytest.mark.asyncio
async def test_abatcher_timed() -> None:
    batches: types.List[types.List[int]] = []
    async for batch in python_utils.abatcher(
        python_utils.acount(stop=10, delay=0.08), interval=0.1
    ):
        batches.append(batch)

    assert batches == [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9]]
    assert len(batches) == 5


@pytest.mark.asyncio
async def test_abatcher_timed_with_timeout():
    async def generator():
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


def test_batcher():
    batch = []
    for batch in python_utils.batcher(range(9), 3):
        assert len(batch) == 3

    for batch in python_utils.batcher(range(4), 3):
        pass

    assert len(batch) == 1
