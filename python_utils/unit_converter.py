# -*- coding: utf-8 -*-
# This unit converter is an extended version of the SI model. It contains 
# most of the typical units a person would want to convert
# the main entry point is the 'convert' function.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import decimal
import math
from typing import Union, Optional


try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    chr = unichr
except NameError:
    # noinspection PyUnboundLocalVariable,PyShadowingBuiltins
    chr = chr


SUPER_SCRIPT_0 = chr(0x2070)  # type: str # ⁰
SUPER_SCRIPT_1 = chr(0x00B9)  # type: str # ¹
SUPER_SCRIPT_2 = chr(0x00B2)  # type: str # ²
SUPER_SCRIPT_3 = chr(0x00B3)  # type: str # ³
SUPER_SCRIPT_4 = chr(0x2074)  # type: str # ⁴
SUPER_SCRIPT_5 = chr(0x2075)  # type: str # ⁵
SUPER_SCRIPT_6 = chr(0x2076)  # type: str # ⁶
SUPER_SCRIPT_7 = chr(0x2077)  # type: str # ⁷
SUPER_SCRIPT_8 = chr(0x2078)  # type: str # ⁸
SUPER_SCRIPT_9 = chr(0x2079)  # type: str # ⁹
SUPER_SCRIPT_DECIMAL = chr(0x00B7)  # type: str # ·  (¹·²)
SUPER_SCRIPT_MINUS = chr(0x207B)  # type: str # ⁻ (⁻¹)
MULTIPLIER = chr(0x22C5)  # type: str # N⋅J

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


def convert(
        value,  # type: Union[int, float, decimal.Decimal]
        from_unit,  # type: str
        to_unit,  # type: str
):
    # type: (...) -> Union[int, float]
    # noinspection PySingleQuotedDocstring
    '''
    Unit converter (main entry point)

    General rules[cc] for writing SI units and quantities:

        * The value of a quantity is written as a number followed by a space
        (representing a multiplication sign) and a unit symbol;
        e.g., 2.21 kg, 7.3×102 m², 22 K. This rule explicitly includes the
        percent sign (%) and the symbol for degrees Celsius (°C)
        Exceptions are the symbols for plane angular degrees, minutes, and
        seconds (°, ′, and ″, respectively), which are placed immediately after
        the number with no intervening space.
        * Symbols are mathematical entities, not abbreviations, and as such do
        not have an appended period/full stop (.), unless the rules of grammar
        demand one for another reason, such as denoting the end of a sentence.
        * A prefix is part of the unit, and its symbol is prepended to a unit
        symbol without a separator (e.g., k in km, M in MPa, G in GHz, μ in μg).
        Compound prefixes are not allowed. A prefixed unit is atomic in
        expressions (e.g., km² is equivalent to (km)²).
        * Unit symbols are written using roman (upright) type, regardless of the
        type used in the surrounding text.
        * Symbols for derived units formed by multiplication are joined with a
        centre dot (⋅) or a non-breaking space; e.g., N⋅m or N m.
        * Symbols for derived units formed by division are joined with a
        solidus (/), or given as a negative exponent. E.g., the
        "metre per second" can be written m/s, m s⁻¹, m⋅s⁻¹, or m/s. A solidus
        followed without parentheses by a centre dot (or space) or a solidus is
        ambiguous and must be avoided;
        e.g., kg/(m⋅s²) and kg⋅m⁻¹⋅s⁻² are acceptable, but kg/m/s² is ambiguous
        and unacceptable.
        * In the expression of acceleration due to gravity, a space separates
        the value and the units, both the 'm' and the 's' are lowercase because
        neither the metre nor the second are named after people, and
        exponentiation is represented with a superscript '²'.
        * The first letter of symbols for units derived from the name of a
        person is written in upper case; otherwise, they are written in lower
        case. E.g., the unit of pressure is named after Blaise Pascal, so its
        symbol is written "Pa", but the symbol for mole is written "mol". Thus,
        "T" is the symbol for tesla, a measure of magnetic field strength, and
        "t" the symbol for tonne, a measure of mass. Since 1979, the litre may
        exceptionally be written using either an uppercase "L" or a lowercase
        "l", a decision prompted by the similarity of the lowercase letter "l"
        to the numeral "1", especially with certain typefaces or English-style
        handwriting. The American NIST recommends that within the United States
        "L" be used rather than "l".
        * Symbols do not have a plural form, e.g., 25 kg, but not 25 kgs.
        * Uppercase and lowercase prefixes are not interchangeable. E.g., the
        quantities 1 mW and 1 MW represent two different quantities
        (milliwatt and megawatt).
        * The symbol for the decimal marker is either a point or comma on the
        line. In practice, the decimal point is used in most English-speaking
        countries and most of Asia, and the comma in most of Latin America and
        in continental European countries.
        * Any line-break inside a compound unit should be avoided.
        * Because the value of "billion" and "trillion" varies between
        languages, the dimensionless terms "ppb" (parts per billion) and "ppt"
        (parts per trillion) should be avoided. The SI Brochure does not
        suggest alternatives.


    :param value: value to be converted
    :type value: int, float, decimal.Decimal
    :param from_unit: unit the passed value is
    :type from_unit: str, bytes
    :param to_unit: unit to convert passed value to
    :type to_unit: str, bytes

    :return: According to the SI standard the returned value should be of
    the same type as the input type and also of the same precision as the input
    type when passing a float to be converted. With Python there is no way to
    know what the precision should be if a float is passed. So to work around
    that issue the value passed can be a `decimal.Decimal` instance which
    preserves the number of trailing zeros and that is used to set the
    precision of the returned value. If you need a precision that is less then
    what gets returned you will have to handle that yourself.
    :rtype: int, float
    '''
    try:
        # noinspection PyUnresolvedReferences
        from_unit = from_unit.decode('utf-8')
    except AttributeError:
        pass

    try:
        # noinspection PyUnresolvedReferences
        to_unit = to_unit.decode('utf-8')
    except AttributeError:
        pass

    v = decimal.Decimal(str(value))
    factor = _get_conversion_factor(from_unit, to_unit)
    val = decimal.Decimal(v * factor)

    if isinstance(value, float):
        val = float(val)
    elif isinstance(value, decimal.Decimal):
        if '.' in str(value):
            precision = len(str(value).split('.')[1])
            val = round(float(val), precision)
        else:
            val = int(round(float(val)))
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


def _process_unit(
        unit, 
        first_pass=True  # type: Optional[bool]
):
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


def main():

    test_units = (
        (71, 'in³', 'mm³'),
        (129.5674, 'in²', 'mm²'),
        (3.657, 'gal', 'l'),
        (500.679, 'g', 'lb'),
        (75.1, '°F', '°K'),
        (132.7, 'mi/h', 'µm/h'),
        (50.34, 'P', 'Pa s')
    )

    for vl, t_unit, f_unit in test_units:
        v1 = convert(vl, t_unit, f_unit)
        print(
            'as ' + vl.__class__.__name__ + ':',
            vl,
            t_unit,
            '=',
            v1,
            f_unit
        )
        for i in range(2, 12, 2):

            vl2 = str(round(float(vl), i))
            vl2 += '0' * (i - len(vl2.split('.')[1]))
            vl2 = decimal.Decimal(vl2)
            v1 = convert(vl2, t_unit, f_unit)
            print(
                'presicion of {0}:'.format(i),
                vl2,
                t_unit,
                '=',
                v1,
                f_unit
            )

        print()


if __name__ == '__main__':
    main()
