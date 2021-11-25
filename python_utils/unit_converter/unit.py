import decimal
import functools
import math

from .unicode_characters import MULTIPLIER
from .unicode_characters import SUPER_SCRIPT_MAPPING

from .quantity import QUANTITY, QUANTITY_BASE

BASE_UNITS = {}
NAMED_DERIVED_UNITS = {}
UNITS = {}


def _is_number(val):
    try:
        int(val)
        return True
    except ValueError:
        pass

    try:
        float(val)
        return True
    except ValueError:
        pass
    return False


class Unit(object):
    # noinspection PySingleQuotedDocstring
    '''
    Unit of measure
    ===============

    This is the workhorse of the conversion
    This class can be used to do unit conversions
    .. seealso:: python-utils.unit_converter

    .. py:method:: __init__(symbol: str,
    base_units: None or list[Unit] = None,
    factor: float = 1.0, exponent: int = 1) -> Unit

    .. py:property:: factor
        :type: decimal.Decimal

        Conversion factor

    .. py:property:: symbol
        :type: str

        String representation for the unit

    .. py:property:: exponent
        :type: decimal.Decimal

        Unit exponent (ex: 2 for square 3 for cubic)

    .. py:property:: value
        :type: decimal.Decimal

        Value of the unit
    '''

    def __init__(
            self,
            symbol,  # type: str
            base_units=None,  # type: list[Unit] or None
            factor=1.0,  # type: float or decimal.Decimal
            exponent=1,  # type: int or decimal.Decimal
            value=None,
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
        self._exponent = decimal.Decimal(str(exponent))
        self._b_units = base_units
        self._from_unit = None
        self._to_unit = None
        self._value = value

        if not base_units and symbol not in BASE_UNITS:
            self._b_units = self._process_unit(symbol)

    def __hash__(self):
        return hash(repr(self))

    def _process_unit(
            self,
            unit,
            exponent=1
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
                return self._process_unit(unit, exponent)
            elif 'H₂O' in unit:
                unit = unit.replace('H₂O', '⋅Aq')
                return self._process_unit(unit, exponent)
            elif 'Aq' in unit and '⋅Aq' not in unit:
                unit = unit.replace('Aq', '⋅Aq')
                return self._process_unit(unit, exponent)
            elif 'Hg' in unit and '⋅Hg' not in unit:
                unit = unit.replace('Hg', '⋅Hg')
                return self._process_unit(unit, exponent)
            elif 'O2' in unit and '⋅O2' not in unit:
                unit = unit.replace('O2', '⋅O2')
                return self._process_unit(unit, exponent)

        if '/' in unit:
            brace_open = 0
            item = ''

            for char in unit:
                if char == '(':
                    brace_open += 1
                elif char == ')':
                    brace_open -= 1
                elif char == '/' and brace_open == 0:
                    break

                item += char

            denominator = self._process_unit(
                unit.replace(item + '/', ''),
                -exponent
            )
            numerator = self._process_unit(item, exponent)
            return numerator + denominator

        if MULTIPLIER not in unit:
            s_exponent = ''
            item = ''
            has_exponent = False
            for i, char in enumerate(unit):
                if has_exponent:
                    if char.isdigit() or char == '-':
                        s_exponent += char
                        continue
                    else:
                        has_exponent = False
                if char in SUPER_SCRIPT_MAPPING:
                    s_exponent += SUPER_SCRIPT_MAPPING[char]
                elif char == '^':
                    has_exponent = True
                elif i > 0 and char == '*':
                    if unit[i - 1] == '*':
                        has_exponent = True
                else:
                    item += char

            if s_exponent == '':
                s_exponent = '1'

            if item in BASE_UNITS:
                found_unit = BASE_UNITS[item]
            elif item in NAMED_DERIVED_UNITS:
                found_unit = NAMED_DERIVED_UNITS[item]
            elif item in UNITS:
                found_unit = UNITS[item]
            else:
                found_unit = self._parse_unit_prefix(item)
                if found_unit is None:
                    raise ValueError(
                        'Unit {0} not found'.format(unit)
                    )

            return [found_unit.derive(exponent=int(s_exponent) * exponent)]

        brace_open = 0
        item = ''
        found_units = []

        for char in unit:
            if char == '(':
                brace_open += 1
            elif char == ')':
                brace_open -= 1
                if brace_open == 0:
                    if item.startswith('sqrt'):
                        f_units = self._process_unit(item[5:], exponent)
                        f_units = [Unit('sqrt', base_units=f_units)]
                    else:
                        f_units = self._process_unit(item[1:], exponent)
                    found_units.extend(f_units)
                    item = ''
                    continue

            elif char == MULTIPLIER and brace_open == 0:
                found_units.extend(self._process_unit(item, exponent))
                item = ''
                continue

            item += char

        if item:
            found_units.extend(self._process_unit(item, exponent))

        return found_units

    @staticmethod
    def _parse_unit_prefix(unit):
        # determines the conversion factor for the prefix of a unit
        # check if prefix exist and if so, get conversion factor
        if len(unit) <= 1:
            return

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

        for key, factor in mapping.items():
            if not unit.startswith(key):
                continue

            symbol = unit.replace(key, '', 1)

            if symbol in BASE_UNITS:
                base_unit = [BASE_UNITS[symbol]]
            elif symbol in NAMED_DERIVED_UNITS:
                base_unit = [NAMED_DERIVED_UNITS[symbol]]
            elif symbol in UNITS:
                base_unit = [UNITS[symbol]]
            else:
                return

            return Unit(
                unit,
                base_units=base_unit,
                factor=factor
            )

    def derive(
            self,
            factor=None,  # type: None or float or decimal.Decimal
            exponent=None,  # type: None or int or decimal.Decimal
            value=None,  # type: None or float or decimal.Decimal
    ):
        if factor is None:
            factor = self._factor
        else:
            factor = decimal.Decimal(str(factor))
            factor *= self._factor

        if exponent is None:
            exponent = self._exponent
        else:
            exponent = decimal.Decimal(str(exponent))

        return Unit(
            self._symbol,
            list(unit.derive() for unit in self._b_units),
            factor=factor,
            exponent=exponent,
            value=value,
        )

    def __call__(self, *args, **kwargs):
        if args:
            value = functools.reduce(lambda x, y: x * y, args,
                                     decimal.Decimal(1))
        else:
            value = None

        return self.derive(value=value, **kwargs)

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
        if isinstance(other, Unit):
            return other._symbol == self._symbol

        elif isinstance(other, str):
            return other in (self.symbol, self.base_unit_string)

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iadd__(self, other):
        if other._symbol != self._symbol:
            raise ValueError('Units must be th same to add them together.')
        self._exponent += other.exponent
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, Unit):
            f_units = list(self)
            t_units = list(other)
            unit = Unit(
                self._symbol + MULTIPLIER + other._symbol,
                base_units=f_units + t_units,
                factor=float(self.factor * other.factor)
            )
            return unit
        elif None in (self._from_unit, self._to_unit)  and self._value is None:
            return float(self.factor * decimal.Decimal(str(other)))
            # raise ValueError('To and From units have not be divided')
        else:
            f_unit = self._from_unit.base_unit_string
            t_unit = self._to_unit.base_unit_string

            if f_unit != t_unit:
                raise ValueError(
                    'Units "{0}" and "{1}" are not compatible({2})'.format(
                        self._from_unit,
                        self._to_unit,
                        (f_unit, t_unit)
                    )
                )

            if isinstance(other, bytes):
                othr = other.decode('utf-8')
            else:
                othr = other

            if isinstance(othr, str) and not _is_number(othr):
                raise ValueError(
                    'Not a numerical value ({0})'.format(repr(other))
                )

            val = decimal.Decimal(str(othr))
            val *= self.factor

            return float(val)

    def __div__(self, other):
        if not isinstance(other, Unit):
            raise TypeError('you can only divide a unit into another unit')

        if (
                self._symbol in ('°R', '°C', '°F', 'K') and
                other._symbol in ('°R', '°C', '°F', 'K')
        ):

            class _Temp(object):

                def __init__(self, from_unit, to_unit):
                    self.from_unit = from_unit
                    self.to_unit = to_unit

                def __rmul__(self, othr):
                    return self.__mul__(othr)

                def __mul__(self, oth):
                    if isinstance(oth, Unit):
                        raise TypeError(
                            'temperature unit needs to be multiplied '
                            'into an int, float or decimal.Decimal'
                        )

                    from_unit = self.from_unit

                    if isinstance(oth, bytes):
                        othr = oth.decode('utf-8')
                    else:
                        othr = oth

                    if isinstance(othr, str) and not _is_number(othr):
                        raise ValueError(
                            'Not a numerical value ({0})'.format(repr(oth))
                        )

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

                    to_unit = self.to_unit
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

                    return float(val)

            return _Temp(self._symbol, other._symbol)

        f_units = list(self)
        t_units = list(other)

        unit = Unit(
            self._symbol + MULTIPLIER + other._symbol,
            base_units=f_units + t_units,
            factor=float(self.factor / other.factor)
        )
        unit._from_unit = self
        unit._to_unit = other
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

            curr_exponent = SUPER_SCRIPT_MAPPING[char] + curr_exponent
            repl_exponent = char + repl_exponent

        if curr_exponent == '':
            curr_exponent = '1'

        curr_exponent = decimal.Decimal(curr_exponent)

        if curr_exponent != self._exponent:
            if int(self._exponent) != 1:
                exponent = SUPER_SCRIPT_MAPPING.convert(
                    int(self._exponent)
                )
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

    @property
    def quantity(self):
        if self.symbol in QUANTITY:
            return QUANTITY[self.symbol]

        if self.base_unit_string in QUANTITY:
            return QUANTITY[self.base_unit_string]

        if self.base_unit_string in QUANTITY_BASE:
            bases = self._b_units
            new_bases = []
            for base in bases:
                if str(base) == self._symbol:
                    del new_bases[:]
                    for b in base._b_units:
                        b = b.derive()
                        b._exponent *= self._exponent
                        if b in new_bases:
                            new_bases[new_bases.index(b)] += b
                        else:
                            new_bases.append(b)
                    break

                base = base.derive()
                base._exponent *= self._exponent

                if base in new_bases:
                    new_bases[new_bases.index(base)] += base
                else:
                    new_bases.append(base)

            symbol = MULTIPLIER.join(sorted(str(u) for u in new_bases))

            if symbol in QUANTITY:
                return QUANTITY[symbol]

    @property
    def base_unit_string(self):
        return MULTIPLIER.join(sorted(str(u) for u in self))

    @property
    def compatible_quantities(self):
        base_symbol = self.base_unit_string

        if base_symbol in QUANTITY_BASE:
            return iter(QUANTITY_BASE[base_symbol]['quantities'])

        return iter([])

    @property
    def compatible_units(self):
        quantities = list(self.compatible_quantities)

        for unit in BASE_UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    yield unit
                    break

        for unit in NAMED_DERIVED_UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    yield unit
                    break

        for unit in UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    yield unit
                    break

    def __iter__(self):
        if self._b_units:
            bases = []
            res = []

            for base in self._b_units:
                bases.extend(list(base))

            for base in bases:
                base = base.derive()
                base._exponent *= self._exponent

                if base in res:
                    res[res.index(base)] += base
                else:
                    res.append(base)

            return iter(list(b for b in res if b))
        else:
            return iter([self()])

    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError(item)
        unit = self / Unit(item)
        print('unit', unit, self._value)
        if self._value is None:
            return unit
        else:
            return self._value * unit
