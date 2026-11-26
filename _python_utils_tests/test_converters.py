"""Tests for the conversion helpers in ``python_utils.converters``."""

import decimal
import math
import re
from fractions import Fraction

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


class _LessEqualOnly:
    """A numeric type with ``__le__`` and ``__float__``, no ``__lt__``."""

    def __init__(self, value: int) -> None:
        self.value: int = value

    def __le__(self, other: object) -> bool:
        return self.value <= other  # type: ignore[operator]

    def __float__(self) -> float:
        return float(self.value)


def test_scale_1024_accepts_number_without_lt() -> None:
    """Keep the 4.1.4 float path for a type without ``__lt__``."""
    value: _LessEqualOnly = _LessEqualOnly(2048)
    assert converters.scale_1024(value, 9) == (2.0, 1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    'value,old_min,old_max,new_min,new_max',
    [
        (1e200, 0.0, 1e200, 0.0, 1e200),
        (-1e200, 0.0, 1e200, 0.0, 1e200),
        (2e200, 1e200, 3e200, 4e200, 8e200),
        (2e200, 3e200, 1e200, 8e200, 4e200),
        (1e-200, 0.0, 1e-200, 0.0, 1e-200),
        (-1e-200, 0.0, 1e-200, 0.0, 1e-200),
        (2e-200, 1e-200, 3e-200, 4e-200, 8e-200),
        (2e-200, 3e-200, 1e-200, 8e-200, 4e-200),
        (0.1, 0.0, 5e-324, 0.0, 5e-324),
        (5e-324, 0.0, 5e-324, 0.0, 0.1),
        (1e308, 0.0, 1e308, 0.0, 2.0),
        (2.0, 0.0, 1e308, 0.0, 1e308),
        (5e-324, 0.0, 0.66, 0.0, 0.3),
        (5e-324, 0.0, 1 / 1.4, 0.0, 0.4),
        (5 * math.ulp(0.0), 0.0, 0.3, 0.0, 0.03),
    ],
)
def test_remap_extreme_float_product(
    value: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float,
) -> None:
    """Keep a representable result when the intermediate product is not."""
    v, lo, hi, out_lo, out_hi = map(
        Fraction, (value, old_min, old_max, new_min, new_max)
    )
    expected = float((v - lo) * (out_hi - out_lo) / (hi - lo) + out_lo)
    result = converters.remap(value, old_min, old_max, new_min, new_max)
    # An absolute tolerance would let zero pass for the tiny expected values.
    assert result == pytest.approx(expected, rel=1e-14, abs=0.0)


def test_remap_preserves_normal_float_rounding() -> None:
    """Keep multiplication before division when the product is usable."""
    assert converters.remap(0.1, 0.0, 3.0, 0.0, 7.0) == 0.23333333333333336
    assert converters.remap(0.0, 0.0, 1.0, 0.0, 1.0) == 0.0


def test_remap_preserves_integer_arithmetic() -> None:
    """Keep floor division and integers larger than a float can hold."""
    assert converters.remap(1, 0, 3, 0, -10) == -4
    large = 10**400
    result = converters.remap(large, 0, large, 0, large)
    assert result == large
    assert type(result) is int


@pytest.mark.parametrize('value', ['1e200', '1e-200'])
def test_remap_preserves_decimal_arithmetic(value: str) -> None:
    """Keep Decimal promotion and precision outside the float fallback."""
    number = decimal.Decimal(value)
    result = converters.remap(number, 0.0, number, 0.0, number)
    assert result == number
    assert isinstance(result, decimal.Decimal)


@pytest.mark.parametrize(
    'value,old_min,old_max,new_min,new_max,expected',
    [
        (math.inf, 0.0, 1.0, 0.0, 1.0, math.inf),
        (math.nan, 0.0, 1.0, 0.0, 1.0, math.nan),
        (1e308, -1e308, 1e308, 0.0, 1.0, math.nan),
        (0.0, -1e308, 1e308, 0.0, 1e308, math.nan),
        (1e308, 0.0, 1e308, -1e308, 1e308, math.inf),
        (1e308, 0.0, 0.5, 0.0, 2.0, math.inf),
    ],
)
def test_remap_preserves_nonfinite_arithmetic(
    value: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float,
    expected: float,
) -> None:
    """Leave nonfinite inputs, differences and final overflow unchanged."""
    result = converters.remap(value, old_min, old_max, new_min, new_max)
    if math.isnan(expected):
        assert math.isnan(result)
    else:
        assert result == expected
