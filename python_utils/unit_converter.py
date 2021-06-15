# -*- coding: utf-8 -*-
# This unit converter is an extended version of the SI model. It contains 
# most of the typical units a person would want to convert
# the main entry point is the "convert" function.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

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
class LENGTH(_IntWrapper):
    """
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
    """
    _values = [1, 0, 0, 0, 0, 0, 0]


class MASS(_IntWrapper):
    """
    kilogram : kg
    gram : g
    pound : lb, lbm
    kip : kip
    ounce : oz
    short ton : sh tn
    long ton : ton
    tonne : t
    slug : slug
    """
    _values = [0, 1, 0, 0, 0, 0, 0]


class TIME(_IntWrapper):
    """
    second : s
    minute : min
    hour : h
    day : d
    year : yr
    """
    _values = [0, 0, 1, 0, 0, 0, 0]


class CURRENT(_IntWrapper):
    """
    ampere : A
    """
    _values = [0, 0, 0, 1, 0, 0, 0]


class TEMPERATURE(_IntWrapper):
    """
    kelvin : K
    degree celsius : °C
    degree fahrenheit : °F
    rankine : R
    """
    _values = [0, 0, 0, 0, 1, 0, 0]


class QUANTITY(_IntWrapper):
    """
    mole : mol
    """
    _values = [0, 0, 0, 0, 0, 1, 0]


class LUMINOSITY(_IntWrapper):
    """
    candela : cd
    lumen : lm
    """
    _values = [0, 0, 0, 0, 0, 0, 1]


class ANGLE(_IntWrapper):
    _values = [0, 0, 0, 0, 0, 0, 0]


class AREA(_IntWrapper):
    """
    acre : ac
    hectare : ha
    circular inch : cir in
    circular thou : cir mil
    """
    _values = [2, 0, 0, 0, 0, 0, 0]


class VOLUME(_IntWrapper):
    """
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
    """
    _values = [3, 0, 0, 0, 0, 0, 0]


class FREQUENCY(_IntWrapper):
    """
    revolution per min : rpm
    hertz : Hz
    """
    _values = [0, 0, -1, 0, 0, 0, 0]


class SPEED(_IntWrapper):
    """
    knot : kn
    mile per hour : mph
    """
    _values = [1, 0, -1, 0, 0, 0, 0]


class ACCELERATION(_IntWrapper):
    """
    G-force : G
    """
    _values = [1, 0, -2, 0, 0, 0, 0]


class FORCE(_IntWrapper):
    """
    newton : N
    pound : lbf
    dyne : dyn
    kilogram-force : kgf, kp
    """
    _values = [1, 1, -2, 0, 0, 0, 0]


class ENERGY(_IntWrapper):
    """
    joule : J
    british thermal unit : BTU
    calorie : cal
    electro-volt : eV
    celsius heat unit : CHU
    """
    _values = [2, 1, -2, 0, 0, 0, 0]


class POWER(_IntWrapper):
    """
    watt : W
    horsepower : hp
    metric horsepower : PS
    """
    _values = [2, 1, -3, 0, 0, 0, 0]


class PRESSURE(_IntWrapper):
    """
    pascal : Pa
    atmosphere : atm
    bar : bar
    pound per squared inch : psi
    torr : torr
    millimeter of mercury : mmHg
    millimeter of water : mmH2O, mmH²O
    inch of water : inH2O, inH²O
    inch of mercury : inHg
    """
    _values = [-1, 1, -2, 0, 0, 0, 0]


class VOLUMETRIC_FLOW(_IntWrapper):
    """
    cubic feet per minute : cfm
    gal US per min : gpm
    """
    _values = [3, 0, -1, 0, 0, 0, 0]


class CHARGE(_IntWrapper):
    """
    coulomb : C
    """
    _values = [0, 0, 1, 1, 0, 0, 0]


class VOLTAGE(_IntWrapper):
    """
    volt : V
    """
    _values = [2, 1, -3, -1, 0, 0, 0]


class CAPACITANCE(_IntWrapper):
    """
    farad : F
    """
    _values = [-2, -1, 4, 2, 0, 0, 0]


class RESISTANCE(_IntWrapper):
    """
    ohm : ohm, Ω
    """
    _values = [2, 1, -3, -2, 0, 0, 0]


class CONDUCTIVITY(_IntWrapper):
    """
    siemen : S
    """
    _values = [-2, -1, 3, 2, 0, 0, 0]


class VISCOSITY(_IntWrapper):
    """
    poise : P
    """
    _values = [-1, 1, -1, 0, 0, 0, 0]


class MAGNETIC_FLUX(_IntWrapper):
    """
    weber : Wb
    maxwell : Mx
    """
    _values = [2, 1, -2, -1, 0, 0, 0]


class INDUCTANCE(_IntWrapper):
    """
    henry : H
    """
    _values = [2, 1, -2, -2, 0, 0, 0]


class MAGNETIC_INDUCTION(_IntWrapper):
    """
    tesla : T
    """
    _values = [0, 1, -2, -1, 0, 0, 0]


class ENGINE_FUEL_CONSUMPTION(_IntWrapper):
    _values = [-2, 0, 2, 0, 0, 0, 0]


class DENSITY(_IntWrapper):
    _values = [-3, 1, 0, 0, 0, 0, 0]


class TORQUE(_IntWrapper):
    _values = [2, 1, -2, 0, 0, 0, 0]


# unit type constants
# these constants get passed to the "convert" function
LENGTH = LENGTH(0)
MASS = MASS(1)
TIME = TIME(2)
CURRENT = CURRENT(3)
TEMPERATURE = TEMPERATURE(4)
QUANTITY = QUANTITY(5)
LUMINOSITY = LUMINOSITY(6)
ANGLE = ANGLE(7)
AREA = AREA(8)
VOLUME = VOLUME(9)
FREQUENCY = FREQUENCY(10)
SPEED = SPEED(11)
ACCELERATION = ACCELERATION(12)
FORCE = FORCE(13)
ENERGY = ENERGY(14)
POWER = POWER(15)
PRESSURE = PRESSURE(16)
VOLUMETRIC_FLOW = VOLUMETRIC_FLOW(17)
CHARGE = CHARGE(18)
VOLTAGE = VOLTAGE(19)
CAPACITANCE = CAPACITANCE(20)
RESISTANCE = RESISTANCE(21)
CONDUCTIVITY = CONDUCTIVITY(22)
VISCOSITY = VISCOSITY(23)
MAGNETIC_FLUX = MAGNETIC_FLUX(24)
INDUCTANCE = INDUCTANCE(25)
MAGNETIC_INDUCTION = MAGNETIC_INDUCTION(26)
ENGINE_FUEL_CONSUMPTION = ENGINE_FUEL_CONSUMPTION(27)
DENSITY = DENSITY(28)
TORQUE = TORQUE(29)


def convert(value, from_unit, to_unit, unit_type):
    """
    Unit converter
    
    :param value: value to be converted
    :type value: int, float
    :param from_unit: unit the passed value is
    :type from_unit: str, bytes
    :param to_unit: unit to convert passed value to
    :type to_unit: str, bytes
    :param unit_type: one of the following constants
        LENGTH
        MASS
        TIME
        CURRENT
        TEMPERATURE
        QUANTITY
        LUMINOSITY
        ANGLE
        AREA
        VOLUME
        FREQUENCY
        SPEED
        ACCELERATION
        FORCE
        ENERGY
        POWER
        PRESSURE
        VOLUMETRIC_FLOW
        CHARGE
        VOLTAGE
        CAPACITANCE
        RESISTANCE
        CONDUCTIVITY
        VISCOSITY
        MAGNETIC_FLUX
        INDUCTANCE
        MAGNETIC_INDUCTION
        ENGINE_FUEL_CONSUMPTION
        DENSITY
        TORQUE
    :return: value converted to new unit
    """
    try:
        from_unit = from_unit.decode('utf-8')
    except AttributeError:
        pass

    try:
        to_unit = to_unit.decode('utf-8')
    except AttributeError:
        pass

    value *= _conversion_factor(from_unit, to_unit, unit_type)
    return value


# The function temperature_conversion returns the converted temperature 'temp' 'from' one unit 'to' another
def temperature_conversion(temp, from_unit, to_unit):
    if from_unit in ("°K", "K"):
        temp_si = temp
    elif from_unit == "R":
        temp_si = temp / 1.8
    elif from_unit in ("°C", "C"):
        temp_si = _number(temp) + 273.15
    elif from_unit in ("°F", "F"):
        temp_si = (_number(temp) + 459.67) / 1.8
    else:
        raise TypeError("'" + from_unit + "' does not define a temperature.")

    if to_unit in ("°K", "K"):
        return temp_si
    elif to_unit == "R":
        return 1.8 * temp_si
    elif to_unit in ("°C", "C"):
        return temp_si - 273.15
    elif to_unit in ("°F", "F"):
        return 1.8 * temp_si - 459.67
    else:
        raise TypeError("'" + to_unit + "' does not define a temperature.")


# ----------------------PRIVATE FUNCTIONS-----------------------

# CFtoSI returns the conversion factor (multiplied) from unit to SI
# CFtoSI returns 0 if unit is not defined
# CFtoSI returns -1 if unit doesn't represent the type expected
# CFtoSI returns -2 if exponent is not a number

# unit is written this way:  [prefix1] unit1 [exponent1] {[separator2] [prefix2] unit2 [exponent2] ...}
# separator is either "." or "/"
# exponent is either "²", "³" or "^" followed by a number
# prefix is as defined in _get_prefix
# unit is as defined in _set_conversion_factor
def _conversion_factor_to_si(unit, type_):  # unit as string, type as integer (see definitions above)
    factor = 1  # conversion factor
    unit_type = [0] * 7

    units = _get_units(unit)  # get the array of units

    for j in range(len(units)):
        # multiply each individual conversion factors together
        factor *= _get_conversion_factor(_get_detailed_unit(units[j], unit_type))
    if factor is None:
        return -2  # returns -2 if an exponent was not a number

    if factor > 0:  # unit is not an error
        # check if unit is of the type expected (returns -1 if it doesn't agree with 'type'):

        if type_.values != unit_type:
            print(unit_type)
            raise TypeError('"{0}" does not define a type of {1}'.format(unit, type_.label))

    return factor  # return conversion factor


# The function _conversion_factor returns the conversion factor 'from' one unit 'to' another of the appropriate 'type'
def _conversion_factor(from_unit, to_unit, type_):
    cf_from = _conversion_factor_to_si(from_unit, type_)
    cf_to = _conversion_factor_to_si(to_unit, type_)

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
        if unit[i] == ".":  # is it a multiplier separator?
            if unit[i + 1].isdigit():
                break
                # if the character following the dot is a number, it is an exponent (ex.: "^0.25").  So ignore it.

            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                units.append("." + unit[prev_index:i])  # add first unit (and add separator)*/

            prev_index = i  # new separator index

        elif unit[i] == "/":  # is it a divider separator
            if prev_index != 0:
                units.append(unit[prev_index:i])  # add unit to array
            else:
                units.append("." + unit[prev_index:i])  # add first unit (and add separator)

            prev_index = i  # new separator index

    if prev_index != 0:
        units.append(unit[prev_index:])  # add last unit
    else:
        units.append("." + unit[prev_index:])  # add first and only unit (and add separator)

    return units  # return array


# _get_detailed_unit store the separator, the unit (with prefix), the exponent and the conversion factor
# separately in an array

def _get_detailed_unit(collapseUnit, unit_type):
    detailed_unit = [collapseUnit[0], None, 1, 1]  # array to store data
    if collapseUnit[-1] == "²":
        detailed_unit[EXPONENT] = 2
        detailed_unit[UNIT] = collapseUnit[1:len(collapseUnit) - 1]  # store unit

    elif collapseUnit.startswith('.sq '):
        detailed_unit[EXPONENT] = 2
        detailed_unit[UNIT] = collapseUnit[4:]  # store unit

    elif collapseUnit[-1] == "³":
        detailed_unit[EXPONENT] = 3
        detailed_unit[UNIT] = collapseUnit[1:len(collapseUnit) - 1]  # store unit

    elif collapseUnit.startswith('.cu '):
        detailed_unit[EXPONENT] = 3
        detailed_unit[UNIT] = collapseUnit[4:]  # store unit

    else:
        index = len(collapseUnit)  # last character for unit

        for i in range(len(collapseUnit)):
            if collapseUnit[i] == "^":  # look for exponent character
                index = i  # new index
                detailed_unit[EXPONENT] = _number(collapseUnit[i + 1:])
                # convert exponent from string to number and store it

        detailed_unit[UNIT] = collapseUnit[1:index]  # store unit

    if detailed_unit[EXPONENT] is None:
        raise TypeError(
            collapseUnit + " is not a valid number"
        )

    _set_conversion_factor(detailed_unit, unit_type)  # find conversion factor

    return detailed_unit  # return array


#  _get_conversion_factor returns the appropriate conversion factor for an individual unit of the complete unit
def _get_conversion_factor(detailed_unit):
    if detailed_unit[CF] == 0:
        return 0  # return 0 if the conversion factor is unknown
    elif detailed_unit[SEPARATOR] == "/":
        return 1 / math.pow(detailed_unit[CF], detailed_unit[EXPONENT])
        # return the inverse of the conversion factor if unit is divided
    else:
        # return the conversion factor if unit is multiplied
        return math.pow(detailed_unit[CF], detailed_unit[EXPONENT])


#  _set_conversion_factor determines the conversion factor for an individual unit
def _set_conversion_factor(detailed_unit, unit_type, first_pass=True):
    if first_pass:
        unit = detailed_unit[UNIT]
    else:
        unit = detailed_unit[UNIT][1:]  # if it is the first pass, use the entire unit, else remove the prefix

    # check if unit exist and if so, store the conversion factor
    if unit == "1":  # unity
        detailed_unit[CF] *= 1
    elif unit == "m":  # meter
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "kg":  # kilogram
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "s":  # second
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, TIME)
    elif unit == "A":  # ampere
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, CURRENT)
    elif unit == "K":  # kelvin
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, TEMPERATURE)
    elif unit == "mol":  # mole
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, QUANTITY)
    elif unit == "cd":  # candela
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, LUMINOSITY)
    elif unit == "rad":  # radian = 1 m/m
        detailed_unit[CF] *= 1
    elif unit in ("°", "deg"):  # degree = 1 / 360 rev
        detailed_unit[CF] = detailed_unit[CF] * math.pi / 180
    elif unit == "rev":  # revolution = 2PI rad
        detailed_unit[CF] = detailed_unit[CF] * 2 * math.pi
    elif unit == "'":  # arcminute = 1/60 deg
        detailed_unit[CF] = detailed_unit[CF] * math.pi / 10800
    elif unit == '"':  # arcsecond = 1/60 '
        detailed_unit[CF] = detailed_unit[CF] * math.pi / 648000
    elif unit == "gon":  # grad = 1/400 rev
        detailed_unit[CF] = detailed_unit[CF] * math.pi / 200
    elif unit == "sr":  # steradian = 1 m²/m²
        detailed_unit[CF] *= 1
    elif unit == "min":  # minute = 60 s
        detailed_unit[CF] *= 60
        _set_unit_type(detailed_unit, unit_type, TIME)
    elif unit == "h":  # hour = 60 min
        detailed_unit[CF] *= 3600
        _set_unit_type(detailed_unit, unit_type, TIME)
    elif unit == "d":  # day = 24 h
        detailed_unit[CF] *= 86400
        _set_unit_type(detailed_unit, unit_type, TIME)
    elif unit == "yr":  # year = 365.2425 d
        detailed_unit[CF] *= 31556952
        _set_unit_type(detailed_unit, unit_type, TIME)
    elif unit == "ft":  # feet = 0.3048 m
        detailed_unit[CF] *= 0.3048
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "yd":  # yard = 3 ft
        detailed_unit[CF] *= 0.9144
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "mi":  # mile = 5280 ft
        detailed_unit[CF] *= 1609.344
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "in":  # inch = 1/12 ft
        detailed_unit[CF] *= 0.0254
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "mil":  # thou = 0.001 in
        detailed_unit[CF] *= 0.0000254
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "µ":  # micron = 1/1000000 m
        detailed_unit[CF] *= 0.000001
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit in ("sm", "nmi"):  # nautical mile = 1852 m
        detailed_unit[CF] *= 1852
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "Ly":  # light-year = 9460730472580800 m
        detailed_unit[CF] *= 9460730472580800
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "AU":  # astronomic unit = 149597871464 m
        detailed_unit[CF] *= 149597871464
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "p":  # point = 5/133 cm
        detailed_unit[CF] = detailed_unit[CF] * 5 / 13300
        _set_unit_type(detailed_unit, unit_type, LENGTH)
    elif unit == "ac":  # acre = = 10 ch² = 4840 yd²
        detailed_unit[CF] *= 4046.8564224
        _set_unit_type(detailed_unit, unit_type, AREA)
    elif unit == "ha":  # hectare = 10000 m²
        detailed_unit[CF] *= 10000
        _set_unit_type(detailed_unit, unit_type, AREA)
    elif unit == "cir in":  # circular inch = pi/4 in²
        detailed_unit[CF] = detailed_unit[CF] * math.pi * 0.00016129
        _set_unit_type(detailed_unit, unit_type, AREA)
    elif unit == "cir mil":  # circular thou = pi/4 mil²
        detailed_unit[CF] = detailed_unit[CF] * math.pi * 0.00000000016129
        _set_unit_type(detailed_unit, unit_type, AREA)
    elif unit == "cc":  # cubic centimeter = 1 cm³ = 0.000001 m³
        detailed_unit[CF] *= 0.000001
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "ci":  # cubic inch = 1 in³ = (0.0254)³ m³
        detailed_unit[CF] = detailed_unit[CF] * 0.0254 * 0.0254 * 0.0254
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit in ("l", "L"):  # liter = 1 dm³ = 0.001 m³
        detailed_unit[CF] *= 0.001
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "gal":  # gallon US = 231 in³
        detailed_unit[CF] *= 0.003785411784
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "qt":  # quart US = 0.25 gal
        detailed_unit[CF] *= 0.000946352946
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "pt":  # pint US = 0.5 quart
        detailed_unit[CF] *= 0.000473176473
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "fl oz":  # fluid ounce US = 1/16 pt
        detailed_unit[CF] *= 0.0000295735295625
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "gal Imp":  # gallon Imp = 4.54609 l
        detailed_unit[CF] *= 0.00454609
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "qt Imp":  # quart Imp = 0.25 gal UK
        detailed_unit[CF] *= 0.0011365225
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "pt Imp":  # pint Imp = 0.5 quart UK
        detailed_unit[CF] *= 0.00056826125
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "fl oz Imp":  # fluid ounce Imp = 1/20 pt UK
        detailed_unit[CF] *= 0.0000284130625
        _set_unit_type(detailed_unit, unit_type, VOLUME)
    elif unit == "rpm":  # revolution per min = 1 rev/min
        detailed_unit[CF] = detailed_unit[CF] * math.pi / 30
        _set_unit_type(detailed_unit, unit_type, FREQUENCY)
    elif unit == "kn":  # knot = 1 sm/h
        detailed_unit[CF] = detailed_unit[CF] * 1852 / 3600
        _set_unit_type(detailed_unit, unit_type, SPEED)
    elif unit == "mph":  # mile per hour = 1 mi/h
        detailed_unit[CF] *= 0.44704
        _set_unit_type(detailed_unit, unit_type, SPEED)
    elif unit == "G":  # G = 9.80665 m/s²
        detailed_unit[CF] *= 9.80665
        _set_unit_type(detailed_unit, unit_type, ACCELERATION)
    elif unit == "g":  # gram = 0.001 kg
        detailed_unit[CF] *= 0.001
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit in ("lb", "lbm"):  # pound-mass = 0.45359237 kg
        detailed_unit[CF] *= 0.45359237
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "kip":  # kip = 1000 lbm
        detailed_unit[CF] *= 453.59237
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "oz":  # ounce = 1/16 lbm
        detailed_unit[CF] *= 0.028349523125
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "sh tn":  # short ton = 2000 lbm
        detailed_unit[CF] *= 907.18474
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "ton":  # long ton = 2240 lbm
        detailed_unit[CF] *= 1016.0469088
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "t":  # tonne = 1000 kg
        detailed_unit[CF] *= 1000
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "slug":  # slug = 1 lb/ft.s²
        detailed_unit[CF] = detailed_unit[CF] * 9.80665 * 0.45359237 / 0.3048
        _set_unit_type(detailed_unit, unit_type, MASS)
    elif unit == "N":  # newton = 1 m.kg/s²
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, FORCE)
    elif unit == "lbf":  # pound = 9.80665 lbm
        detailed_unit[CF] = detailed_unit[CF] * 9.80665 * 0.45359237
        _set_unit_type(detailed_unit, unit_type, FORCE)
    elif unit == "dyn":  # dyne = 1 g.cm/s²
        detailed_unit[CF] *= 0.00001
        _set_unit_type(detailed_unit, unit_type, FORCE)
    elif unit in ("kgf", "kp"):  # kilogram-force = 9.80665 N
        detailed_unit[CF] *= 9.80665
        _set_unit_type(detailed_unit, unit_type, FORCE)
    elif unit == "J":  # joule = 1 N.m
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, ENERGY)
    elif unit == "BTU":  # british thermal unit = 1055.056 J
        detailed_unit[CF] *= 1055.056
        _set_unit_type(detailed_unit, unit_type, ENERGY)
    elif unit == "cal":  # calorie = 4.1868 J
        detailed_unit[CF] *= 4.1868
        _set_unit_type(detailed_unit, unit_type, ENERGY)
    elif unit == "eV":  # electro-volt = 1.602176487 e-19 J
        detailed_unit[CF] *= 1.602176487e-19
        _set_unit_type(detailed_unit, unit_type, ENERGY)
    elif unit == "CHU":  # celsius heat unit = 1899.1 J
        detailed_unit[CF] *= 1899.1
        _set_unit_type(detailed_unit, unit_type, ENERGY)
    elif unit == "W":  # watt = 1 J/s
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, POWER)
    elif unit == "hp":  # horsepower = 550 lb.ft/s
        detailed_unit[CF] = detailed_unit[CF] * 550 * 9.80665 * 0.45359237 * 0.3048
        _set_unit_type(detailed_unit, unit_type, POWER)
    elif unit == "PS":  # metric horsepower = 75 m.kgf/s
        detailed_unit[CF] *= 735.49875
        _set_unit_type(detailed_unit, unit_type, POWER)
    elif unit == "Pa":  # pascal = 1 N/m²
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "atm":  # atmosphere = 101325 Pa
        detailed_unit[CF] *= 101325
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "bar":  # bar = 100 000 Pa
        detailed_unit[CF] *= 100000
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "psi":  # pound per squared inch = 1 lb/in²
        detailed_unit[CF] = detailed_unit[CF] * 9.80665 * 0.45359237 / math.pow(0.3048 / 12, 2)
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "torr":  # torr = 1 mmHg
        detailed_unit[CF] = detailed_unit[CF] * 101325 / 760
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "mmHg":  # millimeter of mercury = 101325 / 760 Pa
        detailed_unit[CF] = detailed_unit[CF] * 101325 / 760
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit in ("mmH2O", "mmH²O"):  # millimeter of water = 0.999972 * 9.80665 Pa
        detailed_unit[CF] *= 9.8063754138
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "inHg":  # inch of mercury = 25.4 mmHg
        detailed_unit[CF] = detailed_unit[CF] * 25.4 * 101325 / 760
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit in ("inH2O", "inH²O"):  # inch of water = 25.4 mmH2O
        detailed_unit[CF] *= 249.08193551052
        _set_unit_type(detailed_unit, unit_type, PRESSURE)
    elif unit == "°C":  # degree celsius = 1 K
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, TEMPERATURE)
    elif unit == "°F":  # degree fahrenheit = 5/9 K
        detailed_unit[CF] /= 1.8
        _set_unit_type(detailed_unit, unit_type, TEMPERATURE)
    elif unit == "R":  # rankine = 5/9 K
        detailed_unit[CF] /= 1.8
        _set_unit_type(detailed_unit, unit_type, TEMPERATURE)
    elif unit == "Hz":  # hertz = 1 s^-1
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, FREQUENCY)
    elif unit == "cfm":  # cubic feet per minute = 1 ft³/min
        detailed_unit[CF] *= 0.0004719474432
        _set_unit_type(detailed_unit, unit_type, VOLUMETRIC_FLOW)
    elif unit == "gpm":  # gal US per min = 1 gal/min
        detailed_unit[CF] *= 0.0000630901964
        _set_unit_type(detailed_unit, unit_type, VOLUMETRIC_FLOW)
    elif unit == "C":  # coulomb = 1 A.s
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, CHARGE)
    elif unit == "V":  # volt = 1 W/A
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, VOLTAGE)
    elif unit == "F":  # farad = 1 C/V
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, CAPACITANCE)
    elif unit == "ohm":  # ohm = 1 V/A
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, RESISTANCE)
    elif unit == "S":  # siemen = 1 A/V
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, CONDUCTIVITY)
    elif unit == "P":  # poise = 0.1 Pa.s
        detailed_unit[CF] *= 0.1
        _set_unit_type(detailed_unit, unit_type, VISCOSITY)
    elif unit == "St":  # stoke = 0.0001 m²/s
        detailed_unit[CF] *= 0.0001
        _set_unit_type(detailed_unit, unit_type, 2, 0, -1, 0, 0, 0, 0)
    elif unit == "Wb":  # weber = 1 V.s
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, MAGNETIC_FLUX)
    elif unit == "H":  # henry = 1 V.s/A
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, INDUCTANCE)
    elif unit == "T":  # tesla = 1 Wb/m²
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, MAGNETIC_INDUCTION)
    elif unit == "Mx":  # maxwell = 0.00000001 Wb
        detailed_unit[CF] *= 0.00000001
        _set_unit_type(detailed_unit, unit_type, MAGNETIC_FLUX)
    elif unit == "lm":  # lumen = 1 cd.sr
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, LUMINOSITY)
    elif unit == "lx":  # lux = 1 lm/m²
        detailed_unit[CF] *= 1
        _set_unit_type(detailed_unit, unit_type, -2, 0, 0, 0, 0, 0, 1)
    else:  # unit doesn't exist
        if first_pass:
            _get_unit_prefix(detailed_unit)
            # if this first pass check prefix and recheck new unit (second pass)
            _set_conversion_factor(detailed_unit, unit_type, False)
        else:
            detailed_unit[CF] = 0
            raise TypeError("'" + detailed_unit[UNIT] + "' is not a defined unit.")
            # prefix has been removed --> still not a unit


# getPrefix determines the conversion factor for the prefix of a unit
def _get_unit_prefix(detailed_unit):
    # check if prefix (first character of unit) exist and if so, get conversion factor

    if detailed_unit[UNIT][0] == "Y":  # yotta
        detailed_unit[CF] *= 1000000000000000000000000
    elif detailed_unit[UNIT][0] == "Z":  # zetta
        detailed_unit[CF] *= 1000000000000000000000
    elif detailed_unit[UNIT][0] == "E":  # exa
        detailed_unit[CF] *= 1000000000000000000
    elif detailed_unit[UNIT][0] == "P":  # peta
        detailed_unit[CF] *= 1000000000000000
    elif detailed_unit[UNIT][0] == "T":  # tera
        detailed_unit[CF] *= 1000000000000
    elif detailed_unit[UNIT][0] == "G":  # giga
        detailed_unit[CF] *= 1000000000
    elif detailed_unit[UNIT][0] == "M":  # mega
        detailed_unit[CF] *= 1000000
    elif detailed_unit[UNIT][0] == "k":  # kilo
        detailed_unit[CF] *= 1000
    elif detailed_unit[UNIT][0] == "h":  # hecto
        detailed_unit[CF] *= 100
    elif detailed_unit[UNIT][0] == "d":  # deci
        detailed_unit[CF] *= 0.1
    elif detailed_unit[UNIT][0] == "c":  # centi
        detailed_unit[CF] *= 0.01
    elif detailed_unit[UNIT][0] == "m":  # milli
        detailed_unit[CF] *= 0.001
    elif detailed_unit[UNIT][0] == "µ":  # micro
        detailed_unit[CF] *= 0.000001
    elif detailed_unit[UNIT][0] == "n":  # nano
        detailed_unit[CF] *= 0.000000001
    elif detailed_unit[UNIT][0] == "p":  # pico
        detailed_unit[CF] *= 0.000000000001
    elif detailed_unit[UNIT][0] == "f":  # femto
        detailed_unit[CF] *= 0.000000000000001
    elif detailed_unit[UNIT][0] == "a":  # atto
        detailed_unit[CF] *= 0.000000000000000001
    elif detailed_unit[UNIT][0] == "z":  # zepto
        detailed_unit[CF] *= 0.000000000000000000001
    elif detailed_unit[UNIT][0] == "y":  # yocto
        detailed_unit[CF] *= 0.000000000000000000000001
    else:  # prefix doesn't exist
        detailed_unit[CF] = 0
        raise TypeError(
            "In the unit '" + detailed_unit[UNIT] + "', '" + detailed_unit[UNIT][0] + "' is not a defined prefix."
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

    if detailed_unit[SEPARATOR] == "/":
        mod = -1  # the unit is divided, so you have to substract the exponent

    # Adjust every type:
    unit_type[LENGTH] += mod * const_unit_type[LENGTH] * detailed_unit[EXPONENT]
    unit_type[MASS] += mod * const_unit_type[MASS] * detailed_unit[EXPONENT]
    unit_type[TIME] += mod * const_unit_type[TIME] * detailed_unit[EXPONENT]
    unit_type[CURRENT] += mod * const_unit_type[CURRENT] * detailed_unit[EXPONENT]
    unit_type[TEMPERATURE] += mod * const_unit_type[TEMPERATURE] * detailed_unit[EXPONENT]
    unit_type[QUANTITY] += mod * const_unit_type[QUANTITY] * detailed_unit[EXPONENT]
    unit_type[LUMINOSITY] += mod * const_unit_type[LUMINOSITY] * detailed_unit[EXPONENT]


if __name__ == "__main__":
    print(convert(1, "cu in", "cu mm", VOLUME))
    print(convert(1, "in³", "mm³", VOLUME))

    print(convert(1, "sq in", "sq mm", AREA))
    print(convert(1, "in²", "mm²", AREA))

    print(convert(1, "gal", "l", VOLUME))
    print(convert(1, "g", "lb", MASS))
    print(convert(1, "lb", "g", MASS))





