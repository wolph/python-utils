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


def convert(value, from_unit, to_unit):
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

    value = decimal.Decimal(str(value))

    factor, unit = _conversion_factor(from_unit, to_unit)
    return float(value * factor), unit


# The function temperature_conversion returns the converted
# temperature 'temp' 'from' one unit 'to' another
def temperature_conversion(temp, from_unit, to_unit):
    if from_unit in ('°K', 'K'):
        temp_si = temp
    elif from_unit == 'R':
        temp_si = temp / 1.8
    elif from_unit in ('°C', 'C'):
        temp_si = _number(temp) + 273.15
    elif from_unit in ('°F', 'F'):
        temp_si = (_number(temp) + 459.67) / 1.8
    else:
        raise TypeError('{from_unit!r} does not define a temperature.'.format(
            from_unit=from_unit, to_unit=to_unit))

    if to_unit in ('°K', 'K'):
        return temp_si, '°K'
    elif to_unit == 'R':
        return 1.8 * temp_si, 'R'
    elif to_unit in ('°C', 'C'):
        return temp_si - 273.15, '°C'
    elif to_unit in ('°F', 'F'):
        return 1.8 * temp_si - 459.67, '°F'
    else:
        raise TypeError('{to_unit!r} does not define a temperature.'.format(
            from_unit=from_unit, to_unit=to_unit))


# ----------------------PRIVATE FUNCTIONS-----------------------

# CFtoSI returns the conversion factor (multiplied) from unit to SI
# CFtoSI returns 0 if unit is not defined
# CFtoSI returns -1 if unit doesn't represent the type expected
# CFtoSI returns -2 if exponent is not a number

# separator is either '.' or '/'
# exponent is either '²', '³' or '^' followed by a number
# prefix is as defined in _get_prefix
# unit is as defined in _set_conversion_factor
def _conversion_factor_to_si(unit):
    conversion_factor = decimal.Decimal('1.0')  # conversion factor
    units = _get_units(unit)  # get the array of units

    for j in range(len(units)):
        # multiply each individual conversion factors together
        sep, unit, exp, factor = _get_detailed_unit(units[j])
        if exp == 2:
            unit += '²'
        elif exp == 3:
            unit += '³'
        units[j] = unit
        conversion_factor *= _get_conversion_factor(sep, exp, factor)

    if conversion_factor is None:
        return -2  # returns -2 if an exponent was not a number

    return conversion_factor, ' '.join(units)  # return conversion factor


# The function _conversion_factor returns the conversion factor
# 'from' one unit 'to' another of the appropriate 'type'
def _conversion_factor(from_unit, to_unit):
    cf_from, _ = _conversion_factor_to_si(from_unit)
    cf_to, unit = _conversion_factor_to_si(to_unit)

    if cf_to == 0:
        return 0, unit

    if cf_from == -1 or cf_to == -1:
        raise TypeError('units not compatible')
    if cf_from == -2 or cf_to == -2:
        raise TypeError('unit not available for conversion')

    return cf_from / cf_to, unit


#  _get_units store each individual unit of the unit separately
def _get_units(unit):
    units = []  # array where the individual units are stored
    prev_index = 0  # index where the previous unit separator was

    for i in range(len(unit)):
        if unit[i] == '.':  # is it a multiplier separator?
            if unit[i + 1].isdigit():
                # if the character following the dot is a number,
                # it is an exponent (ex.: '^0.25').  So ignore it.
                break


            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                # add first unit (and add separator)
                units.append('.' + unit[prev_index:i])

            prev_index = i  # new separator index

        elif unit[i] == '/':  # is it a divider separator
            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                # add first unit (and add separator)
                units.append('.' + unit[prev_index:i])

            prev_index = i  # new separator index

    if prev_index != 0:
        units.append(unit[prev_index:])  # add last unit
    else:
        # add first and only unit (and add separator)
        units.append('.' + unit[prev_index:])

    return units  # return array


# _get_detailed_unit store the separator, the unit (with prefix),
# the exponent and the conversion factor
def _get_detailed_unit(collapseUnit):

    if collapseUnit.startswith('.sq '):
        collapseUnit = '.' + collapseUnit[4:] + '²'
    elif collapseUnit.startswith('.cu '):
        collapseUnit = '.' + collapseUnit[4:] + '³'

    separator = collapseUnit[0]
    exponent = decimal.Decimal('1.0')
    conversion_factor = decimal.Decimal('1.0')

    if collapseUnit[-1] == '²':
        exponent = decimal.Decimal('2.0')
        unit = collapseUnit[1:len(collapseUnit) - 1]  # store unit

    elif collapseUnit[-1] == '³':
        exponent = decimal.Decimal('3.0')
        unit = collapseUnit[1:len(collapseUnit) - 1]  # store unit

    else:
        index = len(collapseUnit)  # last character for unit
        if '^' in collapseUnit:  # look for exponent character
            index = collapseUnit.rfind('^')
            exponent = decimal.Decimal(str(_number(collapseUnit[index + 1:])))

        unit = collapseUnit[1:index]  # store unit

    if exponent is None:
        raise TypeError(
            collapseUnit + ' is not a valid number'
        )

    conversion_factor, unit = _set_conversion_factor(
        separator,
        unit,
        exponent,
        conversion_factor
    )  # find conversion factor

    return separator, unit, exponent, conversion_factor


#  _get_conversion_factor returns the appropriate conversion factor
#  for an individual unit of the complete unit
def _get_conversion_factor(separator, exponent, conversion_factor):
    if conversion_factor == 0:
        # return 0 if the conversion factor is unknown
        return decimal.Decimal('0.0')
    elif separator == '/':
        # return the inverse of the conversion factor if unit is divided
        return (
            decimal.Decimal('1.0') /
            decimal.Decimal(str(math.pow(conversion_factor, exponent)))
        )

    else:
        # return the conversion factor if unit is multiplied
        return decimal.Decimal(str(math.pow(conversion_factor, exponent)))


#  _set_conversion_factor determines the conversion factor for an
#  individual unit
def _set_conversion_factor(
        separator,
        unit,
        exponent,
        conversion_factor,
        first_pass=True
):
    out_unit = unit
    if not first_pass:
        # if it is the first pass, use the entire unit, else remove the prefix
        unit = unit[1:]

    # check if unit exist and if so, store the conversion factor
    if unit == '1':  # unity
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'mol':  # mole
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'cd':  # candela
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'lm':  # lumen = 1 cd.sr
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'lx':  # lux = 1 lm/m²
        conversion_factor *= 1
    elif unit == 'rad':  # radian = 1 m/m
        conversion_factor *= decimal.Decimal('1.0')
    elif unit in ('°', 'deg'):  # degree = 1 / 360 rev
        out_unit = '°'
        conversion_factor = (
                conversion_factor *
                decimal.Decimal(str(math.pi)) /
                decimal.Decimal('180.0')
        )
    elif unit == 'rev':  # revolution = 2PI rad
        conversion_factor *= decimal.Decimal('6.2831853071795860')
    elif unit == '\'':  # arcminute = 1/60 deg
        conversion_factor = (
                conversion_factor *
                decimal.Decimal(str(math.pi)) /
                decimal.Decimal('10800.0')
        )
    elif unit == '"':  # arcsecond = 1/60 '
        conversion_factor = (
                conversion_factor *
                decimal.Decimal(str(math.pi)) /
                decimal.Decimal('648000.0')
        )
    elif unit == 'gon':  # grad = 1/400 rev
        conversion_factor = (
                conversion_factor *
                decimal.Decimal(str(math.pi)) /
                decimal.Decimal('200.0')
        )
    elif unit == 'sr':  # steradian = 1 m²/m²
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 's':  # second
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'min':  # minute = 60 s
        conversion_factor *= decimal.Decimal('60.0')
    elif unit == 'h':  # hour = 60 min
        conversion_factor *= decimal.Decimal('3600.0')
    elif unit == 'd':  # day = 24 h
        conversion_factor *= decimal.Decimal('86400.0')
    elif unit == 'yr':  # year = 365.2425 d
        conversion_factor *= decimal.Decimal('31556952.0')
    elif unit == 'm':  # meter
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'ft':  # feet = 0.3048 m
        conversion_factor *= decimal.Decimal('0.3048')
    elif unit == 'yd':  # yard = 3 ft
        conversion_factor *= decimal.Decimal('0.9144')
    elif unit == 'mi':  # mile = 5280 ft
        conversion_factor *= decimal.Decimal('1609.344')
    elif unit == 'in':  # inch = 1/12 ft
        conversion_factor *= decimal.Decimal('0.0254')
    elif unit == 'mil':  # thou = 0.001 in
        conversion_factor *= decimal.Decimal('0.0000254')
    elif unit == 'µ':  # micron = 1/1000000 m
        conversion_factor *= decimal.Decimal('0.000001')
    elif unit in ('sm', 'nmi'):  # nautical mile = 1852 m
        conversion_factor *= decimal.Decimal('1852.0')
    elif unit == 'Ly':  # light-year = 9460730472580800 m
        conversion_factor *= decimal.Decimal('9460730472580800.0')
    elif unit == 'AU':  # astronomic unit = 149597871464 m
        conversion_factor *= decimal.Decimal('149597871464.0')
    elif unit == 'p':  # point = 5/133 cm
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('5.0') /
                decimal.Decimal('13300.0')
        )
    elif unit == 'ac':  # acre = = 10 ch² = 4840 yd²
        conversion_factor *= decimal.Decimal('4046.8564224')
    elif unit == 'ha':  # hectare = 10000 m²
        conversion_factor *= decimal.Decimal('10000.0')
    elif unit == 'cir in':  # circular inch = pi/4 in²
        conversion_factor *= decimal.Decimal('0.00050670747909749771297')
    elif unit == 'cir mil':  # circular thou = pi/4 mil²
        conversion_factor *= decimal.Decimal('5.0670747909749771297E-10')
    elif unit == 'cc':  # cubic centimeter = 1 cm³ = 0.000001 m³
        conversion_factor *= decimal.Decimal('0.000001')
    elif unit == 'ci':  # cubic inch = 1 in³ = (0.0254)³ m³
        conversion_factor *= decimal.Decimal('0.000016387064')
    elif unit in ('l', 'L'):  # liter = 1 dm³ = 0.001 m³
        conversion_factor *= decimal.Decimal('0.001')
    elif unit == 'gal':  # gallon US = 231 in³
        conversion_factor *= decimal.Decimal('0.003785411784')
    elif unit == 'qt':  # quart US = 0.25 gal
        conversion_factor *= decimal.Decimal('0.000946352946')
    elif unit == 'pt':  # pint US = 0.5 quart
        conversion_factor *= decimal.Decimal('0.000473176473')
    elif unit == 'fl oz':  # fluid ounce US = 1/16 pt
        conversion_factor *= decimal.Decimal('0.0000295735295625')
    elif unit == 'gal Imp':  # gallon Imp = 4.54609 l
        conversion_factor *= decimal.Decimal('0.00454609')
    elif unit == 'qt Imp':  # quart Imp = 0.25 gal UK
        conversion_factor *= decimal.Decimal('0.0011365225')
    elif unit == 'pt Imp':  # pint Imp = 0.5 quart UK
        conversion_factor *= decimal.Decimal('0.00056826125')
    elif unit == 'fl oz Imp':  # fluid ounce Imp = 1/20 pt UK
        conversion_factor *= decimal.Decimal('0.0000284130625')
    elif unit == 'rpm':  # revolution per min = 1 rev/min
        conversion_factor = (
                conversion_factor *
                decimal.Decimal(str(math.pi)) /
                decimal.Decimal('30.0')
        )
    elif unit == 'Hz':  # hertz = 1 s^-1
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'kn':  # knot = 1 sm/h
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('1852.0') /
                decimal.Decimal('3600.0')
        )
    elif unit == 'mph':  # mile per hour = 1 mi/h
        conversion_factor *= decimal.Decimal('0.44704')
    elif unit == 'G':  # G = 9.80665 m/s²
        conversion_factor *= decimal.Decimal('9.80665')
    elif unit == 'kg':  # kilogram
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'g':  # gram = 0.001 kg
        conversion_factor *= decimal.Decimal('0.001')
    elif unit in ('lb', 'lbm'):  # pound-mass = 0.45359237 kg
        conversion_factor *= decimal.Decimal('0.45359237')
    elif unit == 'kip':  # kip = 1000 lbm
        conversion_factor *= decimal.Decimal('453.59237')
    elif unit == 'oz':  # ounce = 1/16 lbm
        conversion_factor *= decimal.Decimal('0.028349523125')
    elif unit == 'sh tn':  # short ton = 2000 lbm
        conversion_factor *= decimal.Decimal('907.18474')
    elif unit == 'ton':  # long ton = 2240 lbm
        conversion_factor *= decimal.Decimal('1016.0469088')
    elif unit == 't':  # tonne = 1000 kg
        conversion_factor *= decimal.Decimal('1000.0')
    elif unit == 'slug':  # slug = 1 lb/ft.s²
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('9.80665') *
                decimal.Decimal('0.45359237') /
                decimal.Decimal('0.3048')
        )
    elif unit == 'N':  # newton = 1 m.kg/s²
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'lbf':  # pound = 9.80665 lbm
        conversion_factor *= decimal.Decimal('4.4482216152605')
    elif unit == 'dyn':  # dyne = 1 g.cm/s²
        conversion_factor *= decimal.Decimal('0.00001')
    elif unit in ('kgf', 'kp'):  # kilogram-force = 9.80665 N
        conversion_factor *= decimal.Decimal('9.80665')
    elif unit == 'J':  # joule = 1 N.m
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'BTU':  # british thermal unit = 1055.056 J
        conversion_factor *= decimal.Decimal('1055.056')
    elif unit == 'cal':  # calorie = 4.1868 J
        conversion_factor *= decimal.Decimal('4.1868')
    elif unit == 'eV':  # electro-volt = 1.602176487 e-19 J
        conversion_factor *= decimal.Decimal('1.602176487e-19')
    elif unit == 'CHU':  # celsius heat unit = 1899.1 J
        conversion_factor *= decimal.Decimal('1899.1')
    elif unit == 'W':  # watt = 1 J/s
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'hp':  # horsepower = 550 lb.ft/s
        conversion_factor *= decimal.Decimal('745.69987158227022')
    elif unit == 'PS':  # metric horsepower = 75 m.kgf/s
        conversion_factor *= decimal.Decimal('735.49875')
    elif unit == 'Pa':  # pascal = 1 N/m²
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'atm':  # atmosphere = 101325 Pa
        conversion_factor *= decimal.Decimal('101325.0')
    elif unit == 'bar':  # bar = 100 000 Pa
        conversion_factor *= decimal.Decimal('100000.0')
    elif unit == 'psi':  # pound per squared inch = 1 lb/in²
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('9.80665') *
                decimal.Decimal('0.45359237') /
                decimal.Decimal(str(
                    math.pow(
                        decimal.Decimal('0.3048') / decimal.Decimal('12.0'),
                        decimal.Decimal('2.0')
                    )
                ))
        )
    elif unit == 'torr':  # torr = 1 mmHg
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('101325.0') /
                decimal.Decimal('760.0')
        )
    elif unit == 'mmHg':  # millimeter of mercury = 101325 / 760 Pa
        conversion_factor = (
                conversion_factor *
                decimal.Decimal('101325.0') /
                decimal.Decimal('760.0')
        )
    elif unit in ('mmH2O', 'mmH²O'):  # mmH2O = 0.999972 * 9.80665 Pa
        out_unit = 'mmH²O'
        conversion_factor *= decimal.Decimal('9.8063754138')
    elif unit == 'inHg':  # inch of mercury = 25.4 mmHg
        conversion_factor = (
            conversion_factor *
            decimal.Decimal('25.4') *
            decimal.Decimal('101325.0') /
            decimal.Decimal('760.0')
        )
    elif unit in ('inH2O', 'inH²O'):  # inch of water = 25.4 mmH2O
        out_unit = 'inH²O'
        conversion_factor *= decimal.Decimal('249.08193551052')
    elif unit in ('K', '°K'):  # kelvin
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = '°K'
    elif unit in ('C', '°C'):  # degree celsius = 1 K
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = '°C'
    elif unit in ('F', '°F'):  # degree fahrenheit = 5/9 K
        conversion_factor /= decimal.Decimal('1.8')
        out_unit = '°F'
    elif unit == 'R':  # rankine = 5/9 K
        conversion_factor /= decimal.Decimal('1.8')
    elif unit == 'cfm':  # cubic feet per minute = 1 ft³/min
        conversion_factor *= decimal.Decimal('0.0004719474432')
    elif unit == 'gpm':  # gal US per min = 1 gal/min
        conversion_factor *= decimal.Decimal('0.0000630901964')
    elif unit == 'amp':  # ampere
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = 'A'
    elif unit == 'coulomb':  # coulomb = 1 A.s
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = 'C'
    elif unit == 'volt':  # volt = 1 W/A
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = 'V'
    elif unit == 'farad':  # farad = 1 C/V
        conversion_factor *= decimal.Decimal('1.0')
        out_unit = 'F'
    elif unit == 'ohm':  # ohm = 1 V/A
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'S':  # siemen = 1 A/V
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'P':  # poise = 0.1 Pa.s
        conversion_factor *= decimal.Decimal('0.1')
    elif unit == 'St':  # stoke = 0.0001 m²/s
        conversion_factor *= decimal.Decimal('0.0001')
    elif unit == 'H':  # henry = 1 V.s/A
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'T':  # tesla = 1 Wb/m²
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'Wb':  # weber = 1 V.s
        conversion_factor *= decimal.Decimal('1.0')
    elif unit == 'Mx':  # maxwell = 0.00000001 Wb
        conversion_factor *= decimal.Decimal('0.00000001')
    else:  # unit doesn't exist
        if first_pass:
            conversion_factor = _get_unit_prefix(unit, conversion_factor)
            # if this first pass check prefix and recheck new unit (second pass)
            conversion_factor, out_unit = _set_conversion_factor(
                separator,
                unit,
                exponent,
                conversion_factor,
                False
            )
        else:
            # prefix has been removed --> still not a unit
            raise TypeError('{0!r} is not a defined unit.'.format(unit))

    return conversion_factor, out_unit


# getPrefix determines the conversion factor for the prefix of a unit
def _get_unit_prefix(unit, conversion_factor):
    # check if prefix (first character of unit)
    # exist and if so, get conversion factor
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
    if unit[0] in mapping:
        conversion_factor *= decimal.Decimal(str(mapping[unit[0]]))
    else:  # prefix doesn't exist
        raise TypeError(
            'In the unit {0!r}, {1!r} is not a defined prefix.'.format(
                unit,
                unit[0]
            )
        )

    return conversion_factor


# converts string int or float to an int or a float
def _number(val):
    if isinstance(val, (int, float)):
        return val

    try:
        if b'.' in val:
            val = float(val)

        else:
            val = int(val)

    except TypeError:
        if '.' in val:
            val = float(val)
        else:
            val = int(val)

    return val


def main():
    test_units = (
        ('cu in', 'cu mm'),
        ('in³', 'mm³'),
        ('sq in', 'sq mm'),
        ('in²', 'mm²'),
        ('gal', 'l'),
        ('g', 'lb'),
        ('K', 'C'),
    )
    for f_unit, t_unit in test_units:
        v1, unt = convert(1.0, f_unit, t_unit)
        print(1.0, f_unit, '=', v1, t_unit, '(' + unt + ')')

        v2, unt = convert(v1, t_unit, f_unit)
        print(v1, t_unit, '=', v2, f_unit, '(' + unt + ')')

        print()


if __name__ == '__main__':
    main()
