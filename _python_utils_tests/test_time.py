import asyncio
import itertools
from datetime import timedelta

import pytest

import python_utils


@pytest.mark.parametrize(
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result', [
        (0.2, 0.1, 0.4, 0.2, python_utils.acount, 2),
        (0.3, 0.1, 0.4, 0.2, python_utils.acount(), 3),
        (0.3, 0.06, 1.0, None, python_utils.acount, 5),
        (timedelta(seconds=0.1), timedelta(seconds=0.06),
         2.0, timedelta(seconds=0.1), python_utils.acount, 2),
    ])
@pytest.mark.asyncio
async def test_aio_timeout_generator(timeout, interval, interval_multiplier,
                                     maximum_interval, iterable, result):
    i = None
    async for i in python_utils.aio_timeout_generator(
        timeout, interval, iterable,
        maximum_interval=maximum_interval
    ):
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
    for i in python_utils.timeout_generator(
        timeout=timeout,
        interval=interval,
        interval_multiplier=interval_multiplier,
        iterable=iterable,
        maximum_interval=maximum_interval,
    ):
        pass

    assert i == result


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector():
    async def generator():
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    detector = python_utils.aio_generator_timeout_detector
    # Test regular timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(generator(), 0.05):
            pass

    # Test regular timeout with clean exit
    async for i in detector(generator(), 0.05, on_timeout=None):
        pass

    assert i == 4

    # Test total timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(generator(), total_timeout=0.1):
            pass

    # Test total timeout with clean exit
    async for i in detector(generator(), total_timeout=0.1, on_timeout=None):
        pass

    assert i == 4

    # Test stop iteration
    async for i in detector(generator(), on_timeout=None):
        pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator():
    # Test regular timeout with reraise
    @python_utils.aio_generator_timeout_detector_decorator(timeout=0.05)
    async def generator():
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    with pytest.raises(asyncio.TimeoutError):
        async for i in generator():
            pass

    # Test regular timeout with clean exit
    @python_utils.aio_generator_timeout_detector_decorator(
        timeout=0.05,
        on_timeout=None
    )
    async def generator():
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    async for i in generator():
        pass

    assert i == 4

    # Test total timeout with reraise
    @python_utils.aio_generator_timeout_detector_decorator(total_timeout=0.1)
    async def generator():
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    with pytest.raises(asyncio.TimeoutError):
        async for i in generator():
            pass

    # Test total timeout with clean exit
    @python_utils.aio_generator_timeout_detector_decorator(
        total_timeout=0.1,
        on_timeout=None
    )
    async def generator():
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    async for i in generator():
        pass

    assert i == 4
