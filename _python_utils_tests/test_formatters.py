"""Tests for the formatting helpers in ``python_utils.formatters``."""

import datetime
import types
import typing
from zoneinfo import ZoneInfo, available_timezones

import pytest

from python_utils import formatters


@pytest.mark.parametrize(
    ('days', 'expected'),
    [
        (30, '1 month ago'),
        (35, '1 month and 5 days ago'),
        (60, '2 months ago'),
        (365, '1 year ago'),
        (730, '2 years ago'),
    ],
)
def test_timesince_units_do_not_overlap(days: int, expected: str) -> None:
    """Take the weeks and days from what the larger units left over."""
    delta: datetime.timedelta = datetime.timedelta(days=days)
    assert formatters.timesince(delta) == expected


@pytest.mark.parametrize(
    ('delta', 'expected'),
    [
        (datetime.timedelta(seconds=-1), '1 second ago'),
        (datetime.timedelta(seconds=-61), '1 minute and 1 second ago'),
        (datetime.timedelta(days=-400), '1 year and 1 month ago'),
    ],
)
def test_timesince_negative_timedelta(
    delta: datetime.timedelta, expected: str
) -> None:
    """Describe a negative timedelta by its size, like a datetime."""
    assert formatters.timesince(delta) == expected


@pytest.mark.parametrize(
    'timezone',
    [
        datetime.timezone.utc,
        datetime.timezone(datetime.timedelta(hours=5, minutes=30)),
    ],
)
def test_timesince_aware_datetime(timezone: datetime.timezone) -> None:
    """Compare a timezone-aware datetime with an aware current time."""
    # Only the two largest units are shown, so the time this test takes
    # cannot change the result.
    age: datetime.timedelta = datetime.timedelta(hours=1, minutes=30)
    moment: datetime.datetime = datetime.datetime.now(timezone) - age
    assert formatters.timesince(moment) == '1 hour and 30 minutes ago'


class _UnknownOffset(datetime.tzinfo):
    """A timezone that does not know its UTC offset, as ``tzinfo`` allows."""

    def utcoffset(self, dt: datetime.datetime | None) -> None:
        """Report the offset as unknown."""
        return

    def dst(self, dt: datetime.datetime | None) -> None:
        """Report the daylight saving offset as unknown."""
        return

    def tzname(self, dt: datetime.datetime | None) -> str:
        """Name the timezone."""
        return 'unknown'

    def fromutc(self, dt: datetime.datetime) -> datetime.datetime:
        """Use the UTC wall clock as the local one."""
        return dt.replace(tzinfo=self)


class _OwnOffsetDateTime(datetime.datetime):
    """A datetime subclass that reports an offset its tzinfo does not know."""

    def utcoffset(self) -> datetime.timedelta:
        """Report a fixed offset of three hours."""
        return datetime.timedelta(hours=3)


def test_timesince_datetime_subclass_with_own_offset() -> None:
    """Subtract a subclass with its own offset the way a datetime does."""
    age: datetime.timedelta = datetime.timedelta(hours=1, minutes=30)
    moment: datetime.datetime = _OwnOffsetDateTime.now(_UnknownOffset()) - age
    assert formatters.timesince(moment) == '1 hour and 30 minutes ago'


class _ClockChange(datetime.tzinfo):
    """A zone that sets its clock back an hour at 2026-10-25 01:00 UTC.

    One instance serves both sides of the change, as a ``dateutil`` zone
    does, so two datetimes in it share their tzinfo.
    """

    _CHANGE_UTC: datetime.datetime = datetime.datetime(2026, 10, 25, 1)
    _CHANGE_WALL: datetime.datetime = datetime.datetime(2026, 10, 25, 2)

    def utcoffset(self, dt: datetime.datetime | None) -> datetime.timedelta:
        """Report two hours before the change and one hour after it."""
        if dt is None or dt.replace(tzinfo=None) < self._CHANGE_WALL:
            return datetime.timedelta(hours=2)
        return datetime.timedelta(hours=1)

    def dst(self, dt: datetime.datetime | None) -> datetime.timedelta:
        """Report the daylight saving part of the offset."""
        return self.utcoffset(dt) - datetime.timedelta(hours=1)

    def tzname(self, dt: datetime.datetime | None) -> str:
        """Name the timezone."""
        return 'clock change'

    def fromutc(self, dt: datetime.datetime) -> datetime.datetime:
        """Convert from UTC by the offset in force at that instant."""
        if dt.replace(tzinfo=None) < self._CHANGE_UTC:
            return dt + datetime.timedelta(hours=2)
        return dt + datetime.timedelta(hours=1)


def test_timesince_counts_elapsed_time_across_dst_in_any_zone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count a clock change for a tzinfo that is not a ``ZoneInfo``."""
    zone = _ClockChange()
    # 23:00 at +02:00 is 21:00 UTC, six hours before the frozen current time.
    moment = datetime.datetime(2026, 10, 24, 23, tzinfo=zone)
    current = datetime.datetime(2026, 10, 25, 3, tzinfo=datetime.timezone.utc)

    class FrozenDateTime(datetime.datetime):
        """Return the chosen instant as the current time."""

        @classmethod
        def now(cls, tz: datetime.tzinfo | None = None) -> 'FrozenDateTime':
            """Keep the same instant while returning the requested timezone."""
            return cls.fromtimestamp(current.timestamp(), tz)

    monkeypatch.setattr(
        formatters,
        'datetime',
        types.SimpleNamespace(
            datetime=FrozenDateTime,
            timedelta=datetime.timedelta,
            timezone=datetime.timezone,
        ),
    )
    assert formatters.timesince(moment) == '6 hours ago'


class _LookAlike:
    """Not a datetime, but subtracts from one, as ``arrow.Arrow`` does."""

    def __init__(self, moment: datetime.datetime) -> None:
        """Wrap an aware datetime."""
        self.moment: datetime.datetime = moment
        self.tzinfo: datetime.tzinfo | None = moment.tzinfo

    def __rsub__(self, other: datetime.datetime) -> datetime.timedelta:
        """Subtract the wrapped datetime from ``other``."""
        return other - self.moment


def test_timesince_datetime_look_alike() -> None:
    """Let an object that is not a datetime do its own subtraction."""
    age: datetime.timedelta = datetime.timedelta(hours=1, minutes=30)
    # Not one of the documented types, so typed as Any like the date test.
    moment: typing.Any = _LookAlike(
        datetime.datetime.now(datetime.timezone.utc) - age
    )
    assert formatters.timesince(moment) == '1 hour and 30 minutes ago'


@pytest.mark.parametrize(
    ('moment', 'current'),
    [
        (
            datetime.datetime(2026, 11, 1, 1, 30, fold=0),
            datetime.datetime(2026, 11, 1, 1, 30, fold=1),
        ),
        (
            datetime.datetime(2026, 11, 1, 1, 30, fold=1),
            datetime.datetime(2026, 11, 1, 1, 30, fold=0),
        ),
        (
            datetime.datetime(2026, 3, 8, 1, 30),
            datetime.datetime(2026, 3, 8, 3, 30),
        ),
        (
            datetime.datetime(2026, 3, 8, 3, 30),
            datetime.datetime(2026, 3, 8, 1, 30),
        ),
    ],
    ids=['fall-back-past', 'fall-back-future', 'spring-past', 'spring-future'],
)
@pytest.mark.skipif(
    'America/New_York' not in available_timezones(),
    reason='IANA timezone data is not available',
)
def test_timesince_counts_elapsed_time_across_dst(
    moment: datetime.datetime,
    current: datetime.datetime,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Count elapsed time when both datetimes share a changing UTC offset."""
    timezone = ZoneInfo('America/New_York')
    current = current.replace(tzinfo=timezone)
    moment = moment.replace(tzinfo=timezone)

    class FrozenDateTime(datetime.datetime):
        """Return the chosen instant as the current time."""

        @classmethod
        def now(cls, tz: datetime.tzinfo | None = None) -> 'FrozenDateTime':
            """Keep the same instant while returning the requested timezone."""
            return cls.fromtimestamp(current.timestamp(), tz)

    monkeypatch.setattr(
        formatters,
        'datetime',
        types.SimpleNamespace(
            datetime=FrozenDateTime,
            timedelta=datetime.timedelta,
            timezone=datetime.timezone,
        ),
    )
    assert formatters.timesince(moment) == '1 hour ago'


class _ElapsedRsub(datetime.datetime):
    """A subclass whose own subtraction counts elapsed time, as in pandas."""

    def __rsub__(self, other: datetime.datetime) -> datetime.timedelta:
        """Subtract by UTC timestamp, so a DST change is counted."""
        seconds: float = other.timestamp() - datetime.datetime.timestamp(self)
        return datetime.timedelta(seconds=seconds)


@pytest.mark.skipif(
    'America/New_York' not in available_timezones(),
    reason='IANA timezone data is not available',
)
def test_timesince_subclass_subtraction_counts_dst_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Leave a subclass that counts elapsed time itself to count it once."""
    timezone = ZoneInfo('America/New_York')
    current = datetime.datetime(2026, 11, 1, 1, 30, fold=1, tzinfo=timezone)
    moment = _ElapsedRsub(2026, 11, 1, 1, 30, fold=0, tzinfo=timezone)

    def frozen_now(tz: datetime.tzinfo | None = None) -> datetime.datetime:
        """Return the chosen instant as a plain datetime, like the clock."""
        return datetime.datetime.fromtimestamp(current.timestamp(), tz)

    monkeypatch.setattr(
        formatters,
        'datetime',
        types.SimpleNamespace(
            datetime=types.SimpleNamespace(now=frozen_now),
            timedelta=datetime.timedelta,
            timezone=datetime.timezone,
        ),
    )
    assert formatters.timesince(moment) == '1 hour ago'


@pytest.mark.parametrize(
    ('moment', 'expected'),
    [
        (
            datetime.datetime.min.replace(
                tzinfo=datetime.timezone(datetime.timedelta(hours=1))
            ),
            '2000 years and 3 months ago',
        ),
        (
            datetime.datetime.max.replace(
                tzinfo=datetime.timezone(datetime.timedelta(hours=-1))
            ),
            '8005 years and 3 months ago',
        ),
    ],
    ids=['min-positive-offset', 'max-negative-offset'],
)
def test_timesince_aware_datetime_boundaries(
    moment: datetime.datetime,
    expected: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Accept aware inputs whose corresponding UTC date is out of range."""
    current = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)

    class FrozenDateTime(datetime.datetime):
        """Return the chosen instant as the current time."""

        @classmethod
        def now(cls, tz: datetime.tzinfo | None = None) -> 'FrozenDateTime':
            """Keep the same instant while returning the requested timezone."""
            return cls.fromtimestamp(current.timestamp(), tz)

    monkeypatch.setattr(
        formatters,
        'datetime',
        types.SimpleNamespace(
            datetime=FrozenDateTime,
            timedelta=datetime.timedelta,
            timezone=datetime.timezone,
        ),
    )
    assert formatters.timesince(moment) == expected


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('SPAM_EGGS', 'spam_eggs'),
        ('HTTP_OK', 'http_ok'),
        ('MAX_SIZE_LIMIT', 'max_size_limit'),
        ('HTML5Parser', 'html5_parser'),
        ('toUTF8String', 'to_utf8_string'),
        ('ABCD_e', 'abcd_e'),
    ],
)
def test_camel_to_underscore_keeps_acronyms_whole(
    name: str, expected: str
) -> None:
    """Leave an acronym whole when an underscore or a digit follows it."""
    assert formatters.camel_to_underscore(name) == expected


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('ABc', 'a_bc'),
        ('ABCd', 'ab_cd'),
        ('IPad', 'i_pad'),
        ('AName', 'a_name'),
        ('__ABc__', '__a_bc__'),
        ('XMLParser', 'xml_parser'),
    ],
)
def test_camel_to_underscore_splits_short_acronym_boundary(
    name: str, expected: str
) -> None:
    """Keep the final capital with the word following even a short acronym."""
    assert formatters.camel_to_underscore(name) == expected


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('IDs', 'ids'),
        ('URLs', 'urls'),
        ('UserIDs', 'user_ids'),
        ('GetURLs', 'get_urls'),
        ('IDsAndNames', 'ids_and_names'),
        ('PDFs_v2', 'pdfs_v2'),
        ('ISpam', 'i_spam'),
        ('IPsec', 'i_psec'),
    ],
)
def test_camel_to_underscore_keeps_plural_acronyms_whole(
    name: str, expected: str
) -> None:
    """Keep a plural ``s`` that ends a word with the acronym before it."""
    assert formatters.camel_to_underscore(name) == expected


def test_timesince_date_raises_type_error() -> None:
    """Keep raising ``TypeError`` for a date, which has no time."""
    today: typing.Any = datetime.date.today()
    with pytest.raises(TypeError):
        formatters.timesince(today)
