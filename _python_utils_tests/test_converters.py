"""Tests for the conversion helpers in ``python_utils.converters``."""

import math
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


@pytest.mark.parametrize('power', range(1, 9))
def test_scale_1024_integer_prefix_boundaries(power: int) -> None:
    """Choose prefixes from the integer value before rounding it to float."""
    boundary = 1024**power
    for value, expected_power in (
        (boundary - 1, power - 1),
        (boundary, power),
        (boundary + 1, power),
    ):
        assert converters.scale_1024(value, 9) == (
            float(value) / 1024**expected_power,
            expected_power,
        )


@pytest.mark.parametrize('power', range(1, 9))
def test_scale_1024_float_prefix_boundaries(power: int) -> None:
    """Keep the float immediately below a prefix boundary in the lower unit."""
    boundary = float(1024**power)
    for value, expected_power in (
        (math.nextafter(boundary, 0.0), power - 1),
        (boundary, power),
        (math.nextafter(boundary, math.inf), power),
    ):
        assert converters.scale_1024(value, 9) == (
            value / 1024**expected_power,
            expected_power,
        )


def test_scale_1024_prefix_limit() -> None:
    """Keep values in the largest available prefix even at higher powers."""
    assert converters.scale_1024(1024**5, 3) == (1024.0**3, 2)


@pytest.mark.parametrize('n_prefixes', [0, -1])
def test_scale_1024_without_prefixes(n_prefixes: int) -> None:
    """Never return a negative power when there are no prefixes."""
    assert converters.scale_1024(2048, n_prefixes) == (2048.0, 0)


@pytest.mark.parametrize('default', [0.0, -1.25])
def test_to_float_float_default(default: float) -> None:
    """Accept the documented float fallback in typed consumer code."""
    assert converters.to_float('missing', default=default) is default
    assert (
        converters.to_float('missing', default=default, regexp=True) is default
    )
    assert converters.to_float('1.5', default=default) == 1.5
