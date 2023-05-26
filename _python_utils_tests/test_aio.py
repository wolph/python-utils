from datetime import datetime
import pytest
import asyncio

from python_utils import types
from python_utils.aio import acount


@pytest.mark.asyncio
async def test_acount(monkeypatch: pytest.MonkeyPatch):
    sleeps: types.List[float] = []

    async def mock_sleep(delay: float):
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, 'sleep', mock_sleep)

    async for i in acount(delay=1, stop=3.5):
        print('i', i, datetime.now())

    assert len(sleeps) == 4
    assert sum(sleeps) == 4
