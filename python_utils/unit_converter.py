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

SEPARATOR = 0  # see _get_detailed_unit
UNIT = 1  # see _get_detailed_unit
EXPONENT = 2  # see _get_detailed_unit
CF = 3  # see _get_detailed_unit


# This is a wrapper class for the unit type constants. There are
# a couple of added items that are there for sanity checks and for 
# labeling exceptions

class _IntWrapper(int):
    _values = []

    @property
    def label(self):
        return self.__class__.__name__.replace('_', '').lower()

    def __getitem__(self, item):
        return self._values[item]

    @property
    def values(self):
        return self._values[:]


# unit type classes, these classes get replaced by instances
class _LENGTH(_IntWrapper):
    '''
    meter : m
    feet : ft
    yard : yd
    mile : mi
    inch : in
    thou : mil
    micron : µ
    nauticle mile : sm, nmi
    light-year : Ly
    astronomic unit : AU
    point : p
    '''
    _values = [1, 0, 0, 0, 0, 0, 0]


class _MASS(_IntWrapper):
    '''
    kilogram : kg
    gram : g
    pound : lb, lbm
    kip : kip
    ounce : oz
    short ton : sh tn
    long ton : ton
    tonne : t
    slug : slug
    '''
    _values = [0, 1, 0, 0, 0, 0, 0]


class _TIME(_IntWrapper):
    '''
    second : s
    minute : min
    hour : h
    day : d
    year : yr
    '''
    _values = [0, 0, 1, 0, 0, 0, 0]


class _CURRENT(_IntWrapper):
    '''
    ampere : A
    '''
    _values = [0, 0, 0, 1, 0, 0, 0]


class _TEMPERATURE(_IntWrapper):
    '''
    kelvin : K
    degree celsius : °C
    degree fahrenheit : °F
    rankine : R
    '''
    _values = [0, 0, 0, 0, 1, 0, 0]


class _QUANTITY(_IntWrapper):
    '''
    mole : mol
    '''
    _values = [0, 0, 0, 0, 0, 1, 0]


class _LUMINOSITY(_IntWrapper):
    '''
    candela : cd
    lumen : lm
    '''
    _values = [0, 0, 0, 0, 0, 0, 1]


class _ANGLE(_IntWrapper):
    _values = [0, 0, 0, 0, 0, 0, 0]


class _AREA(_IntWrapper):
    '''
    acre : ac
    hectare : ha
    circular inch : cir in
    circular thou : cir mil
    '''
    _values = [2, 0, 0, 0, 0, 0, 0]


class _VOLUME(_IntWrapper):
    '''
    cubic centimeter : cc
    cubic inch : ci
        ,  : l
    gallon US : gal
    quart US : qt
    pint US : pt
    fluid ounce US : fl oz
    gallon Imp : gal Imp
    quart Imp : qt Imp
    pint Imp : pt Imp
    fluid ounce Imp : fl oz Imp
    '''
    _values = [3, 0, 0, 0, 0, 0, 0]


class _FREQUENCY(_IntWrapper):
    '''
    revolution per min : rpm
    hertz : Hz
    '''
    _values = [0, 0, -1, 0, 0, 0, 0]


class _SPEED(_IntWrapper):
    '''
    knot : kn
    mile per hour : mph
    '''
    _values = [1, 0, -1, 0, 0, 0, 0]


class _ACCELERATION(_IntWrapper):
    '''
    G-force : G
    '''
    _values = [1, 0, -2, 0, 0, 0, 0]


class _FORCE(_IntWrapper):
    '''
    newton : N
    pound : lbf
    dyne : dyn
    kilogram-force : kgf, kp
    '''
    _values = [1, 1, -2, 0, 0, 0, 0]


class _ENERGY(_IntWrapper):
    '''
    joule : J
    british thermal unit : BTU
    calorie : cal
    electro-volt : eV
    celsius heat unit : CHU
    '''
    _values = [2, 1, -2, 0, 0, 0, 0]


class _POWER(_IntWrapper):
    '''
    watt : W
    horsepower : hp
    metric horsepower : PS
    '''
    _values = [2, 1, -3, 0, 0, 0, 0]


class _PRESSURE(_IntWrapper):
    '''
    pascal : Pa
    atmosphere : atm
    bar : bar
    pound per squared inch : psi
    torr : torr
    millimeter of mercury : mmHg
    millimeter of water : mmH2O, mmH²O
    inch of water : inH2O, inH²O
    inch of mercury : inHg
    '''
    _values = [-1, 1, -2, 0, 0, 0, 0]


class _VOLUMETRIC_FLOW(_IntWrapper):
    '''
    cubic feet per minute : cfm
    gal US per min : gpm
    '''
    _values = [3, 0, -1, 0, 0, 0, 0]


class _CHARGE(_IntWrapper):
    '''
    coulomb : C
    '''
    _values = [0, 0, 1, 1, 0, 0, 0]


class _VOLTAGE(_IntWrapper):
    '''
    volt : V
    '''
    _values = [2, 1, -3, -1, 0, 0, 0]


class _CAPACITANCE(_IntWrapper):
    '''
    farad : F
    '''
    _values = [-2, -1, 4, 2, 0, 0, 0]


class _RESISTANCE(_IntWrapper):
    '''
    ohm : ohm, Ω
    '''
    _values = [2, 1, -3, -2, 0, 0, 0]


class _CONDUCTIVITY(_IntWrapper):
    '''
    siemen : S
    '''
    _values = [-2, -1, 3, 2, 0, 0, 0]


class _VISCOSITY(_IntWrapper):
    '''
    poise : P
    '''
    _values = [-1, 1, -1, 0, 0, 0, 0]


class _MAGNETIC_FLUX(_IntWrapper):
    '''
    weber : Wb
    maxwell : Mx
    '''
    _values = [2, 1, -2, -1, 0, 0, 0]


class _INDUCTANCE(_IntWrapper):
    '''
    henry : H
    '''
    _values = [2, 1, -2, -2, 0, 0, 0]


class _MAGNETIC_INDUCTION(_IntWrapper):
    '''
    tesla : T
    '''
    _values = [0, 1, -2, -1, 0, 0, 0]


class ENGINE_FUEL_CONSUMPTION(_IntWrapper):
    _values = [-2, 0, 2, 0, 0, 0, 0]


class _DENSITY(_IntWrapper):
    _values = [-3, 1, 0, 0, 0, 0, 0]


class _TORQUE(_IntWrapper):
    _values = [2, 1, -2, 0, 0, 0, 0]


# unit type constants
# these constants get passed to the 'convert' function
_LENGTH = _LENGTH(0)
_MASS = _MASS(1)
_TIME = _TIME(2)
_CURRENT = _CURRENT(3)
_TEMPERATURE = _TEMPERATURE(4)
_QUANTITY = _QUANTITY(5)
_LUMINOSITY = _LUMINOSITY(6)
_ANGLE = _ANGLE(7)
_AREA = _AREA(8)
_VOLUME = _VOLUME(9)
_FREQUENCY = _FREQUENCY(10)
_SPEED = _SPEED(11)
_ACCELERATION = _ACCELERATION(12)
_FORCE = _FORCE(13)
_ENERGY = _ENERGY(14)
_POWER = _POWER(15)
_PRESSURE = _PRESSURE(16)
_VOLUMETRIC_FLOW = _VOLUMETRIC_FLOW(17)
_CHARGE = _CHARGE(18)
_VOLTAGE = _VOLTAGE(19)
_CAPACITANCE = _CAPACITANCE(20)
_RESISTANCE = _RESISTANCE(21)
_CONDUCTIVITY = _CONDUCTIVITY(22)
_VISCOSITY = _VISCOSITY(23)
_MAGNETIC_FLUX = _MAGNETIC_FLUX(24)
_INDUCTANCE = _INDUCTANCE(25)
_MAGNETIC_INDUCTION = _MAGNETIC_INDUCTION(26)
ENGINE_FUEL_CONSUMPTION = ENGINE_FUEL_CONSUMPTION(27)
_DENSITY = _DENSITY(28)
_TORQUE = _TORQUE(29)


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

    import decimal

    value = decimal.Decimal(str(value))

    factor = _conversion_factor(from_unit, to_unit)
    return float(value * factor)


# The function temperature_conversion returns the converted temperature 'temp' 'from' one unit 'to' another
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
        return temp_si
    elif to_unit == 'R':
        return 1.8 * temp_si
    elif to_unit in ('°C', 'C'):
        return temp_si - 273.15
    elif to_unit in ('°F', 'F'):
        return 1.8 * temp_si - 459.67
    else:
        raise TypeError('{to_unit!r} does not define a temperature.'.format(
            from_unit=from_unit, to_unit=to_unit))


# ----------------------PRIVATE FUNCTIONS-----------------------

# CFtoSI returns the conversion factor (multiplied) from unit to SI
# CFtoSI returns 0 if unit is not defined
# CFtoSI returns -1 if unit doesn't represent the type expected
# CFtoSI returns -2 if exponent is not a number

# unit is written this way:  [prefix1] unit1 [exponent1] {[separator2] [prefix2] unit2 [exponent2] ...}
# separator is either '.' or '/'
# exponent is either '²', '³' or '^' followed by a number
# prefix is as defined in _get_prefix
# unit is as defined in _set_conversion_factor
def _conversion_factor_to_si(
        unit):  # unit as string, type as integer (see definitions above)
    factor = decimal.Decimal('1.0')  # conversion factor
    unit_type = [0] * 7

    units = _get_units(unit)  # get the array of units

    for j in range(len(units)):
        # multiply each individual conversion factors together
        factor *= _get_conversion_factor(
            _get_detailed_unit(units[j], unit_type))
    if factor is None:
        return -2  # returns -2 if an exponent was not a number

    # if factor > 0:  # unit is not an error
    #     # check if unit is of the type expected (returns -1 if it doesn't agree with 'type'):
    # 
    #     if type_.values != unit_type:
    #         print(unit_type)
    #         raise TypeError(''{0}' does not define a type of {1}'.format(unit, type_.label))

    return factor  # return conversion factor


# The function _conversion_factor returns the conversion factor 'from' one unit 'to' another of the appropriate 'type'
def _conversion_factor(from_unit, to_unit):
    cf_from = _conversion_factor_to_si(from_unit)
    cf_to = _conversion_factor_to_si(to_unit)

    if cf_to == 0:
        return 0

    if cf_from == -1 or cf_to == -1:
        raise TypeError('units not compatible')
    if cf_from == -2 or cf_to == -2:
        raise TypeError('unit not available for conversion')

    return cf_from / cf_to


#  _get_units store each individual unit of the unit separately
def _get_units(unit):
    units = []  # array where the individual units are stored
    prev_index = 0  # index where the previous unit separator was

    for i in range(len(unit)):
        if unit[i] == '.':  # is it a multiplier separator?
            if unit[i + 1].isdigit():
                break
                # if the character following the dot is a number, it is an exponent (ex.: '^0.25').  So ignore it.

            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                units.append('.' + unit[
                                   prev_index:i])  # add first unit (and add separator)*/

            prev_index = i  # new separator index

        elif unit[i] == '/':  # is it a divider separator
            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                units.append('.' + unit[
                                   prev_index:i])  # add first unit (and add separator)

            prev_index = i  # new separator index

    if prev_index != 0:
        units.append(unit[prev_index:])  # add last unit
    else:
        units.append('.' + unit[
                           prev_index:])  # add first and only unit (and add separator)

    return units  # return array


# _get_detailed_unit store the separator, the unit (with prefix), the exponent and the conversion factor
# separately in an array

def _get_detailed_unit(collapseUnit, unit_type):
    detailed_unit = [collapseUnit[0], None, decimal.Decimal('1.0'),
                     decimal.Decimal('1.0')]  # array to store data
    if collapseUnit[-1] == '²':
        detailed_unit[EXPONENT] = decimal.Decimal('2.0')
        detailed_unit[UNIT] = collapseUnit[
                              1:len(collapseUnit) - 1]  # store unit

    elif collapseUnit.startswith('.sq '):
        detailed_unit[EXPONENT] = decimal.Decimal('2')
        detailed_unit[UNIT] = collapseUnit[4:]  # store unit

    elif collapseUnit[-1] == '³':
        detailed_unit[EXPONENT] = decimal.Decimal('3')
        detailed_unit[UNIT] = collapseUnit[
                              1:len(collapseUnit) - 1]  # store unit

    elif collapseUnit.startswith('.cu '):
        detailed_unit[EXPONENT] = decimal.Decimal('3')
        detailed_unit[UNIT] = collapseUnit[4:]  # store unit

    else:
        index = len(collapseUnit)  # last character for unit

        for i in range(len(collapseUnit)):
            if collapseUnit[i] == '^':  # look for exponent character
                index = i  # new index
                detailed_unit[EXPONENT] = decimal.Decimal(
                    str(_number(collapseUnit[i + 1:])))
                # convert exponent from string to number and store it

        detailed_unit[UNIT] = collapseUnit[1:index]  # store unit

    if detailed_unit[EXPONENT] is None:
        raise TypeError(
            collapseUnit + ' is not a valid number'
        )

    _set_conversion_factor(detailed_unit, unit_type)  # find conversion factor

    return detailed_unit  # return array


#  _get_conversion_factor returns the appropriate conversion factor for an individual unit of the complete unit
def _get_conversion_factor(detailed_unit):
    if detailed_unit[CF] == 0:
        return decimal.Decimal(
            '0.0')  # return 0 if the conversion factor is unknown
    elif detailed_unit[SEPARATOR] == '/':
        return decimal.Decimal('1.0') / decimal.Decimal(
            str(math.pow(detailed_unit[CF], detailed_unit[EXPONENT])))
        # return the inverse of the conversion factor if unit is divided
    else:
        # return the conversion factor if unit is multiplied
        return decimal.Decimal(
            str(math.pow(detailed_unit[CF], detailed_unit[EXPONENT])))


#  _set_conversion_factor determines the conversion factor for an individual unit
def _set_conversion_factor(detailed_unit, unit_type, first_pass=True):
    if first_pass:
        unit = detailed_unit[UNIT]
    else:
        unit = detailed_unit[UNIT][
               1:]  # if it is the first pass, use the entire unit, else remove the prefix

    # check if unit exist and if so, store the conversion factor
    if unit == '1':  # unity
        detailed_unit[CF] *= decimal.Decimal('1.0')
    elif unit == 'mol':  # mole
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _QUANTITY)

    elif unit == 'cd':  # candela
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _LUMINOSITY)
    elif unit == 'lm':  # lumen = 1 cd.sr
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _LUMINOSITY)
    elif unit == 'lx':  # lux = 1 lm/m²
        cls = _IntWrapper(0)
        cls._values = [-2, 0, 0, 0, 0, 0, 1]
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, cls)

    elif unit == 'rad':  # radian = 1 m/m
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit in ('°', 'deg'):  # degree = 1 / 360 rev
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            str(math.pi)) / decimal.Decimal('180.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit == 'rev':  # revolution = 2PI rad
        detailed_unit[CF] *= decimal.Decimal('6.2831853071795860')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit == ''':  # arcminute = 1/60 deg
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(str(math.pi)) / decimal.Decimal('10800.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit == ''':  # arcsecond = 1/60 '
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            str(math.pi)) / decimal.Decimal('648000.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit == 'gon':  # grad = 1/400 rev
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            str(math.pi)) / decimal.Decimal('200.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)
    elif unit == 'sr':  # steradian = 1 m²/m²
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _ANGLE)

    elif unit == 's':  # second
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _TIME)
    elif unit == 'min':  # minute = 60 s
        detailed_unit[CF] *= decimal.Decimal('60.0')
        _set_unit_type(detailed_unit, unit_type, _TIME)
    elif unit == 'h':  # hour = 60 min
        detailed_unit[CF] *= decimal.Decimal('3600.0')
        _set_unit_type(detailed_unit, unit_type, _TIME)
    elif unit == 'd':  # day = 24 h
        detailed_unit[CF] *= decimal.Decimal('86400.0')
        _set_unit_type(detailed_unit, unit_type, _TIME)
    elif unit == 'yr':  # year = 365.2425 d
        detailed_unit[CF] *= decimal.Decimal('31556952.0')
        _set_unit_type(detailed_unit, unit_type, _TIME)

    elif unit == 'm':  # meter
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'ft':  # feet = 0.3048 m
        detailed_unit[CF] *= decimal.Decimal('0.3048')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'yd':  # yard = 3 ft
        detailed_unit[CF] *= decimal.Decimal('0.9144')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'mi':  # mile = 5280 ft
        detailed_unit[CF] *= decimal.Decimal('1609.344')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'in':  # inch = 1/12 ft
        detailed_unit[CF] *= decimal.Decimal('0.0254')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'mil':  # thou = 0.001 in
        detailed_unit[CF] *= decimal.Decimal('0.0000254')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'µ':  # micron = 1/1000000 m
        detailed_unit[CF] *= decimal.Decimal('0.000001')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit in ('sm', 'nmi'):  # nautical mile = 1852 m
        detailed_unit[CF] *= decimal.Decimal('1852.0')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'Ly':  # light-year = 9460730472580800 m
        detailed_unit[CF] *= decimal.Decimal('9460730472580800.0')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'AU':  # astronomic unit = 149597871464 m
        detailed_unit[CF] *= decimal.Decimal('149597871464.0')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)
    elif unit == 'p':  # point = 5/133 cm
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            '5.0') / decimal.Decimal('13300.0')
        _set_unit_type(detailed_unit, unit_type, _LENGTH)

    elif unit == 'ac':  # acre = = 10 ch² = 4840 yd²
        detailed_unit[CF] *= decimal.Decimal('4046.8564224')
        _set_unit_type(detailed_unit, unit_type, _AREA)
    elif unit == 'ha':  # hectare = 10000 m²
        detailed_unit[CF] *= decimal.Decimal('10000.0')
        _set_unit_type(detailed_unit, unit_type, _AREA)
    elif unit == 'cir in':  # circular inch = pi/4 in²
        detailed_unit[CF] *= decimal.Decimal('0.00050670747909749771297')
        _set_unit_type(detailed_unit, unit_type, _AREA)
    elif unit == 'cir mil':  # circular thou = pi/4 mil²
        detailed_unit[CF] *= decimal.Decimal('5.0670747909749771297E-10')
        _set_unit_type(detailed_unit, unit_type, _AREA)

    elif unit == 'cc':  # cubic centimeter = 1 cm³ = 0.000001 m³
        detailed_unit[CF] *= decimal.Decimal('0.000001')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'ci':  # cubic inch = 1 in³ = (0.0254)³ m³
        detailed_unit[CF] *= decimal.Decimal('0.000016387064')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit in ('l', 'L'):  # liter = 1 dm³ = 0.001 m³
        detailed_unit[CF] *= decimal.Decimal('0.001')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'gal':  # gallon US = 231 in³
        detailed_unit[CF] *= decimal.Decimal('0.003785411784')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'qt':  # quart US = 0.25 gal
        detailed_unit[CF] *= decimal.Decimal('0.000946352946')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'pt':  # pint US = 0.5 quart
        detailed_unit[CF] *= decimal.Decimal('0.000473176473')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'fl oz':  # fluid ounce US = 1/16 pt
        detailed_unit[CF] *= decimal.Decimal('0.0000295735295625')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'gal Imp':  # gallon Imp = 4.54609 l
        detailed_unit[CF] *= decimal.Decimal('0.00454609')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'qt Imp':  # quart Imp = 0.25 gal UK
        detailed_unit[CF] *= decimal.Decimal('0.0011365225')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'pt Imp':  # pint Imp = 0.5 quart UK
        detailed_unit[CF] *= decimal.Decimal('0.00056826125')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)
    elif unit == 'fl oz Imp':  # fluid ounce Imp = 1/20 pt UK
        detailed_unit[CF] *= decimal.Decimal('0.0000284130625')
        _set_unit_type(detailed_unit, unit_type, _VOLUME)

    elif unit == 'rpm':  # revolution per min = 1 rev/min
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            str(math.pi)) / decimal.Decimal('30.0')
        _set_unit_type(detailed_unit, unit_type, _FREQUENCY)
    elif unit == 'Hz':  # hertz = 1 s^-1
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _FREQUENCY)

    elif unit == 'kn':  # knot = 1 sm/h
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            '1852.0') / decimal.Decimal('3600.0')
        _set_unit_type(detailed_unit, unit_type, _SPEED)
    elif unit == 'mph':  # mile per hour = 1 mi/h
        detailed_unit[CF] *= decimal.Decimal('0.44704')
        _set_unit_type(detailed_unit, unit_type, _SPEED)

    elif unit == 'G':  # G = 9.80665 m/s²
        detailed_unit[CF] *= decimal.Decimal('9.80665')
        _set_unit_type(detailed_unit, unit_type, _ACCELERATION)

    elif unit == 'kg':  # kilogram
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'g':  # gram = 0.001 kg
        detailed_unit[CF] *= decimal.Decimal('0.001')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit in ('lb', 'lbm'):  # pound-mass = 0.45359237 kg
        detailed_unit[CF] *= decimal.Decimal('0.45359237')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'kip':  # kip = 1000 lbm
        detailed_unit[CF] *= decimal.Decimal('453.59237')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'oz':  # ounce = 1/16 lbm
        detailed_unit[CF] *= decimal.Decimal('0.028349523125')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'sh tn':  # short ton = 2000 lbm
        detailed_unit[CF] *= decimal.Decimal('907.18474')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'ton':  # long ton = 2240 lbm
        detailed_unit[CF] *= decimal.Decimal('1016.0469088')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 't':  # tonne = 1000 kg
        detailed_unit[CF] *= decimal.Decimal('1000.0')
        _set_unit_type(detailed_unit, unit_type, _MASS)
    elif unit == 'slug':  # slug = 1 lb/ft.s²
        detailed_unit[CF] = (
                detailed_unit[CF] *
                decimal.Decimal('9.80665') *
                decimal.Decimal('0.45359237') /
                decimal.Decimal('0.3048')
        )
        _set_unit_type(detailed_unit, unit_type, _MASS)

    elif unit == 'N':  # newton = 1 m.kg/s²
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _FORCE)
    elif unit == 'lbf':  # pound = 9.80665 lbm
        detailed_unit[CF] *= decimal.Decimal('4.4482216152605')
        _set_unit_type(detailed_unit, unit_type, _FORCE)
    elif unit == 'dyn':  # dyne = 1 g.cm/s²
        detailed_unit[CF] *= decimal.Decimal('0.00001')
        _set_unit_type(detailed_unit, unit_type, _FORCE)
    elif unit in ('kgf', 'kp'):  # kilogram-force = 9.80665 N
        detailed_unit[CF] *= decimal.Decimal('9.80665')
        _set_unit_type(detailed_unit, unit_type, _FORCE)

    elif unit == 'J':  # joule = 1 N.m
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _ENERGY)
    elif unit == 'BTU':  # british thermal unit = 1055.056 J
        detailed_unit[CF] *= decimal.Decimal('1055.056')
        _set_unit_type(detailed_unit, unit_type, _ENERGY)
    elif unit == 'cal':  # calorie = 4.1868 J
        detailed_unit[CF] *= decimal.Decimal('4.1868')
        _set_unit_type(detailed_unit, unit_type, _ENERGY)
    elif unit == 'eV':  # electro-volt = 1.602176487 e-19 J
        detailed_unit[CF] *= decimal.Decimal('1.602176487e-19')
        _set_unit_type(detailed_unit, unit_type, _ENERGY)
    elif unit == 'CHU':  # celsius heat unit = 1899.1 J
        detailed_unit[CF] *= decimal.Decimal('1899.1')
        _set_unit_type(detailed_unit, unit_type, _ENERGY)

    elif unit == 'W':  # watt = 1 J/s
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _POWER)
    elif unit == 'hp':  # horsepower = 550 lb.ft/s
        detailed_unit[CF] *= decimal.Decimal('745.69987158227022')
        _set_unit_type(detailed_unit, unit_type, _POWER)
    elif unit == 'PS':  # metric horsepower = 75 m.kgf/s
        detailed_unit[CF] *= decimal.Decimal('735.49875')
        _set_unit_type(detailed_unit, unit_type, _POWER)

    elif unit == 'Pa':  # pascal = 1 N/m²
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'atm':  # atmosphere = 101325 Pa
        detailed_unit[CF] *= decimal.Decimal('101325.0')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'bar':  # bar = 100 000 Pa
        detailed_unit[CF] *= decimal.Decimal('100000.0')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'psi':  # pound per squared inch = 1 lb/in²
        detailed_unit[CF] = (
                detailed_unit[CF] *
                decimal.Decimal('9.80665') *
                decimal.Decimal('0.45359237') /
                decimal.Decimal(str(math.pow(
                    decimal.Decimal('0.3048') / decimal.Decimal('12.0'),
                    decimal.Decimal('2.0'))))
        )
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'torr':  # torr = 1 mmHg
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            '101325.0') / decimal.Decimal('760.0')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'mmHg':  # millimeter of mercury = 101325 / 760 Pa
        detailed_unit[CF] = detailed_unit[CF] * decimal.Decimal(
            '101325.0') / decimal.Decimal('760.0')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit in (
            'mmH2O', 'mmH²O'):  # millimeter of water = 0.999972 * 9.80665 Pa
        detailed_unit[CF] *= decimal.Decimal('9.8063754138')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit == 'inHg':  # inch of mercury = 25.4 mmHg
        detailed_unit[CF] = (
                detailed_unit[CF] *
                decimal.Decimal('25.4') *
                decimal.Decimal('101325.0') /
                decimal.Decimal('760.0')
        )
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)
    elif unit in ('inH2O', 'inH²O'):  # inch of water = 25.4 mmH2O
        detailed_unit[CF] *= decimal.Decimal('249.08193551052')
        _set_unit_type(detailed_unit, unit_type, _PRESSURE)

    elif unit == 'K':  # kelvin
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _TEMPERATURE)
    elif unit == '°C':  # degree celsius = 1 K
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _TEMPERATURE)
    elif unit == '°F':  # degree fahrenheit = 5/9 K
        detailed_unit[CF] /= decimal.Decimal('1.8')
        _set_unit_type(detailed_unit, unit_type, _TEMPERATURE)
    elif unit == 'R':  # rankine = 5/9 K
        detailed_unit[CF] /= decimal.Decimal('1.8')
        _set_unit_type(detailed_unit, unit_type, _TEMPERATURE)

    elif unit == 'cfm':  # cubic feet per minute = 1 ft³/min
        detailed_unit[CF] *= decimal.Decimal('0.0004719474432')
        _set_unit_type(detailed_unit, unit_type, _VOLUMETRIC_FLOW)
    elif unit == 'gpm':  # gal US per min = 1 gal/min
        detailed_unit[CF] *= decimal.Decimal('0.0000630901964')
        _set_unit_type(detailed_unit, unit_type, _VOLUMETRIC_FLOW)

    elif unit == 'A':  # ampere
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _CURRENT)

    elif unit == 'C':  # coulomb = 1 A.s
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _CHARGE)

    elif unit == 'V':  # volt = 1 W/A
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _VOLTAGE)

    elif unit == 'F':  # farad = 1 C/V
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _CAPACITANCE)

    elif unit == 'ohm':  # ohm = 1 V/A
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _RESISTANCE)

    elif unit == 'S':  # siemen = 1 A/V
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _CONDUCTIVITY)

    elif unit == 'P':  # poise = 0.1 Pa.s
        detailed_unit[CF] *= decimal.Decimal('0.1')
        _set_unit_type(detailed_unit, unit_type, _VISCOSITY)
    elif unit == 'St':  # stoke = 0.0001 m²/s
        cls = _IntWrapper(0)
        cls._values = [2, 0, -1, 0, 0, 0, 0]

        detailed_unit[CF] *= decimal.Decimal('0.0001')
        _set_unit_type(detailed_unit, unit_type, cls)

    elif unit == 'H':  # henry = 1 V.s/A
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _INDUCTANCE)

    elif unit == 'T':  # tesla = 1 Wb/m²
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _MAGNETIC_INDUCTION)

    elif unit == 'Wb':  # weber = 1 V.s
        detailed_unit[CF] *= decimal.Decimal('1.0')
        _set_unit_type(detailed_unit, unit_type, _MAGNETIC_FLUX)
    elif unit == 'Mx':  # maxwell = 0.00000001 Wb
        detailed_unit[CF] *= decimal.Decimal('0.00000001')
        _set_unit_type(detailed_unit, unit_type, _MAGNETIC_FLUX)
    else:  # unit doesn't exist
        if first_pass:
            _get_unit_prefix(detailed_unit)
            # if this first pass check prefix and recheck new unit (second pass)
            _set_conversion_factor(detailed_unit, unit_type, False)
        else:
            detailed_unit[CF] = decimal.Decimal('0.0')
            raise TypeError(
                '{0!r} is not a defined unit.'.format(detailed_unit[UNIT]))
            # prefix has been removed --> still not a unit


# getPrefix determines the conversion factor for the prefix of a unit
def _get_unit_prefix(detailed_unit):
    # check if prefix (first character of unit) exist and if so, get conversion factor
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
    if detailed_unit[UNIT][0] in mapping:
        detailed_unit[CF] *= decimal.Decimal(
            str(mapping[detailed_unit[UNIT][0]]))
    else:  # prefix doesn't exist
        detailed_unit[CF] = decimal.Decimal('0.0')
        raise TypeError(
            'In the unit {0!r}, {1!r} is not a defined prefix.'.format(
                detailed_unit[UNIT],
                detailed_unit[UNIT][0]
            )
        )


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


# _set_unit_type determines what is the combination of the unit from L, M, T, I, H, Q and LU
def _set_unit_type(detailed_unit, unit_type, const_unit_type):
    mod = 1

    if detailed_unit[SEPARATOR] == '/':
        mod = -1  # the unit is divided, so you have to substract the exponent

    # Adjust every type:
    unit_type[_LENGTH] += mod * const_unit_type[_LENGTH] * detailed_unit[
        EXPONENT]
    unit_type[_MASS] += mod * const_unit_type[_MASS] * detailed_unit[EXPONENT]
    unit_type[_TIME] += mod * const_unit_type[_TIME] * detailed_unit[EXPONENT]
    unit_type[_CURRENT] += mod * const_unit_type[_CURRENT] * detailed_unit[
        EXPONENT]
    unit_type[_TEMPERATURE] += mod * const_unit_type[_TEMPERATURE] * \
                               detailed_unit[EXPONENT]
    unit_type[_QUANTITY] += mod * const_unit_type[_QUANTITY] * detailed_unit[
        EXPONENT]
    unit_type[_LUMINOSITY] += mod * const_unit_type[_LUMINOSITY] * \
                              detailed_unit[EXPONENT]


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
        v1 = convert(1.0, f_unit, t_unit)
        print(1.0, f_unit, '=', v1, t_unit)

        v2 = convert(v1, t_unit, f_unit)
        print(v1, t_unit, '=', v2, f_unit)

        print()


if __name__ == '__main__':
    main()
