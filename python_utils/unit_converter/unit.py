import decimal
import math
from typing import Sequence, Optional, Union

from .unicode_characters import MULTIPLIER
from .unicode_characters import SUPER_SCRIPT_MAPPING


BASE_UNITS = {}
NAMED_DERIVED_UNITS = {}
UNITS = {}

UnitOperatorType = Union[int, float, decimal.Decimal, "Unit"]
MathOperatorType = Union[int, float, decimal.Decimal]


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
            exponent: Optional[Union[int, decimal.Decimal]] = 1
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

        |
        |

        .. py:property:: factor
            :type: float

            Conversion factor

        |

        .. py:property:: symbol
            :type: str

            String representation for the unit

        |

        .. py:property:: exponent
            :type: int

            Unit exponent (ex: 2 for square 3 for cubic)

        |

        .. py:property:: value
            :type: float

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

        while '**' in symbol:
            beg, end = symbol.split('**', 1)
            s_exp = ''
            for char in end:
                if char.isdigit() or char == '-':
                    s_exp += char
                else:
                    break

            exp = SUPER_SCRIPT_MAPPING.convert(int(s_exp))
            end = end.replace(s_exp, exp, 1)
            symbol = beg + end

        while '^' in symbol:
            beg, end = symbol.split('^', 1)
            s_exp = ''
            for char in end:
                if char.isdigit() or char == '-':
                    s_exp += char
                else:
                    break

            exp = SUPER_SCRIPT_MAPPING.convert(int(s_exp))
            end = end.replace(s_exp, exp, 1)
            symbol = beg + end

        if base_units is None:
            base_units = []

        self._symbol = symbol
        self._factor = decimal.Decimal(str(factor))
        self._exponent = decimal.Decimal(str(exponent))
        self._b_units = base_units
        self._convert_to = None

        self._value = None
        if not base_units and symbol not in BASE_UNITS:
            self._b_units = self._process_unit(symbol)

        self.__quantities = None

    @property
    def _quantities(self):
        from .quantity import Quantities

        if self.__quantities is None:
            self.__quantities = []
            for quantity in Quantities.get_quantities():
                if quantity.is_unit_compatible(self):
                    self.__quantities.append(quantity)
        return self.__quantities

    def __hash__(self):
        return hash(str(self))

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
            for i, char in enumerate(unit):
                if char in SUPER_SCRIPT_MAPPING:
                    s_exponent += SUPER_SCRIPT_MAPPING[char]
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
        if value is not None is not self._convert_to:
            self.value = value
            return self._convert_to.value

        if factor is None:
            factor = self._factor
        else:
            factor = decimal.Decimal(str(factor))
            factor *= self._factor

        if exponent is None:
            exponent = self._exponent
        else:
            exponent = decimal.Decimal(str(exponent))

        unit = Unit(
            self._symbol,
            list(unit() for unit in self._b_units),
            factor=factor,
            exponent=exponent
        )

        if value is not None:
            unit.value = value

        return unit

    @property
    def factor(self) -> float:
        """
        The factor used to convert the unit to the base unit for the quantity.
        """
        factor = decimal.Decimal('1.0')

        for unit in self._b_units:
            # unit = unit()
            # unit._exponent *= self._exponent
            factor *= decimal.Decimal(str(unit.factor))

        factor *= self._factor
        factor = decimal.Decimal(str(math.pow(factor, self._exponent)))

        if self._symbol == 'sqrt':
            factor = decimal.Decimal(str(math.sqrt(factor)))

        return float(factor)

    @property
    def exponent(self) -> int:
        """
        Exponen this unit has.
        """
        return int(self._exponent)

    def __eq__(self, other):
        # noinspection PyProtectedMember
        if isinstance(other, Unit):
            return other._symbol == self._symbol

        elif isinstance(other, str):
            return other in (self.symbol, self.base_unit_string)

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def si_value(self) -> Optional[float]:
        if self._value is None:
            return None

        return float(self._value)

    @property
    def value(self) -> Optional[float]:
        if self._value is None:
            return None

        if self.raw_unit in ('°R', '°C', '°F', 'K'):
            val = self.__convert_temperature(
                self._value,
                to_unit=self.raw_unit
            )
            exponent = decimal.Decimal(str(self.exponent))
            try:
                val **= exponent
            except decimal.InvalidOperation:
                val = -((-val) ** exponent)

        else:
            val = self._value / decimal.Decimal(str(self.factor))

        return float(val)

    @value.setter
    def value(self, val: MathOperatorType):
        val = decimal.Decimal(str(val))

        if self.raw_unit in ('°R', '°C', '°F', 'K'):
            exponent = decimal.Decimal(str(self.exponent))
            exponent = decimal.Decimal("1.0") / exponent
            try:
                val **= exponent
            except decimal.InvalidOperation:
                val = -((-val) ** exponent)

            val = self.__convert_temperature(
                val,
                self.raw_unit
            )

        val *= decimal.Decimal(str(self.factor))

        if self._convert_to is not None:
            self._convert_to._value = decimal.Decimal('1.0') * val

        self._value = val

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
                symbol = symbol.replace(repl_exponent, exponent)
            else:
                symbol += exponent

        return symbol

    @property
    def base_unit_string(self) -> str:
        return MULTIPLIER.join(
            sorted(str(u) for u in self if u)
        )

    @property
    def raw_unit(self):
        symbol = self._symbol
        repl_exponent = ''

        for i in range(len(symbol) - 1, -1, -1):
            char = symbol[i]
            if char not in SUPER_SCRIPT_MAPPING:
                break

            repl_exponent = char + repl_exponent

        if repl_exponent:
            symbol = symbol.replace(repl_exponent, '')

        return symbol

    @property
    def quantities(self) -> list:
        return list(q() for q in self._quantities)

    @property
    def compatible_units(self) -> Sequence['Unit']:
        units = []
        for quantity in self._quantities:
            for unit in quantity:
                if unit in units:
                    continue

                units.append(unit)

        res = []

        for unit in units:
            res.append(unit())
            s_unit = str(unit)
            if MULTIPLIER in s_unit:
                continue

            new_unit = 'da' + s_unit
            if (
                new_unit not in UNITS and
                new_unit not in BASE_UNITS and
                new_unit not in NAMED_DERIVED_UNITS
            ):
                res.append(Unit(new_unit))

            for prefix in 'YZEPTGMkhdcmµnpfazy':
                new_unit = prefix + s_unit
                if new_unit in UNITS:
                    continue
                if new_unit in BASE_UNITS:
                    continue
                if new_unit in NAMED_DERIVED_UNITS:
                    continue

                try:
                    res.append(Unit(new_unit))
                except MalformedUnitError:
                    pass

        return res

    @staticmethod
    def __convert_temperature(
            value: MathOperatorType,
            from_unit: str = 'K',
            to_unit: str = 'K'
    ) -> decimal.Decimal:

        value = decimal.Decimal(str(value))

        if from_unit == '°R':
            value /= decimal.Decimal('1.8')
        elif from_unit == '°C':
            value += decimal.Decimal('273.15')
        elif from_unit == '°F':
            value = (
                    (value + decimal.Decimal('459.67')) /
                    decimal.Decimal('1.8')
            )

        if to_unit == '°R':
            value *= decimal.Decimal('1.8')
        elif to_unit == '°C':
            value -= decimal.Decimal('273.15')
        elif to_unit == '°F':
            value = (
                    decimal.Decimal('1.8') *
                    value -
                    decimal.Decimal('459.67')
            )

        return value

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

        try:
            unit = Unit(item)
        except MalformedUnitError:
            raise MalformedUnitError(item) from None

        if unit.base_unit_string != self.base_unit_string:
            raise UnitsNotCompatibleError(self, unit)

        unit = self / unit

        return unit

    def __bool__(self):
        return self._exponent != 0

    def __str__(self):
        if self._exponent == 0:
            return ''

        return self.symbol

    # ########################  SUBTRACTION   ###########################
    def __isub__(self, other: UnitOperatorType) -> "Unit":
        # cls -= other

        if isinstance(other, Unit):
            if self._value is not None is not other._value:
                if self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                value = decimal.Decimal(str(self.si_unit))
                value -= decimal.Decimal(str(other.si_unit))

                value /= decimal.Decimal(str(self.factor))
                self.value = value

                return self

        elif self._value is not None:
            value = decimal.Decimal(str(self.value))
            value -= decimal.Decimal(str(other))
            self.value = value
            return self

        raise ValueError("Unable to perform operation")

    def __sub__(self, other: UnitOperatorType) -> "Unit":
        # cls - other

        if isinstance(other, Unit):
            if self._value is not None is not other._value:
                if self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                value = decimal.Decimal(str(self.si_unit))
                value -= decimal.Decimal(str(other.si_unit))

                value /= decimal.Decimal(str(self.factor))
                self.value = value

                return self

        elif self._value is not None:
            value = decimal.Decimal(str(self.value))
            value -= decimal.Decimal(str(other))
            unit = self(value)
            return unit

        raise TypeError('Unable to perform operation')

    def __rsub__(self, other: MathOperatorType) -> float:
        # other -= cls
        # other - cls

        if self._value is not None:
            value = decimal.Decimal(str(self.value))
        else:
            value = decimal.Decimal(str(self.factor))

        value = decimal.Decimal(str(other)) - value
        return float(value)

    # ########################    ADDITION    ###########################
    def __iadd__(self, other: UnitOperatorType) -> "Unit":
        # cls += other

        if isinstance(other, Unit):
            if self._value is not None is not other._value:
                if self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                value = decimal.Decimal(str(self.si_value))
                value += decimal.Decimal(str(other.si_value))
                value /= decimal.Decimal(str(self.factor))
                self.value = value
                return self

            elif self.raw_unit != other.raw_unit:
                raise UnitsNotCompatibleError(self, other)

            elif self._value is None is other._value:
                self._exponent += other._exponent
                return self

        elif self._value is not None:
            value = decimal.Decimal(str(self.value))
            value += decimal.Decimal(str(other))
            self.value = value
            return self

        raise ValueError("Unable to perform operation")

    def __add__(self, other: UnitOperatorType) -> UnitOperatorType:
        # cls + other

        if isinstance(other, Unit):
            if self._value is not None is not other._value:
                if self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                value = decimal.Decimal(str(self.si_value))
                value += decimal.Decimal(str(other.si_value))
                value /= decimal.Decimal(str(self.factor))
                self.value = value
                return self

        elif self._value is not None:
            value = decimal.Decimal(str(self.value))
            value += decimal.Decimal(str(other))
            unit = self(value)
            return unit

        else:
            value = decimal.Decimal(str(self.factor))
            value += decimal.Decimal(str(other))
            return float(value)

        raise TypeError('Unable to perform operation')

    def __radd__(self, other: MathOperatorType) -> float:
        # other += cls
        # other + cls

        if self._value is not None:
            value = decimal.Decimal(str(self.value))
        else:
            value = decimal.Decimal(str(self.factor))

        value += decimal.Decimal(str(other))
        return float(value)

    # ######################## MULTIPLICATION ###########################
    def __imul__(self, other: UnitOperatorType) -> "Unit":
        # cls *= other

        if isinstance(other, Unit):
            is_temp = (
                self.raw_unit in ('°R', '°C', '°F', 'K') and
                other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is not None is not other._value:
                if is_temp:
                    value = self.__convert_temperature(
                        other.value,
                        other.raw_unit
                    )

                    value *= self.__convert_temperature(
                        self.value,
                        self.raw_unit
                    )

                    value = self.__convert_temperature(
                        value,
                        to_unit=self.raw_unit
                    )

                elif self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                else:
                    value = decimal.Decimal(str(self.si_value))
                    value *= decimal.Decimal(str(other.si_value))
                    value /= decimal.Decimal(str(self.factor))

                self.value = value
                return self
            else:
                f_units = list(self)
                t_units = list(other)
                unit = Unit(
                    self.symbol + MULTIPLIER + other.symbol,
                    base_units=f_units + t_units,
                    factor=float(self.factor * other.factor)
                )
                return unit
        else:
            other = decimal.Decimal(str(other))

            if self._convert_to is not None:
                if (
                        self.raw_unit in ('°R', '°C', '°F', 'K') and
                        self._convert_to.raw_unit in ('°R', '°C', '°F', 'K')
                ):
                    if self._value is not None:
                        value = self.si_value
                        value += self.__convert_temperature(
                            other,
                            self.raw_unit
                        )

                    else:
                        value = other

                    value = self.__convert_temperature(
                        value,
                        to_unit=self.raw_unit
                    )
                else:
                    if self._value is not None:
                        value = decimal.Decimal(str(self.value))
                        value *= other
                    else:
                        value = other

                self.value = value
                return self

            elif self._value is not None:
                value = decimal.Decimal(str(self.value))
                value *= other
                self.value = value
                return self

        raise TypeError('Unable to perform operation')

    def __mul__(self, other: UnitOperatorType) -> UnitOperatorType:
        # cls * other

        if isinstance(other, Unit):
            self_unit = self._symbol
            other_unit = other._symbol

            is_temp = (
                self.raw_unit in ('°R', '°C', '°F', 'K') and
                other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is not None is not other._value:
                if is_temp:
                    value = self.__convert_temperature(other.value, other_unit)
                    value *= self.__convert_temperature(self.value, self_unit)
                    value = self.__convert_temperature(
                        value,
                        to_unit=self_unit
                    )
                elif self.base_unit_string != other.base_unit_string:
                    raise UnitsNotCompatibleError(self, other)

                else:
                    value = decimal.Decimal(str(self.si_value))
                    value *= decimal.Decimal(str(other.si_value))
                    value /= decimal.Decimal(str(self.factor))

                unit = self()
                unit.value = value
                return unit

            elif self._value is None is other._value:
                f_units = list(self)
                t_units = list(other)
                unit = Unit(
                    self._symbol + MULTIPLIER + other._symbol,
                    base_units=f_units + t_units,
                    factor=float(self.factor * other.factor)
                )

                return unit

            elif self._value is not None:
                f_units = list(self)
                t_units = list(other)
                unit = Unit(
                    self._symbol + MULTIPLIER + other._symbol,
                    base_units=f_units + t_units,
                    factor=float(self.factor * other.factor)
                )
                unit._factor *= self.decimal.Decimal(str(self.si_units))
                return unit

            else:
                f_units = list(self)
                t_units = list(other)
                unit = Unit(
                    self._symbol + MULTIPLIER + other._symbol,
                    base_units=f_units + t_units,
                    factor=float(self.factor * other.factor)
                )
                unit._factor *= self.decimal.Decimal(str(other.si_units))
                return unit

        else:
            other = decimal.Decimal(str(other))

            if self._convert_to is not None:
                if (
                        self.raw_unit in ('°R', '°C', '°F', 'K') and
                        self._convert_to.raw_unit in ('°R', '°C', '°F', 'K')
                ):
                    if self._value is not None:
                        value = self.si_value
                        value += self.__convert_temperature(
                            other,
                            self.raw_unit
                        )

                    else:
                        value = other

                    value = self.__convert_temperature(
                        value,
                        to_unit=self.raw_unit
                    )
                elif self._value is not None:
                    value = decimal.Decimal(str(self.value))
                    value *= other
                else:
                    value = other

                unit = self(value)
                return unit

            elif self._value is None:
                factor = decimal.Decimal(str(self.factor))
                return float(factor * other)

    def __rmul__(self, other: MathOperatorType) -> float:
        # other *= cls
        # other * cls

        other = decimal.Decimal(str(other))

        if self._convert_to is not None:
            if (
                    self.raw_unit in ('°R', '°C', '°F', 'K') and
                    self._convert_to.raw_unit in ('°R', '°C', '°F', 'K')
            ):
                value = self.__convert_temperature(
                    other,
                    self.raw_unit,
                    self._convert_to.raw_unit
                )
                return float(value)

            else:
                factor = decimal.Decimal(str(self.factor))
                factor /= decimal.Decimal(str(self._convert_to.factor))
                return float(other * factor)

        if self._value is not None:
            value = decimal.Decimal(str(self.value))
        else:
            value = decimal.Decimal(str(self.factor))

        return float(value * other)

    # ########################  FLOOR DIVISION  ###########################
    def __ifloordiv__(self, other: UnitOperatorType) -> "Unit":
        # cls //= other

        if isinstance(other, Unit):
            is_temp = (
                    self.raw_unit in ('°R', '°C', '°F', 'K') and
                    other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is None is other._value:
                if self.base_unit_string != other.base_unit_string:
                    unit = Unit(
                        self.symbol + '/' + other.symbol
                    )
                    return unit
                else:
                    other._convert_to = self
                    self._convert_to = other
                    return self

            elif self._value is None:
                if is_temp:
                    self.value = self.__convert_temperature(
                        other.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                    return self
                else:
                    value = decimal.Decimal(str(other.factor))
                    value /= decimal.Decimal(str(self.factor))
                    value *= decimal.Decimal(str(other.value))
                    self.value = value
                    return self

        elif self._value is not None:
            other = decimal.Decimal(str(other))
            value = decimal.Decimal(str(self.value))
            self.value = value // other
            return self

        raise ValueError('Unable to perform operation')

    def __floordiv__(self, other: UnitOperatorType) -> UnitOperatorType:
        # cls // other

        if isinstance(other, Unit):
            is_temp = (
                self.raw_unit in ('°R', '°C', '°F', 'K') and
                other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is None is other._value:
                if self.base_unit_string != other.base_unit_string:
                    unit = Unit(
                        self.symbol + '/' + other.symbol
                    )
                else:
                    other._convert_to = self
                    unit = self()
                    unit._convert_to = other

                return unit

            elif self._value is None:
                if is_temp:
                    self.value = self.__convert_temperature(
                        other.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                    return self
                else:
                    value = decimal.Decimal(str(other.factor))
                    value /= decimal.Decimal(str(self.factor))
                    value *= decimal.Decimal(str(other.value))
                    self.value = value
                    return self
            else:
                if is_temp:
                    return self.__convert_temperature(
                        self.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                else:
                    value = decimal.Decimal(str(self.factor))
                    value /= decimal.Decimal(str(other.factor))
                    value *= decimal.Decimal(str(self.value))

                    return float(value)

        elif self._value is not None:
            other = decimal.Decimal(str(other))
            value = decimal.Decimal(str(self.value))
            self.value = value // other
            return self

        raise ValueError('Unable to perform operation')

    def __rfloordiv__(self, other: MathOperatorType) -> float:
        # other //= cls
        # other // cls

        if isinstance(other, Unit):
            raise TypeError('Unable to perform operation')
        if self._value is None:
            value = decimal.Decimal(str(self.factor))
        else:
            value = decimal.Decimal(str(self.value))

        other = decimal.Decimal(str(other))
        return float(other // value)

    # ########################   TRUE DIVISION  ###########################
    def __itruediv__(self, other: UnitOperatorType) -> "Unit":
        # cls /= other

        if isinstance(other, Unit):
            is_temp = (
                    self.raw_unit in ('°R', '°C', '°F', 'K') and
                    other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is None is other._value:
                if self.base_unit_string != other.base_unit_string:
                    unit = Unit(
                        self.symbol + '/' + other.symbol
                    )
                    return unit
                else:
                    other._convert_to = self
                    self._convert_to = other
                    return self

            elif self._value is None:
                if is_temp:
                    self.value = self.__convert_temperature(
                        other.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                    return self
                else:
                    value = decimal.Decimal(str(other.factor))
                    value /= decimal.Decimal(str(self.factor))
                    value *= decimal.Decimal(str(other.value))
                    self.value = value
                    return self

        elif self._value is not None:
            other = decimal.Decimal(str(other))
            value = decimal.Decimal(str(self.value))
            self.value = value / other
            return self

        raise ValueError('Unable to perform operation')

    def __truediv__(self, other: UnitOperatorType) -> UnitOperatorType:
        # cls / other

        if isinstance(other, Unit):
            is_temp = (
                self.raw_unit in ('°R', '°C', '°F', 'K') and
                other.raw_unit in ('°R', '°C', '°F', 'K')
            )

            if self._value is None is other._value:
                if self.base_unit_string != other.base_unit_string:
                    unit = Unit(
                        self.symbol + '/' + other.symbol
                    )
                else:
                    other._convert_to = self
                    unit = self()
                    unit._convert_to = other

                return unit

            elif self._value is None:
                if is_temp:
                    self.value = self.__convert_temperature(
                        other.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                    return self
                else:
                    value = decimal.Decimal(str(other.factor))
                    value /= decimal.Decimal(str(self.factor))
                    value *= decimal.Decimal(str(other.value))
                    self.value = value
                    return self
            else:
                if is_temp:
                    return self.__convert_temperature(
                        self.value,
                        self.raw_unit,
                        other.raw_unit,
                    )
                else:
                    value = decimal.Decimal(str(self.factor))
                    value /= decimal.Decimal(str(other.factor))
                    value *= decimal.Decimal(str(self.value))

                    return float(value)

        elif self._value is not None:
            other = decimal.Decimal(str(other))
            value = decimal.Decimal(str(self.value))
            self.value = value / other
            return self

        raise ValueError('Unable to perform operation')

    def __rtruediv__(self, other: MathOperatorType) -> float:
        # other /= cls
        # other / cls

        if isinstance(other, Unit):
            raise TypeError('Unable to perform operation')
        if self._value is None:
            value = decimal.Decimal(str(self.factor))
        else:
            value = decimal.Decimal(str(self.value))

        other = decimal.Decimal(str(other))
        return float(other / value)

    def __ipow__(self, other: MathOperatorType) -> 'Unit':
        # cls **= other
        unit = self()
        unit._exponent *= decimal.Decimal(str(other))
        return unit

    def __pow__(self, power: MathOperatorType, modulo=None) -> "Unit":
        # cls ** other
        unit = self()
        unit._exponent *= decimal.Decimal(str(power))
        return unit

    def __rpow__(self, other: MathOperatorType) -> float:
        # other **= cls
        # other ** cls

        if self._value is None:
            raise TypeError('Unable to complete operation')

        value = decimal.Decimal(str(self.value))
        other = decimal.Decimal(str(other))

        try:
            return float(other ** value)
        except decimal.InvalidOperation:
            return float(-((-other) ** value))
