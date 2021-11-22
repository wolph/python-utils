from . import units
from .unicode_characters import (
    MULTIPLIER,
    SUPER_SCRIPT_MAPPING
)
from .unit import (
    Unit,
    BASE_UNITS,
    NAMED_DERIVED_UNITS,
    UNITS
)

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
    BASE_UNITS[symbol] = None
    BASE_UNITS[symbol] = Unit(symbol, [])

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(units, attr_name, BASE_UNITS[symbol])

    else:
        setattr(units, symbol, BASE_UNITS[symbol])


def _build_derived_unit(symbol, units_):
    base_units = []

    for u in units_.split(MULTIPLIER):
        exponent = ''
        unit = ''

        for char in u:
            if char in SUPER_SCRIPT_MAPPING:
                exponent += SUPER_SCRIPT_MAPPING[char]
            else:
                unit += char

        if exponent == '':
            exponent = '1'

        base_unit = BASE_UNITS[unit](exponent=int(exponent))
        base_units.append(base_unit)

    NAMED_DERIVED_UNITS[symbol] = Unit(symbol, base_units[:])

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(units, attr_name, NAMED_DERIVED_UNITS[symbol])

    else:
        setattr(units, symbol, NAMED_DERIVED_UNITS[symbol])


def build_unit(symbol, factor, units_):
    base_units = []

    if symbol in BASE_UNITS:
        raise RuntimeError(
            'unit {0} already exists in BASE_UNITS'.format(symbol)
        )

    if symbol in NAMED_DERIVED_UNITS:
        raise RuntimeError(
            'unit {0} already exists in NAMED_DERIVED_UNITS'.format(symbol)
        )

    if symbol in UNITS:
        raise RuntimeError(
            'unit {0} already exists in UNITS'.format(symbol)
        )

    for u in units_.split(MULTIPLIER):
        exponent = ''
        unit = ''

        for char in u:
            if char in SUPER_SCRIPT_MAPPING:
                exponent += SUPER_SCRIPT_MAPPING[char]
            else:
                unit += char

        if exponent == '':
            exponent = '1'

        if unit in BASE_UNITS:
            unit = BASE_UNITS[unit]
        elif unit in NAMED_DERIVED_UNITS:
            unit = NAMED_DERIVED_UNITS[unit]
        elif unit in UNITS:
            unit = UNITS[unit]
        else:
            if not unit:
                continue
            raise RuntimeError('Sanity Check ({0})'.format(repr(unit)))

        unit = unit(exponent=int(exponent))
        base_units.append(unit)

    if base_units:
        UNITS[symbol] = Unit(symbol, base_units[:], factor=factor)
    else:
        UNITS[symbol] = None
        UNITS[symbol] = Unit(symbol, factor=factor)

    if symbol in _UNIT_TO_ATTRIBUTE:
        attr_name = _UNIT_TO_ATTRIBUTE[symbol]
        if attr_name is not None:
            setattr(units, attr_name, UNITS[symbol])

    else:
        setattr(units, symbol, UNITS[symbol])


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
_build_derived_unit('°C', 'K')

# temperature

build_unit('°R', 1.0, 'K')
build_unit('°F', 1.0, 'K')
# a.u. of length
build_unit('au_length', 5.2917699999999994e-11, 'm')
build_unit('am', 1e-18, 'm')  # attometer
build_unit('Å', 1e-10, 'm')  # ångström
build_unit('ft', 0.3048000000012192, 'm')  # foot
build_unit('ft_survey', 0.30480061, 'm')  # US Survey foot
build_unit('yd', 0.9144000000315285, 'm')  # yard
build_unit('mi', 1609.344, 'm')  # mile
build_unit('in', 0.02539999999997257, 'm')  # inch
build_unit('µ', 1e-06, 'm')  # micron
build_unit('arcmin', 0.000290888, 'm')  # arcmin
build_unit('AU', 149597870700, 'm')  # astronomical unit
build_unit('UA', 149597870700, 'm')  # astronomical unit
build_unit('au', 149597870700, 'm')  # astronomical unit
build_unit('agate', 0.00181428571429, 'm')  # agate
build_unit('aln', 0.593778, 'm')  # alens
build_unit('bcorn', 0.0084666666666667, 'm')  # barleycorn (UK)
build_unit('a0', 5.2917699999999994e-11, 'm')  # first Bohr radius
build_unit('rBohr', 5.2917699999999994e-11, 'm')  # first Bohr radius
build_unit('bolt', 36.576, 'm')  # bolt (US cloth)
build_unit('bl', 80.4672, 'm')  # blocks
build_unit('line_UK', 0.00211667, 'm')  # button (UK)
build_unit('line', 0.000635, 'm')  # button (US)
build_unit('cable_int', 185.2, 'm')  # cable length (int.)
build_unit('cable_UK', 185.318, 'm')  # cable length (UK)
build_unit('cable', 219.456, 'm')  # cable length (US)
build_unit('caliber', 2.54e-4, 'm')  # caliber (centiinch)
build_unit('ch_engineer', 30.48, 'm')  # chain (engineer's)
build_unit('ch_gunter', 20.1168, 'm')  # chain (Gunter's)
build_unit('ch_ramsden', 30.48, 'm')  # chain (Ramsden's)
build_unit('ch_surveyor', 20.1168, 'm')  # chain (surveyor's)
build_unit('cbt', 0.4572, 'm')  # cubit (UK)
build_unit('didotpoint', 0.000375972222, 'm')  # didot point
build_unit('digit', 0.01905, 'm')  # digits
build_unit('re', 2.81794e-15, 'm')  # electron classical radius
build_unit('Ec', 40000000, 'm')  # Earth circumfrence
build_unit('eel_scottish', 0.94, 'm')  # ell (Scottish)
build_unit('eel_flemish', 0.686, 'm')  # ell (Flemish)
build_unit('eel_french', 1.372, 'm')  # ell (French)
build_unit('eel_polish', 0.787, 'm')  # ell (Polish)
build_unit('eel_danish', 0.627708, 'm')  # ell (Danish)
build_unit('eel_swedish', 0.59, 'm')  # ell (Swedish)
build_unit('eel_german', 0.547, 'm')  # ell (German)
build_unit('EM_pica', 0.0042175176, 'm')  # ems (pica)
build_unit('Em', 1e+17, 'm')  # exameter
build_unit('fath', 1.8288, 'm')  # fathom
build_unit('fm', 1e-15, 'm')  # femtometer
build_unit('f', 1e-15, 'm')  # fermi
build_unit('finer', 0.1143, 'm')  # finger-cloth
build_unit('fb', 0.022225, 'm')  # fingerbreadth
build_unit('fod', 0.3141, 'm')  # fod
build_unit('fbf', 91.44, 'm')  # football-field
build_unit('fur', 201.168, 'm')  # furlong
build_unit('pleth', 30.8, 'm')  # greek-plethron
build_unit('std', 185.0, 'm')  # greek-stadion
build_unit('hand', 0.1016, 'm')  # hands
build_unit('hiMetric', 1e-05, 'm')  # himetric
build_unit('hl', 2.4, 'm')  # horse-length
build_unit('hvat', 1.89648384, 'm')  # hvat
build_unit('ly', 9461000000000000.0, 'm')  # light years
build_unit('li', 0.201168402337, 'm')  # links
build_unit('LD', 384402000, 'm')  # lunar-distance
build_unit('mil', 2.54e-05, 'm')  # mils
build_unit('Mym', 10000, 'm')  # myriameters
build_unit('nail', 0.05715, 'm')  # nails-cloth
build_unit('NL', 5556, 'm')  # Nautical Leagues
build_unit('NM', 1852, 'm')  # Nautical Miles
build_unit('pace', 0.762, 'm')  # paces
build_unit('palm', 0.0762, 'm')  # palms
build_unit('pc', 3.0856775814914e+16, 'm')  # parsecs
build_unit('perch', 5.0292, 'm')  # perch
build_unit('p', 0.00423333333, 'm')  # picas
build_unit('PX', 0.0002645833, 'm')  # pixels
build_unit('pl', 1.6e-35, 'm')  # planck-length
build_unit('pole', 5.0292, 'm')  # poles
build_unit('ru', 0.04445, 'm')  # rack-unit
build_unit('rem', 0.0042333328, 'm')  # rems
build_unit('rd', 5.0292, 'm')  # rods
build_unit('actus', 35.5, 'm')  # roman-actus
build_unit('rope', 6.096, 'm')  # ropes
build_unit('sir', 1.496e+17, 'm')  # siriometer
build_unit('span', 0.2286, 'm')  # spans
build_unit('twip', 1.7639e-05, 'm')  # twips
build_unit('vr', 0.84667, 'm')  # varas
build_unit('vst', 1066.8, 'm')  # versts
build_unit('xu', 1.002004e-13, 'm')  # x-unit
build_unit('zoll', 0.0254, 'm')  # zolls
build_unit('µµ', 1e-12, 'm')  # bicrons

build_unit('D', 9.86923e-13, 'm²')  # darcy
build_unit('ac', 4046.8564224, 'm²')  # acre
build_unit('acre', 4046.8564224, 'm²')  # acre
build_unit('are', 100, 'm²')  # are
build_unit('b', 1e-27, 'm²')  # barn
build_unit('cirin', 0.0005067074790975, 'm²')  # circular inch
build_unit('cirmil', 5.067074790975e-10, 'm²')  # circular mil
build_unit('Mg_dutch', 8244.35, 'm²')  # morgen (Dutch)
build_unit('Mg_prussian', 2532.24, 'm²')  # morgen (Prussian)
build_unit('Mg_southafrica', 8565.3, 'm²')  # morgen (South Africa)
build_unit('¼mi²_stat', 647497.0, 'm²')  # quarter section
build_unit('¼ac', 1011.71, 'm²')  # rood (UK)
build_unit('rood', 1011.71, 'm²')  # rood (UK)
build_unit('sqmi', 2589990.0, 'm²')  # section (square statute mile)
build_unit('mi²_stat', 2589990.0, 'm²')  # section (square statute mile)
build_unit('outhouse', 1e-34, 'm²')  # outhouse
build_unit('shed', 1e-52, 'm²')  # shed
build_unit('sqch_engineer', 929.03, 'm²')  # square chain (engineer's)
build_unit('sqch_gunter', 404.686, 'm²')  # square chain (Gunter's)

build_unit('acre⋅ft', 1233.48, 'm³')  # acre foot
build_unit('bag', 0.109106, 'm³')  # bag (UK)
build_unit('bbl_UScranb', 0.095471, 'm³')  # barrel (US, cranb.)
build_unit('bbl', 0.1192404712, 'm³')  # barrel (US)
build_unit('bbl_USpetrol', 0.1589872949, 'm³')  # barrel (US petrol)
build_unit('bbl_UK', 0.16365924, 'm³')  # barrel (UK)
build_unit('FBM', 0.002359737, 'm³')  # board foot measure
build_unit('bouteille', 0.000757682, 'm³')  # bouteille
build_unit('bk_UK', 0.0181844, 'm³')  # bucket (UK)
build_unit('bu_UK', 0.036368700000000004, 'm³')  # bushel (UK)
build_unit('bu_US', 0.0352391, 'm³')  # bushel (US, dry)
build_unit('bt_UK', 0.490978, 'm³')  # butt (UK)
build_unit('chal_UK', 1.30927, 'm³')  # chaldron (UK)
build_unit('cc', 1.00238e-06, 'm³')  # cubic centimeter (Mohr cubic centimeter)
build_unit('l', 0.001, 'm³')  # Liter
build_unit('L', 0.001, 'm³')  # Liter
build_unit('gal', 0.00378541178, 'm³')  # Gallon (US)
build_unit('gal_UK', 4.54609e-3, 'm³')  # Gallon (UK)
build_unit('qt', 0.000946352946, 'm³')  # Quart (US)
build_unit('qt_UK', 0.0011365225, 'm³')  # Quart (UK)
build_unit('pt', 0.000473176473, 'm³')  # Pint (US)
build_unit('pt_UK', 0.00056826125, 'm³')  # Pint (UK)
build_unit('floz', 2.95735296875e-05, 'm³')  # Fluid Ounce (US)
build_unit('floz_UK', 2.84130625e-05, 'm³')  # Fluid Ounce (UK)
build_unit('cran', 0.170478, 'm³')  # cran
build_unit('dr', 3.6967e-06, 'm³')  # dram
build_unit('st', 1.0, 'm³')  # stere
build_unit('gi', 0.0001182941, 'm³')  # gill (US)
build_unit('gi_UK', 0.0001420653, 'm³')  # gill (UK)
build_unit('cup', 0.00025, 'm³')  # cup (US)
build_unit('cup_UK', 0.0002841306, 'm³')  # cup (UK)
build_unit('dstspn', 9.8578e-06, 'm³')  # dessertspoon (US)
build_unit('dstspn_UK', 1.18388e-05, 'm³')  # dessertspoon (UK)
build_unit('tbsp', 1.5e-05, 'm³')  # tablespoon (US)
build_unit('tbsp_UK', 1.77582e-05, 'm³')  # tablespoon (UK)
build_unit('tsp', 5e-06, 'm³')  # teaspoon (US)
build_unit('tsp_UK', 5.9194e-06, 'm³')  # teaspoon (UK)

# electron rest mass (a.u. of mass)
build_unit('m₀', 9.10939e-31, 'kg')
# electron rest mass (a.u. of mass)
build_unit('me', 9.10939e-31, 'kg')
build_unit('u_dalton', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
build_unit('u', 1.660540199e-27, 'kg')  # atomic mass unit
build_unit('uma', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
build_unit('Da', 1.66054e-27, 'kg')  # dalton (atomic unit of mass)
build_unit('dr_troy', 0.00388793, 'kg')  # dram (troy)
build_unit('dr_apoth', 0.00388793, 'kg')  # dram or drachm (apothecary)
# dram or drachm (avoirdupois)
build_unit('dr_avdp', 0.001771845195312458, 'kg')
build_unit('g', 0.001, 'kg')  # gram
build_unit('lb', 0.45359237001003544, 'kg')  # pound
build_unit('oz', 0.028349523124984257, 'kg')  # ounce
build_unit('t_long', 1016.0469088, 'kg')  # ton (long)
build_unit('t_short', 907.18474, 'kg')  # ton(short)
build_unit('t', 1000.0, 'kg')  # metric ton
build_unit('dwt', 0.0015551738, 'kg')  # pennyweight
build_unit('kip', 453.59237, 'kg')  # kip
build_unit('gr', 6.479891000000013e-5, 'kg')  # grain
build_unit('slug', 14.5939029372, 'kg')  # geepound (slug)
build_unit('t_assay', 0.029167, 'kg')  # assay ton
build_unit('Da_12C', 1.66054e-27, 'kg')  # atomic unit of mass (¹²C)
build_unit('Da_16O', 1.66001e-27, 'kg')  # atomic unit of mass (¹⁶O)
build_unit('Da_1H', 1.67353e-27, 'kg')  # atomic unit of mass (¹H)
build_unit('avogram', 1.66036e-24, 'kg')  # avogram
build_unit('bag_UK', 42.6377, 'kg')  # bag (UK, cement)
build_unit('ct', 0.0002, 'kg')  # carat (metric)
build_unit('ct_troy', 0.000205197, 'kg')  # carat (troy)
build_unit('cH', 45.3592, 'kg')  # cental
build_unit('cwt', 100.0, 'kg')  # quintal

# a.u. of time
build_unit('au_time', 2.4188800000000002e-17, 's')
build_unit('blink', 0.864, 's')  # blink
build_unit('d', 86400.0, 's')  # day
build_unit('d_sidereal', 86164.0, 's')  # day (sidereal)
build_unit('fortnight', 1209600.0, 's')  # fortnight
build_unit('h', 3600.0, 's')  # hour
build_unit('min', 60.0, 's')  # minute
build_unit('mo', 2592000.0, 's')  # month (30 days)
build_unit('mo_sidereal', 2360590.0, 's')  # month (sidereal)
build_unit('mo_mean', 2628000.0, 's')  # month (solar mean)
build_unit('mo_synodic', 2551440.0, 's')  # month (synodic), lunar month
build_unit('shake', 1e-08, 's')  # shake
build_unit('week', 604800.0, 's')  # week
build_unit('wink', 3.33333e-10, 's')  # wink
build_unit('a_astr', 31557900.0, 's')  # year (astronomical), Bessel year
build_unit('a', 31536000.0, 's')  # year (calendar)
build_unit('y', 31536000.0, 's')  # year (calendar)
build_unit('a_sidereal', 31558200.0, 's')  # year (sidereal)
build_unit('a_mean', 31557600.0, 's')  # year (solar mean)
build_unit('a_tropical', 31556900.0, 's')  # year (tropical)

build_unit('bd', 1.02, 'cd')  # bougie d&egrave;cimale
build_unit('bi', 1.0, 'cd')  # bougie international
build_unit('c_int', 1.01937, 'cd')  # candle (int.)
build_unit('c', 1.0, 'cd')  # candle (new unit)
build_unit('carcel', 10.0, 'cd')  # carcel
build_unit('HK', 0.903, 'cd')  # hefner unit (hefnerkerze)
build_unit('violle', 20.4, 'cd')  # violle

build_unit('entities', 1.66054e-24, 'mol')  # entities
build_unit('SCF', 1.19531, 'mol')  # standard cubic foot
build_unit('SCM', 44.6159, 'mol')  # standard cubic meter

build_unit('\'', 0.000290888, 'r')  # arc minute (minute of arc)
build_unit('"', 4.84814e-06, 'r')  # arc second (second of arc)
build_unit('pid', 6.28319, 'r')  # circumference
build_unit('°', 0.0174533, 'r')  # degree
build_unit('gon', 0.015708, 'r')  # gon
build_unit('grade', 0.015708, 'r')  # grade
build_unit('ah', 0.261799, 'r')  # hour of arc
build_unit('%', 0.00999967, 'r')  # percent
build_unit('rev', 6.28319, 'r')  # revolution
build_unit('sign', 0.523599, 'r')  # sign

build_unit('B', 8, 'bit')  # byte
build_unit('Gib', 1073740000.0, 'bit')  # gigabinarybit (gibibit)
build_unit('GiB', 8589930000.0, 'bit')  # gigabinarybyte (gibibyte)
build_unit('Gb', 1000000000.0, 'bit')  # gigabit
build_unit('GB', 8000000000.0, 'bit')  # gigabyte
build_unit('Kib', 1024, 'bit')  # kilobinarybit (kibibit)
build_unit('KiB', 8192, 'bit')  # kilobinarybyte (kibibyte)
build_unit('Kb', 1000, 'bit')  # kilobit
build_unit('KB', 8000, 'bit')  # kilobyte
build_unit('Mib', 1048580.0, 'bit')  # megabinarybit (mebibit)
build_unit('MiB', 8388610.0, 'bit')  # megabinarybyte (mebibyte)
build_unit('Mb', 1000000.0, 'bit')  # megabit
build_unit('MB', 8000000.0, 'bit')  # megabyte
build_unit('Tib', 1099510000000.0, 'bit')  # terabinarybit (tebibit)
build_unit('TiB', 8796090000000.0, 'bit')  # terabinarybyte (tebibyte)
build_unit('Tb', 100000000000.0, 'bit')  # terabit
build_unit('TB', 8000000000000.0, 'bit')  # terabyte

build_unit('aW', 1e-07, 'W')  # abwatt (emu of power)
build_unit('hp', 745.7, 'W')  # horsepower (550 ft-lbf/s)
build_unit('hp_boiler', 9809.5, 'W')  # horsepower (boiler)
build_unit('hp_British', 745.7, 'W')  # horsepower (British)
build_unit('cv', 735.499, 'W')  # horsepower (cheval-vapeur)
build_unit('hp_cheval', 735.499, 'W')  # horsepower (cheval-vapeur)
build_unit('hp_electric', 746.0, 'W')  # horsepower (electric)
build_unit('hp_metric', 735.499, 'W')  # horsepower (metric)
build_unit('hp_water', 746.043, 'W')  # horsepower (water)
build_unit('prony', 98.0665, 'W')  # prony

build_unit('at', 98066.5, 'Pa')  # atmosphere (technical)
build_unit('atm', 101325.0, 'Pa')  # atmosphere (standard)
build_unit('bar', 100000.0, 'Pa')  # bar
build_unit('Ba', 0.1, 'Pa')  # Bayre
build_unit('p_P', 4.63309e+113, 'Pa')  # Planck pressure
build_unit('cgs', 0.1, 'Pa')  # centimeter-gram-second
build_unit('torr', 133.32236842, 'Pa')  # Torr
build_unit('pz', 1000.0, 'Pa')  # pieze
build_unit('Hg', 133322.368421, 'Pa')  # Hg (mercury) (0°C)
build_unit('H₂O', 9806.65, 'Pa')  # H₂O (water) (0°C)
build_unit('H2O', 9806.65, 'Pa')  # H₂O (water) (0°C)
build_unit('Aq', 9806.65, 'Pa')  # H₂O (water) (0°C)
build_unit('O₂', 12.677457000000462, 'Pa')  # O₂ (air) (0°C)
build_unit('O2', 12.677457000000462, 'Pa')  # O₂ (air) (0°C)
build_unit('ksi', 6894757.293200044, 'Pa')  # kilopound force per square inch
build_unit('psi', 6894.7572932, 'Pa⋅m')  # pound force per square inch

build_unit('psf', 47.88025897999996, 'Pa')  # pound force per square foot
build_unit('osi', 430.9223300000048, 'Pa')  # ounce force per square inch

build_unit('kerma', 1.0, 'Gy')  # kerma
build_unit('Mrd', 10000.0, 'Gy')  # megarad
build_unit('rad', 0.01, 'Gy')  # radian (radioactive)

build_unit('B_power', 10.0, 'dB')  # bel (power)
build_unit('B_voltage', 5.0, 'dB')  # bel (voltage)
build_unit('dB_power', 1.0, 'dB')  # decibel (power)
build_unit('dB_voltage', 0.5, 'dB')  # decibel (voltage)
build_unit('Nₚ', 4.34294, 'dB')  # neper

# a.u. of magnetic field
build_unit('au_mf', 235052.0, 'T')
build_unit('Gs', 1e-05, 'T')  # gauss

build_unit('M', 1e-09, 'Wb')  # maxwell

# a.u. of charge
build_unit('au_charge', 1.60218e-19, 'C')
build_unit('aC', 10, 'C')  # abcoulomb (emu of charge)
build_unit('esc', 1.6022e-19, 'C')  # electronic charge
build_unit('esu', 3.336e-06, 'C')  # electrostatic unit
build_unit('Fr', 3.33564e-10, 'C')  # franklin
build_unit('statC', 3.35564e-10, 'C')  # statcoulomb

build_unit('aS', 1000000000.0, 'S')  # abmho (emu of conductance)
build_unit('aW-1', 1000000000.0, 'S')  # abmho (emu of conductance)
build_unit('gemʊ', 1e-07, 'S')  # gemmho
build_unit('mho', 1.0, 'S')  # mho
build_unit('statmho', 1.11265e-12, 'S')  # statmho

build_unit('aH', 1e-10, 'H')  # abhenry (emu of inductance)
build_unit('statH', 898755000000.0, 'H')  # stathenry

# a.u. of electric potential
build_unit('au_ep', 27.2114, 'V')
build_unit('aV', 1e-09, 'V')  # abvolt (emu of electric potential)
build_unit('statV', 299.792, 'V')  # statvolt
build_unit('V_mean', 1.00034, 'V')  # volt (mean)
build_unit('V_US', 1.00033, 'V')  # volt (US)

build_unit('aΩ', 1e-10, 'Ω')  # abohm (emu of resistance)
build_unit('SΩ', 0.96, 'Ω')  # siemens (resistance)
build_unit('statohm', 898755000000.0, 'Ω')  # statohm

# a.u. of energy
build_unit('au_energy', 4.35975e-18, 'J')
build_unit('bboe', 6120000000.0, 'J')  # barrel oil equivalent
build_unit('BeV', 1.60218e-10, 'J')  # BeV (billion eV)
build_unit('Btu_ISO', 1055.06, 'J')  # British thermal unit (ISO)
build_unit('Btu_IT', 1055.06, 'J')  # British thermal unit (IT)
build_unit('Btu_mean', 1055.87, 'J')  # British thermal unit (mean)
build_unit('Btu_therm', 1054.35, 'J')  # British thermal unit (thermochemical)
build_unit('cal_15', 4.185, 'J')  # calorie (15°C)
build_unit('cal_4', 4.2045, 'J')  # calorie (4°C)
build_unit('Cal', 4180.0, 'J')  # Calorie (diet kilocalorie)
build_unit('kcal', 4180.0, 'J')  # Calorie (diet kilocalorie)
build_unit('cal_IT', 4.18674, 'J')  # calorie (IT) (International Steam Table)
build_unit('cal_mean', 4.19002, 'J')  # calorie (mean)
build_unit('cal_therm', 4.184, 'J')  # calorie (thermochemical)
build_unit('Chu', 1899.18, 'J')  # Celsius-heat unit
build_unit('eV', 1.60218e-19, 'J')  # electronvolt
build_unit('erg', 1e-07, 'J')  # erg
build_unit('Eh', 4.35975e-18, 'J')  # hartree

# a.u. of force
build_unit('au_force', 8.23873e-08, 'N')
build_unit('crinal', 0.1, 'N')  # crinal
build_unit('dyn', 1e-05, 'N')  # dyne
build_unit('gf', 0.00980665, 'N')  # gram force
build_unit('kgf', 9.80665, 'N')  # kilogram force
build_unit('kgp', 9.80665, 'N')  # kilogram force
build_unit('grf', 0.6355, 'N')  # grain force
build_unit('kp', 9.80665, 'N')  # kilopond
build_unit('kipf', 4448.22, 'N')  # kilopound force (kip force)
build_unit('lbf', 4.4482216, 'N')  # Poundal force (US) (pound force)
build_unit('pdl', 0.138255, 'N')  # Poundal force (UK)
build_unit('slugf', 143.117, 'N')  # slug force
build_unit('tf_long', 9964.02, 'N')  # ton force (long)
build_unit('tf_metric', 9806.65, 'N')  # ton force (metric)
build_unit('tf_short', 8896.44, 'N')  # ton force (short)
build_unit('ozf', 0.278014, 'N')  # ounce force

# a.u. of electric current
build_unit('au_ec', 0.00662362, 'A')
build_unit('abA', 10, 'A')  # abampere
build_unit('Bi', 10, 'A')  # biot
build_unit('edison', 100.0, 'A')  # edison
build_unit('statA', 3.35564e-10, 'A')  # statampere
build_unit('gilbert', 0.79577, 'A')  # gilbert
build_unit('pragilbert', 11459.1, 'A')  # pragilbert

build_unit('cps', 1.0, 'Hz')  # cycles per second

build_unit('Kt', 0.0416667, '')  # carat (karat)
build_unit('ppb', 1e-10, '')  # part per billion
build_unit('pph', 0.001, '')  # part per hundred
build_unit('pphm', 1e-09, '')  # part per hundred million
build_unit('ppht', 1e-06, '')  # part per hundred thousand
build_unit('ppm', 1e-07, '')  # part per million
build_unit('ppq', 1e-15, '')  # part per quadrillion
build_unit('ppt_tera', 1e-13, '')  # part per tera
build_unit('ppt', 0.001, '')  # part per thousand

build_unit('Ci', 37000000000.0, 'Bq')  # curie

build_unit('sp', 12.5664, 'sr')  # spat

build_unit('gy', 1000, 'kg⋅m⁻³')  # specific gravity

build_unit('lbm', 0.45359237001003544, 'kg⋅m²')  # pound mass

build_unit('Ω_mechanical', 1.0, 'Pa⋅s⋅m⁻³')  # ohm (mechanical, SI)

build_unit('perm_0C', 5.72135e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (0°C)
build_unit('perm_23C', 5.74525e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (23°C)
build_unit('permin_0C', 1.45322e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (0°C)
build_unit('permin_23C', 1.45929e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (23°C)
build_unit('permmil_0C', 1.45322e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (0°C)
build_unit('permmil_23C', 1.45929e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (23°C)

build_unit('brewster', 1e-12, 'm²⋅N⁻¹')  # brewster

build_unit('aF', 1000000000.0, 'F')  # abfarad (emu of electric capacitance)
build_unit('jar', 1.11111e-09, 'F')  # jar
build_unit('statF', 1.11265e-12, 'F')  # statfarad

build_unit('P', 0.1, 'Pa⋅s')  # Poise
build_unit('Pl', 1.0, 'Pa⋅s')  # poiseuille
build_unit('reyn', 6894.76, 'Pa⋅s')  # reynolds (reyns)

build_unit('clo', 0.15482, 'K⋅m²⋅W⁻¹')  # clo
build_unit('°F⋅ft²⋅h⋅Btu_therm⁻¹', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
build_unit('°F⋅ft²⋅h/Btu_therm', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
build_unit('RSI', 1.0, 'K⋅m²⋅W⁻¹')  # RSI (metric R-value)
build_unit('tog', 0.1, 'K⋅m²⋅W⁻¹')  # tog

build_unit('Bz', 1.0, 'm⋅s⁻¹')  # benz
build_unit('kn_noeud', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
build_unit('knot_noeud', 0.514444, 'm⋅s⁻¹')  # knot (noeud)
build_unit('mpy', 8.04327e-13, 'm⋅s⁻¹')  # mil per year
build_unit('kn', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
build_unit('knot', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
build_unit('c_light', 299792000.0, 'm⋅s⁻¹')  # speed of light

build_unit('dioptre', 1.0, 'm⁻¹')  # dioptre
build_unit('mayer', 1000.0, 'J⋅kg⁻¹⋅K⁻¹')  # mayer
build_unit('helmholtz', 3.336e-10, 'C⋅m⁻¹')  # helmholtz

build_unit('mired', 1000000.0, 'K⁻¹')  # mired

build_unit('cumec', 1.0, 'm³⋅s⁻¹')  # cumec (musec)
build_unit('gph_UK', 1.2627999999999998e-06, 'm³⋅s⁻¹')  # gallon (UK) per hour
build_unit('gpm_UK', 7.57682e-05, 'm³⋅s⁻¹')  # gallon (UK) per minute
build_unit('gps_UK', 0.004546090000000001, 'm³⋅s⁻¹')  # gallon (UK) per second
build_unit('lusec', 0.001, 'm³⋅s⁻¹')  # lusec
build_unit('CO', 0.000707921, 'm³⋅s⁻¹')  # miner's inch

build_unit('gph', 1.0, 'gal⋅h⁻¹')  # gallon (US, liq.) per hour
build_unit('gpm', 1.0, 'gal⋅min⁻¹')  # gallon (US, liq.) per minute
# gallon (US, liq.) per second
build_unit('gps', 0.0037854100000000003, 'gal⋅s⁻¹')

build_unit('G', 9.80665, 'm⋅s⁻²')  # g (gravitational acceleration)
build_unit('rps', 1.0, 'rev⋅s⁻¹')  # revolution per second

build_unit('den', 1.11111e-07, 'kg⋅m⁻¹')  # denier
build_unit('denier', 1.11111e-07, 'kg⋅m⁻¹')  # denier
build_unit('te', 1e-07, 'kg⋅m⁻¹')  # tex

# a.u. of linear momentum
build_unit('au_lm', 1.99285e-24, 'N⋅s')

build_unit('c_power', 12.5664, 'cd⋅sr')  # candlepower (spherical)

build_unit('asb', 0.31831, 'cd⋅m⁻²')  # apostilb
# build_unit('L', 31831.0, 'cd⋅m⁻²')  # lambert
build_unit('nit', 1.0, 'cd⋅m⁻²')  # nit
build_unit('sb', 10000.0, 'cd⋅m⁻²')  # stilb

build_unit('oe', 79.5775, 'A⋅m⁻¹')  # oersted
build_unit('praoersted', 11459.1, 'A⋅m⁻¹')  # praoersted

# a.u. of magnetic dipole moment
build_unit('au_mdm', 1.8548e-23, 'J⋅T⁻¹')
build_unit('Gal', 0.001, 'm⋅s⁻²')  # galileo
build_unit('leo', 10, 'm⋅s⁻²')  # leo
build_unit('gn', 9.80665, 'm⋅s⁻²')  # normal acceleration

build_unit('Ω_acoustic', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)
build_unit('Ω_SI', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)

build_unit('rayl_cgs', 10, 'kg⋅m⁻²⋅s⁻¹')  # rayl (cgs)
build_unit('rayl_MKSA', 1, 'kg⋅m⁻²⋅s⁻¹')  # rayl (MKSA)

build_unit('Na', 6.02214e+23, 'mol⁻¹')  # avogadro

# a.u. of action
build_unit('au_action', 1.05457e-34, 'J⋅s')
# a.u. of angular momentum
build_unit('au_am', 1.05457e-34, 'J⋅s')
build_unit('planck', 1, 'J⋅s')  # planck

build_unit('rpm', 1, 'rev⋅min⁻¹')  # revolution per minute

# a.u. of charge density
build_unit('au_cd', 1081200000000.0, 'C⋅m⁻³')

build_unit('Ah', 1.0, 'A⋅h⁻¹')  # ampere-hour

build_unit('F_12C', 96485.3, 'C⋅mol⁻¹')  # faraday (based on ¹²C)
build_unit('F_chemical', 96495.7, 'C⋅mol⁻¹')  # faraday (chemical)
build_unit('F_physical', 96512.9, 'C⋅mol⁻¹')  # faraday (physical)

build_unit('roc', 100, 'S⋅m⁻¹')  # reciprocal ohm per centimeter
build_unit('rom', 1.0, 'S⋅m⁻¹')  # reciprocal ohm per meter

# a.u. of electric quadrupole moment
build_unit('au_eqm', 4.48655e-40, 'C⋅m²')
# a.u. of electric dipole moment
build_unit('au_edm', 8.47836e-30, 'C⋅m')
# a.u. of electric field strength
build_unit('au_efs', 514221000000.0, 'V⋅m⁻¹')

build_unit('Jy', 1e-27, 'W⋅m⁻²⋅Hz')  # jansky

build_unit('MGOe', 7957.75, 'J⋅m⁻³')  # megagauss-oersted (MGOe)
build_unit('Ly', 41850.0, 'J⋅m⁻²')  # langley (energy)
build_unit('ly_langley', 697.5, 'W⋅m⁻²')  # langley (flux)

build_unit('ue', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy
build_unit('eu', 4.184, 'J⋅K⁻¹⋅mol')  # unit of entropy

build_unit('UI', 1.66667e-08, 'mol⋅s⁻¹')  # international unit
build_unit('IU', 1.66667e-08, 'mol⋅s⁻¹')  # international unit

build_unit('ph', 0.01, 'lm⋅m⁻²')  # phot

build_unit('cSt', 1e-07, 'm²⋅s⁻¹')  # centistokes
build_unit('St', 1e-05, 'm²⋅s⁻¹')  # stokes

build_unit('fps', 1.0, 'ft⋅s⁻¹')  # foot per second
build_unit('fpm', 1.0, 'ft⋅min⁻¹')  # foot per minute
build_unit('fph', 1.0, 'ft⋅h⁻¹')  # foot per hour

build_unit('ips', 1.0, 'in⋅s⁻¹')  # inch per second

build_unit('mph', 1.0, 'mi⋅h⁻¹')  # mile (stat.) per hour

build_unit('cfm', 1.0, 'ft³⋅min⁻¹')  # cubic foot per minute
build_unit('cfs', 1.0, 'ft³⋅s⁻¹')  # cubic foot per second


