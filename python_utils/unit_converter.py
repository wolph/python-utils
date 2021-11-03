# -*- coding: utf-8 -*-
# This unit converter is an extended version of the SI model. It contains 
# most of the typical units a person would want to convert
# the main entry point is the 'convert' function.


"""
General rules[cc] for writing SI units and quantities apply to text that is
either handwritten or produced using an automated process:

  * The value of a quantity is written as a number followed by a space
  (representing a multiplication sign) and a unit symbol;
  e.g., 2.21 kg, 7.3×102 m², 22 K. This rule explicitly includes the percent
  sign (%) and the symbol for degrees Celsius (°C)
  Exceptions are the symbols for plane angular degrees, minutes, and seconds
  (°, ′, and ″, respectively), which are placed immediately after the number
  with no intervening space.
  * Symbols are mathematical entities, not abbreviations, and as such do not
  have an appended period/full stop (.), unless the rules of grammar demand
  one for another reason, such as denoting the end of a sentence.
  * A prefix is part of the unit, and its symbol is prepended to a unit
  symbol without a separator (e.g., k in km, M in MPa, G in GHz, μ in μg).
  Compound prefixes are not allowed. A prefixed unit is atomic in expressions
  (e.g., km² is equivalent to (km)²).
  * Unit symbols are written using roman (upright) type, regardless of the
  type used in the surrounding text.
  * Symbols for derived units formed by multiplication are joined with a
  centre dot (⋅) or a non-breaking space; e.g., N⋅m or N m.
  * Symbols for derived units formed by division are joined with a solidus (/),
  or given as a negative exponent. E.g., the "metre per second" can be written
  m/s, m s⁻¹, m⋅s⁻¹, or m/s. A solidus followed without parentheses by a centre
  dot (or space) or a solidus is ambiguous and must be avoided;
  e.g., kg/(m⋅s²) and kg⋅m⁻¹⋅s⁻² are acceptable, but kg/m/s² is ambiguous
  and unacceptable.
  * In the expression of acceleration due to gravity, a space separates the
  value and the units, both the 'm' and the 's' are lowercase because neither
  the metre nor the second are named after people, and exponentiation is
  represented with a superscript '²'.
  * The first letter of symbols for units derived from the name of a person is
  written in upper case; otherwise, they are written in lower case.
  E.g., the unit of pressure is named after Blaise Pascal, so its symbol is
  written "Pa", but the symbol for mole is written "mol". Thus, "T" is the
  symbol for tesla, a measure of magnetic field strength, and "t" the symbol
  for tonne, a measure of mass. Since 1979, the litre may exceptionally be
  written using either an uppercase "L" or a lowercase "l", a decision
  prompted by the similarity of the lowercase letter "l" to the numeral "1",
  especially with certain typefaces or English-style handwriting. The American
  NIST recommends that within the United States "L" be used rather than "l".
  * Symbols do not have a plural form, e.g., 25 kg, but not 25 kgs.
  * Uppercase and lowercase prefixes are not interchangeable. E.g., the
  quantities 1 mW and 1 MW represent two different quantities
  (milliwatt and megawatt).
  * The symbol for the decimal marker is either a point or comma on the line.
  In practice, the decimal point is used in most English-speaking countries
  and most of Asia, and the comma in most of Latin America and in continental
  European countries.
  * Any line-break inside a compound unit should be avoided.
  * Because the value of "billion" and "trillion" varies between languages,
  the dimensionless terms "ppb" (parts per billion) and "ppt"
  (parts per trillion) should be avoided. The SI Brochure does not
  suggest alternatives.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import decimal
import math


SUPER_SCRIPT_0 = chr(0x2070)  # ⁰
SUPER_SCRIPT_1 = chr(0x00B9)  # ¹
SUPER_SCRIPT_2 = chr(0x00B2)  # ²
SUPER_SCRIPT_3 = chr(0x00B3)  # ³
SUPER_SCRIPT_4 = chr(0x2074)  # ⁴
SUPER_SCRIPT_5 = chr(0x2075)  # ⁵
SUPER_SCRIPT_6 = chr(0x2076)  # ⁶
SUPER_SCRIPT_7 = chr(0x2077)  # ⁷
SUPER_SCRIPT_8 = chr(0x2078)  # ⁸
SUPER_SCRIPT_9 = chr(0x2079)  # ⁹
SUPER_SCRIPT_DECIMAL = chr(0x00B7)  # ·  (¹·²)
SUPER_SCRIPT_MINUS = chr(0x207B)  # ⁻ (⁻¹)
MULTIPLIER = chr(0x22C5)  # N⋅J

SPECIAL_CHARACTERS = {
    SUPER_SCRIPT_0: '0',  # ⁰
    SUPER_SCRIPT_1: '1',  # ¹
    SUPER_SCRIPT_2: '2',  # ²
    SUPER_SCRIPT_3: '3',  # ³
    SUPER_SCRIPT_4: '4',  # ⁴
    SUPER_SCRIPT_5: '5',  # ⁵
    SUPER_SCRIPT_6: '6',  # ⁶
    SUPER_SCRIPT_7: '7',  # ⁷
    SUPER_SCRIPT_8: '8',  # ⁸
    SUPER_SCRIPT_9: '9',  # ⁹
    SUPER_SCRIPT_DECIMAL: '.',  # ·
    SUPER_SCRIPT_MINUS: '-'  # ⁻
}

SPECIAL_CHARACTERS_REVERSE = {v: k for k, v in SPECIAL_CHARACTERS.items()}


def convert(value, from_unit, to_unit, precision=10):
    '''
    Unit converter
    
    :param value: value to be converted
    :type value: int, float
    :param from_unit: unit the passed value is
    :type from_unit: str, bytes
    :param to_unit: unit to convert passed value to
    :type to_unit: str, bytes

    :return: value converted to new unit
    :rtype: float
    '''
    try:
        from_unit = from_unit.decode('utf-8')
    except AttributeError:
        pass

    try:
        to_unit = to_unit.decode('utf-8')
    except AttributeError:
        pass

    v = decimal.Decimal(str(value))

    factor = _get_conversion_factor(from_unit, to_unit)
    val = float(v * factor)
    if isinstance(value, float):
        val = round(val, precision)
    else:
        val = int(round(val))
    return val


# The function temperature_conversion returns the converted
# temperature 'temp' 'from' one unit 'to' another
def temperature_conversion(temp, from_unit, to_unit):
    if from_unit == '°K':
        temp_si = temp
    elif from_unit == '°R':
        temp_si = temp / 1.8
    elif from_unit == '°C':
        temp_si = _number(temp) + 273.15
    elif from_unit == '°F':
        temp_si = (_number(temp) + 459.67) / 1.8
    else:
        raise TypeError(
            '{from_unit!r} is not a temperature.'.format(from_unit=from_unit)
        )

    if to_unit == '°K':
        return temp_si
    elif to_unit == '°R':
        return 1.8 * temp_si
    elif to_unit == '°C':
        return temp_si - 273.15
    elif to_unit == '°F':
        return 1.8 * temp_si - 459.67
    else:
        raise TypeError(
            '{to_unit!r} is not a temperature.'.format(to_unit=to_unit)
        )


# ----------------------PRIVATE FUNCTIONS-----------------------

_UNIT_TO_SI_EQUIVILENT = {
    'NM': 'nmi',
    'kgf': 'kg',
    'lbf': 'lb',
    'kipf': 'kip',
    'gf': 'g',
    'ozf': 'oz',
    'tf': 't',
    'lbm': 'lb',
    'AU': 'au',
    'gpm': 'gal/min',
    'cfm': 'ft³/min',
    'mmH2O': 'mmH²O',
    'inH2O': 'inH²O',
    'ci': 'in³',
    'cc': 'cm³',
    'kmh': 'km/h',
    'mph': 'mi/h',
    'psi': 'lbf/in²',
    'rad': 'm/m',
    'sr': 'm²/m²',
    'Hz': 's⁻¹',
    'N': 'kg⋅m⋅s⁻²',
    'Pa': 'N/m²',
    'J': 'N⋅m',
    'W': 'J/s',
    'C': 'A⋅s',
    'V': 'W/A',
    'F': 'C/V',
    'Ω': 'V/A',
    'S': 'A/V',
    'Wb': 'V⋅s',
    'T': 'Wb/m²',
    'H': 'Wb/A',
    'lm': 'cd⋅sr',
    'lx': 'lm/m²',
    'Bq': 's⁻¹',
    'Gy': 'J/kg',
    'Sv': 'J/kg',
    'kat': 'mol⋅s⁻¹'
}

_DECIMAL_PI = decimal.Decimal(str(math.pi))


def _get_conversion_factor(from_unit, to_unit):
    cf_from = _process_unit(from_unit)
    cf_to = _process_unit(to_unit)

    if cf_to == 0:
        return 0

    if cf_from == -1 or cf_to == -1:
        raise TypeError('units not compatible')
    if cf_from == -2 or cf_to == -2:
        raise TypeError('unit not available for conversion')

    return cf_from / cf_to


def _process_unit(unit, first_pass=True):
    unit = unit.replace(' ', MULTIPLIER)

    units = []
    brace_open = 0
    item = ''

    for char in unit:
        if char == '(':
            brace_open += 1

        elif char == ')':
            brace_open -= 1

        elif char == '/' and brace_open == 0:
            units.append(item)
            item = ''
            continue

        item += char

    if item:
        units.append(item)

    item = ''
    brace_open = 0
    marker = 1
    cfs = {}

    conversion_factor = None

    for item1 in units:
        for char in item1[:]:
            if char == '(':
                brace_open += 1

            elif char == ')':
                brace_open -= 1
                if brace_open == 0:
                    item1.replace(item + ')', 'MARKER' + str(marker))
                    cfs['MARKER' + str(marker)] = (
                        _process_unit(item[1:])
                    )
                    marker += 1
                    item = ''
                    continue

            item += char

        cf = decimal.Decimal('1.0')
        for unit in item1.split(MULTIPLIER):
            if unit in cfs:
                cf *= cfs[unit]
            elif unit in _UNIT_TO_SI_EQUIVILENT:
                unit = _UNIT_TO_SI_EQUIVILENT[unit]
                cf *= _process_unit(unit)
            else:
                cf *= _decode_unit(unit, first_pass)

        if conversion_factor is None:
            conversion_factor = cf
        else:
            conversion_factor /= cf

    return conversion_factor


def _decode_unit(unit, first_pass):
    # look for exponent written as superscript
    exponent = ''
    conversion_factor = decimal.Decimal('1.0')
    c_unit = ''
    for i, char in enumerate(unit):
        if char in SPECIAL_CHARACTERS:
            exponent += SPECIAL_CHARACTERS[char]
        else:
            c_unit += char

    if exponent == '':
        exponent = '1'

    exponent = decimal.Decimal(exponent)
    conversion_factor = _calculate_conversion_factor(
        c_unit,
        conversion_factor,
        first_pass
    )  # find conversion factor

    return decimal.Decimal(str(math.pow(conversion_factor, exponent)))


def _calculate_conversion_factor(
        unit,
        conversion_factor,
        first_pass=True
):
    # check if unit exist and if so, store the conversion factor
    if unit == '1':  # unity
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'mol':  # mole
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'cd':  # candela
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'kg':  # kilogram
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'm':  # meter
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 's':  # second
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'A':  # ampere
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == '°K':  # kelvin
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'K':  # kelvin
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == '°':  # degree = 1 / 360 rev
        conversion_factor *= _DECIMAL_PI / decimal.Decimal('180.0')
    elif unit == 'c':  # revolution = 2PI rad
        conversion_factor *= decimal.Decimal(2) * _DECIMAL_PI
    elif unit == '\'':  # arcminute = 1/60 deg
        conversion_factor *= _DECIMAL_PI / decimal.Decimal('10800.0')
    elif unit == '"':  # arcsecond = 1/60 '
        conversion_factor *= _DECIMAL_PI / decimal.Decimal('648000.0')
    elif unit == 'gon':  # grad = 1/400 rev
        conversion_factor *= _DECIMAL_PI / decimal.Decimal('200.0')
    elif unit == 'min':  # minute = 60 seconds
        conversion_factor *= decimal.Decimal('60.0')
    elif unit == 'h':  # hour = 3600 seconds
        conversion_factor *= decimal.Decimal('3600.0')
    elif unit == 'd':  # day = 86400 seconds
        conversion_factor *= decimal.Decimal('86400.0')
    elif unit == 'a':  # year = 31556952 seconds
        conversion_factor *= decimal.Decimal('31556952.0')
    elif unit == 'ft':  # feet = 0.3048 meters
        conversion_factor *= decimal.Decimal('0.3048')
    elif unit == 'yd':  # yard = 0.9144 meters
        conversion_factor *= decimal.Decimal('0.9144')
    elif unit == 'mi':  # mile = 1609344 meters
        conversion_factor *= decimal.Decimal('1609.344')
    elif unit == 'in':  # inch = 0.0254 meters
        conversion_factor *= decimal.Decimal('0.0254')
    elif unit == 'mil':  # thou = 2.54e-5 meters
        conversion_factor *= decimal.Decimal('2.54e-5')
    elif unit == 'µ':  # micron = 1.0e-6 meters
        conversion_factor *= decimal.Decimal('1.0e-6')
    elif unit == 'nmi':  # nautical mile = 1.852e3 meters
        conversion_factor *= decimal.Decimal('1.852e3')
    elif unit == 'ly':  # light-year = 9.4607304725808e15 meters
        conversion_factor *= decimal.Decimal('9.4607304725808e15')
    elif unit == 'au':  # astronomical unit = 149597871464 meters
        conversion_factor *= decimal.Decimal('149597871464.0')
    elif unit == 'p':  # point = 3.52778e-4 meters
        conversion_factor *= decimal.Decimal('3.52778e-4')
    elif unit == 'ac':  # acre = 4046.8564224²
        conversion_factor *= decimal.Decimal('4046.8564224')
    elif unit == 'ha':  # hectare = 1.0e4 m²
        conversion_factor *= decimal.Decimal('1.0e4')
    elif unit == 'lea':  # league = 4828.032 meters
        conversion_factor *= decimal.Decimal('4828.032')
    elif unit == 'fur':  # furlong = 201.16840234 meters
        conversion_factor *= decimal.Decimal('201.16840234')
    elif unit == 'ch':  # chain = 20.116840234 meters
        conversion_factor *= decimal.Decimal('20.116840234')
    elif unit == 'rd':  # rod = 5.0292100584 meters
        conversion_factor *= decimal.Decimal('5.0292100584')
    elif unit == 'fath':  # fathom = 1.8288036576 meters
        conversion_factor *= decimal.Decimal('1.8288036576')
    elif unit == 'li':  # link = 0.2011684023 meters
        conversion_factor *= decimal.Decimal('0.2011684023')
    elif unit == 'f':  # fermi = 9.999999999E-16 meters
        conversion_factor *= decimal.Decimal('9.999999999E-16')
    elif unit == 'cl':  # caliber = 2.54e-4 meters
        conversion_factor *= decimal.Decimal('2.54e-4')
    elif unit == 'pc':  # parsec = 3.08567758128e+16 meters
        conversion_factor *= decimal.Decimal('3.08567758128e16')
    elif unit == 'crin':  # circular inch = 5.067075e-3 m²
        conversion_factor *= decimal.Decimal('5.067075e-3')
    elif unit == 'crmil':  # circular thou = 5.067074790975e-10 m²
        conversion_factor *= decimal.Decimal('5.067074790975e-10')
    elif unit == 'a':  # are = 100.0 m²
        conversion_factor *= decimal.Decimal('100.0')
    elif unit == 'b':  # barn = 1.0e-28 m²
        conversion_factor *= decimal.Decimal('1.0e-28')
    elif unit in ('l', 'L'):  # liter = 1.0e-3 m³
        conversion_factor *= decimal.Decimal('1.0e-3')
    elif unit == 'gal':  # gallon US = 3.78541178e-3 m³
        conversion_factor *= decimal.Decimal('3.78541178e-3')
    elif unit == 'qt':  # quart US = 9.46352946e-4 m³
        conversion_factor *= decimal.Decimal('9.46352946e-4')
    elif unit == 'pt':  # pint US = 4.73176473e-4 m³
        conversion_factor *= decimal.Decimal('4.73176473e-4')
    elif unit == 'bbl':  # barrel US = 0.1192404712 m³
        conversion_factor *= decimal.Decimal('0.1192404712')
    elif unit == 'bblImp':  # barrel UK = 0.16365924 m³
        conversion_factor *= decimal.Decimal('0.16365924')
    elif unit == 'tsp':  # teapoon US = 5.0e-6 m³
        conversion_factor *= decimal.Decimal('5.0e-6')
    elif unit == 'tspImp':  # teapoon UK = 5.9194e-6 m³
        conversion_factor *= decimal.Decimal('5.9194e-6')
    elif unit == 'tbsp':  # tablespoon US = 1.5e-5 m³
        conversion_factor *= decimal.Decimal('1.5e-5')
    elif unit == 'tbspImp':  # tablespoon UK = 1.77582e-5 m³
        conversion_factor *= decimal.Decimal('1.77582e-5')
    elif unit == 'dstspn':  # dessertspoon US = 9.8578e-6 m³
        conversion_factor *= decimal.Decimal('9.8578e-6')
    elif unit == 'dstspnImp':  # dessertspoon UK = 1.18388e-5 m³
        conversion_factor *= decimal.Decimal('1.18388e-5')
    elif unit == 'cup':  # cup US = 2.5e-4 m³
        conversion_factor *= decimal.Decimal('2.5e-4')
    elif unit == 'cupImp':  # cup UK = 2.841306e-4 m³
        conversion_factor *= decimal.Decimal('2.841306e-4')
    elif unit == 'gi':  # gill US = 1.182941e-4 m³
        conversion_factor *= decimal.Decimal('1.182941e-4')
    elif unit == 'giImp':  # gill UK = 1.420653e-4 m³
        conversion_factor *= decimal.Decimal('1.420653e-4')
    elif unit == 'st':  # stere = 1.0 m³
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'dr':  # dram = 3.6967e-6 m³
        conversion_factor *= decimal.Decimal('3.6967e-6')
    elif unit == 'floz':  # fluid ounce US = 2.95735296875e-5 m³
        conversion_factor *= decimal.Decimal('2.95735296875e-5')
    elif unit == 'galImp':  # gallon Imp = 4.54609e-3 m³
        conversion_factor *= decimal.Decimal('4.54609e-3')
    elif unit == 'qtImp':  # quart Imp = 1.1365225e-3 m³
        conversion_factor *= decimal.Decimal('1.1365225e-3')
    elif unit == 'ptImp':  # pint Imp = 5.6826125e-4 m³
        conversion_factor *= decimal.Decimal('5.6826125e-4')
    elif unit == 'flozImp':  # fluid ounce Imp = 2.84130625e-5 m³
        conversion_factor *= decimal.Decimal('2.84130625e-5')
    elif unit == 'rpm':  # revolution per min = 0.016666666666666666 Hz
        conversion_factor *= decimal.Decimal('0.016666666666666666')
    elif unit == 'Hz':  # hertz = 1 s^-1
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'kn':  # knot = 1.852 km/h
        conversion_factor *= decimal.Decimal('1.852')
    elif unit == 'G':  # G = 9.80665 m/s²
        conversion_factor *= decimal.Decimal('9.80665')
    elif unit == 'g':  # gram = 1.0e-3 kg
        conversion_factor *= decimal.Decimal('1.0e-3')
    elif unit == 'lb':  # pound-mass = 0.45359237 kg
        conversion_factor *= decimal.Decimal('0.45359237')
    elif unit == 'kip':  # kip = 453.59237 kg
        conversion_factor *= decimal.Decimal('453.59237')
    elif unit == 'oz':  # ounce = 2.8349523125e-2 kg
        conversion_factor *= decimal.Decimal('2.8349523125e-2')
    elif unit == 'tImp':  # short ton = 907.18474 kg
        conversion_factor *= decimal.Decimal('907.18474')
    elif unit == 't':  # long ton = 1016.0469088 kg
        conversion_factor *= decimal.Decimal('1016.0469088')
    elif unit == 'tonne':  # tonne = 1.0e3 kg
        conversion_factor *= decimal.Decimal('1.0e3')
    elif unit == 'slug':  # slug = 14.5939029372 kg
        conversion_factor *= decimal.Decimal('14.5939029372')
    elif unit == 'N':  # newton = 0.10197 kg
        conversion_factor *= decimal.Decimal('0.10197')
    elif unit == 'dyn':  # dyne = 1.01971621e-6 kg
        conversion_factor *= decimal.Decimal('1.01971621e-6')
    elif unit == 'Torr':  # Torr = 13.595098063 kgf/mm²
        conversion_factor *= decimal.Decimal('13.595098063')
    elif unit == 'Btu':  # british thermal unit = 1055.056 J
        conversion_factor *= decimal.Decimal('1055.056')
    elif unit == 'cal':  # calorie = 4.1868 J
        conversion_factor *= decimal.Decimal('4.1868')
    elif unit == 'eV':  # electro-volt = 1.602176487 e-19 J
        conversion_factor *= decimal.Decimal('1.602176487e-19')
    elif unit == 'u':  # atomic mass unit = 1.660540199E-27 kg
        conversion_factor *= decimal.Decimal('1.660540199E-27')
    elif unit == 'cwt':  # quintal = 100 kg
        conversion_factor *= decimal.Decimal('100')
    elif unit == 'pwt':  # pennyweight = 1.5551738e-3 kg
        conversion_factor *= decimal.Decimal('1.5551738e-3')
    elif unit == 'gr':  # grain = 6.47989e-5 kg
        conversion_factor *= decimal.Decimal('6.47989e-5')
    elif unit == 'pdl':  # poundal = 1.40867196e-2 kg
        conversion_factor *= decimal.Decimal('1.40867196e-2')
    elif unit == 'CHU':  # celsius heat unit = 1899.1 J
        conversion_factor *= decimal.Decimal('1899.1')
    elif unit == 'W':  # watt = 1 J/s
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'hp':  # horsepower = 550 lb.ft/s
        conversion_factor *= decimal.Decimal('745.69987158227022')
    elif unit == 'PS':  # metric horsepower = 75 m.kgf/s
        conversion_factor *= decimal.Decimal('735.49875')
    elif unit == 'Pa':  # pascal = 0.1019716213 kg/m²
        conversion_factor *= decimal.Decimal('0.1019716213')
    elif unit == 'atm':  # atmosphere = 10332.274528 kg/m²
        conversion_factor *= decimal.Decimal('10332.274528')
    elif unit == 'bar':  # bar = 10197.162129779 kg/m²
        conversion_factor *= decimal.Decimal('10197.162129779')
    elif unit == 'torr':  # torr = 13.595060494664 kg/m²
        conversion_factor *= decimal.Decimal(' 13.595060494664')
    elif unit == 'ftHg':  # ft mercury = 4143.77590716 kg/m²
        conversion_factor *= decimal.Decimal('4143.77590716')
    elif unit == 'inHg':  # in mercury = 345.31465893 kg/m²
        conversion_factor *= decimal.Decimal('345.31465893')
    elif unit == 'cmHg':  # cm mercury = 135.95060495 kg/m²
        conversion_factor *= decimal.Decimal('135.95060495')
    elif unit == 'mmHg':  # mm mercury = 13.595060495 kg/m²
        conversion_factor *= decimal.Decimal('13.595060495')
    elif unit == 'ftAq':  # ft water = 304.79113663 kg/m²
        conversion_factor *= decimal.Decimal('304.79113663')
    elif unit == 'inAq':  # in water = 25.399295376 kg/m²
        conversion_factor *= decimal.Decimal('25.399295376')
    elif unit == 'cmAq':  # cm water = 9.9997246766 kg/m²
        conversion_factor *= decimal.Decimal('9.9997246766')
    elif unit == 'mmAq':  # mm water = 0.9999724677 kg/m²
        conversion_factor *= decimal.Decimal('0.9999724677')
    elif unit == '°C':  # degree celsius = 1 K
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == '°F':  # degree fahrenheit = 5/9 K
        conversion_factor /= decimal.Decimal('1.8')
    elif unit == '°R':  # rankine = 5/9 K
        conversion_factor /= decimal.Decimal('1.8')
    elif unit == 'P':  # poise = 0.1 Pa.s
        conversion_factor *= decimal.Decimal('0.1')
    elif unit == 'St':  # stoke = 1.0e-4 m²/s
        conversion_factor *= decimal.Decimal('1.0e-4')
    elif unit == 'Mx':  # maxwell = 1.0e-8 Wb
        conversion_factor *= decimal.Decimal('1.0e-8')
    else:  # unit doesn't exist
        if first_pass is True:
            # if this first pass check prefix and recheck new unit (second pass)
            unit, conversion_factor = _parse_unit_prefix(
                unit,
                conversion_factor
            )
            conversion_factor = _calculate_conversion_factor(
                unit,
                conversion_factor,
                False
            )

        elif first_pass is False:
            conversion_factor *= _process_unit(unit, first_pass=None)

        else:
            # prefix has been removed --> still not a unit
            raise TypeError('{0!r} is not a defined unit.'.format(unit))

    return conversion_factor


# determines the conversion factor for the prefix of a unit
def _parse_unit_prefix(unit, conversion_factor):
    # check if prefix exist and if so, get conversion factor
    mapping = {
        'Y': 1.0e24,  # yotta
        'Z': 1.0e21,  # zetta
        'E': 1.0e18,  # exa
        'P': 1.0e15,  # peta
        'T': 1.0e12,  # tera
        'G': 1.0e9,  # giga
        'M': 1.0e6,  # mega
        'k': 1.0e3,  # kilo
        'h': 1.0e2,  # hecto
        'da': 10.0,  # deka
        'd': 0.1,  # deci
        'c': 1.0e-2,  # centi
        'm': 1.0e-3,  # milli
        'µ': 1.0e-6,  # micro
        'n': 1.0e-9,  # nano
        'p': 1.0e-12,  # pico
        'f': 1.0e-15,  # femto
        'a': 1.0e-18,  # atto
        'z': 1.0e-21,  # zepto
        'y': 1.0e-24  # yocto
    }

    if len(unit) > 1:
        for key, value in mapping.items():
            if unit.startswith(key):
                unit = unit.replace(key, '', 1)
                conversion_factor *= decimal.Decimal(str(value))
                break

    return unit, conversion_factor


# converts string int or float to an int or a float
def _number(val):
    if isinstance(val, (int, float)):
        return val

    try:
        if b'.' in val:
            val = float(val)
        else:
            val = int(val)

        return val
    except TypeError:
        try:
            if '.' in val:
                val = float(val)
            else:
                val = int(val)

            return val
        except TypeError:
            pass


write = None


def main():
    import time

    test_units = (
        (75, 'in³', 'mm³'),
        (129.5674, 'in²', 'mm²'),
        (3.657, 'gal', 'l'),
        (500.679, 'g', 'lb'),
        (75.1, '°F', '°K'),
        (132.7, 'mi/h', 'µm/h'),
        (50.34, 'P', 'Pa s')
    )

    length_units = [
        'm',
        'km',
        'dm',
        'cm',
        'mm',
        'µm',
        'mi',
        'yd',
        'ft',
        'in',
        'ly',
        'Em',
        'Pm',
        'Tm',
        'Gm',
        'Mm',
        'hm',
        'dam',
        'µ',
        'pm',
        'fm',
        'am',
        'Mpc',
        'kpc',
        'pc',
        'au',
        'nmi',
        'kyd',
        'lea',
        'fur',
        'ch',
        'rd',
        'fath',
        'li',
        'f',
        'cl',
        'mil',
        'cin',
    ]

    volume_units = [
        'm³',
        'km³',
        'cm³',
        'mm³',
        'l',
        'mL',
        'gal',
        'qt',
        'pt',
        'mi³',
        'yd³',
        'ft³',
        'in³',
        'dm³',
        'EL',
        'PL',
        'TL',
        'GL',
        'ML',
        'kL',
        'hL',
        'daL',
        'dL',
        'cL',
        'µL',
        'nL',
        'pL',
        'fL',
        'aL',
        'bbl',
        'bblImp',
        'tsp',
        'tspImp',
        'tbsp',
        'tbspImp',
        'dstspn',
        'dstspnImp',
        'cup',
        'cupImp',
        'galImp',
        'qtImp',
        'ptImp',
        'floz',
        'flozImp',
        'gi',
        'giImp',
        'ac ft',
        'ac in',
        'st',
        'cd',
        'dr',
    ]
    
    area_units = [
        'm²',
        'km²',
        'cm²',
        'mm²',
        'µm²',
        'ha',
        'ac',
        'mi²',
        'yd²',
        'ft²',
        'ft²',
        'in²',
        'hm²',
        'dam²',
        'dm²',
        'nm²',
        'a',
        'b',
        'ch²',
        'mil²',
        'crin',
        'crmil',
    ]
    
    energy_units = [
        'J',
        'kJ',
        'kW h',
        'W h',
        'hp',
        'Btu',
        'GJ',
        'MJ',
        'mJ',
        'µJ',
        'nJ',
        'aJ',
        'MeV',
        'keV',
        'eV',
        'GW h',
        'MW h',
        'kW h',
        'W s',
        'N m',
        'hp h',
        'MBtu',
        'dyn cm',
        'gf m',
        'gf cm',
        'kgf cm',
        'kgf m',
        'kp m',
        'lbf ft',
        'lbf in',
        'ozf in',
        'ft lbf',
        'in lbf',
        'in ozf',
        'pdl ft',
    ]

    force_units = [
        'N',
        'kN',
        'gf',
        'kgf',
        'tf',
        'EN',
        'PN',
        'TN',
        'GN',
        'MN',
        'hN',
        'daN',
        'dN',
        'cN',
        'mN',
        'µN',
        'nN',
        'pN',
        'fN',
        'aN',
        'dyn',
        'J/m',
        'J/cm',
        'kipf',
        'klbf',
        'lbf',
        'ozf',
        'pdl',
        'p',
    ]

    speed_units = [
        'm/s',
        'km/h',
        'mi/h',
        'm/h',
        'm/min',
        'km/min',
        'km/s',
        'cm/h',
        'cm/min',
        'cm/s',
        'mm/h',
        'mm/min',
        'mm/s',
        'ft/h',
        'ft/min',
        'ft/s',
        'yd/h',
        'yd/min',
        'yd/s',
        'mi/min',
        'mi/s',
        'kn',
    ]

    fuel_consumption_units = [
        'm/L',
        'Em/L',
        'Pm/L',
        'Tm/L',
        'Gm/L',
        'Mm/L',
        'km/L',
        'hm/L',
        'dam/L',
        'cm/L',
        'mi/L',
        'nmi/L',
        'nmi/gal',
        'km/gal',
        'm/gal',
        'm/galImp',
        'mi/gal',
        'mi/galImp',
        'm/m³',
        'm/cm³',
        'm/yd³',
        'm/ft³',
        'm/in³',
        'm/qt',
        'm/qtImp',
        'm/pt',
        'm/ptImp',
        'm/floz',
        'm/flozImp',
        'L/m',
        'gal/mi',
        'galImp/mi',
    ]
    
    mass_units = [
        'kg',
        'g',
        'mg',
        'lb',
        'oz',
        'ct',
        'tImp',
        't',
        'tonne',
        'u',
        'Eg',
        'Pg',
        'Tg',
        'Gg',
        'Mg',
        'hG',
        'dag',
        'dg',
        'cg',
        'µg',
        'ng',
        'pg',
        'fg',
        'ag',
        'klb',
        'kip',
        'slug',
        'kgf s²/m',
        'lbf s²/ft',
        'pdl',
        'kt',
        'cwt',
        'pwt',
        'gr',
    ]

    temp_units = [
        '°K',
        '°F',
        '°C',
        '°R',
    ]

    pressure_units = [
        'Ps',
        'kPa',
        'bar',
        'psi',
        # 'ksi',  # ksi
        'atm',
        'EPa',
        'PPa',
        'TPa',
        'GPa',
        'MPa',
        'hPa',
        'daPa',
        'dPa',
        'cPa',
        'mPa',
        'µPa',
        'nPa',
        'fPa',
        'aPa',
        'N/m²',
        'N/cm²',
        'N/mm²',
        'kN/m²',
        'mbar',
        'µbar',
        'dyn/cm²',
        'kgf/m²',
        'kgf/cm²',
        'kgf/mm²',
        'gf/cm²',
        'tImp/in²',
        'tImp/ft²',
        't/in²',
        't/ft²',
        'kipf/in²',
        'lbf/ft²',
        'lbf/in²',
        'pdl/ft²',
        'Torr',
        'cmHg',
        'mmHg',
        'inHg',
        'ftHg',
        'cmAq',
        'mmAq',
        'inAq',
        'ftAq',
    ]
    
    power_units = [
        'W',
        'EW',
        'PW',
        'TW',
        'GW',
        'MW',
        'kW',
        'hW',
        'daW',
        'dW',
        'cW',
        'mW',
        'µW',
        'nW',
        'pW',
        'fW',
        'aW',
        'hp',
        'Btu/h',
        'Btu/min',
        'Btu/s',
        'MBtu/h',
        'lbf/h',
        'lbf/min',
        'lbf/s',
        'lbf ft/h',
        'lbf ft/min',
        'lbf ft/s',
        'kV A',
        'V A',
        'N m/s',
        'J/s',
        'EJ/s',
        'PJ/s',
        'TJ/s',
        'GJ/s',
        'MJ/s',
        'kJ/s',
        'hJ/s',
        'daJ/s',
        'dJ/s',
        'cJ/s',
        'mJ/s',
        'µJ/s',
        'nJ/s',
        'pJ/s',
        'fJ/s',
        'aJ/s',
        'J/h',
        'J/min',
        'kJ/H',
        'kJ/min',
    ]
    
    time_units = [
        's',
        'ms',
        'min',
        'h',
        'd',
        'a',
        'µs',
        'ns',
        'ps',
        'fs',
        'as',
    ]

    angle_units = [
        '°',
        'rad',
        "'",
        '"',
        'gon',
        'mil',
        'rpm',
    ]
    
    # log = open(r'C:\Users\Administrator\Desktop\New folder (3)\idea.log', 'wb')
    global write

    def _write(*args):
        print(*args)
        # line = ' '.join(str(arg) for arg in args)
        # log.write(line.encode('utf-8') + b'\n')

    write = _write
        
    def run_test(input_list):
        tests_run = []

        for item1 in input_list:
            for item2 in input_list:
                if item1 == item2:
                    continue

                if (item1, item2) in tests_run or (item2, item1) in tests_run:
                    continue

                tests_run.append((item2, item1))

                try:
                    v1 = convert(500.50505, item1, item2, 60)
                    write(500.505050, item1, '=', v1, item2)
                    v2 = convert(v1, item2, item1, 5)
                    write(v1, item2, '=', v2, item1)
                    write(500.505050 == v2)
                except:
                    import traceback
                    write(traceback.format_exc())

                write()
                write()

    # start = time.time()
    write('*' * 15, 'length_units', '*' * 15)
    run_test(length_units)
    write('*' * 40)
    write()

    write('*' * 15, 'volume_units', '*' * 15)
    run_test(volume_units)
    write('*' * 40)
    write()

    write('*' * 15, 'area_units', '*' * 15)
    run_test(area_units)
    write('*' * 40)
    write()

    write('*' * 15, 'energy_units', '*' * 15)
    run_test(energy_units)
    write('*' * 40)
    write()

    write('*' * 15, 'force_units', '*' * 15)
    run_test(force_units)
    write('*' * 40)
    write()

    write('*' * 15, 'speed_units', '*' * 15)
    run_test(speed_units)
    write('*' * 40)
    write()

    write('*' * 15, 'fuel_consumption_units', '*' * 15)
    run_test(fuel_consumption_units)
    write('*' * 40)
    write()

    write('*' * 15, 'mass_units', '*' * 15)
    run_test(mass_units)
    write('*' * 40)
    write()

    write('*' * 15, 'temp_units', '*' * 15)
    run_test(temp_units)
    write('*' * 40)
    write()

    write('*' * 15, 'pressure_units', '*' * 15)
    run_test(pressure_units)
    write('*' * 40)
    write()

    write('*' * 15, 'power_units', '*' * 15)
    run_test(power_units)
    write('*' * 40)
    write()

    write('*' * 15, 'time_units', '*' * 15)
    run_test(time_units)
    write('*' * 40)
    write()

    write('*' * 15, 'angle_units', '*' * 15)
    run_test(angle_units)
    write('*' * 40)
    write()

    # stop = time.time()

    # print(((stop - start) * 1000) / 1000)
    # log.close()

    # 6932 tests run in 2.106767416000366 seconds

if __name__ == '__main__':
    main()


# TODO:
# add the following units
# length: lea, ur, rd, ath, li, f,
# volume: bbl, loz, gi, st, r,
# area: b,
# energy: Btu, gf, ozf, oxf, dl
# force: gf, tf,  ipf, oxf, dl
# speed: sec,
# fuel consumption:  loz,
# mass: u, dl, wt,
# temp:
# pressure: si, pa, gf, ipf, dl, orr,
# power: Btu, erg
# time: y,
# angle:






