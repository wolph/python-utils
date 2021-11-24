# -*- coding: utf-8 -*-
# This unit converter is an extended version of the SI model. It contains
# most of the typical units a person would want to convert
# the main entry point is the 'convert' function.
# Author: Kevin Schlosser 11/2021

# noinspection PySingleQuotedDocstring,PyUnresolvedReferences
'''
unit_converter
==============

There are 3 ways to use this module The 3 ways are outlined below

if you pass an inetger for the value to be converted an integer
will be returned.  You must use superscript for square and cubic.
The super script constants can be used to make things a bit easier.

>>> round(convert(71, 'in³', 'mm³'))
1163482


The converter will properly handle forward slashes in the unit. a forward slash
indicated division of a unit.

>>> convert(132.7, 'mi/h', 'km/h')
213.5599488


You can pass complex units  by using `" "` to separate units. This symbol
indicates multiplication of units.

>>> convert(1.0, 'P', 'Pa s')
0.1

You can change the precision of the value that is  returned by using
:py:class:`decimal.Decimal`. This allows the trailing 0's in a floating point
number to be preserved. If you need less precision then what is passed in for
a value you will need to do that yourself.

>>> convert(decimal.Decimal('71.0'), 'in³', 'mm³')
1163481.5439962302

>>> convert(decimal.Decimal('71.00'), 'in³', 'mm³')
1163481.5439962302


There are only 2 daya types that will get returned, :py:class:`int` and
:py:class:`float`. an :py:class:`int` will only get returned only when an
:py:class:`int` is passed as the value. All other times a :py:class:`float`
will get returned.

There is more then one way to use this module. If you find that you
have a need to use a  unit over and over again and you want to speed up the
conversion process then you can build equations that can be used
over and over again.

>>> inch_unit = Unit('in', exponent=3)
>>> mm_unit = Unit('mm', exponent=3)
>>> 71 * (inch_unit / mm_unit)
1163481.5439962302

>>> inch_unit = Unit('in', exponent=2)
>>> mm_unit = Unit('mm', exponent=2)
>>> 129.5674 * (inch_unit / mm_unit)
83591.70378381947


>>> mi_unit = Unit('mi')
>>> h_unit = Unit('h')
>>> km_unit = Unit('km')
>>> mi_unit /= h_unit
>>> km_unit /= h_unit
>>> 132.7 * (mi_unit / km_unit)
213.5599488

>>> P_unit = Unit('P')
>>> Pa_unit = Unit('Pa')
>>> s_unit = Unit('s')
>>> Pas_unit = Pa_unit * s_unit
>>> 1.0 * (P_unit / Pas_unit)
0.1

There is another way that you can build units. It can be done using unit
constants.

>>>
71 * (units.inch(exponent=3) / units.mm(exponent=3))
1163481.544

>>> 129.5674 * (units.inch(exponent=2) / units.mm(exponent=2))
83591.70378381947


>>> mi_unit = units.mi
>>> km_unit = units.km
>>> mi_unit /= units.h
>>> km_unit /= units.h
>>> 132.7 * (mi_unit / km_unit)
213.5599488

>>> 1.0 * (units.P / (units.Pa * units.s))
0.1


Superscript constants
=====================

.. py:data:: SUP_0
    :type: str
    :value: '⁰'

.. py:data:: SUP_1
    :type: str
    :value: '¹'

.. py:data:: SUP_2
    :type: str
    :value: '²'

.. py:data:: SUP_3
    :type: str
    :value: '³'

.. py:data:: SUP_4
    :type: str
    :value: '⁴'

.. py:data:: SUP_5
    :type: str
    :value: '⁵'

.. py:data:: SUP_6
    :type: str
    :value: '⁶'

.. py:data:: SUP_7
    :type: str
    :value: '⁷'

.. py:data:: SUP_8
    :type: str
    :value: '⁸'

.. py:data:: SUP_9
    :type: str
    :value: '⁹'

.. py:data:: SUP_MINUS
    :type: str
    :value: '⁻'



Special character constants
===========================

.. py:data:: MULTIPLIER
    :type: str
    :value: '⋅'

.. py:data:: QUARTER
    :type: str
    :value: '¼'

.. py:data:: OHM
    :type: str
    :value: 'Ω'

.. py:data:: DEGREE
    :type: str
    :value: '°'

.. py:data:: PI
    :type: str
    :value: 'π'

.. py:data:: UPSILON
    :type: str
    :value: 'ʊ'

.. py:data:: RING_A
    :type: str
    :value: 'Å'

.. py:data:: MICRO_SIGN
    :type: str
    :value: 'µ'

.. py:data:: EL
    :type: str
    :value: 'л'

.. py:data:: ES
    :type: str
    :value: 'с'

.. py:data:: KA
    :type: str
    :value: 'к'


Subscript character constants
=============================

.. py:data:: SUB_0
    :type: str
    :value: '₀'

.. py:data:: SUB_2
    :type: str
    :value: '₂'


Convience superscript mapping table
===================================

.. py:data:: SUPER_SCRIPT_MAPPING
    :type: dict

    This contains a mapping of ``SUP_*``
    constants to :py:class:`str(int())` values. This constant has 2 convience
    features, one is the property :py:attr:`SUPER_SCRIPT_MAPPING.reverse` that
    returnes a :py:class:`dict` of :py:class:`str(int())` to ``SUP_*`` values.
    The other convience feature is the
    method :py:meth:`SUPER_SCRIPT_MAPPING.convert` that will convert a passed
    in :py:class:`int` into its superscript version. You can also pass
    in a :py:class:`str` that contains a superscript and it will read the
    superscript and return the :py:class:`int` version of it.

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import decimal

from .unit import (
    BASE_UNITS,
    NAMED_DERIVED_UNITS,
    UNITS,
    Unit
)
from .unit_builder import build_unit
from . import units
from .unicode_characters import (
    SUP_0,
    SUP_1,
    SUP_2,
    SUP_3,
    SUP_4,
    SUP_5,
    SUP_6,
    SUP_7,
    SUP_8,
    SUP_9,
    SUP_MINUS,
    MULTIPLIER,
    QUARTER,
    OHM,
    DEGREE,
    PI,
    UPSILON,
    RING_A,
    MICRO_SIGN,
    SUB_0,
    SUB_2,
    SUPER_SCRIPT_MAPPING,
    EL,
    ES,
    KA
)


def convert(
        value,  # type: int, float, decimal.Decimal
        from_unit,  # type: str, bytes
        to_unit  # type: str, bytes
):  # type: (...) -> int or float
    # noinspection PySingleQuotedDocstring
    '''
    Unit converter (main entry point)

    General rules[cc] for writing SI units and quantities:

        * The value of a quantity is written as a number followed by a space
          (representing a multiplication sign) and a unit symbol;
          e.g., 2.21 kg, 7.3×102 m², 22 K. This rule explicitly includes the
          percent sign (%) and the symbol for degrees Celsius (°C)
          Exceptions are the symbols for plane angular degrees, minutes, and
          seconds (°, ′, and ″, respectively), which are placed immediately
          after the number with no intervening space.
        * Symbols are mathematical entities, not abbreviations, and as such do
          not have an appended period/full stop (.), unless the rules of grammar
          demand one for another reason, such as denoting the end of a sentence.
        * A prefix is part of the unit, and its symbol is prepended to a unit
          symbol without a separator (e.g., k in km, M in MPa, G in GHz,
          μ in μg). Compound prefixes are not allowed. A prefixed unit is
          atomic in expressions (e.g., km² is equivalent to (km)²).
        * Unit symbols are written using roman (upright) type, regardless of the
          type used in the surrounding text.
        * Symbols for derived units formed by multiplication are joined with a
          centre dot (⋅) or a non-breaking space; e.g., N⋅m or N m.
        * Symbols for derived units formed by division are joined with a
          solidus (/), or given as a negative exponent. E.g., the
          "metre per second" can be written m/s, m s⁻¹, m⋅s⁻¹, or m/s. A solidus
          followed without parentheses by a centre dot (or space) or a solidus
          is ambiguous and must be avoided;
          e.g., kg/(m⋅s²) and kg⋅m⁻¹⋅s⁻² are acceptable, but kg/m/s² is
          ambiguous and unacceptable.
        * In the expression of acceleration due to gravity, a space separates
          the value and the units, both the 'm' and the 's' are lowercase
          because neither the metre nor the second are named after people, and
          exponentiation is represented with a superscript '²'.
        * The first letter of symbols for units derived from the name of a
          person is written in upper case; otherwise, they are written in lower
          case. E.g., the unit of pressure is named after Blaise Pascal, so its
          symbol is written "Pa", but the symbol for mole is written "mol".
          Thus, "T" is the symbol for tesla, a measure of magnetic field
          strength, and "t" the symbol for tonne, a measure of mass. Since
          1979, the litre may exceptionally be written using either an
          uppercase "L" or a lowercase "l", a decision prompted by the
          similarity of the lowercase letter "l" to the numeral "1", especially
          with certain typefaces or English-style handwriting. The American
          NIST recommends that within the United States "L" be used rather
          than "l".
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
    :type value: :py:class:`int`, :py:class:`float` or
      :py:class:`decimal.Decimal`
    :param from_unit: unit the passed value is
    :type from_unit: :py:class:`str` or :py:class:`bytes`
    :param to_unit: unit to convert passed value to
    :type to_unit: :py:class:`str` or :py:class:`bytes`

    :return: According to the SI standard the returned value should be of
      the same type as the input type and also of the same precision as the
      input type when passing a float to be converted. With Python there is no
      way to know what the precision should be if a float is passed. So to work
      around that issue the value passed can be a `decimal.Decimal` instance
      which preserves the number of trailing zeros and that is used to set the
      precision of the returned value. If you need a precision that is less then
      what gets returned you will have to handle that yourself.

    :rtype: :py:class:`int` or :py:class:`float`
    '''  # NOQA
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

    from_units = Unit(from_unit, [])
    to_units = Unit(to_unit, [])

    value *= (from_units / to_units)

    return value
