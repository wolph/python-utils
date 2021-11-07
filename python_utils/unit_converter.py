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
SUP_DECIMAL = chr(0x00B7)  # type: str # ·  (¹·²)
SUP_MINUS = chr(0x207B)  # type: str # ⁻ (⁻¹)
SUP_R = chr(0x036C)  # type: str # ͬ

MULTIPLIER = chr(0x22C5)  # type: str # N⋅J
QUARTER = chr(0x00BC)  # type: str  # ¼
OHM = chr(0x2126)  # type: str # Ω
DEGREE = chr(0x00B0)  # type: str # °
PI = chr(0x03C0)  # type: str # π

SUB_1 = chr(0x2081)  # type: str # ₁
SUB_2 = chr(0x2082)  # type: str # ₂
SUB_4 = chr(0x2084)  # type: str # ₄
SUB_5 = chr(0x2085)  # type: str # ₅
SUB_6 = chr(0x2086)  # type: str # ₆
SUB_A = chr(0x2090)  # type: str # ₐ

SUPER_SCRIPT_MAPPING = {
    SUP_0: '0',
    SUP_1: '1',
    SUP_2: '2',
    SUP_3: '3',
    SUP_4: '4',
    SUP_5: '5',
    SUP_6: '6',
    SUP_7: '7',
    SUP_8: '8',
    SUP_9: '9',
    SUP_MINUS: '-',
    SUP_DECIMAL: '.',
}

SUPER_SCRIPT_MAPPING_REVERSE = {v: k for k, v in SUPER_SCRIPT_MAPPING.items()}

_BASE_UNITS = {}
_NAMED_DERIVED_UNITS = {}
_UNITS = {}


class _Unit(object):

    def __init__(self, symbol, base_units, factor=1.0, exponent=1):
        self._symbol = symbol
        self._factor = decimal.Decimal(str(factor))
        self._exponent = exponent
        self._b_units = base_units

        if not base_units and symbol not in _BASE_UNITS:
            self._b_units = self._process_unit(symbol)

    def _process_unit(
            self,
            unit,
            first_pass=True  # type: Optional[bool]
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
                    found_units.extend(self._process_unit(ut))

            base_unit = _Unit(unit, base_units=found_units)

            if i > 0:
                self._exponent = -self._exponent

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

                    return _Unit(
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

        return _Unit(
            self._symbol,
            list(unit() for unit in self._b_units),
            factor=factor,
            exponent=exponent
        )

    @property
    def factor(self):
        factor = decimal.Decimal('1.0')

        for unit in self._b_units:
            unit = unit()
            unit._exponent *= self._exponent

            factor *= unit.factor

        factor *= self._factor

        return decimal.Decimal(str(math.pow(factor, self._exponent)))

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

        if isinstance(other, _Unit):
            return factor * other.factor
        else:
            return other * factor

    # def __imul__(self, other):
    #     factor = self.factor
    #
    #     if isinstance(other, _Unit):
    #         return factor * other.factor
    #     else:
    #         return other * factor

    @property
    def symbol(self):
        symbol = self._symbol
        curr_exponent = ''
        repl_exponent = ''

        for i in range(len(symbol), -1, -1):
            char = symbol[i]
            if char not in SUPER_SCRIPT_MAPPING:
                break

            curr_exponent += SUPER_SCRIPT_MAPPING[char]
            repl_exponent += char

        if curr_exponent == '':
            curr_exponent = '1'

        curr_exponent = decimal.Decimal(curr_exponent)

        if curr_exponent != self._exponent:
            exponent = ''
            if self._exponent != 1:
                for char in str(self._exponent):
                    exponent += SUPER_SCRIPT_MAPPING_REVERSE[char]

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


def _build_base_unit(symbol):
    _BASE_UNITS[symbol] = _Unit(symbol, [])


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

    _NAMED_DERIVED_UNITS[symbol] = _Unit(symbol, base_units[:])


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

    _UNITS[symbol] = _Unit(symbol, base_units[:], factor=factor)


_build_base_unit('mol'),  # mole
_build_base_unit('cd'),  # candela
_build_base_unit('kg'),  # kilogram
_build_base_unit('m'),  # meter
_build_base_unit('s'),  # second
_build_base_unit('A'),  # ampere
_build_base_unit('K'),  # kelvin
_build_base_unit('bit'),  # bit
# these next 4 aren't really base units but they have a factor of 1.0
_build_base_unit('sqrt(m)'),  # Fracture toughness
_build_base_unit('sqrt(m)'),  # radian
_build_base_unit('sr'),  # steradian
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
_build_derived_unit('r', 'm⋅m⁻¹')  # radian

# a.u. of length
_build_unit('au(length)', 5.2917699999999994e-11, 'm')
_build_unit('am', 1e-18, 'm')  # attometer
_build_unit('Å', 1e-10, 'm')  # ångström
_build_unit('ft', 0.3048, 'm')  # foot
_build_unit('yd', 0.9144, 'm')  # yard
_build_unit('mi', 1609344, 'm')  # mile
_build_unit('in', 0.0254, 'm')  # inch
_build_unit('µ', 1e-06, 'm')  # micron
_build_unit('arcmin', 0.000290888, 'm')  # arcmin
_build_unit('AU', 149597870700, 'm')  # astronomical unit
_build_unit('UA', 149597870700, 'm')  # astronomical unit
_build_unit('au', 149597870700, 'm')  # astronomical unit
_build_unit('agate', 0.00181428571429, 'm')  # agate
_build_unit('aln', 0.593778, 'm')  # alens
_build_unit('bcorn', 0.0084666666666667, 'm')  # barleycorn (UK)
_build_unit('a₀', 5.2917699999999994e-11, 'm')  # first Bohr radius
_build_unit('ʳBohr', 5.2917699999999994e-11, 'm')  # first Bohr radius
_build_unit('bolt', 36.576, 'm')  # bolt (US cloth)
_build_unit('bl', 80.4672, 'm')  # blocks
_build_unit('line(UK)', 0.00211667, 'm')  # button (UK)
_build_unit('line(US)', 0.000635, 'm')  # button (US)
_build_unit('cable(int)', 185.2, 'm')  # cable length (int.)
_build_unit('cable(UK)', 185.318, 'm')  # cable length (UK)
_build_unit('cable(US)', 219.456, 'm')  # cable length (US)
_build_unit('cable', 219.456, 'm')  # cable length (US)
_build_unit('caliber', 2.54e-4, 'm')  # caliber (centiinch)
_build_unit('ch(engineer)', 30.48, 'm')  # chain (engineer's)
_build_unit('ch(Gunter)', 20.1168, 'm')  # chain (Gunter's)
_build_unit('ch(Ramsden)', 30.48, 'm')  # chain (Ramsden's)
_build_unit('ch(surveyor)', 20.1168, 'm')  # chain (surveyor's)
_build_unit('cbt', 0.4572, 'm')  # cubit (UK)
_build_unit('didotpoint', 0.000375972222, 'm')  # didot point
_build_unit('digit', 0.01905, 'm')  # digits
_build_unit('re', 2.81794e-15, 'm')  # electron classical radius
_build_unit('Ec', 40000000, 'm')  # Earth circumfrence
_build_unit('eel(Scottish)', 0.94, 'm')  # ell (Scottish)
_build_unit('eel(Flemish)', 0.686, 'm')  # ell (Flemish)
_build_unit('eel(French)', 1.372, 'm')  # ell (French)
_build_unit('eel(Polish)', 0.787, 'm')  # ell (Polish)
_build_unit('eel(Danish)', 0.627708, 'm')  # ell (Danish)
_build_unit('eel(Swedish)', 0.59, 'm')  # ell (Swedish)
_build_unit('eel(German)', 0.547, 'm')  # ell (German)
_build_unit('EM(pica)', 0.0042175176, 'm')  # ems (pica)
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
_build_unit('Mg(Dutch)', 8244.35, 'm²')  # morgen (Dutch)
_build_unit('Mg(Prussian)', 2532.24, 'm²')  # morgen (Prussian)
_build_unit('Mg(South Africa)', 8565.3, 'm²')  # morgen (South Africa)
_build_unit('¼mi²(stat.)', 647497.0, 'm²')  # quarter section
_build_unit('¼ac', 1011.71, 'm²')  # rood (UK)
_build_unit('rood', 1011.71, 'm²')  # rood (UK)
_build_unit('sqmi', 2589990.0, 'm²')  # section (square statute mile)
_build_unit('mi²(stat.)', 2589990.0, 'm²')  # section (square statute mile)
_build_unit('outhouse', 1e-34, 'm²')  # outhouse
_build_unit('shed', 1e-52, 'm²')  # shed
_build_unit('sqch(engineer)', 929.03, 'm²')  # square chain (engineer's)
_build_unit('sqch(Gunter)', 404.686, 'm²')  # square chain (Gunter's)

_build_unit('acre⋅ft', 1233.48, 'm³')  # acre foot
_build_unit('bag', 0.109106, 'm³')  # bag (UK)
_build_unit('bbl(US cranb)', 0.095471, 'm³')  # barrel (US, cranb.)
_build_unit('bbl', 0.1192404712, 'm³')  # barrel (US)
_build_unit('bbl(US petrol)', 0.1589872949, 'm³')  # barrel (US petrol)
_build_unit('bbl(UK)', 0.16365924, 'm³')  # barrel (UK)
_build_unit('FBM', 0.002359737, 'm³')  # board foot measure
_build_unit('bouteille', 0.000757682, 'm³')  # bouteille
_build_unit('bk(UK)', 0.0181844, 'm³')  # bucket (UK)
_build_unit('bu(UK)', 0.036368700000000004, 'm³')  # bushel (UK)
_build_unit('bu(US dry)', 0.0352391, 'm³')  # bushel (US, dry)
_build_unit('bt(UK)', 0.490978, 'm³')  # butt (UK)
_build_unit('chal(UK)', 1.30927, 'm³')  # chaldron (UK)
_build_unit('cc', 1.00238e-06, 'm³')  # cubic centimeter (Mohr cubic centimeter)
_build_unit('l', 0.001, 'm³')  # Liter
_build_unit('L', 0.001, 'm³')  # Liter
_build_unit('gal', 0.00378541178, 'm³')  # Gallon (US)
_build_unit('gal(UK)', 4.54609e-3, 'm³')  # Gallon (UK)
_build_unit('qt', 0.000946352946, 'm³')  # Quart (US)
_build_unit('qt(UK)', 0.0011365225, 'm³')  # Quart (UK)
_build_unit('pt', 0.000473176473, 'm³')  # Pint (US)
_build_unit('pt(UK)', 0.00056826125, 'm³')  # Pint (UK)
_build_unit('floz', 2.95735296875e-05, 'm³')  # Fluid Ounce (US)
_build_unit('floz(UK)', 2.84130625e-05, 'm³')  # Fluid Ounce (UK)
_build_unit('cran', 0.170478, 'm³')  # cran
_build_unit('dr', 3.6967e-06, 'm³')  # dram
_build_unit('st', 1.0, 'm³')  # stere
_build_unit('gi', 0.0001182941, 'm³')  # gill (US)
_build_unit('gi(UK)', 0.0001420653, 'm³')  # gill (UK)
_build_unit('cup', 0.00025, 'm³')  # cup (US)
_build_unit('cup(UK)', 0.0002841306, 'm³')  # cup (UK)
_build_unit('dstspn', 9.8578e-06, 'm³')  # dessertspoon (US)
_build_unit('dstspn(UK)', 1.18388e-05, 'm³')  # dessertspoon (UK)
_build_unit('tbsp', 1.5e-05, 'm³')  # tablespoon (US)
_build_unit('tbsp(UK)', 1.77582e-05, 'm³')  # tablespoon (UK)
_build_unit('tsp', 5e-06, 'm³')  # teaspoon (US)
_build_unit('tsp(UK)', 5.9194e-06, 'm³')  # teaspoon (UK)

# electron rest mass (a.u. of mass)
_build_unit('m₀', 9.10939e-31, 'kg')
# electron rest mass (a.u. of mass)
_build_unit('me', 9.10939e-31, 'kg')
_build_unit('u(dalton)', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('u', 1.660540199e-27, 'kg')  # atomic mass unit
_build_unit('uma', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('Da', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
_build_unit('dr(troy)', 0.00388793, 'kg')  # dram (troy)
_build_unit('dr(ap)', 0.00388793, 'kg')  # dram or drachm (apothecary)
_build_unit('dr(apoth)', 0.00388793, 'kg')  # dram or drachm (apothecary)
_build_unit('dr(av)', 0.00177185, 'kg')  # dram or drachm (avoirdupois)
_build_unit('dr(avdp)', 0.00177185, 'kg')  # dram or drachm (avoirdupois)
_build_unit('g', 0.001, 'kg')  # gram
_build_unit('lb', 0.45359237, 'kg')  # pound
_build_unit('oz', 0.028349523125, 'kg')  # ounce
_build_unit('t(long)', 1016.0469088, 'kg')  # ton (long)
_build_unit('t(short)', 907.18474, 'kg')  # ton(short)
_build_unit('t', 1000.0, 'kg')  # metric ton
_build_unit('pwt', 0.0015551738, 'kg')  # pennyweight
_build_unit('kip', 453.59237, 'kg')  # kip
_build_unit('gr', 6.47989e-05, 'kg')  # grain
_build_unit('slug', 14.5939029372, 'kg')  # geepound (slug)
_build_unit('t(assay)', 0.029167, 'kg')  # assay ton
_build_unit('Da(¹²C)', 1.66054e-27, 'kg')  # atomic unit of mass (¹²C)
_build_unit('Da(¹⁶O)', 1.66001e-27, 'kg')  # atomic unit of mass (¹⁶O)
_build_unit('Da(¹H)', 1.67353e-27, 'kg')  # atomic unit of mass (¹H)
_build_unit('avogram', 1.66036e-24, 'kg')  # avogram
_build_unit('bag(UK cement)', 42.6377, 'kg')  # bag (UK, cement)
_build_unit('ct.', 0.0002, 'kg')  # carat (metric)
_build_unit('ct(troy)', 0.000205197, 'kg')  # carat (troy)
_build_unit('cH', 45.3592, 'kg')  # cental
_build_unit('cwt', 100.0, 'kg')  # quintal

# a.u. of time
_build_unit('au(time)', 2.4188800000000002e-17, 's')
_build_unit('blink', 0.864, 's')  # blink
_build_unit('d', 86400.0, 's')  # day
_build_unit('d(sidereal)', 86164.0, 's')  # day (sidereal)
_build_unit('fortnight', 1209600.0, 's')  # fortnight
_build_unit('h', 3600.0, 's')  # hour
_build_unit('min', 60.0, 's')  # minute
_build_unit('month', 2592000.0, 's')  # month (30 days)
_build_unit('month(sidereal)', 2360590.0, 's')  # month (sidereal)
_build_unit('month(mean)', 2628000.0, 's')  # month (solar mean)
_build_unit('month(synodic)', 2551440.0, 's')  # month (synodic), lunar month
_build_unit('shake', 1e-08, 's')  # shake
_build_unit('week', 604800.0, 's')  # week
_build_unit('wink', 3.33333e-10, 's')  # wink
_build_unit('a(astr)', 31557900.0, 's')  # year (astronomical), Bessel year
_build_unit('a', 31536000.0, 's')  # year (calendar)
_build_unit('y', 31536000.0, 's')  # year (calendar)
_build_unit('a(sidereal)', 31558200.0, 's')  # year (sidereal)
_build_unit('a(mean)', 31557600.0, 's')  # year (solar mean)
_build_unit('a(tropical)', 31556900.0, 's')  # year (tropical)

_build_unit('°K', 1.0, 'K')  # Kelvin degree
_build_unit('°C', 274.15, 'K')  # Celsius degree
_build_unit('°F', 255.927556, 'K')  # Fahrenheit degree
_build_unit('°R', 0.555556, 'K')  # Rankine degree

_build_unit('bd', 1.02, 'cd')  # bougie d&egrave;cimale
_build_unit('bi', 1.0, 'cd')  # bougie international
_build_unit('c(int)', 1.01937, 'cd')  # candle (int.)
_build_unit('c', 1.0, 'cd')  # candle (new unit)
_build_unit('carcel', 10.0, 'cd')  # carcel
_build_unit('HK', 0.903, 'cd')  # hefner unit (hefnerkerze)
_build_unit('violle', 20.4, 'cd')  # violle

_build_unit('entities', 1.66054e-24, 'mol')  # entities
_build_unit('SCF', 1.19531, 'mol')  # standard cubic foot
_build_unit('SCM', 44.6159, 'mol')  # standard cubic meter

_build_unit('\'', 0.000290888, 'r')  # arc minute (minute of arc)
_build_unit('"', 4.84814e-06, 'r')  # arc second (second of arc)
_build_unit('πd', 6.28319, 'r')  # circumference
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
_build_unit('hp(boiler)', 9809.5, 'W')  # horsepower (boiler)
_build_unit('hp(British)', 745.7, 'W')  # horsepower (British)
_build_unit('cv', 735.499, 'W')  # horsepower (cheval-vapeur)
_build_unit('hp(cheval)', 735.499, 'W')  # horsepower (cheval-vapeur)
_build_unit('hp(electric)', 746.0, 'W')  # horsepower (electric)
_build_unit('hp(metric)', 735.499, 'W')  # horsepower (metric)
_build_unit('hp(water)', 746.043, 'W')  # horsepower (water)
_build_unit('prony', 98.0665, 'W')  # prony

_build_unit('at', 98066.5, 'Pa')  # atmosphere (technical)
_build_unit('atm', 101325.0, 'Pa')  # atmosphere (standard)
_build_unit('bar', 100000.0, 'Pa')  # bar
_build_unit('Ba', 0.1, 'Pa')  # Bayre
_build_unit('p(P)', 4.63309e+113, 'Pa')  # Planck pressure
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

_build_unit('B(power)', 10.0, 'dB')  # bel (power)
_build_unit('B(voltage)', 5.0, 'dB')  # bel (voltage)
_build_unit('dB(power)', 1.0, 'dB')  # decibel (power)
_build_unit('dB(voltage)', 0.5, 'dB')  # decibel (voltage)
_build_unit('Nₚ', 4.34294, 'dB')  # neper

# a.u. of magnetic field
_build_unit('au(magnetic field)', 235052.0, 'T')
_build_unit('Gs', 1e-05, 'T')  # gauss

_build_unit('M', 1e-09, 'Wb')  # maxwell

# a.u. of charge
_build_unit('au(charge)', 1.60218e-19, 'C')
_build_unit('aC', 10, 'C')  # abcoulomb (emu of charge)
_build_unit('esc', 1.6022e-19, 'C')  # electronic charge
_build_unit('esu', 3.336e-06, 'C')  # electrostatic unit
_build_unit('Fr', 3.33564e-10, 'C')  # franklin
_build_unit('statC', 3.35564e-10, 'C')  # statcoulomb

_build_unit('aS', 1000000000.0, 'S')  # abmho (emu of conductance)
_build_unit('(aW)⁻¹', 1000000000.0, 'S')  # abmho (emu of conductance)
_build_unit('gemʊ', 1e-07, 'S')  # gemmho
_build_unit('mho', 1.0, 'S')  # mho
_build_unit('statmho', 1.11265e-12, 'S')  # statmho

_build_unit('aH', 1e-10, 'H')  # abhenry (emu of inductance)
_build_unit('statH', 898755000000.0, 'H')  # stathenry

# a.u. of electric potential
_build_unit('au(electric potential)', 27.2114, 'V')
_build_unit('aV', 1e-09, 'V')  # abvolt (emu of electric potential)
_build_unit('statV', 299.792, 'V')  # statvolt
_build_unit('V(mean)', 1.00034, 'V')  # volt (mean)
_build_unit('V(US)', 1.00033, 'V')  # volt (US)

_build_unit('aΩ', 1e-10, 'Ω')  # abohm (emu of resistance)
_build_unit('SΩ', 0.96, 'Ω')  # siemens (resistance)
_build_unit('statohm', 898755000000.0, 'Ω')  # statohm

# a.u. of energy
_build_unit('au(energy)', 4.35975e-18, 'J')
_build_unit('bboe', 6120000000.0, 'J')  # barrel oil equivalent
_build_unit('BeV', 1.60218e-10, 'J')  # BeV (billion eV)
_build_unit('Btu(ISO)', 1055.06, 'J')  # British thermal unit (ISO)
_build_unit('Btu(IT)', 1055.06, 'J')  # British thermal unit (IT)
_build_unit('Btu(mean)', 1055.87, 'J')  # British thermal unit (mean)
_build_unit('Btu(therm)', 1054.35, 'J')  # British thermal unit (thermochemical)
_build_unit('cal₁₅', 4.185, 'J')  # calorie (15°C)
_build_unit('cal₄', 4.2045, 'J')  # calorie (4°C)
_build_unit('Cal', 4180.0, 'J')  # Calorie (diet kilocalorie)
_build_unit('kcal', 4180.0, 'J')  # Calorie (diet kilocalorie)
_build_unit('cal(IT)', 4.18674, 'J')  # calorie (IT) (International Steam Table)
_build_unit('cal(mean)', 4.19002, 'J')  # calorie (mean)
_build_unit('cal(therm)', 4.184, 'J')  # calorie (thermochemical)
_build_unit('Chu', 1899.18, 'J')  # Celsius-heat unit
_build_unit('eV', 1.60218e-19, 'J')  # electronvolt
_build_unit('erg', 1e-07, 'J')  # erg
_build_unit('Eh', 4.35975e-18, 'J')  # hartree

# a.u. of force
_build_unit('au(force)', 8.23873e-08, 'N')
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
_build_unit('tf(long)', 9964.02, 'N')  # ton force (long)
_build_unit('tf(metric)', 9806.65, 'N')  # ton force (metric)
_build_unit('tf(short)', 8896.44, 'N')  # ton force (short)
_build_unit('ozf', 0.278014, 'N')  # ounce force

# a.u. of electric current
_build_unit('au(electric current)', 0.00662362, 'A')
_build_unit('abA', 10, 'A')  # abampere
_build_unit('Bi', 10, 'A')  # biot
_build_unit('edison', 100.0, 'A')  # edison
_build_unit('statA', 3.35564e-10, 'A')  # statampere
_build_unit('gilbert', 0.79577, 'A')  # gilbert
_build_unit('pragilbert', 11459.1, 'A')  # pragilbert

_build_unit('cps', 1.0, 'Hz')  # cycles per second

_build_unit('ct', 0.0416667, '')  # carat (karat)
_build_unit('Kt', 0.0416667, '')  # carat (karat)
_build_unit('ppb', 1e-10, '')  # part per billion
_build_unit('pph', 0.001, '')  # part per hundred
_build_unit('pphm', 1e-09, '')  # part per hundred million
_build_unit('ppht', 1e-06, '')  # part per hundred thousand
_build_unit('ppm', 1e-07, '')  # part per million
_build_unit('ppq', 1e-15, '')  # part per quadrillion
_build_unit('ppt(tera)', 1e-13, '')  # part per tera
_build_unit('ppt', 0.001, '')  # part per thousand

_build_unit('Ci', 37000000000.0, 'Bq')  # curie

_build_unit('sp', 12.5664, 'sr')  # spat

_build_unit('gy', 1000, 'kg⋅m⁻³')  # specific gravity

_build_unit('lbm', 0.453592, 'kg⋅m²')  # pound mass

_build_unit('Ω(mechanial)', 1.0, 'Pa⋅s⋅m⁻³')  # ohm (mechanical, SI)

_build_unit('perm(0⋅°C)', 5.72135e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (0°C)
_build_unit('perm(23⋅°C)', 5.74525e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (23°C)
_build_unit('permin(0⋅°C)', 1.45322e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (0°C)
_build_unit('permin(23⋅°C)', 1.45929e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (23°C)
_build_unit('permmil(0⋅°C)', 1.45322e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (0°C)
_build_unit('permmil(23⋅°C)', 1.45929e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (23°C)

_build_unit('brewster', 1e-12, 'm²⋅N⁻¹')  # brewster

_build_unit('aF', 1000000000.0, 'F')  # abfarad (emu of electric capacitance)
_build_unit('jar', 1.11111e-09, 'F')  # jar
_build_unit('statF', 1.11265e-12, 'F')  # statfarad

_build_unit('P', 0.1, 'Pa⋅s')  # Poise
_build_unit('Pl', 1.0, 'Pa⋅s')  # poiseuille
_build_unit('reyn', 6894.76, 'Pa⋅s')  # reynolds (reyns)

_build_unit('clo', 0.15482, 'K⋅m²⋅W⁻¹')  # clo
_build_unit('°F⋅ft²⋅h⋅Btu(therm)⁻¹', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
_build_unit('°F⋅ft²⋅h/Btu(therm)', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
_build_unit('RSI', 1.0, 'K⋅m²⋅W⁻¹')  # RSI (metric R-value)
_build_unit('tog', 0.1, 'K⋅m²⋅W⁻¹')  # tog

_build_unit('Bz', 1.0, 'm⋅s⁻¹')  # benz
_build_unit('kn(noeud)', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
_build_unit('knot(noeud)', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
_build_unit('mpy', 8.04327e-13, 'm⋅s⁻¹')  # mil per year
_build_unit('kn', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
_build_unit('knot', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
_build_unit('c(speedlight)', 299792000.0, 'm⋅s⁻¹')  # speed of light

_build_unit('dioptre', 1.0, 'm⁻¹')  # dioptre
_build_unit('mayer', 1000.0, 'J⋅kg⁻¹⋅K⁻¹')  # mayer
_build_unit('helmholtz', 3.336e-10, 'C⋅m⁻¹')  # helmholtz

_build_unit('mired', 1000000.0, 'K⁻¹')  # mired

_build_unit('cumec', 1.0, 'm³⋅s⁻¹')  # cumec (musec)
_build_unit('gph(UK)', 1.2627999999999998e-06, 'm³⋅s⁻¹')  # gallon (UK) per hour
_build_unit('gpm(UK)', 7.57682e-05, 'm³⋅s⁻¹')  # gallon (UK) per minute
_build_unit('gps(UK)', 0.004546090000000001, 'm³⋅s⁻¹')  # gallon (UK) per second
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
_build_unit('au(linear momentum)', 1.99285e-24, 'N⋅s')

_build_unit('c(power)', 12.5664, 'cd⋅sr')  # candlepower (spherical)

_build_unit('asb', 0.31831, 'cd⋅m⁻²')  # apostilb
# _build_unit('L', 31831.0, 'cd⋅m⁻²')  # lambert
_build_unit('nit', 1.0, 'cd⋅m⁻²')  # nit
_build_unit('sb', 10000.0, 'cd⋅m⁻²')  # stilb

_build_unit('oe', 79.5775, 'A⋅m⁻¹')  # oersted
_build_unit('praoersted', 11459.1, 'A⋅m⁻¹')  # praoersted

# a.u. of magnetic dipole moment
_build_unit('au(magnetic dipole moment)', 1.8548e-23, 'J⋅T⁻¹')
_build_unit('Gal', 0.001, 'm⋅s⁻²')  # galileo
_build_unit('leo', 10, 'm⋅s⁻²')  # leo
_build_unit('gn', 9.80665, 'm⋅s⁻²')  # normal acceleration

_build_unit('Ω(acoustic, SI)', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)

_build_unit('rayl(cgs)', 10, 'kg⋅m⁻²⋅s⁻¹')  # rayl (cgs)
_build_unit('rayl(MKSA)', 1, 'kg⋅m⁻²⋅s⁻¹')  # rayl (MKSA)

_build_unit('Nₐ', 6.02214e+23, 'mol⁻¹')  # avogadro

# a.u. of action
_build_unit('au(action)', 1.05457e-34, 'J⋅s')
# a.u. of angular momentum
_build_unit('au(angular momentum)', 1.05457e-34, 'J⋅s')
_build_unit('planck', 1, 'J⋅s')  # planck

_build_unit('rpm', 1, 'rev⋅min⁻¹')  # revolution per minute

# a.u. of charge density
_build_unit('au(charge density)', 1081200000000.0, 'C⋅m⁻³')

_build_unit('Ah', 1.0, 'A⋅h⁻¹')  # ampere-hour

_build_unit('F(¹²C)', 96485.3, 'C⋅mol⁻¹')  # faraday (based on ¹²C)
_build_unit('F(chemical)', 96495.7, 'C⋅mol⁻¹')  # faraday (chemical)
_build_unit('F(physical)', 96512.9, 'C⋅mol⁻¹')  # faraday (physical)

_build_unit('roc', 100, 'S⋅m⁻¹')  # reciprocal ohm per centimeter
_build_unit('rom', 1.0, 'S⋅m⁻¹')  # reciprocal ohm per meter

# a.u. of electric quadrupole moment
_build_unit('au(electric quadrupole moment)', 4.48655e-40, 'C⋅m²')
# a.u. of electric dipole moment
_build_unit('au(electric dipole moment)', 8.47836e-30, 'C⋅m')
# a.u. of electric field strength
_build_unit('au(electric field strength)', 514221000000.0, 'V⋅m⁻¹')

_build_unit('Jy', 1e-27, 'W⋅m⁻²⋅Hz')  # jansky

_build_unit('MGOe', 7957.75, 'J⋅m⁻³')  # megagauss-oersted (MGOe)
_build_unit('Ly', 41850.0, 'J⋅m⁻²')  # langley (energy)
_build_unit('ly(langley)', 697.5, 'W⋅m⁻²')  # langley (flux)

_build_unit('ue', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy
_build_unit('eu', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy

_build_unit('UI', 1.66667e-08, 'mol⋅s⁻¹')  # international unit
_build_unit('IU', 1.66667e-08, 'mol⋅s⁻¹')  # international unit

_build_unit('ksi⋅sqrt(in)', 1098840.0, 'Pa⋅sqrt(m)')  # ksi-sqrt(inch)
_build_unit('psi⋅sqrt(in)', 1098.84, 'Pa⋅sqrt(m)')  # psi-sqrt(inch)

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
    cf_from, cf_to = _get_conversion_factor(from_unit, to_unit)
    val = v * (cf_from / cf_to)

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


def _get_conversion_factor(from_unit, to_unit):
    from_units = _Unit(from_unit, [])
    to_units = _Unit(to_unit, [])

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

    return from_units.factor, to_units.factor


def main():
    test_units = (
        (71, 'in³', 'mm³'),
        (129.5674, 'in²', 'mm²'),
        (3.657, 'gal', 'l'),
        (500.679, 'g', 'lb'),
        (75.1, '°F', '°K'),
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


if __name__ == '__main__':
    main()
