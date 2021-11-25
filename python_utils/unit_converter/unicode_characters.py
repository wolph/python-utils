
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
EL = chr(0x041B)  # type: str # л
ES = chr(0x0441)  # type: str # с
KA = chr(0x041A)  # type: str # к

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
