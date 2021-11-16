import pytest

from python_utils import unit_converter


def test_main():
    unit_converter.main()


temperature_units = (
    '°K', 'K',
    '°C', 'C',
    '°F', 'F',
    'R',
    pytest.param('X', marks=pytest.mark.xfail),
)
units = ('value', 'from_unit', 'to_unit', 'expected'), [
    # (71, 'in³', 'mm³', 1163481.544),
    (129.5674, 'in²', 'mm²', 83591.704),
    (3.657, 'gal', 'l', 13.843),
    (500.679, 'g', 'lb', 1.104),
    #(75.1, '°F', '°K', 297.094),
    (132.7, 'mi/h', 'km/h', 213.560),
    (1.0, 'P', 'Pa s', 0.1),
    (56.0, 'in', 'cm', 142.24),
    (50.34, 'ftHg', 'mmHg', 15343.632),
    (50.34, 'inH2O', 'cmH2O', 127.864),
    (50.34, 'inHg', 'psi', 24.725)
]


@pytest.mark.parametrize('input_', temperature_units)
@pytest.mark.parametrize('output', temperature_units)
def test_temperature(input_, output):
    unit_converter.convert(1, input_, output)


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


@pytest.mark.parametrize(*units)
def test_units(value, from_unit, to_unit, expected):
    result = unit_converter.convert(value, from_unit, to_unit)
    print(f'{value} {from_unit} = {result} {to_unit}')
    assert round(result, 3) == expected


@pytest.mark.parametrize(*units)
def test_calculated_units(value, from_unit, to_unit, expected):
    from_unit = unit_converter.Unit(from_unit)
    to_unit = unit_converter.Unit(to_unit)
    result = value * (from_unit / to_unit)
    print(f'{value} {from_unit} = {result} {to_unit}')
    assert round(result, 3) == expected
