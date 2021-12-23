import pytest
import datetime
import itertools
from python_utils import time


@pytest.mark.asyncio
async def test_aio_timeout_generator():
    async for i in time.aio_timeout_generator(0.1, 0.06):
        print(i)

    time.aio_timeout = datetime.timedelta(seconds=0.1)
    interval = datetime.timedelta(seconds=0.06)
    async for i in time.aio_timeout_generator(time.aio_timeout, interval,
                                          itertools.count()):
        print(i)

    async for i in time.aio_timeout_generator(1, interval=0.1, iterable='ab'):
        print(i)

    # Testing small interval:
    time.aio_timeout = datetime.timedelta(seconds=0.1)
    interval = datetime.timedelta(seconds=0.06)
    async for i in time.aio_timeout_generator(time.aio_timeout, interval,
                                          interval_multiplier=2):
        print(i)

    # Testing large interval:
    time.aio_timeout = datetime.timedelta(seconds=0.1)
    interval = datetime.timedelta(seconds=2)
    async for i in time.aio_timeout_generator(time.aio_timeout, interval,
                                          interval_multiplier=2):
        print(i)
