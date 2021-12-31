import datetime
import itertools

import pytest

from python_utils import time


@pytest.mark.parametrize('timeout', [0.01, datetime.timedelta(seconds=0.01)])
@pytest.mark.parametrize('interval', [0.006, datetime.timedelta(seconds=0.006)])
@pytest.mark.parametrize('interval_multiplier', [0.5, 1.0, 2.0])
@pytest.mark.parametrize('maximum_interval', [0.01, datetime.timedelta(
    seconds=0.01), None])
@pytest.mark.parametrize('iterable', ['ab', itertools.count(), itertools.count])
@pytest.mark.asyncio
async def test_aio_timeout_generator(iterable, timeout, interval,
                                     interval_multiplier,
                                     maximum_interval):
    async for _ in time.aio_timeout_generator(
            timeout, interval, iterable,
            maximum_interval=maximum_interval):
        pass
