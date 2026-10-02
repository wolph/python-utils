"""
This module provides utility functions for handling time-related operations.

Functions::

    timedelta_to_seconds: Convert a timedelta to seconds (microseconds as
        fraction).
    delta_to_seconds: Convert a timedelta or numeric interval to seconds.
    delta_to_seconds_or_none: Convert a timedelta to seconds or return None.
    format_time: Format a timestamp (timedelta, datetime, or seconds).
    timeout_generator: Generate items from an iterable until a timeout.
    aio_timeout_generator: Async generate items from an iterable until a
        timeout.
    aio_generator_timeout_detector: Detect if an async generator has stalled.
    aio_generator_timeout_detector_decorator: Decorator for the detector.
"""

# pyright: reportUnnecessaryIsInstance=false
import collections.abc
import datetime
import functools
import itertools
import time
import typing

import python_utils
from python_utils import _aliases, exceptions

#: Item type produced by the time/timeout generators.
_T = typing.TypeVar('_T')
#: Parameter specification for the timeout-detector decorator's target.
_P = typing.ParamSpec('_P')


#: The Unix epoch (1970-01-01) as a naive ``datetime``, used as a reference.
# There might be a better way to get the epoch with tzinfo; please open a
# pull request if you know one.
epoch = datetime.datetime(year=1970, month=1, day=1)


def timedelta_to_seconds(delta: datetime.timedelta) -> _aliases.Number:
    """Convert a timedelta to seconds with the microseconds as fraction.

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
    """
    seconds: int = delta.seconds + delta.days * 60 * 60 * 24

    # Only convert to float if needed
    if delta.microseconds:
        # Divide the whole microseconds once, the way `total_seconds()` does.
        # Adding a float fraction to a large number of seconds loses digits.
        return (seconds * 10**6 + delta.microseconds) / 10**6
    else:
        return seconds


def delta_to_seconds(interval: _aliases.delta_type) -> _aliases.Number:
    """
    Convert a timedelta to seconds.

    >>> delta_to_seconds(datetime.timedelta(seconds=1))
    1
    >>> delta_to_seconds(datetime.timedelta(seconds=1, microseconds=1))
    1.000001
    >>> delta_to_seconds(1)
    1
    >>> delta_to_seconds('whatever')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: Unknown type ...
    """
    if isinstance(interval, datetime.timedelta):
        return timedelta_to_seconds(interval)
    elif isinstance(interval, (int, float)):
        return interval
    else:
        raise TypeError(f'Unknown type {type(interval)}: {interval!r}')


def delta_to_seconds_or_none(
    interval: _aliases.delta_type | None,
) -> _aliases.Number | None:
    """Convert a timedelta to seconds, passing ``None`` through unchanged.

    Args:
        interval: A timedelta or a number of seconds, or ``None``.

    Returns:
        The interval in seconds, or ``None`` when ``interval`` is ``None``.

    >>> delta_to_seconds_or_none(datetime.timedelta(seconds=2))
    2
    >>> delta_to_seconds_or_none(None) is None
    True
    """
    if interval is None:
        return None
    else:
        return delta_to_seconds(interval)


def format_time(
    timestamp: _aliases.timestamp_type,
    precision: datetime.timedelta = datetime.timedelta(seconds=1),
) -> str:
    """Formats timedelta/datetime/seconds.

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

    """
    if isinstance(timestamp, str):
        timestamp = float(timestamp)

    if isinstance(timestamp, (int, float)):
        try:
            timestamp = datetime.timedelta(seconds=timestamp)
        except (OverflowError, ValueError):
            # Too large for a timedelta, or not a number at all: nan raises
            # a ValueError where infinity raises an OverflowError.
            timestamp = None

    if isinstance(timestamp, datetime.timedelta):
        # Truncate the number to the given precision. A timedelta counts in
        # whole microseconds, which keeps the modulo exact. In float seconds
        # `1.0 % 0.1` is just under 0.1 and the result drops a whole step.
        return str(timestamp - timestamp % precision)
    elif isinstance(timestamp, datetime.datetime):  # pragma: no cover
        # Python 2 doesn't have the timestamp method
        if hasattr(timestamp, 'timestamp'):
            seconds = timestamp.timestamp()
        else:
            seconds = timedelta_to_seconds(timestamp - epoch)

        # Truncate the number to the given precision, in whole microseconds
        # for the same reason as above
        since_epoch: datetime.timedelta = datetime.timedelta(seconds=seconds)
        seconds = (since_epoch - since_epoch % precision).total_seconds()

        try:  # pragma: no cover
            dt = datetime.datetime.fromtimestamp(seconds)
        except (ValueError, OSError):  # pragma: no cover
            dt = datetime.datetime.max
        return str(dt)
    elif isinstance(timestamp, datetime.date):
        return str(timestamp)
    elif timestamp is None:
        return '--:--:--'
    else:
        raise TypeError(f'Unknown type {type(timestamp)}: {timestamp!r}')


@typing.overload
def _to_iterable(
    iterable: collections.abc.Callable[[], collections.abc.AsyncIterable[_T]]
    | collections.abc.AsyncIterable[_T],
) -> collections.abc.AsyncIterable[_T]:
    """Async overload: async iterable or factory in, async iterable out."""


@typing.overload
def _to_iterable(
    iterable: collections.abc.Callable[[], collections.abc.Iterable[_T]]
    | collections.abc.Iterable[_T],
) -> collections.abc.Iterable[_T]:
    """Sync overload: sync iterable or factory in, sync iterable out."""


def _to_iterable(
    iterable: collections.abc.Iterable[_T]
    | collections.abc.Callable[[], collections.abc.Iterable[_T]]
    | collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[[], collections.abc.AsyncIterable[_T]],
) -> collections.abc.Iterable[_T] | collections.abc.AsyncIterable[_T]:
    """Return ``iterable``, calling it first if it is a zero-arg callable."""
    if callable(iterable):
        return iterable()
    else:
        return iterable


def timeout_generator(
    timeout: _aliases.delta_type,
    interval: _aliases.delta_type = datetime.timedelta(seconds=1),
    iterable: collections.abc.Iterable[_T]
    | collections.abc.Callable[
        [], collections.abc.Iterable[_T]
    ] = itertools.count,  # type: ignore[assignment]
    interval_multiplier: float = 1.0,
    maximum_interval: _aliases.delta_type | None = None,
) -> collections.abc.Iterable[_T]:
    """
    Generator that walks through the given iterable (a counter by default)
    until the float_timeout is reached with a configurable float_interval
    between items.

    This can be used to limit the time spent on a slow operation. This can be
    useful for testing slow APIs so you get a small sample of the data in a
    reasonable amount of time.

    After every sleep the interval is multiplied by `interval_multiplier`. No
    sleep is longer than `maximum_interval`, and that includes the first one.
    A `maximum_interval` of `None` or `0` means that there is no maximum.

    >>> for i in timeout_generator(0.1, 0.06):
    ...     # Put your slow code here
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
    """
    float_interval: float = delta_to_seconds(interval)
    float_maximum_interval: float | None = delta_to_seconds_or_none(
        maximum_interval
    )
    iterable_ = _to_iterable(iterable)

    # The maximum holds for the first sleep as well. Zero is not a maximum
    # here, it means the same as `None`.
    if float_maximum_interval:
        float_interval = min(float_interval, float_maximum_interval)

    end = delta_to_seconds(timeout) + time.perf_counter()
    for item in iterable_:
        yield item

        if time.perf_counter() >= end:
            break

        time.sleep(float_interval)

        float_interval *= interval_multiplier
        if float_maximum_interval:
            float_interval = min(float_interval, float_maximum_interval)


async def aio_timeout_generator(
    timeout: _aliases.delta_type,  # noqa: ASYNC109
    interval: _aliases.delta_type = datetime.timedelta(seconds=1),
    iterable: collections.abc.AsyncIterable[_T]
    | collections.abc.Callable[..., collections.abc.AsyncIterable[_T]]
    | None = None,
    interval_multiplier: float = 1.0,
    maximum_interval: _aliases.delta_type | None = None,
) -> collections.abc.AsyncGenerator[_T, None]:
    """
    Async generator that walks through the given async iterable (a counter by
    default) until the float_timeout is reached with a configurable
    float_interval between items.

    After every sleep the interval is multiplied by `interval_multiplier`. To
    double the interval with each run, specify 2. A value below 1 makes the
    interval shorter with each run. No sleep is longer than
    `maximum_interval`, and that includes the first one. A `maximum_interval`
    of `None` or `0` means that there is no maximum.

    Doctests and asyncio are not friends, so no examples. But this function is
    effectively the same as the `timeout_generator` but it uses `async for`
    instead.
    """
    # Imported lazily so that importing `python_utils.time` for its
    # synchronous helpers (e.g. ``format_time``) does not pull in ``asyncio``.
    import asyncio

    from python_utils import aio

    if iterable is None:
        iterable = typing.cast(
            collections.abc.Callable[[], collections.abc.AsyncIterable[_T]],
            aio.acount,
        )

    float_interval: float = delta_to_seconds(interval)
    float_maximum_interval: float | None = delta_to_seconds_or_none(
        maximum_interval
    )
    iterable_ = _to_iterable(iterable)

    # The maximum holds for the first sleep as well. Zero is not a maximum
    # here, it means the same as `None`.
    if float_maximum_interval:
        float_interval = min(float_interval, float_maximum_interval)

    end = delta_to_seconds(timeout) + time.perf_counter()
    async for item in iterable_:  # pragma: no branch
        yield item

        if time.perf_counter() >= end:
            break

        await asyncio.sleep(float_interval)

        float_interval *= interval_multiplier
        if float_maximum_interval:  # pragma: no branch
            float_interval = min(float_interval, float_maximum_interval)


async def _next_item(
    generator: collections.abc.AsyncGenerator[_T, None],
    timeout_s: float | None,
    total_timeout_end: float | None,
) -> _T:
    """Wait for the next item for as long as both timeouts allow.

    Args:
        generator: The async generator to take the next item from.
        timeout_s: Seconds to wait for this item. ``None`` and ``0`` wait
            without a limit of their own.
        total_timeout_end: The ``time.perf_counter()`` value at which the
            total timeout is up, or ``None`` without a total timeout.

    Returns:
        The next item of ``generator``.

    Raises:
        asyncio.TimeoutError: When the item takes longer than ``timeout_s``,
            or with ``'Total timeout reached'`` when the total timeout is up
            first.
        StopAsyncIteration: When ``generator`` has no items left.
    """
    # Imported lazily so importing `python_utils.time` stays asyncio-free.
    import asyncio

    if total_timeout_end:
        remaining: float = total_timeout_end - time.perf_counter()
        if remaining <= 0:
            raise asyncio.TimeoutError('Total timeout reached')

        # The total timeout has to end the wait for the next item as well,
        # otherwise a stalled generator outlives it.
        if not timeout_s or remaining < timeout_s:
            next_item: asyncio.Future[_T] = asyncio.ensure_future(
                generator.__anext__()
            )
            try:
                return await asyncio.wait_for(next_item, remaining)
            except asyncio.TimeoutError:
                # `wait_for` cancels the item when the time is up. A timeout
                # raised by the generator itself leaves the item uncancelled
                # and is passed on as it is.
                if next_item.cancelled():
                    raise asyncio.TimeoutError(
                        'Total timeout reached'
                    ) from None
                raise

    if timeout_s:
        return await asyncio.wait_for(generator.__anext__(), timeout_s)
    else:
        return await generator.__anext__()


async def aio_generator_timeout_detector(
    generator: collections.abc.AsyncGenerator[_T, None],
    timeout: _aliases.delta_type | None = None,  # noqa: ASYNC109
    total_timeout: _aliases.delta_type | None = None,
    on_timeout: collections.abc.Callable[
        [
            collections.abc.AsyncGenerator[_T, None],
            _aliases.delta_type | None,
            _aliases.delta_type | None,
            BaseException,
        ],
        typing.Any,
    ]
    | None = exceptions.reraise,
    **on_timeout_kwargs: collections.abc.Mapping[str, typing.Any],
) -> collections.abc.AsyncGenerator[_T, None]:
    """
    This function is used to detect if an asyncio generator has not yielded
    an element for a set amount of time.

    The `timeout` is the time a single element may take. A `timeout` of `None`
    or `0` means that there is no timeout per element. The `total_timeout` is
    the time all elements together may take, and it also ends the wait for an
    element that does not arrive.

    The `on_timeout` argument is called with the `generator`, `timeout`,
    `total_timeout`, `exception` and the extra `**kwargs` to this function as
    arguments. It can be a plain function or a coroutine function.
    If `on_timeout` is not specified, the exception is reraised.
    If `on_timeout` is `None`, the exception is silently ignored and the
    generator will finish as normal.
    """
    # Imported lazily so importing `python_utils.time` stays asyncio-free.
    import asyncio

    if total_timeout is None:
        total_timeout_end = None
    else:
        total_timeout_end = time.perf_counter() + delta_to_seconds(
            total_timeout
        )

    timeout_s = python_utils.delta_to_seconds_or_none(timeout)

    while True:
        try:
            yield await _next_item(generator, timeout_s, total_timeout_end)

        except asyncio.TimeoutError as exception:  # noqa: PERF203
            if on_timeout is not None:
                result: typing.Any = on_timeout(
                    generator,
                    timeout,
                    total_timeout,
                    exception,
                    **on_timeout_kwargs,
                )
                # A coroutine function hands back something to await, a
                # plain function has already done its work by now.
                if isinstance(result, collections.abc.Awaitable):
                    await result
            break

        except StopAsyncIteration:
            break


def aio_generator_timeout_detector_decorator(
    timeout: _aliases.delta_type | None = None,
    total_timeout: _aliases.delta_type | None = None,
    on_timeout: collections.abc.Callable[
        [
            collections.abc.AsyncGenerator[typing.Any, None],
            _aliases.delta_type | None,
            _aliases.delta_type | None,
            BaseException,
        ],
        typing.Any,
    ]
    | None = exceptions.reraise,
    **on_timeout_kwargs: collections.abc.Mapping[str, typing.Any],
) -> collections.abc.Callable[
    [collections.abc.Callable[_P, collections.abc.AsyncGenerator[_T, None]]],
    collections.abc.Callable[_P, collections.abc.AsyncGenerator[_T, None]],
]:
    """Wrap a generator function with ``aio_generator_timeout_detector``.

    Args:
        timeout: Per-item timeout. If a single yield takes longer,
            ``on_timeout`` fires. ``None`` or ``0`` disables the per-item
            check.
        total_timeout: Overall timeout across the whole generator. It also
            ends the wait for an item that does not arrive.
        on_timeout: Callback invoked on a timeout; defaults to re-raising.
        **on_timeout_kwargs: Extra keyword arguments passed to ``on_timeout``.

    Returns:
        A decorator that wraps an async-generator function so every call is
        guarded against stalls.
    """

    def _timeout_detector_decorator(
        generator: collections.abc.Callable[
            _P, collections.abc.AsyncGenerator[_T, None]
        ],
    ) -> collections.abc.Callable[
        _P, collections.abc.AsyncGenerator[_T, None]
    ]:
        """Wrap ``generator`` so each call is timeout-guarded."""

        @functools.wraps(generator)
        def wrapper(
            *args: _P.args,
            **kwargs: _P.kwargs,
        ) -> collections.abc.AsyncGenerator[_T, None]:
            """Forward the call to ``aio_generator_timeout_detector``."""
            return aio_generator_timeout_detector(
                generator(*args, **kwargs),
                timeout,
                total_timeout,
                on_timeout,
                **on_timeout_kwargs,
            )

        return wrapper

    return _timeout_detector_decorator
