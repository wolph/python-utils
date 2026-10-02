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
    fake_clock: clock.FakeClock,
    monkeypatch: pytest.MonkeyPatch,
    timeout: float,
    interval: float,
    interval_multiplier: float,
    maximum_interval: float,
    iterable: types.AsyncIterable[types.Any],
    result: int,
) -> None:
    """Stop the async generator near the configured timeout."""

    async def sleep(delay: float) -> None:
        """Let the fake clock pass the delay without waiting for it."""
        fake_clock.sleep(delay)

    monkeypatch.setattr(asyncio, 'sleep', sleep)

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


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_sync_callback(
    fake_clock: clock.FakeClock,
) -> None:
    """Accept an ``on_timeout`` callback that is a plain function."""
    exceptions: types.List[BaseException] = []

    def on_timeout(
        generator: types.AsyncGenerator[int, None],
        timeout: types.Optional[types.delta_type],
        total_timeout: types.Optional[types.delta_type],
        exception: BaseException,
    ) -> None:
        """Record the timeout and return nothing to await."""
        exceptions.append(exception)

    items: types.List[int] = [
        i
        async for i in python_utils.aio_generator_timeout_detector(
            ticking_generator(fake_clock),
            total_timeout=0.45,
            on_timeout=on_timeout,
        )
    ]

    assert items == [0, 1, 2, 3, 4]
    assert len(exceptions) == 1
    assert isinstance(exceptions[0], asyncio.TimeoutError)


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_async_callback(
    fake_clock: clock.FakeClock,
) -> None:
    """Await an ``on_timeout`` callback that is a coroutine function."""
    calls: types.List[types.Mapping[str, types.Any]] = []

    async def on_timeout(
        generator: types.AsyncGenerator[int, None],
        timeout: types.Optional[types.delta_type],
        total_timeout: types.Optional[types.delta_type],
        exception: BaseException,
        **kwargs: types.Mapping[str, types.Any],
    ) -> None:
        """Record the extra keyword arguments after a real await."""
        await asyncio.sleep(0)
        calls.append(kwargs)

    items: types.List[int] = [
        i
        async for i in python_utils.aio_generator_timeout_detector(
            ticking_generator(fake_clock),
            total_timeout=0.45,
            on_timeout=on_timeout,
            context={'attempt': 1},
        )
    ]

    assert items == [0, 1, 2, 3, 4]
    assert calls == [{'context': {'attempt': 1}}]


async def collect_before_stall(
    generator: types.AsyncGenerator[int, None],
) -> types.List[int]:
    """Collect the items of a detector that has to stop at the stall."""
    items: types.List[int] = []

    async def collect() -> None:
        """Gather every item the detector lets through."""
        item: int
        async for item in generator:
            items.append(item)

    try:
        # Without the guard a detector that waits out the stall would keep
        # the test busy for `STALL` seconds before it fails.
        await asyncio.wait_for(collect(), STALL / 10)
    finally:
        await generator.aclose()

    return items


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_total_timeout_stall() -> None:
    """Enforce the total timeout while waiting for the next item."""
    items: types.List[int] = await collect_before_stall(
        python_utils.aio_generator_timeout_detector(
            stalling_generator(), total_timeout=STALL / 500, on_timeout=None
        )
    )

    # The stall comes before item 5, so that item can never arrive in time.
    # How many of the earlier items arrive depends on the machine.
    assert items == list(range(len(items)))
    assert len(items) <= 5


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_total_timeout_reraise() -> None:
    """Raise the total timeout error from a wait that it cut short."""
    detector: types.AsyncGenerator[int, None] = (
        python_utils.aio_generator_timeout_detector(
            stalling_generator(), total_timeout=STALL / 500
        )
    )

    with pytest.raises(asyncio.TimeoutError, match='Total timeout reached'):
        await collect_before_stall(detector)


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_total_before_item() -> None:
    """Let the total timeout win when it ends before the item timeout."""
    detector: types.AsyncGenerator[int, None] = (
        python_utils.aio_generator_timeout_detector(
            stalling_generator(), timeout=STALL, total_timeout=STALL / 500
        )
    )

    with pytest.raises(asyncio.TimeoutError, match='Total timeout reached'):
        await collect_before_stall(detector)


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_item_before_total() -> None:
    """Let the item timeout win when it ends before the total timeout."""
    detector: types.AsyncGenerator[int, None] = (
        python_utils.aio_generator_timeout_detector(
            stalling_generator(), timeout=STALL / 500, total_timeout=STALL
        )
    )

    with pytest.raises(asyncio.TimeoutError) as exc_info:
        await collect_before_stall(detector)

    assert 'Total timeout reached' not in str(exc_info.value)


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_total_timeout_finishes() -> None:
    """Finish as normal when the generator ends within the total timeout."""

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield three items without waiting."""
        i: int
        for i in range(3):
            yield i

    items: types.List[int] = [
        i
        async for i in python_utils.aio_generator_timeout_detector(
            generator(), total_timeout=STALL
        )
    ]

    assert items == [0, 1, 2]


@pytest.mark.asyncio
async def test_aio_generator_timeout_detector_generator_timeout() -> None:
    """Hand a timeout raised by the generator itself over unchanged."""
    exceptions: types.List[BaseException] = []

    async def generator() -> types.AsyncGenerator[int, None]:
        """Yield one item and then fail with a timeout of its own."""
        yield 0
        raise asyncio.TimeoutError('raised by the generator')

    def on_timeout(
        generator: types.AsyncGenerator[int, None],
        timeout: types.Optional[types.delta_type],
        total_timeout: types.Optional[types.delta_type],
        exception: BaseException,
    ) -> None:
        """Record the exception the detector reports."""
        exceptions.append(exception)

    items: types.List[int] = [
        i
        async for i in python_utils.aio_generator_timeout_detector(
            generator(), total_timeout=STALL, on_timeout=on_timeout
        )
    ]

    assert items == [0]
    assert [str(exception) for exception in exceptions] == [
        'raised by the generator'
    ]


@pytest.mark.parametrize(
    'timestamp,precision,expected',
    [
        (1, datetime.timedelta(milliseconds=100), '0:00:01'),
        (60, datetime.timedelta(milliseconds=100), '0:01:00'),
        (0.3, datetime.timedelta(milliseconds=100), '0:00:00.300000'),
        (1.234, datetime.timedelta(milliseconds=1), '0:00:01.234000'),
        (1.239, datetime.timedelta(milliseconds=10), '0:00:01.230000'),
        (
            datetime.timedelta(seconds=2),
            datetime.timedelta(milliseconds=100),
            '0:00:02',
        ),
        (
            datetime.datetime(2000, 1, 2, 3, 4, 5),
            datetime.timedelta(milliseconds=100),
            '2000-01-02 03:04:05',
        ),
        (
            datetime.datetime(2000, 1, 2, 3, 4, 5, 678901),
            datetime.timedelta(milliseconds=10),
            '2000-01-02 03:04:05.670000',
        ),
    ],
)
def test_format_time_sub_second_precision(
    timestamp: types.timestamp_type,
    precision: datetime.timedelta,
    expected: str,
) -> None:
    """Keep a value that is on the precision grid where it is."""
    assert python_utils.format_time(timestamp, precision) == expected


@pytest.mark.parametrize(
    'timestamp',
    [float('nan'), 'nan', float('inf'), float('-inf'), 1e20, 10**30],
)
def test_format_time_placeholder_for_impossible_numbers(
    timestamp: types.timestamp_type,
) -> None:
    """Print the placeholder for a number that is not a duration."""
    assert python_utils.format_time(timestamp) == '--:--:--'


def test_format_time_extreme_timedeltas() -> None:
    """Format the largest and the smallest timedelta without overflow."""
    largest: str = python_utils.format_time(datetime.timedelta.max)
    smallest: str = python_utils.format_time(datetime.timedelta.min)

    assert largest == '999999999 days, 23:59:59'
    assert smallest == '-999999999 days, 0:00:00'


@pytest.mark.parametrize(
    'delta',
    [
        datetime.timedelta(microseconds=1),
        datetime.timedelta(microseconds=-1),
        datetime.timedelta(seconds=437, microseconds=579262),
        datetime.timedelta(days=-5, microseconds=1),
        datetime.timedelta(days=1000000, microseconds=999999),
        datetime.timedelta.max,
    ],
)
def test_timedelta_to_seconds_fraction_precision(
    delta: datetime.timedelta,
) -> None:
    """Keep the precision of ``total_seconds`` for a fraction of a second."""
    seconds: types.Number = python_utils.timedelta_to_seconds(delta)

    assert isinstance(seconds, float)
    assert seconds == delta.total_seconds()


@pytest.mark.parametrize(
    'delta,expected',
    [
        (datetime.timedelta(0), 0),
        (datetime.timedelta(seconds=1), 1),
        (datetime.timedelta(seconds=-1), -1),
        (datetime.timedelta(days=1), 86400),
        (datetime.timedelta(days=999999999, seconds=86399), 86399999999999),
        (datetime.timedelta.min, -86399999913600),
    ],
)
def test_timedelta_to_seconds_whole_seconds_stay_int(
    delta: datetime.timedelta, expected: int
) -> None:
    """Return whole seconds as the exact ``int`` they have always been."""
    seconds: types.Number = python_utils.timedelta_to_seconds(delta)

    assert isinstance(seconds, int)
    assert seconds == expected


def test_timeout_generator_maximum_interval_first_sleep(
    fake_clock: clock.FakeClock,
) -> None:
    """Hold the first sleep to ``maximum_interval`` as well."""
    items: types.List[str] = list(
        python_utils.timeout_generator(
            timeout=100, interval=10, iterable='abc', maximum_interval=1
        )
    )

    assert items == ['a', 'b', 'c']
    assert fake_clock.sleeps == [1, 1, 1]


def test_timeout_generator_maximum_interval_zero(
    fake_clock: clock.FakeClock,
) -> None:
    """Read a ``maximum_interval`` of zero as no maximum at all."""
    items: types.List[str] = list(
        python_utils.timeout_generator(
            timeout=100,
            interval=1,
            iterable='abc',
            interval_multiplier=2,
            maximum_interval=0,
        )
    )

    assert items == ['a', 'b', 'c']
    assert fake_clock.sleeps == [1, 2, 4]


@pytest.mark.asyncio
async def test_aio_timeout_generator_maximum_interval_first_sleep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Hold the first async sleep to ``maximum_interval`` as well."""
    sleeps: types.List[float] = []

    async def mock_sleep(delay: float) -> None:
        """Record each requested delay instead of sleeping."""
        sleeps.append(delay)

    monkeypatch.setattr(asyncio, 'sleep', mock_sleep)

    async def letters() -> types.AsyncGenerator[str, None]:
        """Yield three letters without waiting."""
        letter: str
        for letter in 'abc':
            yield letter

    items: types.List[str] = [
        item
        async for item in python_utils.aio_timeout_generator(
            timeout=100, interval=10, iterable=letters, maximum_interval=1
        )
    ]

    assert items == ['a', 'b', 'c']
    assert sleeps == [1, 1, 1]
