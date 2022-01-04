import itertools
from datetime import timedelta

import pytest

from python_utils import aio
from python_utils import time


@pytest.mark.parametrize(
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result', [
        (0.01, 0.003, 0.5, 0.01, aio.acount, 3),
        (0.02, 0.003, 0.5, 0.01, aio.acount(), 6),
        (0.03, 0.003, 1.0, None, aio.acount, 9),
        (timedelta(seconds=0.01), timedelta(seconds=0.006),
         2.0, timedelta(seconds=0.01), aio.acount, 2),
    ])
@pytest.mark.asyncio
async def test_aio_timeout_generator(timeout, interval, interval_multiplier,
                                     maximum_interval, iterable, result):
    i = None
    async for i in time.aio_timeout_generator(
            timeout, interval, iterable,
            maximum_interval=maximum_interval):
        pass

    assert i == result


@pytest.mark.parametrize(
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result', [
        (0.01, 0.006, 0.5, 0.01, 'abc', 'c'),
        (0.01, 0.006, 0.5, 0.01, itertools.count, 2),
        (0.01, 0.006, 0.5, 0.01, itertools.count(), 2),
        (0.01, 0.006, 1.0, None, 'abc', 'c'),
        (timedelta(seconds=0.01),
         timedelta(seconds=0.006),
         2.0, timedelta(seconds=0.01),
         itertools.count, 2),
    ])
def test_timeout_generator(timeout, interval, interval_multiplier,
                           maximum_interval, iterable, result):
    i = None
    for i in time.timeout_generator(
            timeout=timeout,
            interval=interval,
            interval_multiplier=interval_multiplier,
            iterable=iterable,
            maximum_interval=maximum_interval,
    ):
        pass

    assert i == result
