# -*- coding: utf-8 -*-
# This unit converter is an extended version of the SI model. It contains
# most of the typical units a person would want to convert
# the main entry point is the 'convert' function.
# Author: Kevin Schlosser 11/2021

# noinspection PySingleQuotedDocstring
'''
unit_converter
==============

There are 3 ways to use this module The 3 ways are outlined below

if you pass an inetger for the value to be converted an integer
will be returned.  You must use superscript for square and cubic.
The super script constants can be used to make things a bit easier.

>>> convert(71, 'in³', 'mm³')
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
1163481.5

>>> convert(decimal.Decimal('71.00'), 'in³', 'mm³')
1163481.54


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
1163481.544

>>> inch_unit = Unit('in', exponent=2)
>>> mm_unit = Unit('mm', exponent=2)
>>> 129.5674 * (inch_unit / mm_unit)
83591.703784

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

>>> 71 * (Unit.inch(exponent=3) / Unit.mm(exponent=3))
1163481.544

>>> 129.5674 * (Unit.inch(exponent=2) / Unit.mm(exponent=2))
83591.703784

>>> mi_unit = Unit.mi
>>> km_unit = Unit.km
>>> mi_unit /= Unit.h
>>> km_unit /= Unit.h
>>> 132.7 * (mi_unit / km_unit)
213.5599488

>>> 1.0 * (Unit.P / (Unit.Pa * Unit.s))
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
import math

try:
    # noinspection PyUnresolvedReferences,PyShadowingBuiltins
    chr = unichr
except NameError:
    # noinspection PyUnboundLocalVariable,PyShadowingBuiltins
    chr = chr

SUP_0 = chr(0x2070)  # type: str # ⁰
SUP_1 = chr(0x00B9)  # type: str # ¹
SUP_2 = chr(0x00B2)  # type: str # ²
SUP_3 = chr(0x00B3)  # type: str # ³
SUP_4 = chr(0x2074)  # type: str # ⁴
SUP_5 = chr(0x2075)  # type: str # ⁵
SUP_6 = chr(0x2076)  # type: str # ⁶
SUP_7 = chr(0x2077)  # type: str # ⁷
SUP_8 = chr(0x2078)  # type: str # ⁸
SUP_9 = chr(0x2079)  # type: str # ⁹
SUP_MINUS = chr(0x207B)  # type: str # ⁻ (⁻¹)


MULTIPLIER = chr(0x22C5)  # type: str # N⋅J
QUARTER = chr(0x00BC)  # type: str  # ¼
OHM = chr(0x2126)  # type: str # Ω
DEGREE = chr(0x00B0)  # type: str # °
PI = chr(0x03C0)  # type: str # π
UPSILON = chr(0x028A)  # type: str # ʊ
RING_A = chr(0x00C5)  # type: str  # Å
MICRO_SIGN = chr(0x00B5)  # type str # µ
SUB_0 = chr(0x2080)  # type: str # ₀
SUB_2 = chr(0x2082)  # type: str # ₂


class _SUPER_SCRIPT_MAPPING(dict):

    @property
    def reverse(self):  # type: (...) -> dict
        # noinspection PySingleQuotedDocstring
        '''
        returns a dictionary with the key and values swapped.

        :rtype: :py:class:`dict`
        '''
        return {v: k for k, v in self.items()}

    def convert(
            self,
            in_value  # type: int, str
    ):  # type: (...) -> int or float
        # noinspection PySingleQuotedDocstring
        '''
        converts a :py:class:`int` to it's supercript version or converts a
        superscript to its :py:class:`int` version

        :param in_value: value to convert
        :type in_value: :py:class:`int` or :py:class:`str`
        :return:  converted value
        :rtype: :py:class:`int` or :py:class:`str`
        '''
        if isinstance(in_value, int):
            out_value = str(in_value)
            for k, v in self.reverse.items():
                out_value = out_value.replace(k, v)

        else:
            out_value = ''
            for char in in_value:
                if char in self:
                    out_value += self[char]

            out_value = int(out_value)

        return out_value


SUPER_SCRIPT_MAPPING = _SUPER_SCRIPT_MAPPING((
    (SUP_0, '0'),
    (SUP_1, '1'),
    (SUP_2, '2'),
    (SUP_3, '3'),
    (SUP_4, '4'),
    (SUP_5, '5'),
    (SUP_6, '6'),
    (SUP_7, '7'),
    (SUP_8, '8'),
    (SUP_9, '9'),
    (SUP_MINUS, '-')
))


_BASE_UNITS = {}
_NAMED_DERIVED_UNITS = {}
_UNITS = {}


class Unit(object):
    # noinspection PySingleQuotedDocstring
    '''
    Unit of measure
    ===============

    This is the workhorse of the conversion
    This class can be used to do unit conversions
    .. seealso:: python-utils.unit_converter

    .. py:method:: __init__(symbol: str, base_units: None or list[Unit] = None, factor: float = 1.0, exponent: int = 1) -> Unit

    .. py:property:: factor
        :type: decimal.Decimal

        Conversion factor

    .. py:property:: symbol
        :type: str

        String representation for the unit

    .. py:property:: exponent
        :type: decimal.Decimal

        Unit exponent (ex: 2 for square 3 for cubic)


    SI Base Units
    _____________

    :cvar mol: Unit constant for ``'mol'`` mole - amount of substance
    :vartype mol: Unit
    
    :cvar cd: Unit constant for ``'cd'`` candela - luminous intensity
    :vartype cd: Unit
    
    :cvar kg: Unit constant for ``'kg'`` kilogram - mass
    :vartype kg: Unit
    
    :cvar m: Unit constant for ``'m'`` meter - length
    :vartype m: Unit
    
    :cvar s: Unit constant for ``'s'`` second - time
    :vartype s: Unit
    
    :cvar A: Unit constant for ``'A'`` ampere - electric current
    :vartype A: Unit
    
    :cvar K: Unit constant for ``'K'`` kelvin - thermodynamic temperature
    :vartype K: Unit


    Non SI Base Units
    ________________

    :cvar bit: Unit constant for ``'bit' binary bit - data
    :vartype bit: Unit
    
    :cvar dB: Unit constant for ``'dB'`` decible - sound
    :vartype dB: Unit


     SI Derived units with special names
     ___________________________________

    :cvar Hz: Unit constant for ``'Hz'`` hertz - frequency
    :vartype Hz: Unit
    
    :cvar N: Unit constant for ``'N'`` newton - force
    :vartype N: Unit
    
    :cvar Pa: Unit constant for ``'Pa'`` pascal - pressure, stress
    :vartype Pa: Unit
    
    :cvar J: Unit constant for ``'J'`` joule - energy, work, quantity of heat
    :vartype J: Unit
    
    :cvar W: Unit constant for ``'W'`` watt - power, radiant flux
    :vartype W: Unit
    
    :cvar C: Unit constant for ``'C'`` coulomb - electric charge, quantity of electricity
    :vartype C: Unit
    
    :cvar V: Unit constant for ``'V'`` volt - electric potential difference, electromotive force
    :vartype V: Unit
    
    :cvar F: Unit constant for ``'F'`` farad - capacitance
    :vartype F: Unit
    
    :cvar ohm: Unit constant for ``'Ω'`` ohm - electric resistance
    :vartype ohm: Unit
    
    :cvar S: Unit constant for ``'S'`` siemens - electric conductance
    :vartype S: Unit
    
    :cvar Wb: Unit constant for ``'Wb'`` weber - magnetic flux
    :vartype Wb: Unit
    
    :cvar T: Unit constant for ``'T'`` tesla - magnetic flux density
    :vartype T: Unit
    
    :cvar H: Unit constant for ``'H'`` henry - inductance
    :vartype H: Unit

    :cvar deg_C: Unit constant for ``'°C'`` degree Celsius - Celsius temperature
    :vartype deg_C: Unit
    
    :cvar lm: Unit constant for ``'lm'`` lumen - luminous flux
    :vartype lm: Unit
    
    :cvar lx: Unit constant for ``'lx'`` lux - illuminance
    :vartype lx: Unit
    
    :cvar Bq: Unit constant for ``'Bq'`` becquerel - activity (of a radionuclide)
    :vartype Bq: Unit
    
    :cvar Gy: Unit constant for ``'Gy'`` gray - absorbed dose, specific energy (imparted), kerma
    :vartype Gy: Unit
    
    :cvar Sv: Unit constant for ``'Sv'`` sievert - dose equivalent
    :vartype Sv: Unit
    
    :cvar kat: Unit constant for ``'kat'`` katal - catalytic activity
    :vartype kat: Unit
    
    :cvar r: Unit constant for ``'r'`` radian - plane angle
    :vartype r: Unit
    
    :cvar sr: Unit constant for ``'sr'`` steradian - solid angle
    :vartype sr: Unit


    Additional units
    ________________
    
    :cvar au_length: Unit constant for ``'au_length'``
    :vartype au_length: Unit
    
    :cvar am: Unit constant for ``'am'``
    :vartype am: Unit
    
    :cvar angstrom: Unit constant for ``'Å'``
    :vartype angstrom: Unit
    
    :cvar ft: Unit constant for ``'ft'``
    :vartype ft: Unit
    
    :cvar yd: Unit constant for ``'yd'``
    :vartype yd: Unit
    
    :cvar mi: Unit constant for ``'mi'``
    :vartype mi: Unit
    
    :cvar inch: Unit constant for ``'in'``
    :vartype inch: Unit
    
    :cvar micron: Unit constant for ``'µ'``
    :vartype micron: Unit
    
    :cvar arcmin: Unit constant for ``'arcmin'``
    :vartype arcmin: Unit
    
    :cvar AU: Unit constant for ``'AU'``
    :vartype AU: Unit
    
    :cvar UA: Unit constant for ``'UA'``
    :vartype UA: Unit
    
    :cvar au: Unit constant for ``'au'``
    :vartype au: Unit
    
    :cvar agate: Unit constant for ``'agate'``
    :vartype agate: Unit
    
    :cvar aln: Unit constant for ``'aln'``
    :vartype aln: Unit
    
    :cvar bcorn: Unit constant for ``'bcorn'``
    :vartype bcorn: Unit
    
    :cvar a0: Unit constant for ``'a0'``
    :vartype a0: Unit
    
    :cvar rBohr: Unit constant for ``'rBohr'``
    :vartype rBohr: Unit
    
    :cvar bolt: Unit constant for ``'bolt'``
    :vartype bolt: Unit
    
    :cvar bl: Unit constant for ``'bl'``
    :vartype bl: Unit
    
    :cvar line_UK: Unit constant for ``'line_UK'``
    :vartype line_UK: Unit
    
    :cvar line: Unit constant for ``'line'``
    :vartype line: Unit
    
    :cvar cable_int: Unit constant for ``'cable_int'``
    :vartype cable_int: Unit
    
    :cvar cable_UK: Unit constant for ``'cable_UK'``
    :vartype cable_UK: Unit
    
    :cvar cable: Unit constant for ``'cable'``
    :vartype cable: Unit
    
    :cvar caliber: Unit constant for ``'caliber'``
    :vartype caliber: Unit
    
    :cvar ch_engineer: Unit constant for ``'ch_engineer'``
    :vartype ch_engineer: Unit
    
    :cvar ch_gunter: Unit constant for ``'ch_gunter'``
    :vartype ch_gunter: Unit
    
    :cvar ch_ramsden: Unit constant for ``'ch_ramsden'``
    :vartype ch_ramsden: Unit
    
    :cvar ch_surveyor: Unit constant for ``'ch_surveyor'``
    :vartype ch_surveyor: Unit
    
    :cvar cbt: Unit constant for ``'cbt'``
    :vartype cbt: Unit
    
    :cvar didotpoint: Unit constant for ``'didotpoint'``
    :vartype didotpoint: Unit
    
    :cvar digit: Unit constant for ``'digit'``
    :vartype digit: Unit
    
    :cvar re: Unit constant for ``'re'``
    :vartype re: Unit
    
    :cvar Ec: Unit constant for ``'Ec'``
    :vartype Ec: Unit
    
    :cvar eel_scottish: Unit constant for ``'eel_scottish'``
    :vartype eel_scottish: Unit
    
    :cvar eel_flemish: Unit constant for ``'eel_flemish'``
    :vartype eel_flemish: Unit
    
    :cvar eel_french: Unit constant for ``'eel_french'``
    :vartype eel_french: Unit
    
    :cvar eel_polish: Unit constant for ``'eel_polish'``
    :vartype eel_polish: Unit
    
    :cvar eel_danish: Unit constant for ``'eel_danish'``
    :vartype eel_danish: Unit
    
    :cvar eel_swedish: Unit constant for ``'eel_swedish'``
    :vartype eel_swedish: Unit
    
    :cvar eel_german: Unit constant for ``'eel_german'``
    :vartype eel_german: Unit
    
    :cvar EM_pica: Unit constant for ``'EM_pica'``
    :vartype EM_pica: Unit
    
    :cvar Em: Unit constant for ``'Em'``
    :vartype Em: Unit
    
    :cvar fath: Unit constant for ``'fath'``
    :vartype fath: Unit
    
    :cvar fm: Unit constant for ``'fm'``
    :vartype fm: Unit
    
    :cvar f: Unit constant for ``'f'``
    :vartype f: Unit
    
    :cvar finer: Unit constant for ``'finer'``
    :vartype finer: Unit
    
    :cvar fb: Unit constant for ``'fb'``
    :vartype fb: Unit
    
    :cvar fod: Unit constant for ``'fod'``
    :vartype fod: Unit
    
    :cvar fbf: Unit constant for ``'fbf'``
    :vartype fbf: Unit
    
    :cvar fur: Unit constant for ``'fur'``
    :vartype fur: Unit
    
    :cvar pleth: Unit constant for ``'pleth'``
    :vartype pleth: Unit
    
    :cvar std: Unit constant for ``'std'``
    :vartype std: Unit
    
    :cvar hand: Unit constant for ``'hand'``
    :vartype hand: Unit
    
    :cvar hiMetric: Unit constant for ``'hiMetric'``
    :vartype hiMetric: Unit
    
    :cvar hl: Unit constant for ``'hl'``
    :vartype hl: Unit
    
    :cvar hvat: Unit constant for ``'hvat'``
    :vartype hvat: Unit
    
    :cvar ly: Unit constant for ``'ly'``
    :vartype ly: Unit
    
    :cvar li: Unit constant for ``'li'``
    :vartype li: Unit
    
    :cvar LD: Unit constant for ``'LD'``
    :vartype LD: Unit
    
    :cvar mil: Unit constant for ``'mil'``
    :vartype mil: Unit
    
    :cvar Mym: Unit constant for ``'Mym'``
    :vartype Mym: Unit
    
    :cvar nail: Unit constant for ``'nail'``
    :vartype nail: Unit
    
    :cvar NL: Unit constant for ``'NL'``
    :vartype NL: Unit
    
    :cvar NM: Unit constant for ``'NM'``
    :vartype NM: Unit
    
    :cvar pace: Unit constant for ``'pace'``
    :vartype pace: Unit
    
    :cvar palm: Unit constant for ``'palm'``
    :vartype palm: Unit
    
    :cvar pc: Unit constant for ``'pc'``
    :vartype pc: Unit
    
    :cvar perch: Unit constant for ``'perch'``
    :vartype perch: Unit
    
    :cvar p: Unit constant for ``'p'``
    :vartype p: Unit
    
    :cvar PX: Unit constant for ``'PX'``
    :vartype PX: Unit
    
    :cvar pl: Unit constant for ``'pl'``
    :vartype pl: Unit
    
    :cvar pole: Unit constant for ``'pole'``
    :vartype pole: Unit
    
    :cvar ru: Unit constant for ``'ru'``
    :vartype ru: Unit
    
    :cvar rem: Unit constant for ``'rem'``
    :vartype rem: Unit
    
    :cvar rd: Unit constant for ``'rd'``
    :vartype rd: Unit
    
    :cvar actus: Unit constant for ``'actus'``
    :vartype actus: Unit
    
    :cvar rope: Unit constant for ``'rope'``
    :vartype rope: Unit
    
    :cvar sir: Unit constant for ``'sir'``
    :vartype sir: Unit
    
    :cvar span: Unit constant for ``'span'``
    :vartype span: Unit
    
    :cvar twip: Unit constant for ``'twip'``
    :vartype twip: Unit
    
    :cvar vr: Unit constant for ``'vr'``
    :vartype vr: Unit
    
    :cvar vst: Unit constant for ``'vst'``
    :vartype vst: Unit
    
    :cvar xu: Unit constant for ``'xu'``
    :vartype xu: Unit
    
    :cvar zoll: Unit constant for ``'zoll'``
    :vartype zoll: Unit
    
    :cvar bicrons: Unit constant for ``'µµ'``
    :vartype bicrons: Unit
    
    :cvar D: Unit constant for ``'D'``
    :vartype D: Unit
    
    :cvar ac: Unit constant for ``'ac'``
    :vartype ac: Unit
    
    :cvar acre: Unit constant for ``'acre'``
    :vartype acre: Unit
    
    :cvar are: Unit constant for ``'are'``
    :vartype are: Unit
    
    :cvar b: Unit constant for ``'b'``
    :vartype b: Unit
    
    :cvar cirin: Unit constant for ``'cirin'``
    :vartype cirin: Unit
    
    :cvar cirmil: Unit constant for ``'cirmil'``
    :vartype cirmil: Unit
    
    :cvar Mg_dutch: Unit constant for ``'Mg_dutch'``
    :vartype Mg_dutch: Unit
    
    :cvar Mg_prussian: Unit constant for ``'Mg_prussian'``
    :vartype Mg_prussian: Unit
    
    :cvar Mg_southafrica: Unit constant for ``'Mg_southafrica'``
    :vartype Mg_southafrica: Unit
    
    :cvar quarter_sq_mi_stat: Unit constant for ``'¼mi²_stat'``
    :vartype quarter_sq_mi_stat: Unit
    
    :cvar quarter_ac: Unit constant for ``'¼ac'``
    :vartype quarter_ac: Unit
    
    :cvar rood: Unit constant for ``'rood'``
    :vartype rood: Unit
    
    :cvar sqmi: Unit constant for ``'sqmi'``
    :vartype sqmi: Unit
    
    :cvar sq_mi_stat: Unit constant for ``'mi²_stat'``
    :vartype sq_mi_stat: Unit
    
    :cvar outhouse: Unit constant for ``'outhouse'``
    :vartype outhouse: Unit
    
    :cvar shed: Unit constant for ``'shed'``
    :vartype shed: Unit
    
    :cvar sqch_engineer: Unit constant for ``'sqch_engineer'``
    :vartype sqch_engineer: Unit
    
    :cvar sqch_gunter: Unit constant for ``'sqch_gunter'``
    :vartype sqch_gunter: Unit
    
    :cvar acre_ft: Unit constant for ``'acre⋅ft'``
    :vartype acre_ft: Unit
    
    :cvar bag: Unit constant for ``'bag'``
    :vartype bag: Unit
    
    :cvar bbl_UScranb: Unit constant for ``'bbl_UScranb'``
    :vartype bbl_UScranb: Unit
    
    :cvar bbl: Unit constant for ``'bbl'``
    :vartype bbl: Unit
    
    :cvar bbl_USpetrol: Unit constant for ``'bbl_USpetrol'``
    :vartype bbl_USpetrol: Unit
    
    :cvar bbl_UK: Unit constant for ``'bbl_UK'``
    :vartype bbl_UK: Unit
    
    :cvar FBM: Unit constant for ``'FBM'``
    :vartype FBM: Unit
    
    :cvar bouteille: Unit constant for ``'bouteille'``
    :vartype bouteille: Unit
    
    :cvar bk_UK: Unit constant for ``'bk_UK'``
    :vartype bk_UK: Unit
    
    :cvar bu_UK: Unit constant for ``'bu_UK'``
    :vartype bu_UK: Unit
    
    :cvar bu_US: Unit constant for ``'bu_US'``
    :vartype bu_US: Unit
    
    :cvar bt_UK: Unit constant for ``'bt_UK'``
    :vartype bt_UK: Unit
    
    :cvar chal_UK: Unit constant for ``'chal_UK'``
    :vartype chal_UK: Unit
    
    :cvar cc: Unit constant for ``'cc'``
    :vartype cc: Unit
    
    :cvar l: Unit constant for ``'l'``
    :vartype l: Unit
    
    :cvar L: Unit constant for ``'L'``
    :vartype L: Unit
    
    :cvar gal: Unit constant for ``'gal'``
    :vartype gal: Unit
    
    :cvar gal_UK: Unit constant for ``'gal_UK'``
    :vartype gal_UK: Unit
    
    :cvar qt: Unit constant for ``'qt'``
    :vartype qt: Unit
    
    :cvar qt_UK: Unit constant for ``'qt_UK'``
    :vartype qt_UK: Unit
    
    :cvar pt: Unit constant for ``'pt'``
    :vartype pt: Unit
    
    :cvar pt_UK: Unit constant for ``'pt_UK'``
    :vartype pt_UK: Unit
    
    :cvar floz: Unit constant for ``'floz'``
    :vartype floz: Unit
    
    :cvar floz_UK: Unit constant for ``'floz_UK'``
    :vartype floz_UK: Unit
    
    :cvar cran: Unit constant for ``'cran'``
    :vartype cran: Unit
    
    :cvar dr: Unit constant for ``'dr'``
    :vartype dr: Unit
    
    :cvar st: Unit constant for ``'st'``
    :vartype st: Unit
    
    :cvar gi: Unit constant for ``'gi'``
    :vartype gi: Unit
    
    :cvar gi_UK: Unit constant for ``'gi_UK'``
    :vartype gi_UK: Unit
    
    :cvar cup: Unit constant for ``'cup'``
    :vartype cup: Unit
    
    :cvar cup_UK: Unit constant for ``'cup_UK'``
    :vartype cup_UK: Unit
    
    :cvar dstspn: Unit constant for ``'dstspn'``
    :vartype dstspn: Unit
    
    :cvar dstspn_UK: Unit constant for ``'dstspn_UK'``
    :vartype dstspn_UK: Unit
    
    :cvar tbsp: Unit constant for ``'tbsp'``
    :vartype tbsp: Unit
    
    :cvar tbsp_UK: Unit constant for ``'tbsp_UK'``
    :vartype tbsp_UK: Unit
    
    :cvar tsp: Unit constant for ``'tsp'``
    :vartype tsp: Unit
    
    :cvar tsp_UK: Unit constant for ``'tsp_UK'``
    :vartype tsp_UK: Unit
    
    :cvar M0: Unit constant for ``'m₀'``
    :vartype M0: Unit
    
    :cvar me: Unit constant for ``'me'``
    :vartype me: Unit
    
    :cvar u_dalton: Unit constant for ``'u_dalton'``
    :vartype u_dalton: Unit
    
    :cvar u: Unit constant for ``'u'``
    :vartype u: Unit
    
    :cvar uma: Unit constant for ``'uma'``
    :vartype uma: Unit
    
    :cvar Da: Unit constant for ``'Da'``
    :vartype Da: Unit
    
    :cvar dr_troy: Unit constant for ``'dr_troy'``
    :vartype dr_troy: Unit
    
    :cvar dr_apoth: Unit constant for ``'dr_apoth'``
    :vartype dr_apoth: Unit
    
    :cvar dr_avdp: Unit constant for ``'dr_avdp'``
    :vartype dr_avdp: Unit
    
    :cvar g: Unit constant for ``'g'``
    :vartype g: Unit
    
    :cvar lb: Unit constant for ``'lb'``
    :vartype lb: Unit
    
    :cvar oz: Unit constant for ``'oz'``
    :vartype oz: Unit
    
    :cvar t_long: Unit constant for ``'t_long'``
    :vartype t_long: Unit
    
    :cvar t_short: Unit constant for ``'t_short'``
    :vartype t_short: Unit
    
    :cvar t: Unit constant for ``'t'``
    :vartype t: Unit
    
    :cvar dwt: Unit constant for ``'dwt'``
    :vartype dwt: Unit
    
    :cvar kip: Unit constant for ``'kip'``
    :vartype kip: Unit
    
    :cvar gr: Unit constant for ``'gr'``
    :vartype gr: Unit
    
    :cvar slug: Unit constant for ``'slug'``
    :vartype slug: Unit
    
    :cvar t_assay: Unit constant for ``'t_assay'``
    :vartype t_assay: Unit
    
    :cvar Da_12C: Unit constant for ``'Da_12C'``
    :vartype Da_12C: Unit
    
    :cvar Da_16O: Unit constant for ``'Da_16O'``
    :vartype Da_16O: Unit
    
    :cvar Da_1H: Unit constant for ``'Da_1H'``
    :vartype Da_1H: Unit
    
    :cvar avogram: Unit constant for ``'avogram'``
    :vartype avogram: Unit
    
    :cvar bag_UK: Unit constant for ``'bag_UK'``
    :vartype bag_UK: Unit
    
    :cvar ct: Unit constant for ``'ct'``
    :vartype ct: Unit
    
    :cvar ct_troy: Unit constant for ``'ct_troy'``
    :vartype ct_troy: Unit
    
    :cvar cH: Unit constant for ``'cH'``
    :vartype cH: Unit
    
    :cvar cwt: Unit constant for ``'cwt'``
    :vartype cwt: Unit
    
    :cvar au_time: Unit constant for ``'au_time'``
    :vartype au_time: Unit
    
    :cvar blink: Unit constant for ``'blink'``
    :vartype blink: Unit
    
    :cvar d: Unit constant for ``'d'``
    :vartype d: Unit
    
    :cvar d_sidereal: Unit constant for ``'d_sidereal'``
    :vartype d_sidereal: Unit
    
    :cvar fortnight: Unit constant for ``'fortnight'``
    :vartype fortnight: Unit
    
    :cvar h: Unit constant for ``'h'``
    :vartype h: Unit
    
    :cvar min: Unit constant for ``'min'``
    :vartype min: Unit
    
    :cvar mo: Unit constant for ``'mo'``
    :vartype mo: Unit
    
    :cvar mo_sidereal: Unit constant for ``'mo_sidereal'``
    :vartype mo_sidereal: Unit
    
    :cvar mo_mean: Unit constant for ``'mo_mean'``
    :vartype mo_mean: Unit
    
    :cvar mo_synodic: Unit constant for ``'mo_synodic'``
    :vartype mo_synodic: Unit
    
    :cvar shake: Unit constant for ``'shake'``
    :vartype shake: Unit
    
    :cvar week: Unit constant for ``'week'``
    :vartype week: Unit
    
    :cvar wink: Unit constant for ``'wink'``
    :vartype wink: Unit
    
    :cvar a_astr: Unit constant for ``'a_astr'``
    :vartype a_astr: Unit
    
    :cvar a: Unit constant for ``'a'``
    :vartype a: Unit
    
    :cvar y: Unit constant for ``'y'``
    :vartype y: Unit
    
    :cvar a_sidereal: Unit constant for ``'a_sidereal'``
    :vartype a_sidereal: Unit
    
    :cvar a_mean: Unit constant for ``'a_mean'``
    :vartype a_mean: Unit
    
    :cvar a_tropical: Unit constant for ``'a_tropical'``
    :vartype a_tropical: Unit
    
    :cvar bd: Unit constant for ``'bd'``
    :vartype bd: Unit
    
    :cvar bi: Unit constant for ``'bi'``
    :vartype bi: Unit
    
    :cvar c_int: Unit constant for ``'c_int'``
    :vartype c_int: Unit
    
    :cvar c: Unit constant for ``'c'``
    :vartype c: Unit
    
    :cvar carcel: Unit constant for ``'carcel'``
    :vartype carcel: Unit
    
    :cvar HK: Unit constant for ``'HK'``
    :vartype HK: Unit
    
    :cvar violle: Unit constant for ``'violle'``
    :vartype violle: Unit
    
    :cvar entities: Unit constant for ``'entities'``
    :vartype entities: Unit
    
    :cvar SCF: Unit constant for ``'SCF'``
    :vartype SCF: Unit
    
    :cvar SCM: Unit constant for ``'SCM'``
    :vartype SCM: Unit
    
    :cvar arcsecond: Unit constant for ``"'"``
    :vartype arcsecond: Unit
    
    :cvar arcminute: ``'"'``
    :vartype arcminute: Unit

    :cvar pid: Unit constant for ``'pid'``
    :vartype pid: Unit
    
    :cvar degree: Unit constant for ``'°'``
    :vartype degree: Unit
    
    :cvar gon: Unit constant for ``'gon'``
    :vartype gon: Unit
    
    :cvar grade: Unit constant for ``'grade'``
    :vartype grade: Unit
    
    :cvar ah: Unit constant for ``'ah'``
    :vartype ah: Unit
    
    :cvar percent: Unit constant for ``'%'``
    :vartype percent: Unit
    
    :cvar rev: Unit constant for ``'rev'``
    :vartype rev: Unit
    
    :cvar sign: Unit constant for ``'sign'``
    :vartype sign: Unit
    
    :cvar B: Unit constant for ``'B'``
    :vartype B: Unit
    
    :cvar Gib: Unit constant for ``'Gib'``
    :vartype Gib: Unit
    
    :cvar GiB: Unit constant for ``'GiB'``
    :vartype GiB: Unit
    
    :cvar Gb: Unit constant for ``'Gb'``
    :vartype Gb: Unit
    
    :cvar GB: Unit constant for ``'GB'``
    :vartype GB: Unit
    
    :cvar Kib: Unit constant for ``'Kib'``
    :vartype Kib: Unit
    
    :cvar KiB: Unit constant for ``'KiB'``
    :vartype KiB: Unit
    
    :cvar Kb: Unit constant for ``'Kb'``
    :vartype Kb: Unit
    
    :cvar KB: Unit constant for ``'KB'``
    :vartype KB: Unit
    
    :cvar Mib: Unit constant for ``'Mib'``
    :vartype Mib: Unit
    
    :cvar MiB: Unit constant for ``'MiB'``
    :vartype MiB: Unit
    
    :cvar Mb: Unit constant for ``'Mb'``
    :vartype Mb: Unit
    
    :cvar MB: Unit constant for ``'MB'``
    :vartype MB: Unit
    
    :cvar Tib: Unit constant for ``'Tib'``
    :vartype Tib: Unit
    
    :cvar TiB: Unit constant for ``'TiB'``
    :vartype TiB: Unit
    
    :cvar Tb: Unit constant for ``'Tb'``
    :vartype Tb: Unit
    
    :cvar TB: Unit constant for ``'TB'``
    :vartype TB: Unit
    
    :cvar aW: Unit constant for ``'aW'``
    :vartype aW: Unit
    
    :cvar hp: Unit constant for ``'hp'``
    :vartype hp: Unit
    
    :cvar hp_boiler: Unit constant for ``'hp_boiler'``
    :vartype hp_boiler: Unit
    
    :cvar hp_British: Unit constant for ``'hp_British'``
    :vartype hp_British: Unit
    
    :cvar cv: Unit constant for ``'cv'``
    :vartype cv: Unit
    
    :cvar hp_cheval: Unit constant for ``'hp_cheval'``
    :vartype hp_cheval: Unit
    
    :cvar hp_electric: Unit constant for ``'hp_electric'``
    :vartype hp_electric: Unit
    
    :cvar hp_metric: Unit constant for ``'hp_metric'``
    :vartype hp_metric: Unit
    
    :cvar hp_water: Unit constant for ``'hp_water'``
    :vartype hp_water: Unit
    
    :cvar prony: Unit constant for ``'prony'``
    :vartype prony: Unit
    
    :cvar at: Unit constant for ``'at'``
    :vartype at: Unit
    
    :cvar atm: Unit constant for ``'atm'``
    :vartype atm: Unit
    
    :cvar bar: Unit constant for ``'bar'``
    :vartype bar: Unit
    
    :cvar Ba: Unit constant for ``'Ba'``
    :vartype Ba: Unit
    
    :cvar p_P: Unit constant for ``'p_P'``
    :vartype p_P: Unit
    
    :cvar cgs: Unit constant for ``'cgs'``
    :vartype cgs: Unit
    
    :cvar torr: Unit constant for ``'torr'``
    :vartype torr: Unit
    
    :cvar pz: Unit constant for ``'pz'``
    :vartype pz: Unit
    
    :cvar Hg: Unit constant for ``'Hg'``
    :vartype Hg: Unit
    
    :cvar H2O: Unit constant for ``'H2O'``
    :vartype H2O: Unit
    
    :cvar Aq: Unit constant for ``'Aq'``
    :vartype Aq: Unit
    
    :cvar O2: Unit constant for ``'O2'``
    :vartype O2: Unit
    
    :cvar ksi: Unit constant for ``'ksi'``
    :vartype ksi: Unit
    
    :cvar psi: Unit constant for ``'psi'``
    :vartype psi: Unit
    
    :cvar psf: Unit constant for ``'psf'``
    :vartype psf: Unit
    
    :cvar osi: Unit constant for ``'osi'``
    :vartype osi: Unit
    
    :cvar kerma: Unit constant for ``'kerma'``
    :vartype kerma: Unit
    
    :cvar Mrd: Unit constant for ``'Mrd'``
    :vartype Mrd: Unit
    
    :cvar rad: Unit constant for ``'rad'``
    :vartype rad: Unit
    
    :cvar B_power: Unit constant for ``'B_power'``
    :vartype B_power: Unit
    
    :cvar B_voltage: Unit constant for ``'B_voltage'``
    :vartype B_voltage: Unit
    
    :cvar dB_power: Unit constant for ``'dB_power'``
    :vartype dB_power: Unit
    
    :cvar dB_voltage: Unit constant for ``'dB_voltage'``
    :vartype dB_voltage: Unit
    
    :cvar au_mf: Unit constant for ``'au_mf'``
    :vartype au_mf: Unit
    
    :cvar Gs: Unit constant for ``'Gs'``
    :vartype Gs: Unit
    
    :cvar M: Unit constant for ``'M'``
    :vartype M: Unit
    
    :cvar au_charge: Unit constant for ``'au_charge'``
    :vartype au_charge: Unit
    
    :cvar aC: Unit constant for ``'aC'``
    :vartype aC: Unit
    
    :cvar esc: Unit constant for ``'esc'``
    :vartype esc: Unit
    
    :cvar esu: Unit constant for ``'esu'``
    :vartype esu: Unit
    
    :cvar Fr: Unit constant for ``'Fr'``
    :vartype Fr: Unit
    
    :cvar statC: Unit constant for ``'statC'``
    :vartype statC: Unit
    
    :cvar aS: Unit constant for ``'aS'``
    :vartype aS: Unit
    
    :cvar aW_1: Unit constant for ``'aW-1'``
    :vartype aW_1: Unit
    
    :cvar gemu: Unit constant for ``'gemʊ'``
    :vartype gemu: Unit
    
    :cvar mho: Unit constant for ``'mho'``
    :vartype mho: Unit
    
    :cvar statmho: Unit constant for ``'statmho'``
    :vartype statmho: Unit
    
    :cvar aH: Unit constant for ``'aH'``
    :vartype aH: Unit
    
    :cvar statH: Unit constant for ``'statH'``
    :vartype statH: Unit
    
    :cvar au_ep: Unit constant for ``'au_ep'``
    :vartype au_ep: Unit
    
    :cvar aV: Unit constant for ``'aV'``
    :vartype aV: Unit
    
    :cvar statV: Unit constant for ``'statV'``
    :vartype statV: Unit
    
    :cvar V_mean: Unit constant for ``'V_mean'``
    :vartype V_mean: Unit
    
    :cvar V_US: Unit constant for ``'V_US'``
    :vartype V_US: Unit
    
    :cvar a_ohm: Unit constant for ``'aΩ'``
    :vartype a_ohm: Unit
    
    :cvar S_ohm: Unit constant for ``'SΩ'``
    :vartype S_ohm: Unit
    
    :cvar statohm: Unit constant for ``'statohm'``
    :vartype statohm: Unit
    
    :cvar au_energy: Unit constant for ``'au_energy'``
    :vartype au_energy: Unit
    
    :cvar bboe: Unit constant for ``'bboe'``
    :vartype bboe: Unit
    
    :cvar BeV: Unit constant for ``'BeV'``
    :vartype BeV: Unit
    
    :cvar Btu_ISO: Unit constant for ``'Btu_ISO'``
    :vartype Btu_ISO: Unit
    
    :cvar Btu_IT: Unit constant for ``'Btu_IT'``
    :vartype Btu_IT: Unit
    
    :cvar Btu_mean: Unit constant for ``'Btu_mean'``
    :vartype Btu_mean: Unit
    
    :cvar Btu_therm: Unit constant for ``'Btu_therm'``
    :vartype Btu_therm: Unit
    
    :cvar cal_15: Unit constant for ``'cal_15'``
    :vartype cal_15: Unit
    
    :cvar cal_4: Unit constant for ``'cal_4'``
    :vartype cal_4: Unit
    
    :cvar Cal: Unit constant for ``'Cal'``
    :vartype Cal: Unit
    
    :cvar kcal: Unit constant for ``'kcal'``
    :vartype kcal: Unit
    
    :cvar cal_IT: Unit constant for ``'cal_IT'``
    :vartype cal_IT: Unit
    
    :cvar cal_mean: Unit constant for ``'cal_mean'``
    :vartype cal_mean: Unit
    
    :cvar cal_therm: Unit constant for ``'cal_therm'``
    :vartype cal_therm: Unit
    
    :cvar Chu: Unit constant for ``'Chu'``
    :vartype Chu: Unit
    
    :cvar eV: Unit constant for ``'eV'``
    :vartype eV: Unit
    
    :cvar erg: Unit constant for ``'erg'``
    :vartype erg: Unit
    
    :cvar Eh: Unit constant for ``'Eh'``
    :vartype Eh: Unit
    
    :cvar au_force: Unit constant for ``'au_force'``
    :vartype au_force: Unit
    
    :cvar crinal: Unit constant for ``'crinal'``
    :vartype crinal: Unit
    
    :cvar dyn: Unit constant for ``'dyn'``
    :vartype dyn: Unit
    
    :cvar gf: Unit constant for ``'gf'``
    :vartype gf: Unit
    
    :cvar kgf: Unit constant for ``'kgf'``
    :vartype kgf: Unit
    
    :cvar kgp: Unit constant for ``'kgp'``
    :vartype kgp: Unit
    
    :cvar grf: Unit constant for ``'grf'``
    :vartype grf: Unit
    
    :cvar kp: Unit constant for ``'kp'``
    :vartype kp: Unit
    
    :cvar kipf: Unit constant for ``'kipf'``
    :vartype kipf: Unit
    
    :cvar lbf: Unit constant for ``'lbf'``
    :vartype lbf: Unit
    
    :cvar pdl: Unit constant for ``'pdl'``
    :vartype pdl: Unit
    
    :cvar slugf: Unit constant for ``'slugf'``
    :vartype slugf: Unit
    
    :cvar tf_long: Unit constant for ``'tf_long'``
    :vartype tf_long: Unit
    
    :cvar tf_metric: Unit constant for ``'tf_metric'``
    :vartype tf_metric: Unit
    
    :cvar tf_short: Unit constant for ``'tf_short'``
    :vartype tf_short: Unit
    
    :cvar ozf: Unit constant for ``'ozf'``
    :vartype ozf: Unit
    
    :cvar au_ec: Unit constant for ``'au_ec'``
    :vartype au_ec: Unit
    
    :cvar abA: Unit constant for ``'abA'``
    :vartype abA: Unit
    
    :cvar Bi: Unit constant for ``'Bi'``
    :vartype Bi: Unit
    
    :cvar edison: Unit constant for ``'edison'``
    :vartype edison: Unit
    
    :cvar statA: Unit constant for ``'statA'``
    :vartype statA: Unit
    
    :cvar gilbert: Unit constant for ``'gilbert'``
    :vartype gilbert: Unit
    
    :cvar pragilbert: Unit constant for ``'pragilbert'``
    :vartype pragilbert: Unit
    
    :cvar cps: Unit constant for ``'cps'``
    :vartype cps: Unit
    
    :cvar Kt: Unit constant for ``'Kt'``
    :vartype Kt: Unit
    
    :cvar ppb: Unit constant for ``'ppb'``
    :vartype ppb: Unit
    
    :cvar pph: Unit constant for ``'pph'``
    :vartype pph: Unit
    
    :cvar pphm: Unit constant for ``'pphm'``
    :vartype pphm: Unit
    
    :cvar ppht: Unit constant for ``'ppht'``
    :vartype ppht: Unit
    
    :cvar ppm: Unit constant for ``'ppm'``
    :vartype ppm: Unit
    
    :cvar ppq: Unit constant for ``'ppq'``
    :vartype ppq: Unit
    
    :cvar ppt_tera: Unit constant for ``'ppt_tera'``
    :vartype ppt_tera: Unit
    
    :cvar ppt: Unit constant for ``'ppt'``
    :vartype ppt: Unit
    
    :cvar Ci: Unit constant for ``'Ci'``
    :vartype Ci: Unit
    
    :cvar sp: Unit constant for ``'sp'``
    :vartype sp: Unit
    
    :cvar gy: Unit constant for ``'gy'``
    :vartype gy: Unit
    
    :cvar lbm: Unit constant for ``'lbm'``
    :vartype lbm: Unit
    
    :cvar ohm_mechanical: Unit constant for ``'Ω_mechanical'``
    :vartype ohm_mechanical: Unit
    
    :cvar perm_0C: Unit constant for ``'perm_0C'``
    :vartype perm_0C: Unit
    
    :cvar perm_23C: Unit constant for ``'perm_23C'``
    :vartype perm_23C: Unit
    
    :cvar permin_0C: Unit constant for ``'permin_0C'``
    :vartype permin_0C: Unit
    
    :cvar permin_23C: Unit constant for ``'permin_23C'``
    :vartype permin_23C: Unit
    
    :cvar permmil_0C: Unit constant for ``'permmil_0C'``
    :vartype permmil_0C: Unit
    
    :cvar permmil_23C: Unit constant for ``'permmil_23C'``
    :vartype permmil_23C: Unit
    
    :cvar brewster: Unit constant for ``'brewster'``
    :vartype brewster: Unit
    
    :cvar aF: Unit constant for ``'aF'``
    :vartype aF: Unit
    
    :cvar jar: Unit constant for ``'jar'``
    :vartype jar: Unit
    
    :cvar statF: Unit constant for ``'statF'``
    :vartype statF: Unit
    
    :cvar P: Unit constant for ``'P'``
    :vartype P: Unit
    
    :cvar Pl: Unit constant for ``'Pl'``
    :vartype Pl: Unit
    
    :cvar reyn: Unit constant for ``'reyn'``
    :vartype reyn: Unit
    
    :cvar clo: Unit constant for ``'clo'``
    :vartype clo: Unit
    
    :cvar RSI: Unit constant for ``'RSI'``
    :vartype RSI: Unit
    
    :cvar tog: Unit constant for ``'tog'``
    :vartype tog: Unit
    
    :cvar Bz: Unit constant for ``'Bz'``
    :vartype Bz: Unit
    
    :cvar kn_noeud: Unit constant for ``'kn_noeud'``
    :vartype kn_noeud: Unit
    
    :cvar knot_noeud: Unit constant for ``'knot_noeud'``
    :vartype knot_noeud: Unit
    
    :cvar mpy: Unit constant for ``'mpy'``
    :vartype mpy: Unit
    
    :cvar kn: Unit constant for ``'kn'``
    :vartype kn: Unit
    
    :cvar knot: Unit constant for ``'knot'``
    :vartype knot: Unit
    
    :cvar c_light: Unit constant for ``'c_light'``
    :vartype c_light: Unit
    
    :cvar dioptre: Unit constant for ``'dioptre'``
    :vartype dioptre: Unit
    
    :cvar mayer: Unit constant for ``'mayer'``
    :vartype mayer: Unit
    
    :cvar helmholtz: Unit constant for ``'helmholtz'``
    :vartype helmholtz: Unit
    
    :cvar mired: Unit constant for ``'mired'``
    :vartype mired: Unit
    
    :cvar cumec: Unit constant for ``'cumec'``
    :vartype cumec: Unit
    
    :cvar gph_UK: Unit constant for ``'gph_UK'``
    :vartype gph_UK: Unit
    
    :cvar gpm_UK: Unit constant for ``'gpm_UK'``
    :vartype gpm_UK: Unit
    
    :cvar gps_UK: Unit constant for ``'gps_UK'``
    :vartype gps_UK: Unit
    
    :cvar lusec: Unit constant for ``'lusec'``
    :vartype lusec: Unit
    
    :cvar CO: Unit constant for ``'CO'``
    :vartype CO: Unit
    
    :cvar gph: Unit constant for ``'gph'``
    :vartype gph: Unit
    
    :cvar gpm: Unit constant for ``'gpm'``
    :vartype gpm: Unit
    
    :cvar gps: Unit constant for ``'gps'``
    :vartype gps: Unit
    
    :cvar G: Unit constant for ``'G'``
    :vartype G: Unit
    
    :cvar rps: Unit constant for ``'rps'``
    :vartype rps: Unit
    
    :cvar den: Unit constant for ``'den'``
    :vartype den: Unit
    
    :cvar denier: Unit constant for ``'denier'``
    :vartype denier: Unit
    
    :cvar te: Unit constant for ``'te'``
    :vartype te: Unit
    
    :cvar au_lm: Unit constant for ``'au_lm'``
    :vartype au_lm: Unit
    
    :cvar c_power: Unit constant for ``'c_power'``
    :vartype c_power: Unit
    
    :cvar asb: Unit constant for ``'asb'``
    :vartype asb: Unit
    
    :cvar nit: Unit constant for ``'nit'``
    :vartype nit: Unit
    
    :cvar sb: Unit constant for ``'sb'``
    :vartype sb: Unit
    
    :cvar oe: Unit constant for ``'oe'``
    :vartype oe: Unit
    
    :cvar praoersted: Unit constant for ``'praoersted'``
    :vartype praoersted: Unit
    
    :cvar au_mdm: Unit constant for ``'au_mdm'``
    :vartype au_mdm: Unit
    
    :cvar Gal: Unit constant for ``'Gal'``
    :vartype Gal: Unit
    
    :cvar leo: Unit constant for ``'leo'``
    :vartype leo: Unit
    
    :cvar gn: Unit constant for ``'gn'``
    :vartype gn: Unit
    
    :cvar ohm_acoustic: Unit constant for ``'Ω_acoustic'``
    :vartype ohm_acoustic: Unit
    
    :cvar ohm_SI: Unit constant for ``'Ω_SI'``
    :vartype ohm_SI: Unit
    
    :cvar rayl_cgs: Unit constant for ``'rayl_cgs'``
    :vartype rayl_cgs: Unit
    
    :cvar rayl_MKSA: Unit constant for ``'rayl_MKSA'``
    :vartype rayl_MKSA: Unit
    
    :cvar Na: Unit constant for ``'Na'``
    :vartype Na: Unit
    
    :cvar au_action: Unit constant for ``'au_action'``
    :vartype au_action: Unit
    
    :cvar au_am: Unit constant for ``'au_am'``
    :vartype au_am: Unit
    
    :cvar planck: Unit constant for ``'planck'``
    :vartype planck: Unit
    
    :cvar rpm: Unit constant for ``'rpm'``
    :vartype rpm: Unit
    
    :cvar au_cd: Unit constant for ``'au_cd'``
    :vartype au_cd: Unit
    
    :cvar Ah: Unit constant for ``'Ah'``
    :vartype Ah: Unit
    
    :cvar F_12C: Unit constant for ``'F_12C'``
    :vartype F_12C: Unit
    
    :cvar F_chemical: Unit constant for ``'F_chemical'``
    :vartype F_chemical: Unit
    
    :cvar F_physical: Unit constant for ``'F_physical'``
    :vartype F_physical: Unit
    
    :cvar roc: Unit constant for ``'roc'``
    :vartype roc: Unit
    
    :cvar rom: Unit constant for ``'rom'``
    :vartype rom: Unit
    
    :cvar au_eqm: Unit constant for ``'au_eqm'``
    :vartype au_eqm: Unit
    
    :cvar au_edm: Unit constant for ``'au_edm'``
    :vartype au_edm: Unit
    
    :cvar au_efs: Unit constant for ``'au_efs'``
    :vartype au_efs: Unit
    
    :cvar Jy: Unit constant for ``'Jy'``
    :vartype Jy: Unit
    
    :cvar MGOe: Unit constant for ``'MGOe'``
    :vartype MGOe: Unit
    
    :cvar Ly: Unit constant for ``'Ly'``
    :vartype Ly: Unit
    
    :cvar ly_langley: Unit constant for ``'ly_langley'``
    :vartype ly_langley: Unit
    
    :cvar ue: Unit constant for ``'ue'``
    :vartype ue: Unit
    
    :cvar eu: Unit constant for ``'eu'``
    :vartype eu: Unit
    
    :cvar UI: Unit constant for ``'UI'``
    :vartype UI: Unit
    
    :cvar IU: Unit constant for ``'IU'``
    :vartype IU: Unit
    
    :cvar ph: Unit constant for ``'ph'``
    :vartype ph: Unit
    
    :cvar cSt: Unit constant for ``'cSt'``
    :vartype cSt: Unit
    
    :cvar St: Unit constant for ``'St'``
    :vartype St: Unit
    
    :cvar fps: Unit constant for ``'fps'``
    :vartype fps: Unit
    
    :cvar fpm: Unit constant for ``'fpm'``
    :vartype fpm: Unit
    
    :cvar fph: Unit constant for ``'fph'``
    :vartype fph: Unit
    
    :cvar ips: Unit constant for ``'ips'``
    :vartype ips: Unit
    
    :cvar mph: Unit constant for ``'mph'``
    :vartype mph: Unit
    
    :cvar cfm: Unit constant for ``'cfm'``
    :vartype cfm: Unit
    
    :cvar cfs: Unit constant for ``'cfs'``
    :vartype cfs: Unit

    :cvar deg_R: Unit constant for ``'°R'``
    :vartype deg_R: Unit

    :cvar deg_F: Unit constant for ``'°F'``
    :vartype deg_F: Unit

    :cvar ft_survey: Unit constant for ``'ft_survey'``
    :vartype ft_survey: Unit


    Unit Prefixes
    _____________

    Units an all be prefixed  with the folling:

      * yotta: `'Y'`
      * zetta: `'Z'`
      * exa: `'E'`
      * peta: `'P'`
      * tera: `'T'`
      * giga: `'G'`
      * mega: `'M'`
      * kilo: `'k'`
      * hecto: `'h'`
      * deka: `'da'`
      * deci: `'d'`
      * centi: `'c'`
      * milli: `'m'`
      * micro: `'µ'`
      * nano: `'n'`
      * pico: `'p'`
      * femto: `'f'`
      * atto: `'a'`
      * zepto: `'z'`
      * yocto: `'y'`

    For example. There is no definition for the unit centimeter,
    however we have the SI base unit meter `'m'` and we have the prefix
    centi `'c'`. Bring bring them together and you get `'cm'` centimeter.
    '''

    mol = None
    cd = None
    kg = None
    m = None
    s = None
    A = None
    K = None
    bit = None
    dB = None
    Hz = None
    N = None
    Pa = None
    J = None
    W = None
    C = None
    V = None
    F = None
    ohm = None
    S = None
    Wb = None
    T = None
    H = None
    lm = None
    lx = None
    Bq = None
    Gy = None
    Sv = None
    kat = None
    r = None
    sr = None
    au_length = None
    am = None
    angstrom = None
    ft = None
    yd = None
    mi = None
    inch = None
    micron = None
    arcmin = None
    AU = None
    UA = None
    au = None
    agate = None
    aln = None
    bcorn = None
    a0 = None
    rBohr = None
    bolt = None
    bl = None
    line_UK = None
    line = None
    cable_int = None
    cable_UK = None
    cable = None
    caliber = None
    ch_engineer = None
    ch_gunter = None
    ch_ramsden = None
    ch_surveyor = None
    cbt = None
    didotpoint = None
    digit = None
    re = None
    Ec = None
    eel_scottish = None
    eel_flemish = None
    eel_french = None
    eel_polish = None
    eel_danish = None
    eel_swedish = None
    eel_german = None
    EM_pica = None
    Em = None
    fath = None
    fm = None
    f = None
    finer = None
    fb = None
    fod = None
    fbf = None
    fur = None
    pleth = None
    std = None
    hand = None
    hiMetric = None
    hl = None
    hvat = None
    ly = None
    li = None
    LD = None
    mil = None
    Mym = None
    nail = None
    NL = None
    NM = None
    pace = None
    palm = None
    pc = None
    perch = None
    p = None
    PX = None
    pl = None
    pole = None
    ru = None
    rem = None
    rd = None
    actus = None
    rope = None
    sir = None
    span = None
    twip = None
    vr = None
    vst = None
    xu = None
    zoll = None
    bicron = None
    D = None
    ac = None
    acre = None
    are = None
    b = None
    cirin = None
    cirmil = None
    Mg_dutch = None
    Mg_prussian = None
    Mg_southafrica = None
    quarter_sq_mi_stat = None
    quarter_ac = None
    rood = None
    sqmi = None
    sq_mi_stat = None
    outhouse = None
    shed = None
    sqch_engineer = None
    sqch_gunter = None
    acre_ft = None
    bag = None
    bbl_UScranb = None
    bbl = None
    bbl_USpetrol = None
    bbl_UK = None
    FBM = None
    bouteille = None
    bk_UK = None
    bu_UK = None
    bu_US = None
    bt_UK = None
    chal_UK = None
    cc = None
    l = None
    L = None
    gal = None
    gal_UK = None
    qt = None
    qt_UK = None
    pt = None
    pt_UK = None
    floz = None
    floz_UK = None
    cran = None
    dr = None
    st = None
    gi = None
    gi_UK = None
    cup = None
    cup_UK = None
    dstspn = None
    dstspn_UK = None
    tbsp = None
    tbsp_UK = None
    tsp = None
    tsp_UK = None
    M0 = None
    me = None
    u_dalton = None
    u = None
    uma = None
    Da = None
    dr_troy = None
    dr_apoth = None
    dr_avdp = None
    g = None
    lb = None
    oz = None
    t_long = None
    t_short = None
    t = None
    dwt = None
    kip = None
    gr = None
    slug = None
    t_assay = None
    Da_12C = None
    Da_16O = None
    Da_1H = None
    avogram = None
    bag_UK = None
    ct = None
    ct_troy = None
    cH = None
    cwt = None
    au_time = None
    blink = None
    d = None
    d_sidereal = None
    fortnight = None
    h = None
    min = None
    mo = None
    mo_sidereal = None
    mo_mean = None
    mo_synodic = None
    shake = None
    week = None
    wink = None
    a_astr = None
    a = None
    y = None
    a_sidereal = None
    a_mean = None
    a_tropical = None
    bd = None
    bi = None
    c_int = None
    c = None
    carcel = None
    HK = None
    violle = None
    entities = None
    SCF = None
    SCM = None
    arcsecond = None
    arcminute = None
    pid = None
    degree = None
    gon = None
    grade = None
    ah = None
    percent = None
    rev = None
    sign = None
    B = None
    Gib = None
    GiB = None
    Gb = None
    GB = None
    Kib = None
    KiB = None
    Kb = None
    KB = None
    Mib = None
    MiB = None
    Mb = None
    MB = None
    Tib = None
    TiB = None
    Tb = None
    TB = None
    aW = None
    hp = None
    hp_boiler = None
    hp_British = None
    cv = None
    hp_cheval = None
    hp_electric = None
    hp_metric = None
    hp_water = None
    prony = None
    at = None
    atm = None
    bar = None
    Ba = None
    p_P = None
    cgs = None
    torr = None
    pz = None
    Hg = None
    H2O = None
    Aq = None
    O2 = None
    ksi = None
    psi = None
    psf = None
    osi = None
    kerma = None
    Mrd = None
    rad = None
    B_power = None
    B_voltage = None
    dB_power = None
    dB_voltage = None
    au_mf = None
    Gs = None
    M = None
    au_charge = None
    aC = None
    esc = None
    esu = None
    Fr = None
    statC = None
    aS = None
    aW_1 = None
    gemu = None
    mho = None
    statmho = None
    aH = None
    statH = None
    au_ep = None
    aV = None
    statV = None
    V_mean = None
    V_US = None
    a_ohm = None
    S_ohm = None
    statohm = None
    au_energy = None
    bboe = None
    BeV = None
    Btu_ISO = None
    Btu_IT = None
    Btu_mean = None
    Btu_therm = None
    cal_15 = None
    cal_4 = None
    Cal = None
    kcal = None
    cal_IT = None
    cal_mean = None
    cal_therm = None
    Chu = None
    eV = None
    erg = None
    Eh = None
    au_force = None
    crinal = None
    dyn = None
    gf = None
    kgf = None
    kgp = None
    grf = None
    kp = None
    kipf = None
    lbf = None
    pdl = None
    slugf = None
    tf_long = None
    tf_metric = None
    tf_short = None
    ozf = None
    au_ec = None
    abA = None
    Bi = None
    edison = None
    statA = None
    gilbert = None
    pragilbert = None
    cps = None
    Kt = None
    ppb = None
    pph = None
    pphm = None
    ppht = None
    ppm = None
    ppq = None
    ppt_tera = None
    ppt = None
    Ci = None
    sp = None
    gy = None
    lbm = None
    ohm_mechanical = None
    perm_0C = None
    perm_23C = None
    permin_0C = None
    permin_23C = None
    permmil_0C = None
    permmil_23C = None
    brewster = None
    aF = None
    jar = None
    statF = None
    P = None
    Pl = None
    reyn = None
    clo = None
    RSI = None
    tog = None
    Bz = None
    kn_noeud = None
    knot_noeud = None
    mpy = None
    kn = None
    knot = None
    c_light = None
    dioptre = None
    mayer = None
    helmholtz = None
    mired = None
    cumec = None
    gph_UK = None
    gpm_UK = None
    gps_UK = None
    lusec = None
    CO = None
    gph = None
    gpm = None
    gps = None
    G = None
    rps = None
    den = None
    denier = None
    te = None
    au_lm = None
    c_power = None
    asb = None
    nit = None
    sb = None
    oe = None
    praoersted = None
    au_mdm = None
    Gal = None
    leo = None
    gn = None
    ohm_acoustic = None
    ohm_SI = None
    rayl_cgs = None
    rayl_MKSA = None
    Na = None
    au_action = None
    au_am = None
    planck = None
    rpm = None
    au_cd = None
    Ah = None
    F_12C = None
    F_chemical = None
    F_physical = None
    roc = None
    rom = None
    au_eqm = None
    au_edm = None
    au_efs = None
    Jy = None
    MGOe = None
    Ly = None
    ly_langley = None
    ue = None
    eu = None
    UI = None
    IU = None
    ph = None
    cSt = None
    St = None
    fps = None
    fpm = None
    fph = None
    ips = None
    mph = None
    cfm = None
    cfs = None
    bicrons = None
    ft_survey = None

    mm = None
    cm = None
    km = None

    deg_R = None
    deg_C = None
    deg_F = None

    def __init__(
            self,
            symbol,  # type: str
            base_units=None,  # type: list[Unit] or None
            factor=1.0,  # type: float
            exponent=1  # type: int
    ):
        # noinspection PySingleQuotedDocstring
        '''
        Unit class

        This is the workhorse of the conversion

        '''
        if base_units is None:
            base_units = []

        self._symbol = symbol
        self._factor = decimal.Decimal(str(factor))
        self._exponent = exponent
        self._b_units = base_units

        if not base_units and symbol not in _BASE_UNITS:
            self._b_units = self._process_unit(symbol)

    def _process_unit(
            self,
            unit,
            first_pass=True
    ):
        unit = unit.strip()
        unit = unit.replace(' ', MULTIPLIER)

        if (
                not unit.startswith('O2') and
                not unit.startswith('Aq') and
                not unit.startswith('Hg')
        ):
            if 'H2O' in unit:
                unit = unit.replace('H2O', '⋅Aq')
                return self._process_unit(unit)
            elif 'H₂O' in unit:
                unit = unit.replace('H₂O', '⋅Aq')
                return self._process_unit(unit)
            elif 'Aq' in unit and '⋅Aq' not in unit:
                unit = unit.replace('Aq', '⋅Aq')
                return self._process_unit(unit)
            elif 'Hg' in unit and '⋅Hg' not in unit:
                unit = unit.replace('Hg', '⋅Hg')
                return self._process_unit(unit)
            elif 'O2' in unit and '⋅O2' not in unit:
                unit = unit.replace('O2', '⋅O2')
                return self._process_unit(unit)

        if (
                MULTIPLIER not in unit and
                '/' not in unit
        ):
            exponent = ''
            c_unit = ''
            for char in unit:
                if char in SUPER_SCRIPT_MAPPING:
                    exponent += SUPER_SCRIPT_MAPPING[char]
                else:
                    c_unit += char

            if exponent == '':
                exponent = '1'

            exponent = decimal.Decimal(exponent)
            u = c_unit

            if u in _BASE_UNITS:
                found_unit = _BASE_UNITS[u](exponent=exponent)
                return [found_unit]
            elif u in _NAMED_DERIVED_UNITS:
                found_unit = _NAMED_DERIVED_UNITS[u](exponent=exponent)
                return [found_unit]
            elif u in _UNITS:
                found_unit = _UNITS[u](exponent=exponent)
                return [found_unit]
            elif first_pass:
                unt = self._parse_unit_prefix(u)
                if unt is None:
                    return []

                unt._exponent = exponent
                return [unt]
            else:
                raise ValueError('Unit {0} not found'.format(unit))

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

        res = []

        for i, item1 in enumerate(units):
            for char in item1[:]:
                if char == '(':
                    brace_open += 1

                elif char == ')':
                    brace_open -= 1
                    if brace_open == 0:
                        if not 'sqrt' + item + ')' in item1:
                            item1.replace(item + ')', 'MARKER' + str(marker))
                            cfs['MARKER' + str(marker)] = (
                                self._process_unit(item[1:])
                            )
                            marker += 1
                        item = ''
                        continue

                item += char

            found_units = []
            for ut in item1.split(MULTIPLIER):
                if ut in cfs:
                    found_units.extend(cfs[ut])
                else:
                    if ut.startswith('sqrt('):
                        ut = ut[5:-1]
                        f_units = self._process_unit(ut)
                        found_units.append(Unit('sqrt', base_units=f_units))

                    found_units.extend(self._process_unit(ut))

            base_unit = Unit(unit, base_units=found_units)

            if i > 0:
                base_unit._exponent = -base_unit._exponent

            res.append(base_unit)

        return res

    @staticmethod
    # determines the conversion factor for the prefix of a unit
    def _parse_unit_prefix(unit):
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
            for key, factor in mapping.items():
                if unit.startswith(key):
                    symbol = unit.replace(key, '', 1)
                    if symbol in _BASE_UNITS:
                        base_unit = [_BASE_UNITS[symbol]]
                    elif symbol in _NAMED_DERIVED_UNITS:
                        base_unit = [_NAMED_DERIVED_UNITS[symbol]]
                    elif unit in _UNITS:
                        base_unit = [_UNITS[symbol]]
                    else:
                        return

                    return Unit(
                        unit,
                        base_units=base_unit,
                        factor=factor
                    )

    def __call__(self, factor=None, exponent=None):
        if factor is None:
            factor = self._factor
        else:
            factor *= self._factor

        if exponent is None:
            exponent = self._exponent

        return Unit(
            self._symbol,
            list(unit() for unit in self._b_units),
            factor=factor,
            exponent=exponent
        )

    @property
    def factor(self):
        factor = decimal.Decimal('1.0')

        for unit in self._b_units:
            # unit = unit()
            # unit._exponent *= self._exponent
            factor *= unit.factor

        factor *= self._factor
        factor = decimal.Decimal(str(math.pow(factor, self._exponent)))

        if self._symbol == 'sqrt':
            factor = decimal.Decimal(str(math.sqrt(factor)))

        return factor

    @property
    def exponent(self):
        return self._exponent

    def __eq__(self, other):
        # noinspection PyProtectedMember
        return other._symbol == self._symbol

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iadd__(self, other):
        self._exponent += other.exponent
        return self

    def __rmul__(self, other):
        factor = self.factor

        if isinstance(other, Unit):
            return factor * other.factor
        else:
            return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, Unit):
            symbol = self.symbol + MULTIPLIER + other.symbol
            return Unit(symbol)

        else:
            v = decimal.Decimal(str(other))
            v *= self.factor

            if isinstance(other, float):
                val = float(v)
            elif isinstance(other, decimal.Decimal):
                if '.' in str(other):
                    precision = len(str(other).split('.')[1])
                    val = round(float(v), precision)
                else:
                    val = int(round(float(v)))
            else:
                val = int(round(v))

            return val

    def __div__(self, other):
        if not isinstance(other, Unit):
            raise TypeError('you can only divide a unit into another unit')

        if (
                self._symbol in ('°R', '°C', '°F', 'K') and
                other._symbol in ('°R', '°C', '°F', 'K')
        ):

            class _Temp(object):

                def __init__(slf, from_unit, to_unit):
                    slf.from_unit = from_unit
                    slf.to_unit = to_unit

                def __rmul__(slf, othr):
                    return slf.__mul__(othr)

                def __mul__(slf, othr):
                    if isinstance(othr, Unit):
                        raise TypeError(
                            'temperature unit needs to be multiplied '
                            'into an int, float or decimal.Decimal'
                        )

                    from_unit = slf.from_unit
                    val = decimal.Decimal(str(othr))

                    if from_unit == '°R':
                        val /= decimal.Decimal('1.8')
                    elif from_unit == '°C':
                        val += decimal.Decimal('273.15')
                    elif from_unit == '°F':
                        val = (
                            (val + decimal.Decimal('459.67')) /
                            decimal.Decimal('1.8')
                        )
                    else:
                        pass

                    to_unit = slf.to_unit
                    if to_unit == '°R':
                        val *= decimal.Decimal('1.8')
                    elif to_unit == '°C':
                        val -= decimal.Decimal('273.15')
                    elif to_unit == '°F':
                        val = (
                            decimal.Decimal('1.8') *
                            val -
                            decimal.Decimal('459.67')
                        )

                    if isinstance(othr, float):
                        val = float(val)
                    elif isinstance(othr, decimal.Decimal):
                        if '.' in str(othr):
                            precision = len(str(othr).split('.')[1])
                            val = round(float(val), precision)
                        else:
                            val = int(round(float(val)))
                    else:
                        val = int(round(val))

                    return val

            return _Temp(self._symbol, other._symbol)

        f_units = list(self)
        t_units = list(other)

        unit = Unit(
            self._symbol + MULTIPLIER + other._symbol,
            base_units=f_units + t_units,
            factor=float(self.factor / other.factor)
        )

        return unit

    def __idiv__(self, other):
        if not isinstance(other, Unit):
            raise TypeError('you can only use /= with another unit')

        return Unit(self.symbol + '/' + other.symbol)

    def __truediv__(self, other):
        return self.__div__(other)

    def __itruediv__(self, other):
        return self.__idiv__(other)

    @property
    def symbol(self):
        symbol = self._symbol
        curr_exponent = ''
        repl_exponent = ''

        for i in range(len(symbol) - 1, -1, -1):
            char = symbol[i]
            if char not in SUPER_SCRIPT_MAPPING:
                break

            curr_exponent += SUPER_SCRIPT_MAPPING[char]
            repl_exponent += char

        if curr_exponent == '':
            curr_exponent = '1'

        curr_exponent = decimal.Decimal(curr_exponent)

        if curr_exponent != self._exponent:
            if int(self._exponent) != 1:
                exponent = SUPER_SCRIPT_MAPPING.convert(int(self._exponent))
            else:
                exponent = ''

            if repl_exponent:
                symbol.replace(repl_exponent, exponent)
            else:
                symbol += exponent

        return symbol

    def __bool__(self):
        return self._exponent != 0

    def __str__(self):
        if self._exponent == 0:
            return ''

        return self.symbol

    def __iter__(self):
        def iter_bases(in_base):
            bases = list(in_base)
            if not bases:
                return [in_base]

            out_bases = []
            for bse in bases:
                out_bases.extend(iter_bases(bse))

            return out_bases

        output = []

        new_bases = []
        for base in self._b_units:
            base = base()
            base._exponent *= self._exponent
            new_bases.extend(iter_bases(base))

        for unit in new_bases:
            if unit in output:
                output[output.index(unit)] += unit
            else:
                output.append(unit())

        return iter(output)


_UNIT_TO_ATTRIBUTE = {
    'Å': 'angstrom',
    'in': 'inch',
    'µ': 'micron',
    'µµ': 'bicrons',
    '¼mi²_stat': 'quarter_sq_mi_stat',
    '¼ac': 'quarter_ac',
    'mi²_stat': 'sq_mi_stat',
    'acre⋅ft': 'acre_ft',
    'm₀': 'M0',
    '\'': 'arcsecond',
    '"': 'arcminute',
    '°': 'degree',
    '%': 'percent',
    'H₂O': None,
    'O₂': None,
    'Nₚ': None,
    'aW-1': 'aW_1',
    'gemʊ': 'gemu',
    'aΩ': 'a_ohm',
    'SΩ': 'S_ohm',
    '°F⋅ft²⋅h⋅Btu_therm⁻¹': None,
    '°F⋅ft²⋅h/Btu_therm': None,
    'Ω_acoustic': 'ohm_acoustic',
    'Ω_SI': 'ohm_SI',
    'Ω': 'ohm',
    'Ω_mechanical': 'ohm_mechanical',
    '°R': 'deg_R',
    '°C': 'deg_C',
    '°F': 'deg_F'
}


def _build_base_unit(symbol):
    _BASE_UNITS[symbol] = Unit(symbol, [])

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(Unit, attr_name, _BASE_UNITS[symbol])

    else:
        setattr(Unit, symbol, _BASE_UNITS[symbol])


def _build_derived_unit(symbol, units):
    base_units = []

    for u in units.split(MULTIPLIER):
        exponent = ''
        unit = ''

        for char in u:
            if char in SUPER_SCRIPT_MAPPING:
                exponent += SUPER_SCRIPT_MAPPING[char]
            else:
                unit += char

        if exponent == '':
            exponent = '1'

        base_unit = _BASE_UNITS[unit](exponent=int(exponent))
        base_units.append(base_unit)

    _NAMED_DERIVED_UNITS[symbol] = Unit(symbol, base_units[:])

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(Unit, attr_name, _NAMED_DERIVED_UNITS[symbol])

    else:
        setattr(Unit, symbol, _NAMED_DERIVED_UNITS[symbol])


def _build_unit(symbol, factor, units):
    base_units = []

    if symbol in _BASE_UNITS:
        raise RuntimeError(
            'unit {0} already exists in _BASE_UNITS'.format(symbol)
        )

    if symbol in _NAMED_DERIVED_UNITS:
        raise RuntimeError(
            'unit {0} already exists in _NAMED_DERIVED_UNITS'.format(symbol)
        )

    if symbol in _UNITS:
        raise RuntimeError(
            'unit {0} already exists in _UNITS'.format(symbol)
        )

    for u in units.split(MULTIPLIER):
        exponent = ''
        unit = ''

        for char in u:
            if char in SUPER_SCRIPT_MAPPING:
                exponent += SUPER_SCRIPT_MAPPING[char]
            else:
                unit += char

        if exponent == '':
            exponent = '1'

        if unit in _BASE_UNITS:
            unit = _BASE_UNITS[unit]
        elif unit in _NAMED_DERIVED_UNITS:
            unit = _NAMED_DERIVED_UNITS[unit]
        elif unit in _UNITS:
            unit = _UNITS[unit]
        else:
            if not unit:
                continue
            raise RuntimeError('Sanity Check ({0})'.format(repr(unit)))

        unit = unit(exponent=int(exponent))
        base_units.append(unit)

    _UNITS[symbol] = Unit(symbol, base_units[:], factor=factor)

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(Unit, attr_name, _UNITS[symbol])

    else:
        setattr(Unit, symbol, _UNITS[symbol])


_build_base_unit('mol'),  # mole
_build_base_unit('cd'),  # candela
_build_base_unit('kg'),  # kilogram
_build_base_unit('m'),  # meter
_build_base_unit('s'),  # second
_build_base_unit('A'),  # ampere
_build_base_unit('K'),  # kelvin
# these next 2 aren't really base units but they have a factor of 1.0
_build_base_unit('bit'),  # bit
_build_base_unit('dB'),  # decible

_build_derived_unit('Hz', 's⁻¹')  # hertz
_build_derived_unit('N', 'kg⋅m⋅s⁻²')  # newton
_build_derived_unit('Pa', 'kg⋅m⁻¹⋅s⁻²')  # pascal
_build_derived_unit('J', 'kg⋅m²⋅s⁻²')  # joule
_build_derived_unit('W', 'kg⋅m²⋅s⁻³')  # watt
_build_derived_unit('C', 's⋅A')  # coulomb
_build_derived_unit('V', 'kg⋅m²⋅s⁻³⋅A⁻¹')  # volt
_build_derived_unit('F', 'kg⁻¹⋅m⁻²⋅s⁴⋅A²')  # farad
_build_derived_unit('Ω', 'kg⋅m²⋅s⁻³⋅A⁻²')  # ohm
_build_derived_unit('S', 'kg⁻¹⋅m⁻²⋅s³⋅A²')  # siemens
_build_derived_unit('Wb', 'kg⋅m²⋅s⁻²⋅A⁻¹')  # weber
_build_derived_unit('T', 'kg⋅s⁻²⋅A⁻¹')  # tesla
_build_derived_unit('H', 'kg⋅m²⋅s⁻²⋅A⁻²')  # henry
_build_derived_unit('lm', 'cd')  # lumen
_build_derived_unit('lx', 'cd⋅m⁻²')  # lux
_build_derived_unit('Bq', 's⁻¹')  # becquerel
_build_derived_unit('Gy', 'm²⋅s⁻²')  # gray
_build_derived_unit('Sv', 'm²⋅s⁻²')  # sievert
_build_derived_unit('kat', 's⁻¹⋅mol')  # katal
_build_derived_unit('r', 'm⋅m⁻¹')  # radian (angle)
_build_derived_unit('sr', 'm²⋅m⁻²'),  # steradian

# temperature

_build_unit('°R', 1.0, 'K')
_build_unit('°C', 1.0, 'K')
_build_unit('°F', 1.0, 'K')
# a.u. of length
_build_unit('au_length', 5.2917699999999994e-11, 'm')
_build_unit('am', 1e-18, 'm')  # attometer
_build_unit('Å', 1e-10, 'm')  # ångström
_build_unit('ft', 0.3048000000012192, 'm')  # foot
_build_unit('ft_survey', 0.30480061, 'm')  # US Survey foot
_build_unit('yd', 0.9144000000315285, 'm')  # yard
_build_unit('mi', 1609.344, 'm')  # mile
_build_unit('in', 0.02539999999997257, 'm')  # inch
_build_unit('µ', 1e-06, 'm')  # micron
_build_unit('arcmin', 0.000290888, 'm')  # arcmin
_build_unit('AU', 149597870700, 'm')  # astronomical unit
_build_unit('UA', 149597870700, 'm')  # astronomical unit
_build_unit('au', 149597870700, 'm')  # astronomical unit
_build_unit('agate', 0.00181428571429, 'm')  # agate
_build_unit('aln', 0.593778, 'm')  # alens
_build_unit('bcorn', 0.0084666666666667, 'm')  # barleycorn (UK)
_build_unit('a0', 5.2917699999999994e-11, 'm')  # first Bohr radius
_build_unit('rBohr', 5.2917699999999994e-11, 'm')  # first Bohr radius
_build_unit('bolt', 36.576, 'm')  # bolt (US cloth)
_build_unit('bl', 80.4672, 'm')  # blocks
_build_unit('line_UK', 0.00211667, 'm')  # button (UK)
_build_unit('line', 0.000635, 'm')  # button (US)
_build_unit('cable_int', 185.2, 'm')  # cable length (int.)
_build_unit('cable_UK', 185.318, 'm')  # cable length (UK)
_build_unit('cable', 219.456, 'm')  # cable length (US)
_build_unit('caliber', 2.54e-4, 'm')  # caliber (centiinch)
_build_unit('ch_engineer', 30.48, 'm')  # chain (engineer's)
_build_unit('ch_gunter', 20.1168, 'm')  # chain (Gunter's)
_build_unit('ch_ramsden', 30.48, 'm')  # chain (Ramsden's)
_build_unit('ch_surveyor', 20.1168, 'm')  # chain (surveyor's)
_build_unit('cbt', 0.4572, 'm')  # cubit (UK)
_build_unit('didotpoint', 0.000375972222, 'm')  # didot point
_build_unit('digit', 0.01905, 'm')  # digits
_build_unit('re', 2.81794e-15, 'm')  # electron classical radius
_build_unit('Ec', 40000000, 'm')  # Earth circumfrence
_build_unit('eel_scottish', 0.94, 'm')  # ell (Scottish)
_build_unit('eel_flemish', 0.686, 'm')  # ell (Flemish)
_build_unit('eel_french', 1.372, 'm')  # ell (French)
_build_unit('eel_polish', 0.787, 'm')  # ell (Polish)
_build_unit('eel_danish', 0.627708, 'm')  # ell (Danish)
_build_unit('eel_swedish', 0.59, 'm')  # ell (Swedish)
_build_unit('eel_german', 0.547, 'm')  # ell (German)
_build_unit('EM_pica', 0.0042175176, 'm')  # ems (pica)
_build_unit('Em', 1e+17, 'm')  # exameter
_build_unit('fath', 1.8288, 'm')  # fathom
_build_unit('fm', 1e-15, 'm')  # femtometer
_build_unit('f', 1e-15, 'm')  # fermi
_build_unit('finer', 0.1143, 'm')  # finger-cloth
_build_unit('fb', 0.022225, 'm')  # fingerbreadth
_build_unit('fod', 0.3141, 'm')  # fod
_build_unit('fbf', 91.44, 'm')  # football-field
_build_unit('fur', 201.168, 'm')  # furlong
_build_unit('pleth', 30.8, 'm')  # greek-plethron
_build_unit('std', 185.0, 'm')  # greek-stadion
_build_unit('hand', 0.1016, 'm')  # hands
_build_unit('hiMetric', 1e-05, 'm')  # himetric
_build_unit('hl', 2.4, 'm')  # horse-length
_build_unit('hvat', 1.89648384, 'm')  # hvat
_build_unit('ly', 9461000000000000.0, 'm')  # light years
_build_unit('li', 0.201168402337, 'm')  # links
_build_unit('LD', 384402000, 'm')  # lunar-distance
_build_unit('mil', 2.54e-05, 'm')  # mils
_build_unit('Mym', 10000, 'm')  # myriameters
_build_unit('nail', 0.05715, 'm')  # nails-cloth
_build_unit('NL', 5556, 'm')  # Nautical Leagues
_build_unit('NM', 1852, 'm')  # Nautical Miles
_build_unit('pace', 0.762, 'm')  # paces
_build_unit('palm', 0.0762, 'm')  # palms
_build_unit('pc', 3.0856775814914e+16, 'm')  # parsecs
_build_unit('perch', 5.0292, 'm')  # perch
_build_unit('p', 0.00423333333, 'm')  # picas
_build_unit('PX', 0.0002645833, 'm')  # pixels
_build_unit('pl', 1.6e-35, 'm')  # planck-length
_build_unit('pole', 5.0292, 'm')  # poles
_build_unit('ru', 0.04445, 'm')  # rack-unit
_build_unit('rem', 0.0042333328, 'm')  # rems
_build_unit('rd', 5.0292, 'm')  # rods
_build_unit('actus', 35.5, 'm')  # roman-actus
_build_unit('rope', 6.096, 'm')  # ropes
_build_unit('sir', 1.496e+17, 'm')  # siriometer
_build_unit('span', 0.2286, 'm')  # spans
_build_unit('twip', 1.7639e-05, 'm')  # twips
_build_unit('vr', 0.84667, 'm')  # varas
_build_unit('vst', 1066.8, 'm')  # versts
_build_unit('xu', 1.002004e-13, 'm')  # x-unit
_build_unit('zoll', 0.0254, 'm')  # zolls
_build_unit('µµ', 1e-12, 'm')  # bicrons

_build_unit('D', 9.86923e-13, 'm²')  # darcy
_build_unit('ac', 4046.8564224, 'm²')  # acre
_build_unit('acre', 4046.8564224, 'm²')  # acre
_build_unit('are', 100, 'm²')  # are
_build_unit('b', 1e-27, 'm²')  # barn
_build_unit('cirin', 0.0005067074790975, 'm²')  # circular inch
_build_unit('cirmil', 5.067074790975e-10, 'm²')  # circular mil
_build_unit('Mg_dutch', 8244.35, 'm²')  # morgen (Dutch)
_build_unit('Mg_prussian', 2532.24, 'm²')  # morgen (Prussian)
_build_unit('Mg_southafrica', 8565.3, 'm²')  # morgen (South Africa)
_build_unit('¼mi²_stat', 647497.0, 'm²')  # quarter section
_build_unit('¼ac', 1011.71, 'm²')  # rood (UK)
_build_unit('rood', 1011.71, 'm²')  # rood (UK)
_build_unit('sqmi', 2589990.0, 'm²')  # section (square statute mile)
_build_unit('mi²_stat', 2589990.0, 'm²')  # section (square statute mile)
_build_unit('outhouse', 1e-34, 'm²')  # outhouse
_build_unit('shed', 1e-52, 'm²')  # shed
_build_unit('sqch_engineer', 929.03, 'm²')  # square chain (engineer's)
_build_unit('sqch_gunter', 404.686, 'm²')  # square chain (Gunter's)

_build_unit('acre⋅ft', 1233.48, 'm³')  # acre foot
_build_unit('bag', 0.109106, 'm³')  # bag (UK)
_build_unit('bbl_UScranb', 0.095471, 'm³')  # barrel (US, cranb.)
_build_unit('bbl', 0.1192404712, 'm³')  # barrel (US)
_build_unit('bbl_USpetrol', 0.1589872949, 'm³')  # barrel (US petrol)
_build_unit('bbl_UK', 0.16365924, 'm³')  # barrel (UK)
_build_unit('FBM', 0.002359737, 'm³')  # board foot measure
_build_unit('bouteille', 0.000757682, 'm³')  # bouteille
_build_unit('bk_UK', 0.0181844, 'm³')  # bucket (UK)
_build_unit('bu_UK', 0.036368700000000004, 'm³')  # bushel (UK)
_build_unit('bu_US', 0.0352391, 'm³')  # bushel (US, dry)
_build_unit('bt_UK', 0.490978, 'm³')  # butt (UK)
_build_unit('chal_UK', 1.30927, 'm³')  # chaldron (UK)
_build_unit('cc', 1.00238e-06, 'm³')  # cubic centimeter (Mohr cubic centimeter)
_build_unit('l', 0.001, 'm³')  # Liter
_build_unit('L', 0.001, 'm³')  # Liter
_build_unit('gal', 0.00378541178, 'm³')  # Gallon (US)
_build_unit('gal_UK', 4.54609e-3, 'm³')  # Gallon (UK)
_build_unit('qt', 0.000946352946, 'm³')  # Quart (US)
_build_unit('qt_UK', 0.0011365225, 'm³')  # Quart (UK)
_build_unit('pt', 0.000473176473, 'm³')  # Pint (US)
_build_unit('pt_UK', 0.00056826125, 'm³')  # Pint (UK)
_build_unit('floz', 2.95735296875e-05, 'm³')  # Fluid Ounce (US)
_build_unit('floz_UK', 2.84130625e-05, 'm³')  # Fluid Ounce (UK)
_build_unit('cran', 0.170478, 'm³')  # cran
_build_unit('dr', 3.6967e-06, 'm³')  # dram
_build_unit('st', 1.0, 'm³')  # stere
_build_unit('gi', 0.0001182941, 'm³')  # gill (US)
_build_unit('gi_UK', 0.0001420653, 'm³')  # gill (UK)
_build_unit('cup', 0.00025, 'm³')  # cup (US)
_build_unit('cup_UK', 0.0002841306, 'm³')  # cup (UK)
_build_unit('dstspn', 9.8578e-06, 'm³')  # dessertspoon (US)
_build_unit('dstspn_UK', 1.18388e-05, 'm³')  # dessertspoon (UK)
_build_unit('tbsp', 1.5e-05, 'm³')  # tablespoon (US)
_build_unit('tbsp_UK', 1.77582e-05, 'm³')  # tablespoon (UK)
_build_unit('tsp', 5e-06, 'm³')  # teaspoon (US)
_build_unit('tsp_UK', 5.9194e-06, 'm³')  # teaspoon (UK)

# electron rest mass (a.u. of mass)
_build_unit('m₀', 9.10939e-31, 'kg')
# electron rest mass (a.u. of mass)
_build_unit('me', 9.10939e-31, 'kg')
_build_unit('u_dalton', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('u', 1.660540199e-27, 'kg')  # atomic mass unit
_build_unit('uma', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('Da', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('dr_troy', 0.00388793, 'kg')  # dram (troy)
_build_unit('dr_apoth', 0.00388793, 'kg')  # dram or drachm (apothecary)
# dram or drachm (avoirdupois)
_build_unit('dr_avdp', 0.001771845195312458, 'kg')
_build_unit('g', 0.001, 'kg')  # gram
_build_unit('lb', 0.45359237001003544, 'kg')  # pound
_build_unit('oz', 0.028349523124984257, 'kg')  # ounce
_build_unit('t_long', 1016.0469088, 'kg')  # ton (long)
_build_unit('t_short', 907.18474, 'kg')  # ton(short)
_build_unit('t', 1000.0, 'kg')  # metric ton
_build_unit('dwt', 0.0015551738, 'kg')  # pennyweight
_build_unit('kip', 453.59237, 'kg')  # kip
_build_unit('gr', 6.479891000000013e-5, 'kg')  # grain
_build_unit('slug', 14.5939029372, 'kg')  # geepound (slug)
_build_unit('t_assay', 0.029167, 'kg')  # assay ton
_build_unit('Da_12C', 1.66054e-27, 'kg')  # atomic unit of mass (¹²C)
_build_unit('Da_16O', 1.66001e-27, 'kg')  # atomic unit of mass (¹⁶O)
_build_unit('Da_1H', 1.67353e-27, 'kg')  # atomic unit of mass (¹H)
_build_unit('avogram', 1.66036e-24, 'kg')  # avogram
_build_unit('bag_UK', 42.6377, 'kg')  # bag (UK, cement)
_build_unit('ct', 0.0002, 'kg')  # carat (metric)
_build_unit('ct_troy', 0.000205197, 'kg')  # carat (troy)
_build_unit('cH', 45.3592, 'kg')  # cental
_build_unit('cwt', 100.0, 'kg')  # quintal

# a.u. of time
_build_unit('au_time', 2.4188800000000002e-17, 's')
_build_unit('blink', 0.864, 's')  # blink
_build_unit('d', 86400.0, 's')  # day
_build_unit('d_sidereal', 86164.0, 's')  # day (sidereal)
_build_unit('fortnight', 1209600.0, 's')  # fortnight
_build_unit('h', 3600.0, 's')  # hour
_build_unit('min', 60.0, 's')  # minute
_build_unit('mo', 2592000.0, 's')  # month (30 days)
_build_unit('mo_sidereal', 2360590.0, 's')  # month (sidereal)
_build_unit('mo_mean', 2628000.0, 's')  # month (solar mean)
_build_unit('mo_synodic', 2551440.0, 's')  # month (synodic), lunar month
_build_unit('shake', 1e-08, 's')  # shake
_build_unit('week', 604800.0, 's')  # week
_build_unit('wink', 3.33333e-10, 's')  # wink
_build_unit('a_astr', 31557900.0, 's')  # year (astronomical), Bessel year
_build_unit('a', 31536000.0, 's')  # year (calendar)
_build_unit('y', 31536000.0, 's')  # year (calendar)
_build_unit('a_sidereal', 31558200.0, 's')  # year (sidereal)
_build_unit('a_mean', 31557600.0, 's')  # year (solar mean)
_build_unit('a_tropical', 31556900.0, 's')  # year (tropical)

_build_unit('bd', 1.02, 'cd')  # bougie d&egrave;cimale
_build_unit('bi', 1.0, 'cd')  # bougie international
_build_unit('c_int', 1.01937, 'cd')  # candle (int.)
_build_unit('c', 1.0, 'cd')  # candle (new unit)
_build_unit('carcel', 10.0, 'cd')  # carcel
_build_unit('HK', 0.903, 'cd')  # hefner unit (hefnerkerze)
_build_unit('violle', 20.4, 'cd')  # violle

_build_unit('entities', 1.66054e-24, 'mol')  # entities
_build_unit('SCF', 1.19531, 'mol')  # standard cubic foot
_build_unit('SCM', 44.6159, 'mol')  # standard cubic meter

_build_unit('\'', 0.000290888, 'r')  # arc minute (minute of arc)
_build_unit('"', 4.84814e-06, 'r')  # arc second (second of arc)
_build_unit('pid', 6.28319, 'r')  # circumference
_build_unit('°', 0.0174533, 'r')  # degree
_build_unit('gon', 0.015708, 'r')  # gon
_build_unit('grade', 0.015708, 'r')  # grade
_build_unit('ah', 0.261799, 'r')  # hour of arc
_build_unit('%', 0.00999967, 'r')  # percent
_build_unit('rev', 6.28319, 'r')  # revolution
_build_unit('sign', 0.523599, 'r')  # sign

_build_unit('B', 8, 'bit')  # byte
_build_unit('Gib', 1073740000.0, 'bit')  # gigabinarybit (gibibit)
_build_unit('GiB', 8589930000.0, 'bit')  # gigabinarybyte (gibibyte)
_build_unit('Gb', 1000000000.0, 'bit')  # gigabit
_build_unit('GB', 8000000000.0, 'bit')  # gigabyte
_build_unit('Kib', 1024, 'bit')  # kilobinarybit (kibibit)
_build_unit('KiB', 8192, 'bit')  # kilobinarybyte (kibibyte)
_build_unit('Kb', 1000, 'bit')  # kilobit
_build_unit('KB', 8000, 'bit')  # kilobyte
_build_unit('Mib', 1048580.0, 'bit')  # megabinarybit (mebibit)
_build_unit('MiB', 8388610.0, 'bit')  # megabinarybyte (mebibyte)
_build_unit('Mb', 1000000.0, 'bit')  # megabit
_build_unit('MB', 8000000.0, 'bit')  # megabyte
_build_unit('Tib', 1099510000000.0, 'bit')  # terabinarybit (tebibit)
_build_unit('TiB', 8796090000000.0, 'bit')  # terabinarybyte (tebibyte)
_build_unit('Tb', 100000000000.0, 'bit')  # terabit
_build_unit('TB', 8000000000000.0, 'bit')  # terabyte

_build_unit('aW', 1e-07, 'W')  # abwatt (emu of power)
_build_unit('hp', 745.7, 'W')  # horsepower (550 ft-lbf/s)
_build_unit('hp_boiler', 9809.5, 'W')  # horsepower (boiler)
_build_unit('hp_British', 745.7, 'W')  # horsepower (British)
_build_unit('cv', 735.499, 'W')  # horsepower (cheval-vapeur)
_build_unit('hp_cheval', 735.499, 'W')  # horsepower (cheval-vapeur)
_build_unit('hp_electric', 746.0, 'W')  # horsepower (electric)
_build_unit('hp_metric', 735.499, 'W')  # horsepower (metric)
_build_unit('hp_water', 746.043, 'W')  # horsepower (water)
_build_unit('prony', 98.0665, 'W')  # prony

_build_unit('at', 98066.5, 'Pa')  # atmosphere (technical)
_build_unit('atm', 101325.0, 'Pa')  # atmosphere (standard)
_build_unit('bar', 100000.0, 'Pa')  # bar
_build_unit('Ba', 0.1, 'Pa')  # Bayre
_build_unit('p_P', 4.63309e+113, 'Pa')  # Planck pressure
_build_unit('cgs', 0.1, 'Pa')  # centimeter-gram-second
_build_unit('torr', 133.32236842, 'Pa')  # Torr
_build_unit('pz', 1000.0, 'Pa')  # pieze
_build_unit('Hg', 133322.368421, 'Pa')  # Hg (mercury) (0°C)
_build_unit('H₂O', 9806.65, 'Pa')  # H₂O (water) (0°C)
_build_unit('H2O', 9806.65, 'Pa')  # H₂O (water) (0°C)
_build_unit('Aq', 9806.65, 'Pa')  # H₂O (water) (0°C)
_build_unit('O₂', 12.677457000000462, 'Pa')  # O₂ (air) (0°C)
_build_unit('O2', 12.677457000000462, 'Pa')  # O₂ (air) (0°C)
_build_unit('ksi', 6894757.293200044, 'Pa')  # kilopound force per square inch
_build_unit('psi', 6894.7572932, 'Pa')  # pound force per square inch

_build_unit('psf', 47.88025897999996, 'Pa')  # pound force per square foot
_build_unit('osi', 430.9223300000048, 'Pa')  # ounce force per square inch

_build_unit('kerma', 1.0, 'Gy')  # kerma
_build_unit('Mrd', 10000.0, 'Gy')  # megarad
_build_unit('rad', 0.01, 'Gy')  # radian (radioactive)

_build_unit('B_power', 10.0, 'dB')  # bel (power)
_build_unit('B_voltage', 5.0, 'dB')  # bel (voltage)
_build_unit('dB_power', 1.0, 'dB')  # decibel (power)
_build_unit('dB_voltage', 0.5, 'dB')  # decibel (voltage)
_build_unit('Nₚ', 4.34294, 'dB')  # neper

# a.u. of magnetic field
_build_unit('au_mf', 235052.0, 'T')
_build_unit('Gs', 1e-05, 'T')  # gauss

_build_unit('M', 1e-09, 'Wb')  # maxwell

# a.u. of charge
_build_unit('au_charge', 1.60218e-19, 'C')
_build_unit('aC', 10, 'C')  # abcoulomb (emu of charge)
_build_unit('esc', 1.6022e-19, 'C')  # electronic charge
_build_unit('esu', 3.336e-06, 'C')  # electrostatic unit
_build_unit('Fr', 3.33564e-10, 'C')  # franklin
_build_unit('statC', 3.35564e-10, 'C')  # statcoulomb

_build_unit('aS', 1000000000.0, 'S')  # abmho (emu of conductance)
_build_unit('aW-1', 1000000000.0, 'S')  # abmho (emu of conductance)
_build_unit('gemʊ', 1e-07, 'S')  # gemmho
_build_unit('mho', 1.0, 'S')  # mho
_build_unit('statmho', 1.11265e-12, 'S')  # statmho

_build_unit('aH', 1e-10, 'H')  # abhenry (emu of inductance)
_build_unit('statH', 898755000000.0, 'H')  # stathenry

# a.u. of electric potential
_build_unit('au_ep', 27.2114, 'V')
_build_unit('aV', 1e-09, 'V')  # abvolt (emu of electric potential)
_build_unit('statV', 299.792, 'V')  # statvolt
_build_unit('V_mean', 1.00034, 'V')  # volt (mean)
_build_unit('V_US', 1.00033, 'V')  # volt (US)

_build_unit('aΩ', 1e-10, 'Ω')  # abohm (emu of resistance)
_build_unit('SΩ', 0.96, 'Ω')  # siemens (resistance)
_build_unit('statohm', 898755000000.0, 'Ω')  # statohm

# a.u. of energy
_build_unit('au_energy', 4.35975e-18, 'J')
_build_unit('bboe', 6120000000.0, 'J')  # barrel oil equivalent
_build_unit('BeV', 1.60218e-10, 'J')  # BeV (billion eV)
_build_unit('Btu_ISO', 1055.06, 'J')  # British thermal unit (ISO)
_build_unit('Btu_IT', 1055.06, 'J')  # British thermal unit (IT)
_build_unit('Btu_mean', 1055.87, 'J')  # British thermal unit (mean)
_build_unit('Btu_therm', 1054.35, 'J')  # British thermal unit (thermochemical)
_build_unit('cal_15', 4.185, 'J')  # calorie (15°C)
_build_unit('cal_4', 4.2045, 'J')  # calorie (4°C)
_build_unit('Cal', 4180.0, 'J')  # Calorie (diet kilocalorie)
_build_unit('kcal', 4180.0, 'J')  # Calorie (diet kilocalorie)
_build_unit('cal_IT', 4.18674, 'J')  # calorie (IT) (International Steam Table)
_build_unit('cal_mean', 4.19002, 'J')  # calorie (mean)
_build_unit('cal_therm', 4.184, 'J')  # calorie (thermochemical)
_build_unit('Chu', 1899.18, 'J')  # Celsius-heat unit
_build_unit('eV', 1.60218e-19, 'J')  # electronvolt
_build_unit('erg', 1e-07, 'J')  # erg
_build_unit('Eh', 4.35975e-18, 'J')  # hartree

# a.u. of force
_build_unit('au_force', 8.23873e-08, 'N')
_build_unit('crinal', 0.1, 'N')  # crinal
_build_unit('dyn', 1e-05, 'N')  # dyne
_build_unit('gf', 0.00980665, 'N')  # gram force
_build_unit('kgf', 9.80665, 'N')  # kilogram force
_build_unit('kgp', 9.80665, 'N')  # kilogram force
_build_unit('grf', 0.6355, 'N')  # grain force
_build_unit('kp', 9.80665, 'N')  # kilopond
_build_unit('kipf', 4448.22, 'N')  # kilopound force (kip force)
_build_unit('lbf', 4.4482216, 'N')  # Poundal force (US) (pound force)
_build_unit('pdl', 0.138255, 'N')  # Poundal force (UK)
_build_unit('slugf', 143.117, 'N')  # slug force
_build_unit('tf_long', 9964.02, 'N')  # ton force (long)
_build_unit('tf_metric', 9806.65, 'N')  # ton force (metric)
_build_unit('tf_short', 8896.44, 'N')  # ton force (short)
_build_unit('ozf', 0.278014, 'N')  # ounce force

# a.u. of electric current
_build_unit('au_ec', 0.00662362, 'A')
_build_unit('abA', 10, 'A')  # abampere
_build_unit('Bi', 10, 'A')  # biot
_build_unit('edison', 100.0, 'A')  # edison
_build_unit('statA', 3.35564e-10, 'A')  # statampere
_build_unit('gilbert', 0.79577, 'A')  # gilbert
_build_unit('pragilbert', 11459.1, 'A')  # pragilbert

_build_unit('cps', 1.0, 'Hz')  # cycles per second

_build_unit('Kt', 0.0416667, '')  # carat (karat)
_build_unit('ppb', 1e-10, '')  # part per billion
_build_unit('pph', 0.001, '')  # part per hundred
_build_unit('pphm', 1e-09, '')  # part per hundred million
_build_unit('ppht', 1e-06, '')  # part per hundred thousand
_build_unit('ppm', 1e-07, '')  # part per million
_build_unit('ppq', 1e-15, '')  # part per quadrillion
_build_unit('ppt_tera', 1e-13, '')  # part per tera
_build_unit('ppt', 0.001, '')  # part per thousand

_build_unit('Ci', 37000000000.0, 'Bq')  # curie

_build_unit('sp', 12.5664, 'sr')  # spat

_build_unit('gy', 1000, 'kg⋅m⁻³')  # specific gravity

_build_unit('lbm', 0.45359237001003544, 'kg⋅m²')  # pound mass

_build_unit('Ω_mechanical', 1.0, 'Pa⋅s⋅m⁻³')  # ohm (mechanical, SI)

_build_unit('perm_0C', 5.72135e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (0°C)
_build_unit('perm_23C', 5.74525e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (23°C)
_build_unit('permin_0C', 1.45322e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (0°C)
_build_unit('permin_23C', 1.45929e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (23°C)
_build_unit('permmil_0C', 1.45322e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (0°C)
_build_unit('permmil_23C', 1.45929e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (23°C)

_build_unit('brewster', 1e-12, 'm²⋅N⁻¹')  # brewster

_build_unit('aF', 1000000000.0, 'F')  # abfarad (emu of electric capacitance)
_build_unit('jar', 1.11111e-09, 'F')  # jar
_build_unit('statF', 1.11265e-12, 'F')  # statfarad

_build_unit('P', 0.1, 'Pa⋅s')  # Poise
_build_unit('Pl', 1.0, 'Pa⋅s')  # poiseuille
_build_unit('reyn', 6894.76, 'Pa⋅s')  # reynolds (reyns)

_build_unit('clo', 0.15482, 'K⋅m²⋅W⁻¹')  # clo
_build_unit('°F⋅ft²⋅h⋅Btu_therm⁻¹', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
_build_unit('°F⋅ft²⋅h/Btu_therm', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
_build_unit('RSI', 1.0, 'K⋅m²⋅W⁻¹')  # RSI (metric R-value)
_build_unit('tog', 0.1, 'K⋅m²⋅W⁻¹')  # tog

_build_unit('Bz', 1.0, 'm⋅s⁻¹')  # benz
_build_unit('kn_noeud', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
_build_unit('knot_noeud', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
_build_unit('mpy', 8.04327e-13, 'm⋅s⁻¹')  # mil per year
_build_unit('kn', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
_build_unit('knot', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
_build_unit('c_light', 299792000.0, 'm⋅s⁻¹')  # speed of light

_build_unit('dioptre', 1.0, 'm⁻¹')  # dioptre
_build_unit('mayer', 1000.0, 'J⋅kg⁻¹⋅K⁻¹')  # mayer
_build_unit('helmholtz', 3.336e-10, 'C⋅m⁻¹')  # helmholtz

_build_unit('mired', 1000000.0, 'K⁻¹')  # mired

_build_unit('cumec', 1.0, 'm³⋅s⁻¹')  # cumec (musec)
_build_unit('gph_UK', 1.2627999999999998e-06, 'm³⋅s⁻¹')  # gallon (UK) per hour
_build_unit('gpm_UK', 7.57682e-05, 'm³⋅s⁻¹')  # gallon (UK) per minute
_build_unit('gps_UK', 0.004546090000000001, 'm³⋅s⁻¹')  # gallon (UK) per second
_build_unit('lusec', 0.001, 'm³⋅s⁻¹')  # lusec
_build_unit('CO', 0.000707921, 'm³⋅s⁻¹')  # miner's inch

_build_unit('gph', 1.0, 'gal⋅h⁻¹')  # gallon (US, liq.) per hour
_build_unit('gpm', 1.0, 'gal⋅min⁻¹')  # gallon (US, liq.) per minute
# gallon (US, liq.) per second
_build_unit('gps', 0.0037854100000000003, 'gal⋅s⁻¹')

_build_unit('G', 9.80665, 'm⋅s⁻²')  # g (gravitational acceleration)
_build_unit('rps', 1.0, 'rev⋅s⁻¹')  # revolution per second

_build_unit('den', 1.11111e-07, 'kg⋅m⁻¹')  # denier
_build_unit('denier', 1.11111e-07, 'kg⋅m⁻¹')  # denier
_build_unit('te', 1e-07, 'kg⋅m⁻¹')  # tex

# a.u. of linear momentum
_build_unit('au_lm', 1.99285e-24, 'N⋅s')

_build_unit('c_power', 12.5664, 'cd⋅sr')  # candlepower (spherical)

_build_unit('asb', 0.31831, 'cd⋅m⁻²')  # apostilb
# _build_unit('L', 31831.0, 'cd⋅m⁻²')  # lambert
_build_unit('nit', 1.0, 'cd⋅m⁻²')  # nit
_build_unit('sb', 10000.0, 'cd⋅m⁻²')  # stilb

_build_unit('oe', 79.5775, 'A⋅m⁻¹')  # oersted
_build_unit('praoersted', 11459.1, 'A⋅m⁻¹')  # praoersted

# a.u. of magnetic dipole moment
_build_unit('au_mdm', 1.8548e-23, 'J⋅T⁻¹')
_build_unit('Gal', 0.001, 'm⋅s⁻²')  # galileo
_build_unit('leo', 10, 'm⋅s⁻²')  # leo
_build_unit('gn', 9.80665, 'm⋅s⁻²')  # normal acceleration

_build_unit('Ω_acoustic', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)
_build_unit('Ω_SI', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)

_build_unit('rayl_cgs', 10, 'kg⋅m⁻²⋅s⁻¹')  # rayl (cgs)
_build_unit('rayl_MKSA', 1, 'kg⋅m⁻²⋅s⁻¹')  # rayl (MKSA)

_build_unit('Na', 6.02214e+23, 'mol⁻¹')  # avogadro

# a.u. of action
_build_unit('au_action', 1.05457e-34, 'J⋅s')
# a.u. of angular momentum
_build_unit('au_am', 1.05457e-34, 'J⋅s')
_build_unit('planck', 1, 'J⋅s')  # planck

_build_unit('rpm', 1, 'rev⋅min⁻¹')  # revolution per minute

# a.u. of charge density
_build_unit('au_cd', 1081200000000.0, 'C⋅m⁻³')

_build_unit('Ah', 1.0, 'A⋅h⁻¹')  # ampere-hour

_build_unit('F_12C', 96485.3, 'C⋅mol⁻¹')  # faraday (based on ¹²C)
_build_unit('F_chemical', 96495.7, 'C⋅mol⁻¹')  # faraday (chemical)
_build_unit('F_physical', 96512.9, 'C⋅mol⁻¹')  # faraday (physical)

_build_unit('roc', 100, 'S⋅m⁻¹')  # reciprocal ohm per centimeter
_build_unit('rom', 1.0, 'S⋅m⁻¹')  # reciprocal ohm per meter

# a.u. of electric quadrupole moment
_build_unit('au_eqm', 4.48655e-40, 'C⋅m²')
# a.u. of electric dipole moment
_build_unit('au_edm', 8.47836e-30, 'C⋅m')
# a.u. of electric field strength
_build_unit('au_efs', 514221000000.0, 'V⋅m⁻¹')

_build_unit('Jy', 1e-27, 'W⋅m⁻²⋅Hz')  # jansky

_build_unit('MGOe', 7957.75, 'J⋅m⁻³')  # megagauss-oersted (MGOe)
_build_unit('Ly', 41850.0, 'J⋅m⁻²')  # langley (energy)
_build_unit('ly_langley', 697.5, 'W⋅m⁻²')  # langley (flux)

_build_unit('ue', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy
_build_unit('eu', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy

_build_unit('UI', 1.66667e-08, 'mol⋅s⁻¹')  # international unit
_build_unit('IU', 1.66667e-08, 'mol⋅s⁻¹')  # international unit


_build_unit('ph', 0.01, 'lm⋅m⁻²')  # phot

_build_unit('cSt', 1e-07, 'm²⋅s⁻¹')  # centistokes
_build_unit('St', 1e-05, 'm²⋅s⁻¹')  # stokes

_build_unit('fps', 1.0, 'ft⋅s⁻¹')  # foot per second
_build_unit('fpm', 1.0, 'ft⋅min⁻¹')  # foot per minute
_build_unit('fph', 1.0, 'ft⋅h⁻¹')  # foot per hour

_build_unit('ips', 1.0, 'in⋅s⁻¹')  # inch per second

_build_unit('mph', 1.0, 'mi⋅h⁻¹')  # mile (stat.) per hour

_build_unit('cfm', 1.0, 'ft³⋅min⁻¹')  # cubic foot per minute
_build_unit('cfs', 1.0, 'ft³⋅s⁻¹')  # cubic foot per second


Unit.mm = Unit('mm')
Unit.cm = Unit('cm')
Unit.km = Unit('km')


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

    cf_from, cf_to = _get_conversion_factor(from_unit, to_unit)
    value *= (cf_from / cf_to)

    return value


def _get_conversion_factor(from_unit, to_unit):
    from_units = Unit(from_unit, [])
    to_units = Unit(to_unit, [])

    def combine_units(in_units):
        out_units = []
        for unit in in_units:
            base_units = list(unit)
            for b_unit in base_units:
                if b_unit in out_units:
                    out_units[out_units.index(b_unit)] += b_unit
                else:
                    out_units.append(b_unit)

        str_units = []

        for unit in out_units:
            if unit:
                str_units.append(str(unit))

        str_unit = MULTIPLIER.join(sorted(str_units))
        return str_unit

    f_unit = combine_units(from_units)
    t_unit = combine_units(to_units)

    if f_unit != t_unit:
        raise ValueError('Units "{0}" and "{1}" are not compatible'.format(
            from_unit,
            to_unit
        ))

    return from_units, to_units


def main():
    test_units = (
        (75.1, '°F', '°C'),
        (71, 'in³', 'mm³'),
        (129.5674, 'in²', 'mm²'),
        (3.657, 'gal', 'l'),
        (500.679, 'g', 'lb'),
        (132.7, 'mi/h', 'km/h'),
        (1.0, 'P', 'Pa s'),
        (56.0, 'in', 'cm'),
        (50.34, 'ftHg', 'mmHg'),
        (50.34, 'inH2O', 'cmH2O'),
        (50.34, 'inHg', 'psi')
    )
    for vl, t_unit, f_unit in test_units:
        v1 = convert(vl, t_unit, f_unit)

        print('as {0}: {1} {2} = {3} {4}'.format(
            vl.__class__.__name__,
            vl, t_unit, v1, f_unit
        ))
        for i in range(2, 12, 4):

            vl2 = str(round(float(vl), i))
            vl2 += '0' * (i - len(vl2.split('.')[1]))
            vl2 = decimal.Decimal(vl2)
            v1 = convert(vl2, t_unit, f_unit)
            print('presicion of {0}: {1} {2} = {3} {4}'.format(
                i, vl2, t_unit, v1, f_unit
            ))

        print()

    print()

    f_unit = Unit('°F')
    c_unit = Unit('°C')
    out_val = 75.1 * (f_unit / c_unit)
    print('{0} {1} = {2} {3}'.format(75.1, '°F', out_val, '°C'))

    inch_unit = Unit('in', exponent=3)
    mm_unit = Unit('mm', exponent=3)
    out_val = 71 * (inch_unit / mm_unit)
    print('{0} {1} = {2} {3}'.format(71, 'in³', out_val, 'mm³'))

    inch_unit = Unit('in', exponent=2)
    mm_unit = Unit('mm', exponent=2)
    out_val = 129.5674 * (inch_unit / mm_unit)
    print('{0} {1} = {2} {3}'.format(129.5674, 'in²', out_val, 'mm²'))

    gal_unit = Unit('gal')
    l_unit = Unit('l')
    out_val = 3.657 * (gal_unit / l_unit)
    print('{0} {1} = {2} {3}'.format(3.657, 'gal', out_val, 'l'))

    g_unit = Unit('g')
    lb_unit = Unit('lb')
    out_val = 500.679 * (g_unit / lb_unit)
    print('{0} {1} = {2} {3}'.format(500.679, 'g', out_val, 'lb'))

    mi_unit = Unit('mi')
    h_unit = Unit('h')
    km_unit = Unit('km')
    mi_unit /= h_unit
    km_unit /= h_unit
    out_val = 132.7 * (mi_unit / km_unit)
    print('{0} {1} = {2} {3}'.format(132.7, 'mi/h', out_val, 'km/h'))

    P_unit = Unit('P')
    Pa_unit = Unit('Pa')
    s_unit = Unit('s')
    Pas_unit = Pa_unit * s_unit
    out_val = 1.0 * (P_unit / Pas_unit)
    print('{0} {1} = {2} {3}'.format(1.0, 'P', out_val, 'Pa s'))

    inch_unit = Unit('in')
    mm_unit = Unit('cm')
    out_val = 56.0 * (inch_unit / mm_unit)
    print('{0} {1} = {2} {3}'.format(56.0, 'in', out_val, 'cm'))

    ftHg_unit = Unit('ftHg')
    mmHg_unit = Unit('mmHg')
    out_val = 50.34 * (ftHg_unit / mmHg_unit)
    print('{0} {1} = {2} {3}'.format(50.34, 'ftHg', out_val, 'mmHg'))

    inH2O_unit = Unit('inH2O')
    cmH2O_unit = Unit('cmH2O')
    out_val = 50.34 * (inH2O_unit / cmH2O_unit)
    print('{0} {1} = {2} {3}'.format(50.34, 'inH2O', out_val, 'cmH2O'))

    inHg_unit = Unit('inHg')
    psi_unit = Unit('psi')
    out_val = 50.34 * (inHg_unit / psi_unit)
    print('{0} {1} = {2} {3}'.format(50.34, 'inHg', out_val, 'psi'))

    print()
    print()

    out_val = 75.1 * (Unit.deg_F() / Unit.deg_C())
    print('{0} {1} = {2} {3}'.format(75.1, '°F', out_val, '°C'))

    out_val = 71 * (Unit.inch(exponent=3) / Unit.mm(exponent=3))
    print('{0} {1} = {2} {3}'.format(71, 'in³', out_val, 'mm³'))

    out_val = 129.5674 * (Unit.inch(exponent=2) / Unit.mm(exponent=2))
    print('{0} {1} = {2} {3}'.format(129.5674, 'in²', out_val, 'mm²'))

    out_val = 3.657 * (Unit.gal / Unit.l)
    print('{0} {1} = {2} {3}'.format(3.657, 'gal', out_val, 'l'))

    out_val = 500.679 * (Unit.g / Unit.lb)
    print('{0} {1} = {2} {3}'.format(500.679, 'g', out_val, 'lb'))

    mi_unit = Unit.mi
    km_unit = Unit.km
    mi_unit /= Unit.h
    km_unit /= Unit.h
    out_val = 132.7 * (mi_unit / km_unit)
    print('{0} {1} = {2} {3}'.format(132.7, 'mi/h', out_val, 'km/h'))

    out_val = 1.0 * (Unit.P / (Unit.Pa * Unit.s))
    print('{0} {1} = {2} {3}'.format(1.0, 'P', out_val, 'Pa s'))

    out_val = 56.0 * (Unit.inch / Unit('cm'))
    print('{0} {1} = {2} {3}'.format(56.0, 'in', out_val, 'cm'))

    out_val = 50.34 * ((Unit.ft * Unit.Hg) / (Unit.mm * Unit.Hg))
    print('{0} {1} = {2} {3}'.format(50.34, 'ftHg', out_val, 'mmHg'))

    out_val = 50.34 * ((Unit.inch * Unit.H2O) / (Unit.cm * Unit.H2O))
    print('{0} {1} = {2} {3}'.format(50.34, 'inH2O', out_val, 'cmH2O'))

    out_val = 50.34 * ((Unit.inch * Unit.Hg) / Unit.psi)
    print('{0} {1} = {2} {3}'.format(50.34, 'inHg', out_val, 'psi'))


if __name__ == '__main__':
    main()
