"""Tests for the timeout generators in ``python_utils.time``."""

import asyncio
import datetime
import itertools

import pytest

import python_utils
from python_utils import types


@pytest.mark.parametrize(
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result',
    [
        (0.2, 0.1, 0.4, 0.2, python_utils.acount, 2),
        (0.3, 0.1, 0.4, 0.2, python_utils.acount(), 3),
        (0.3, 0.06, 1.0, None, python_utils.acount, 5),
        (
            datetime.timedelta(seconds=0.1),
            datetime.timedelta(seconds=0.06),
            2.0,
            datetime.timedelta(seconds=0.1),
            python_utils.acount,
            2,
        ),
    ],
)
@pytest.mark.asyncio
async def test_aio_timeout_generator(
    timeout: float,
    interval: float,
    interval_multiplier: float,
    maximum_interval: float,
    iterable: types.AsyncIterable[types.Any],
    result: int,
) -> None:
    """Stop the async generator near the configured timeout."""
    i = None
    async for i in python_utils.aio_timeout_generator(
        timeout, interval, iterable, maximum_interval=maximum_interval
    ):
        pass

    assert i == result


@pytest.mark.parametrize(
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result',
    [
        (0.1, 0.06, 0.5, 0.1, 'abc', 'c'),
        (0.1, 0.07, 0.5, 0.1, itertools.count, 2),
        (0.1, 0.07, 0.5, 0.1, itertools.count(), 2),
        (0.1, 0.06, 1.0, None, 'abc', 'c'),
        (
            datetime.timedelta(seconds=0.1),
            datetime.timedelta(seconds=0.06),
            2.0,
            datetime.timedelta(seconds=0.1),
            itertools.count,
            2,
        ),
    ],
)
def test_timeout_generator(
    timeout: float,
    interval: float,
    interval_multiplier: float,
    maximum_interval: float,
    iterable: types.Union[
        str,
        types.Iterable[types.Any],
        types.Callable[..., types.Iterable[types.Any]],
    ],
    result: int,
) -> None:
    """Stop the sync generator near the configured timeout."""
    i = None
    for i in python_utils.timeout_generator(
        timeout=timeout,
        interval=interval,
        interval_multiplier=interval_multiplier,
        iterable=iterable,
        maximum_interval=maximum_interval,
    ):
        assert i is not None

    assert i == result


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector() -> None:
    """Raise or exit on per-item and total timeouts."""
    # Make pyright happy
    i = None

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield 0-9 with increasing sleeps between items."""
        for i in range(10):
            await asyncio.sleep(i / 20.0)
            yield i

    detector = python_utils.aio_generator_timeout_detector
    # Test regular timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(generator(), 0.25):
            pass

    # Test regular timeout with clean exit
    async for i in detector(generator(), 0.25, on_timeout=None):
        pass

    assert i == 4

    # Test total timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(generator(), total_timeout=0.5):
            pass

    # Test total timeout with clean exit
    async for i in detector(generator(), total_timeout=0.5, on_timeout=None):
        pass

    assert i == 4

    # Test stop iteration
    async for i in detector(generator(), on_timeout=None):
        pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_reraise() -> None:
    """Reraise ``TimeoutError`` on a per-item timeout."""

    # Test regular timeout with reraise
    @python_utils.aio_generator_timeout_detector_decorator(timeout=0.05)
    async def generator_timeout() -> types.AsyncGenerator[int, None]:
        """Yield with increasing delays to trip the timeout."""
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    with pytest.raises(asyncio.TimeoutError):
        async for _ in generator_timeout():
            pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_clean_exit() -> None:
    """Exit cleanly when ``on_timeout`` is ``None``."""
    # Make pyright happy
    i = None

    # Test regular timeout with clean exit
    @python_utils.aio_generator_timeout_detector_decorator(
        timeout=0.05, on_timeout=None
    )
    async def generator_clean() -> types.AsyncGenerator[int, None]:
        """Yield with increasing delays to trip the timeout."""
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    async for i in generator_clean():
        pass

    assert i == 4


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_reraise_total() -> (
    None
):
    """Reraise ``TimeoutError`` on a total timeout."""

    # Test total timeout with reraise
    @python_utils.aio_generator_timeout_detector_decorator(total_timeout=0.1)
    async def generator_reraise() -> types.AsyncGenerator[int, None]:
        """Yield with increasing delays to trip the timeout."""
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    with pytest.raises(asyncio.TimeoutError):
        async for _ in generator_reraise():
            pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_clean_total() -> None:
    """Exit cleanly on total timeout when ``on_timeout`` is ``None``."""
    # Make pyright happy
    i = None

    # Test total timeout with clean exit
    @python_utils.aio_generator_timeout_detector_decorator(
        total_timeout=0.1, on_timeout=None
    )
    async def generator_clean_total() -> types.AsyncGenerator[int, None]:
        """Yield with increasing delays to trip the timeout."""
        for i in range(10):
            await asyncio.sleep(i / 100.0)
            yield i

    async for i in generator_clean_total():
        pass

    assert i == 4
