import decimal
import math

from .unicode_characters import (
    MULTIPLIER,
    SUPER_SCRIPT_MAPPING
)


BASE_UNITS = {}
NAMED_DERIVED_UNITS = {}
UNITS = {}


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
    '''

    def __init__(
            self,
            symbol,  # type: str
            base_units=None,  # type: list[Unit] or None
            factor=1.0,  # type: float or decimal.Decimal
            exponent=1  # type: int or decimal.Decimal
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

        if not base_units and symbol not in BASE_UNITS:
            self._b_units = self._process_unit(symbol)

    def _process_unit(
            self,
            unit
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
            exp = False
            for i, char in enumerate(unit):
                if exp:
                    if char.isdigit() or char == '-':
                        exponent += char
                        continue
                    else:
                        exp = False
                if char in SUPER_SCRIPT_MAPPING:
                    exponent += SUPER_SCRIPT_MAPPING[char]
                elif char == '^':
                    exp = True
                elif i > 0 and char == '*':
                    if unit[i-1] == '*':
                        exp = True
                else:
                    c_unit += char

            if exponent == '':
                exponent = '1'

            exponent = decimal.Decimal(exponent)
            u = c_unit

            if u in BASE_UNITS:
                unt = BASE_UNITS[u]
                if unt is None:
                    return []

                found_unit = unt(exponent=exponent)
                return [found_unit]
            elif u in NAMED_DERIVED_UNITS:
                found_unit = NAMED_DERIVED_UNITS[u](exponent=exponent)
                return [found_unit]
            elif u in UNITS:
                unt = UNITS[u]
                if unt is None:
                    return []

                found_unit = unt(exponent=exponent)
                return [found_unit]
            else:
                unt = self._parse_unit_prefix(u)
                if unt is None:
                    raise ValueError('Unit {0} not found'.format(unit))

                unt._exponent = exponent
                return [unt]

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
                    if symbol in BASE_UNITS:
                        base_unit = [BASE_UNITS[symbol]]
                    elif symbol in NAMED_DERIVED_UNITS:
                        base_unit = [NAMED_DERIVED_UNITS[symbol]]
                    elif unit in UNITS:
                        base_unit = [UNITS[symbol]]
                    else:
                        return

                    return Unit(
                        unit,
                        base_units=base_unit,
                        factor=factor
                    )

    def __call__(
            self,
            factor=None,  # type: None or float or decimal.Decimal
            exponent=None  # type: None or int or decimal.Decimal
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
        return self.__mul__(other)

        # factor = self.factor
        #
        # if isinstance(other, Unit):
        #     return factor * other.factor
        # else:
        #     return self.__mul__(other)

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

        else:
            if isinstance(other, bytes):
                othr = other.decode('utf-8')
            else:
                othr = other

            if isinstance(othr, str):
                try:
                    int(othr)
                except ValueError:
                    try:
                        float(othr)
                    except ValueError:
                        raise ValueError(
                            'Not a numerical value ({0})'.format(
                                repr(other)
                            )
                        ) from None

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

                    if isinstance(othr, str):
                        try:
                            int(othr)
                        except ValueError:
                            try:
                                float(othr)
                            except ValueError:
                                raise ValueError(
                                    'Not a numerical value ({0})'.format(
                                        repr(oth)
                                    )
                                ) from None

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
