"""Tests for the timeout generators in ``python_utils.time``."""

import asyncio
import datetime
import itertools
import time

import pytest

import python_utils
from _python_utils_tests import clock
from python_utils import types

#: Far longer than every timeout in this module, so a generator that sleeps
#: this long is always interrupted first.
STALL: float = 10.0


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
    'timeout,interval,interval_multiplier,maximum_interval,iterable,result,'
    'sleeps',
    [
        (0.1, 0.06, 0.5, 0.1, 'abc', 'c', [0.06, 0.03, 0.015]),
        (0.1, 0.07, 0.5, 0.1, itertools.count, 2, [0.07, 0.035]),
        (0.1, 0.07, 0.5, 0.1, itertools.count(), 2, [0.07, 0.035]),
        (0.1, 0.06, 1.0, None, 'abc', 'c', [0.06, 0.06]),
        (
            datetime.timedelta(seconds=0.1),
            datetime.timedelta(seconds=0.06),
            2.0,
            datetime.timedelta(seconds=0.1),
            itertools.count,
            2,
            [0.06, 0.1],
        ),
    ],
)
def test_timeout_generator(
    fake_clock: clock.FakeClock,
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
    sleeps: types.List[float],
) -> None:
    """Stop the sync generator at the timeout and scale the interval."""
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
    assert fake_clock.sleeps == pytest.approx(sleeps)


def test_timeout_generator_real_clock() -> None:
    """Keep yielding on the real clock until the timeout has passed."""
    timeout: float = 0.05
    interval: float = 0.01
    start: float = time.perf_counter()
    items: types.List[int] = list(
        python_utils.timeout_generator(timeout, interval, itertools.count())
    )
    elapsed: float = time.perf_counter() - start

    # A sleep can take longer than requested but never shorter, so these
    # hold on any machine. The exact number of items does not.
    assert items == list(range(len(items)))
    assert len(items) <= timeout / interval + 2
    assert elapsed >= timeout


async def stalling_generator() -> types.AsyncGenerator[int, None]:
    """Yield 0-4 without waiting, then stall before the next item."""
    for i in range(10):
        if i == 5:
            await asyncio.sleep(STALL)
        yield i


def ticking_generator(
    fake_clock: clock.FakeClock,
) -> types.AsyncGenerator[int, None]:
    """Yield 0-9 and let 0.1 seconds pass on the fake clock for each item."""

    async def generator() -> types.AsyncGenerator[int, None]:
        """Advance the fake clock before every item."""
        for i in range(10):
            fake_clock.sleep(0.1)
            yield i

    return generator()


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector(
    fake_clock: clock.FakeClock,
) -> None:
    """Raise or exit on per-item and total timeouts."""
    # Make pyright happy
    i = None

    detector = python_utils.aio_generator_timeout_detector
    # Test regular timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(stalling_generator(), 0.05):
            pass

    # Test regular timeout with clean exit
    async for i in detector(stalling_generator(), 0.05, on_timeout=None):
        pass

    assert i == 4

    # Test total timeout with reraise
    with pytest.raises(asyncio.TimeoutError):
        async for i in detector(
            ticking_generator(fake_clock), total_timeout=0.45
        ):
            pass

    # Test total timeout with clean exit
    async for i in detector(
        ticking_generator(fake_clock), total_timeout=0.45, on_timeout=None
    ):
        pass

    assert i == 4

    # Test stop iteration
    async for i in detector(ticking_generator(fake_clock), on_timeout=None):
        pass

    assert i == 9


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_reraise() -> None:
    """Reraise ``TimeoutError`` on a per-item timeout."""
    # Test regular timeout with reraise
    generator_timeout = python_utils.aio_generator_timeout_detector_decorator(
        timeout=0.05
    )(stalling_generator)

    with pytest.raises(asyncio.TimeoutError):
        async for _ in generator_timeout():
            pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_clean_exit() -> None:
    """Exit cleanly when ``on_timeout`` is ``None``."""
    # Make pyright happy
    i = None

    # Test regular timeout with clean exit
    generator_clean = python_utils.aio_generator_timeout_detector_decorator(
        timeout=0.05, on_timeout=None
    )(stalling_generator)

    async for i in generator_clean():
        pass

    assert i == 4


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_reraise_total(
    fake_clock: clock.FakeClock,
) -> None:
    """Reraise ``TimeoutError`` on a total timeout."""

    # Test total timeout with reraise
    @python_utils.aio_generator_timeout_detector_decorator(total_timeout=0.45)
    async def generator_reraise() -> types.AsyncGenerator[int, None]:
        """Let the fake clock pass the total timeout while yielding."""
        async for i in ticking_generator(fake_clock):
            yield i

    with pytest.raises(asyncio.TimeoutError):
        async for _ in generator_reraise():
            pass


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_decorator_clean_total(
    fake_clock: clock.FakeClock,
) -> None:
    """Exit cleanly on total timeout when ``on_timeout`` is ``None``."""
    # Make pyright happy
    i = None

    # Test total timeout with clean exit
    @python_utils.aio_generator_timeout_detector_decorator(
        total_timeout=0.45, on_timeout=None
    )
    async def generator_clean_total() -> types.AsyncGenerator[int, None]:
        """Let the fake clock pass the total timeout while yielding."""
        async for i in ticking_generator(fake_clock):
            yield i

    async for i in generator_clean_total():
        pass

    assert i == 4
