"""Tests for the conversion helpers in ``python_utils.converters``."""

import re

import pytest

from python_utils import converters


@pytest.mark.parametrize('regexp', [r'\d+', re.compile(r'\d+')])
def test_to_int_regexp_without_group(regexp: re.Pattern[str] | str) -> None:
    """Use the whole match when the pattern has no capture group."""
    assert converters.to_int('abc123', regexp=regexp) == 123


@pytest.mark.parametrize('regexp', [r'\d+\.\d+', re.compile(r'\d+\.\d+')])
def test_to_float_regexp_without_group(
    regexp: re.Pattern[str] | str,
) -> None:
    """Use the whole match when the pattern has no capture group."""
    assert converters.to_float('abc1.5', regexp=regexp) == 1.5


def test_regexp_with_groups_keeps_its_group() -> None:
    """Keep the last group for ``to_int`` and the first for ``to_float``."""
    assert converters.to_int('a1b2', regexp=r'(\d)\D(\d)') == 2
    assert converters.to_float('a1b2', regexp=r'(\d)\D(\d)') == 1.0


@pytest.mark.parametrize('value', [0.0001, 1e-9, 2**-11])
def test_scale_1024_small_number(value: float) -> None:
    """Never scale a number below one up to a negative power."""
    assert converters.scale_1024(value, 9) == (value, 0)


@pytest.mark.parametrize('n_prefixes', [0, -1])
def test_scale_1024_without_prefixes(n_prefixes: int) -> None:
    """Never return a negative power when there are no prefixes."""
    assert converters.scale_1024(2048, n_prefixes) == (2048.0, 0)
