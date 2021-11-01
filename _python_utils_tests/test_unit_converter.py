import pytest

from python_utils import unit_converter


def test_empty_int_wrapper():
    a = unit_converter._IntWrapper(123)
    assert a.label == 'intwrapper'
    assert a.values == []


def test_main():
    unit_converter.main()


temperature_units = (
    '°K', 'K',
    '°C', 'C',
    '°F', 'F',
    'R',
    pytest.param('X', marks=pytest.mark.xfail),
)


@pytest.mark.parametrize('input_', temperature_units)
@pytest.mark.parametrize('output', temperature_units)
def test_temperature(input_, output):
    unit_converter.temperature_conversion(1, input_, output)


@pytest.mark.parametrize('prefix', [
    'Y',
    'Z',
    'E',
    'P',
    'T',
    'G',
    'M',
    'k',
    'h',
    'd',
    'c',
    'm',
    'µ',
    'n',
    'p',
    'f',
    'a',
    'z',
    'y',
    pytest.param('X', marks=pytest.mark.xfail),
])
def test_unit_prefixes(prefix):
    unit_converter.convert(1, '%sm' % prefix, 'm')
