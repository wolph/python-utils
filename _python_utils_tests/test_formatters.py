"""Tests for the formatting helpers in ``python_utils.formatters``."""

import datetime
import typing

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


def test_timesince_date_raises_type_error() -> None:
    """Keep raising ``TypeError`` for a date, which has no time."""
    today: typing.Any = datetime.date.today()
    with pytest.raises(TypeError):
        formatters.timesince(today)
