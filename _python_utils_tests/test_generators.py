import pytest

import python_utils


@pytest.mark.asyncio
async def test_abatcher():
    async for batch in python_utils.abatcher(python_utils.acount(stop=9), 3):
        assert len(batch) == 3

    async for batch in python_utils.abatcher(python_utils.acount(stop=2), 3):
        assert len(batch) == 2


@pytest.mark.asyncio
async def test_abatcher_timed():
    batches = []
    async for batch in python_utils.abatcher(
        python_utils.acount(stop=10, delay=0.08),
        interval=0.2
    ):
        batches.append(batch)

    assert len(batches) == 3
    assert sum(len(batch) for batch in batches) == 10


def test_batcher():
    batch = []
    for batch in python_utils.batcher(range(9), 3):
        assert len(batch) == 3

    for batch in python_utils.batcher(range(4), 3):
        pass

    assert len(batch) == 1
