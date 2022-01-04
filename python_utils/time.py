import asyncio
import datetime
import itertools
import typing

from . import aio
import time

delta_type = typing.Union[datetime.timedelta, int, float]
timestamp_type = typing.Union[
    datetime.timedelta,
    datetime.date,
    datetime.datetime,
    str,
    int,
    float,
    None,
]

# There might be a better way to get the epoch with tzinfo, please create
# a pull request if you know a better way that functions for Python 2 and 3
epoch = datetime.datetime(year=1970, month=1, day=1)


def timedelta_to_seconds(delta: datetime.timedelta):
    '''Convert a timedelta to seconds with the microseconds as fraction

    Note that this method has become largely obsolete with the
    `timedelta.total_seconds()` method introduced in Python 2.7.

    >>> from datetime import timedelta
    >>> '%d' % timedelta_to_seconds(timedelta(days=1))
    '86400'
    >>> '%d' % timedelta_to_seconds(timedelta(seconds=1))
    '1'
    >>> '%.6f' % timedelta_to_seconds(timedelta(seconds=1, microseconds=1))
    '1.000001'
    >>> '%.6f' % timedelta_to_seconds(timedelta(microseconds=1))
    '0.000001'
    '''
    # Only convert to float if needed
    if delta.microseconds:
        total = delta.microseconds * 1e-6
    else:
        total = 0
    total += delta.seconds
    total += delta.days * 60 * 60 * 24
    return total


def format_time(timestamp: timestamp_type,
                precision: datetime.timedelta = datetime.timedelta(seconds=1)):
    '''Formats timedelta/datetime/seconds

    >>> format_time('1')
    '0:00:01'
    >>> format_time(1.234)
    '0:00:01'
    >>> format_time(1)
    '0:00:01'
    >>> format_time(datetime.datetime(2000, 1, 2, 3, 4, 5, 6))
    '2000-01-02 03:04:05'
    >>> format_time(datetime.date(2000, 1, 2))
    '2000-01-02'
    >>> format_time(datetime.timedelta(seconds=3661))
    '1:01:01'
    >>> format_time(None)
    '--:--:--'
    >>> format_time(format_time)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Unknown type ...

    '''
    precision_seconds = precision.total_seconds()

    if isinstance(timestamp, str):
        timestamp = float(timestamp)

    if isinstance(timestamp, (int, float)):
        try:
            timestamp = datetime.timedelta(seconds=timestamp)
        except OverflowError:  # pragma: no cover
            timestamp = None

    if isinstance(timestamp, datetime.timedelta):
        seconds = timestamp.total_seconds()
        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        return str(datetime.timedelta(seconds=seconds))
    elif isinstance(timestamp, datetime.datetime):  # pragma: no cover
        # Python 2 doesn't have the timestamp method
        if hasattr(timestamp, 'timestamp'):
            seconds = timestamp.timestamp()
        else:
            seconds = timedelta_to_seconds(timestamp - epoch)

        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        try:  # pragma: no cover
            dt = datetime.datetime.fromtimestamp(seconds)
        except ValueError:  # pragma: no cover
            dt = datetime.datetime.max
        return str(dt)
    elif isinstance(timestamp, datetime.date):
        return str(timestamp)
    elif timestamp is None:
        return '--:--:--'
    else:
        raise TypeError('Unknown type %s: %r' % (type(timestamp), timestamp))


def timeout_generator(
        timeout: delta_type,
        interval: delta_type = datetime.timedelta(seconds=1),
        iterable: typing.Union[typing.Iterable, typing.Callable] =
        itertools.count,
        interval_multiplier: float = 1.0,
        maximum_interval: typing.Optional[delta_type] = None,
):
    '''
    Generator that walks through the given iterable (a counter by default)
    until the float_timeout is reached with a configurable float_interval
    between items

    >>> for i in timeout_generator(0.1, 0.06):
    ...     print(i)
    0
    1
    2
    >>> timeout = datetime.timedelta(seconds=0.1)
    >>> interval = datetime.timedelta(seconds=0.06)
    >>> for i in timeout_generator(timeout, interval, itertools.count()):
    ...     print(i)
    0
    1
    2
    >>> for i in timeout_generator(1, interval=0.1, iterable='ab'):
    ...     print(i)
    a
    b

    >>> timeout = datetime.timedelta(seconds=0.1)
    >>> interval = datetime.timedelta(seconds=0.06)
    >>> for i in timeout_generator(timeout, interval, interval_multiplier=2):
    ...     print(i)
    0
    1
    2
    '''
    float_timeout: float = _to_seconds(timeout)
    float_interval: float = _to_seconds(interval)
    float_maximum_interval: typing.Optional[float] = _to_seconds_or_none(
        maximum_interval)

    iterable_: typing.Iterable
    if callable(iterable):
        iterable_ = iterable()
    else:
        iterable_ = iterable

    end = float_timeout + time.perf_counter()
    for item in iterable_:
        yield item

        if time.perf_counter() >= end:
            break

        time.sleep(float_interval)

        interval *= interval_multiplier
        if float_maximum_interval:
            float_interval = min(float_interval, float_maximum_interval)


async def aio_timeout_generator(
        timeout: delta_type,
        interval: delta_type = datetime.timedelta(seconds=1),
        iterable: typing.Union[typing.AsyncIterable, typing.Callable] =
        aio.acount,
        interval_multiplier: float = 1.0,
        maximum_interval: typing.Optional[delta_type] = None,
):
    '''
    Aync generator that walks through the given iterable (a counter by
    default) until the float_timeout is reached with a configurable
    float_interval between items

    The interval_exponent automatically increases the float_timeout with each
    run. Note that if the float_interval is less than 1, 1/interval_exponent
    will be used so the float_interval is always growing. To double the
    float_interval with each run, specify 2.

    Doctests and asyncio are not friends, so no examples. But this function is
    effectively the same as the timeout_generor but it uses `async for`
    instead.
    '''
    float_timeout: float = _to_seconds(timeout)
    float_interval: float = _to_seconds(interval)
    float_maximum_interval: typing.Optional[float] = _to_seconds_or_none(
        maximum_interval)

    iterable_: typing.AsyncIterable
    if callable(iterable):
        iterable_ = iterable()
    else:
        iterable_ = iterable

    end = float_timeout + time.perf_counter()
    async for item in iterable_:  # pragma: no branch
        yield item

        if time.perf_counter() >= end:
            break

        await asyncio.sleep(float_interval)

        float_interval *= interval_multiplier
        if float_maximum_interval:  # pragma: no branch
            float_interval = min(float_interval, float_maximum_interval)


def _to_seconds(interval: delta_type) -> float:
    '''
    Convert a timedelta to seconds

    >>> _to_seconds(datetime.timedelta(seconds=1))
    1
    >>> _to_seconds(datetime.timedelta(seconds=1, microseconds=1))
    1.000001
    >>> _to_seconds(1)
    1
    >>> _to_seconds('whatever')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Unknown type ...
    '''
    if isinstance(interval, datetime.timedelta):
        return timedelta_to_seconds(interval)
    elif isinstance(interval, (int, float)):
        return interval
    else:
        raise TypeError('Unknown type %s: %r' % (type(interval), interval))


def _to_seconds_or_none(interval: typing.Optional[delta_type]) -> \
        typing.Optional[float]:
    if interval is None:
        return None
    else:
        return _to_seconds(interval)
