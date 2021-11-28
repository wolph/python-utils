import decimal
import math
from typing import Sequence, Optional, Union


from .unicode_characters import MULTIPLIER
from .unicode_characters import SUPER_SCRIPT_MAPPING
from .quantity import QUANTITY, QUANTITY_BASE


BASE_UNITS = {}
NAMED_DERIVED_UNITS = {}
UNITS = {}


class MalformedUnitError(ValueError):
    _template = 'Malformed/Unsupported unit ("{0}")'

    def __init__(self, unit):
        self.unit = unit

    def __str__(self):
        return self._template.format(self.unit)


class UnitsNotCompatibleError(ValueError):
    _template = (
        'Units "{0}" and "{1}" are not compatible ("{2}", "{3}")'
    )

    def __init__(self, from_unit, to_unit):
        self.from_unit = from_unit
        self.to_unit = to_unit

    def __str__(self):
        return self._template.format(
            self.from_unit,
            self.to_unit,
            self.from_unit.base_unit_string,
            self.to_unit.base_unit_string
        )


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

    def __init__(
            self,
            symbol: str,
            base_units: Optional[Sequence["Unit"]] = None,
            factor: Optional[Union[int, float, decimal.Decimal]] = 1.0,
            exponent: Optional[Union[int, decimal.Decimal]] = 1,
            value: Optional[Union[int, float, decimal.Decimal]] = None,
    ):
        # noinspection PySingleQuotedDocstring
        '''
        Unit
        ====

        This is the workhorse of the conversion
        This class can be used to do unit conversions

        :param symbol: the unit
        :type symbol: str

        :param base_units: list of base units. Base units are the
          7 base SI units. All units in the SI system convert to
          a sequence of base units. If you don't know what I mean
          by this then then do not set this parameter.
        :type base_units: Optional, list[Unit] or None

        :param factor: the conversion factor used to convert the
          unit to/from it's quantity unit.
        :type factor: Optional, int, float or decimal.Decimal

        :param exponent: 2 for square, 3 for cubic....
        :type exponent: Optional, int or decimal.Decimal

        :param value: Internal Use
        :type value: None

        |
        |

        .. py:property:: factor
            :type: decimal.Decimal

            Conversion factor

        |

        .. py:property:: symbol
            :type: str

            String representation for the unit

        |

        .. py:property:: exponent
            :type: decimal.Decimal

            Unit exponent (ex: 2 for square 3 for cubic)

        |

        .. py:property:: value
            :type: decimal.Decimal

            Value of the unit

        |

        .. py:property:: quantity
            :type: list[str]

            Quantity this unit belongs to.

        |

        .. py:property:: base_unit_string
            :type: str

            Base SI expression.

        |

        .. py:property:: compatible_quantities
            :type: list[str]

            List of compatable quantities this unit can convert to/from.

        |

        .. py:property:: compatible_units
            :type: list[Unit]

            List of compatable units this unit can convert to/from.

        |
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
            numerator = self._process_unit(
                item,
                exponent
            )
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
                    raise MalformedUnitError(unit)

            return [
                found_unit(exponent=int(s_exponent) * exponent)
            ]

        brace_open = 0
        item = ''
        found_units = []

        for char in unit:
            if char == '(':
                brace_open += 1
            elif char == ')':
                brace_open -= 1
                if brace_open != 0:
                    item += char
                    continue

                if item.startswith('sqrt'):
                    f_units = self._process_unit(
                        item[5:],
                        exponent
                    )
                    f_units = [
                        Unit('sqrt', base_units=f_units)
                    ]
                else:
                    f_units = self._process_unit(
                        item[1:],
                        exponent
                    )
                found_units.extend(f_units)
                item = ''
                continue

            elif char == MULTIPLIER and brace_open == 0:
                found_units.extend(
                    self._process_unit(item, exponent)
                )
                item = ''
                continue

            item += char

        if item:
            found_units.extend(
                self._process_unit(item, exponent)
            )

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
            elif key == 'da':
                continue

            else:
                return

            return Unit(
                unit,
                base_units=base_unit,
                factor=factor
            )

    def __call__(
        self,
        value: Optional[Union[float, int, decimal.Decimal]] = None,
        /,
        factor: Optional[Union[float, int, decimal.Decimal]] = None,
        exponent: Optional[Union[int, decimal.Decimal]] = None,
    ) -> Union["Unit", float]:
        """
        Returns a copy of the :py:class:`Unit` instance or returns a converted
        value.

        :param value: If wanting to call the unit to do the conversion
        :type value: Optional, int, float or decimal.Decimal

        :param factor: Factor the unit uses to do the conversion. This mainly
          used for internal purposes. If passing a factor if get multiplied
          by the curent factor the unit has. If you need to pass a factor and
          not have that factor altere then contruct a new :py:class:`Unit`
          instance.
        :type factor: Optional, int, float or decimal.Decimal

        :param exponent: Exponent of the unit
        :type exponent: Optional, int or decimal.Decimal

        :return: New :py:class:`Unit` instance
        :rtype: Unit or float
        """
        if None not in (value, self._to_unit, self._from_unit):
            return value * self

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
            list(unit() for unit in self._b_units),
            factor=factor,
            exponent=exponent,
            value=value,
        )

    @property
    def factor(self) -> decimal.Decimal:
        """
        The factor used to convert the unit to the base unit for the quantity.
        """
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
    def exponent(self) -> decimal.Decimal:
        """
        Exponen this unit has.
        """
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
        # noinspection PyProtectedMember
        if other._symbol != self._symbol:
            raise ValueError(
                'Units must be the same to add them together.'
            )
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
                factor=float(self.factor * other.factor),
                value=self._value
            )
            return unit
        elif (
                None in (self._from_unit, self._to_unit) and
                self._value is None
        ):
            return self._factor * decimal.Decimal(str(other))
            # raise ValueError('To and From units have not be divided')
        elif self._value is None:
            f_unit = self._from_unit.base_unit_string
            t_unit = self._to_unit.base_unit_string

            if f_unit != t_unit:
                raise UnitsNotCompatibleError(
                    self._from_unit,
                    self._to_unit,
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
            raise TypeError(
                'you can only divide a unit into another unit'
            )

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

        if self._value is None:
            unit._from_unit = self
            unit._to_unit = other
            return unit

        else:
            return self._value * unit

    def __idiv__(self, other):
        if not isinstance(other, Unit):
            raise TypeError(
                'you can only use /= with another unit'
            )

        return Unit(self.symbol + '/' + other.symbol)

    def __truediv__(self, other):
        return self.__div__(other)

    def __itruediv__(self, other):
        return self.__idiv__(other)

    @property
    def symbol(self) -> str:
        """
        Symbol of this unit.
        """
        symbol = self._symbol
        curr_exponent = ''
        repl_exponent = ''

        for i in range(len(symbol) - 1, -1, -1):
            char = symbol[i]
            if char not in SUPER_SCRIPT_MAPPING:
                break

            curr_exponent = (
                SUPER_SCRIPT_MAPPING[char] +
                curr_exponent
            )
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
    def quantity(self) -> Sequence[str]:
        if self.symbol in QUANTITY:
            return QUANTITY[self.symbol]

        if self.base_unit_string in QUANTITY:
            return QUANTITY[self.base_unit_string]

        bases = self._b_units
        new_bases = []
        for base in bases:
            base = base()
            base._exponent *= self._exponent

            if base in new_bases:
                new_bases[new_bases.index(base)] += base
            else:
                new_bases.append(base)

        symbol = MULTIPLIER.join(
            sorted(str(u) for u in new_bases if u)
        )

        if symbol in QUANTITY:
            return QUANTITY[symbol]

    @property
    def base_unit_string(self) -> str:
        return MULTIPLIER.join(
            sorted(str(u) for u in self if u)
        )

    @property
    def compatible_quantities(self) -> Sequence[str]:
        base_symbol = self.base_unit_string

        if base_symbol in QUANTITY_BASE:
            return QUANTITY_BASE[base_symbol]['quantities']

        return []

    @property
    def compatible_units(self) -> Sequence['Unit']:
        quantities = list(self.compatible_quantities)
        units = []

        for unit in BASE_UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    units.append(unit())
                    break

        for unit in NAMED_DERIVED_UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    units.append(unit())
                    break

        for unit in UNITS.values():
            if unit == self:
                continue

            for quantity in unit.compatible_quantities:
                if quantity in quantities:
                    units.append(unit())
                    break

        for unit in units[:]:
            s_unit = str(unit)
            new_unit = 'da' + s_unit
            if (
                new_unit not in UNITS and
                new_unit not in BASE_UNITS and
                new_unit not in NAMED_DERIVED_UNITS
            ):
                units.append(Unit(new_unit))

            for prefix in 'YZEPTGMkhdcmµnpfazy':
                new_unit = prefix + s_unit
                if new_unit in UNITS:
                    continue
                if new_unit in BASE_UNITS:
                    continue
                if new_unit in NAMED_DERIVED_UNITS:
                    continue
                units.append(Unit(new_unit))

        return units

    def __iter__(self):
        if self._b_units:
            bases = []
            res = []

            for base in self._b_units:
                bases.extend(list(base))

            for base in bases:
                base = base()
                # noinspection PyProtectedMember
                base._exponent *= self._exponent

                if base in res:
                    res[res.index(base)] += base
                else:
                    res.append(base)

            return iter(list(b for b in res if b))
        else:
            return iter([self()])

    def __dir__(self):
        attrs = object.__dir__(self)
        attrs += self.compatible_units
        return attrs

    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError(item)

        compatible_units = self.compatible_units
        if item in compatible_units:
            unit = compatible_units[compatible_units.index(item)]
        else:
            try:
                unit = Unit(item)
            except MalformedUnitError:
                raise MalformedUnitError(item) from None

            raise UnitsNotCompatibleError(self, unit)

        unit = self / unit()

        return unit
