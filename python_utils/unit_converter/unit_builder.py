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
from .constants import (
    PI,
    TANSEC,
    SPEED_OF_LIGHT,
    PLANCK_CONST,
    ELEMENTARY_CHARGE_CONST,
    BOLTZMANN_CONST,
    GRAVITY_CONST,
    DIRAC_CONST,
    NEWTONIAN_CONST_GRAVITATION,
    RYDBERG_CONST,
    ATOMIC_MASS_CONST,
    ELECTRON_MASS,
    ATMOSPHERE_CONST,
    ZETA_CONST,
    AVOGADRO_CONST,
    VACUUM_PERMITTIVITY,
    COULOMB_CONST,
    PROTON_MASS
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
    '\'': 'arcminute',
    '"': 'arcsecond',
    '°': 'degree',
    '%': 'percent',
    'H₂O': None,
    'O₂': None,
    'Nₚ': None,
    'aW-1': 'aW_1',
    'gemʊ': 'gemu',
    'aΩ': 'a_ohm',
    'SΩ': 'S_ohm',
    '°F⋅ft²⋅h⋅Btu_th⁻¹': None,
    '°F⋅ft²⋅h/Btu_th': None,
    'Ω_acoustic': 'ohm_acoustic',
    'Ω_SI': 'ohm_SI',
    'Ω': 'ohm',
    'Ω_it': 'ohm_it',
    'Ω_us': 'ohm_us',
    'Ω_mechanical': 'ohm_mechanical',
    'λ': 'lambda_',
    'γ': 'gamma',
    '°R': 'deg_R',
    '°C': 'deg_C',
    '°F': 'deg_F',
    'лс': 'Nc',
    'кс': 'Kc'
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

            unit = Unit(unit)

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

# derived base units
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
_build_derived_unit('°C', 'K')

# permittivity ε  (F·m⁻¹)
build_unit('apu', 1.11265005545e-10, 'F⋅m⁻¹')  # a.u. of permittivity

# angle
_build_base_unit('rad')  # radian (angle)
build_unit('rev', 2 * PI * units.rad, 'rad')  # revolution
build_unit('°', PI / 180 * units.rad, 'rad')  # degree
build_unit('\'', units.degree * (60 ** -1), 'rad')  # arc minute (minute of arc)
build_unit('"', units.arcminute * (60 ** -1), 'rad')  # arc second (second of arc)
build_unit('mas', 1e-3 * units.arcsecond * (60 ** -1), 'rad')  # milliarcsecond
build_unit('grad', PI / 200 * units.rad, 'rad')  # grade
build_unit('gon', 1.0 * units.grad, 'rad')  # gon
build_unit('mrad', PI / 32000 * units.rad, 'rad')  # milliradian
build_unit('pid', 6.28319, 'rad')  # circumference
build_unit('ah', 0.261799, 'rad')  # hour of arc
build_unit('%', 0.00999967, 'rad')  # percent
build_unit('sign', 0.523599, 'rad')  # sign

# solid angle
_build_base_unit('sr'),  # steradian
build_unit('sp', 12.5664, 'sr')  # spat

# data_speed
build_unit('baud', 1.0, 'bit⋅s⁻¹')  # circumference

# data size
build_unit('B', 8, 'bit')  # byte
build_unit('Kib', 2 ** 10, 'bit')  # kilobinarybit (kibibit)
build_unit('KiB', 8 * units.Kib, 'bit')  # kilobinarybyte (kibibyte)
build_unit('Kb', 10 ** 3, 'bit')  # kilobit
build_unit('KB', 8 * units.Kb, 'bit')  # kilobyte
build_unit('Mib', 2 ** 20, 'bit')  # megabinarybit (mebibit)
build_unit('MiB', 8 * units.Mib, 'bit')  # megabinarybyte (mebibyte)
build_unit('Mb', 10 ** 6, 'bit')  # megabit
build_unit('MB', 8 * units.Mb, 'bit')  # megabyte
build_unit('Gib', 2 ** 30, 'bit')  # gigabinarybit (gibibit)
build_unit('GiB', 8 * units.Gib, 'bit')  # gigabinarybyte (gibibyte)
build_unit('Gb', 10 ** 9, 'bit')  # gigabit
build_unit('GB', 8 * units.Gb, 'bit')  # gigabyte
build_unit('Tib', 2 ** 40, 'bit')  # terabinarybit (tebibit)
build_unit('TiB', 8 * units.Tib, 'bit')  # terabinarybyte (tebibyte)
build_unit('Tb', 10 ** 12, 'bit')  # terabit
build_unit('TB', 8 * units.Tb, 'bit')  # terabyte

# length
build_unit('Å', 1e-10, 'm')  # ångström
build_unit('µ', 0.000001, 'm')  # micron
build_unit('f', 9.999999999E-16, 'm')  # fermi
build_unit('ly', SPEED_OF_LIGHT, 'm')  # light years
build_unit('AU', 149597870700, 'm')  # astronomical unit
build_unit('UA', 149597870700, 'm')  # astronomical unit
build_unit('au', 149597870700, 'm')  # astronomical unit
build_unit('pc', 1 / TANSEC * units.au, 'm')  # parsecs
build_unit('NM', 1852, 'm')  # Nautical Miles
build_unit('alu', 5.29177210903e-11, 'm')  # a.u. of length
build_unit('a0', 1.0 * units.alu, 'm')  # Bohr
build_unit('rBohr', 1.0 * units.a0, 'm')  # first Bohr radius
build_unit('pl', (DIRAC_CONST * NEWTONIAN_CONST_GRAVITATION / SPEED_OF_LIGHT ** 3) ** 0.5, 'm')  # planck-length
build_unit('am', 1e-18, 'm')  # attometer
build_unit('ft_survey', 1200 / 3937, 'm')  # US Survey foot
build_unit('smi', 5280 * units.ft_survey, 'm')  # US statute mile, survey mile
build_unit('in', 0.02539999999997257, 'm')  # inch
build_unit('yd', 36 * units.inch, 'm')  # yard
build_unit('ft', 12 * units.inch, 'm')  # foot
build_unit('mi', 5280 * units.ft, 'm')  # mile
build_unit('arcmin', 0.000290888, 'm')  # arcmin
build_unit('agate', 0.00181428571429, 'm')  # agate
build_unit('aln', 0.593778, 'm')  # alens
build_unit('bcorn', 0.0084666666666667, 'm')  # barleycorn (UK)
build_unit('bolt', 36.576, 'm')  # bolt (US cloth)
build_unit('bl', 80.4672, 'm')  # blocks
build_unit('line_UK', 0.00211667, 'm')  # button (UK)
build_unit('line', 0.000635, 'm')  # button (US)
build_unit('caliber', 2.54e-4, 'm')  # caliber (centiinch)
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
build_unit('finer', 0.1143, 'm')  # finger-cloth
build_unit('fb', 0.022225, 'm')  # fingerbreadth
build_unit('fod', 0.3141, 'm')  # fod
build_unit('fbf', 91.44, 'm')  # football-field
build_unit('pleth', 30.8, 'm')  # greek-plethron
build_unit('std', 185.0, 'm')  # greek-stadion
build_unit('fath', 6 * units.ft_survey, 'm')  # fathom
build_unit('hand', 4 * units.inch, 'm')  # hands
build_unit('NL', 3 * units.smi, 'm')  # Nautical Leagues
build_unit('rd', 16.5 * units.ft_survey, 'm')  # rods
build_unit('perch', 1.0 * units.rd, 'm')  # perch
build_unit('pole', 1.0 * units.rd, 'm')  # poles
build_unit('fur', 40 * units.rd, 'm')  # furlong
build_unit('ch_gunter', 20.1168, 'm')  # chain (Gunter's)
build_unit('ch_engineer', 30.48, 'm')  # chain (engineer's)
build_unit('ch_ramsden', 30.48, 'm')  # chain (Ramsden's)
build_unit('ch_surveyor', 4 * units.rd, 'm')  # chain (surveyor's)
build_unit('cable_int', 185.2, 'm')  # cable length (int.)
build_unit('cable_UK', 185.318, 'm')  # cable length (UK)
build_unit('cable', 120 * units.fath, 'm')  # cable length (US)
build_unit('li', 1e-2 * units.ch_surveyor, 'm')  # links
build_unit('hiMetric', 1e-05, 'm')  # himetric
build_unit('hl', 2.4, 'm')  # horse-length
build_unit('hvat', 1.89648384, 'm')  # hvat
build_unit('LD', 384402000, 'm')  # lunar-distance
build_unit('mil', 2.54e-05, 'm')  # mils
build_unit('Mym', 10000, 'm')  # myriameters
build_unit('nail', 0.05715, 'm')  # nails-cloth
build_unit('pace', 0.762, 'm')  # paces
build_unit('palm', 0.0762, 'm')  # palms
build_unit('p', 0.00423333333, 'm')  # picas
build_unit('rem', 0.0042333328, 'm')  # rems
build_unit('PX', 0.0002645833, 'm')  # pixels
build_unit('ru', 0.04445, 'm')  # rack-unit
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


# mass
build_unit('g', 0.001, 'kg')  # gram
build_unit('me', 9.1093837015e-31, 'kg')  # electron rest mass (a.u. of mass)
build_unit('m₀', 1.0 * units.me, 'kg')  # electron rest mass (a.u. of mass)
build_unit('t', 1000.0, 'kg')  # metric ton
build_unit('amu', ATOMIC_MASS_CONST, 'kg')  # dalton (atomic unit of mass)
build_unit('u', ATOMIC_MASS_CONST, 'kg')  # atomic mass unit
build_unit('Da', ATOMIC_MASS_CONST, 'kg')  # dalton (atomic unit of mass)
build_unit('gr', 64.79891 * 0.001, 'kg')  # grain
build_unit('ct', 0.0002, 'kg')  # carat (metric)
build_unit('pm', (DIRAC_CONST * SPEED_OF_LIGHT / NEWTONIAN_CONST_GRAVITATION) ** 0.5, 'm')  # planck_mass
build_unit('dr_troy', 0.00388793, 'kg')  # dram (troy)
build_unit('dr_apoth', 0.00388793, 'kg')  # dram or drachm (apothecary)
build_unit('dr_avdp', 0.001771845195312458, 'kg')  # dram or drachm (avoirdupois)
build_unit('lb', 0.45359237001003544, 'kg')  # pound
build_unit('oz', 0.028349523124984257, 'kg')  # ounce
build_unit('t_long', 1016.0469088, 'kg')  # ton (long)
build_unit('t_short', 907.18474, 'kg')  # ton(short)
build_unit('dwt', 0.0015551738, 'kg')  # pennyweight
build_unit('kip', 453.59237, 'kg')  # kip
build_unit('slug', 14.5939029372, 'kg')  # geepound (slug)
build_unit('t_assay', 0.029167, 'kg')  # assay ton
build_unit('Da_12C', 1.66054e-27, 'kg')  # atomic unit of mass (¹²C)
build_unit('Da_16O', 1.66001e-27, 'kg')  # atomic unit of mass (¹⁶O)
build_unit('Da_1H', 1.67353e-27, 'kg')  # atomic unit of mass (¹H)
build_unit('avogram', 1.66036e-24, 'kg')  # avogram
build_unit('bag_UK', 42.6377, 'kg')  # bag (UK, cement)
build_unit('ct_troy', 0.000205197, 'kg')  # carat (troy)
build_unit('cH', 45.3592, 'kg')  # cental
build_unit('cwt', 100.0, 'kg')  # quintal

# time
build_unit('min', 60.0, 's')  # minute
build_unit('h', 60.0 * units.min, 's')  # hour
build_unit('d', 24 * units.h, 's')  # day
build_unit('week', 7 * units.d, 's')  # week
build_unit('fortnight', 2 * units.week, 's')  # fortnight
build_unit('yr', 365.25 * units.d, 's')  # year (calendar)
build_unit('a', 1.0 * units.yr, 's')  # year (calendar)
build_unit('eon', 1e9 * units.yr, 's')  # eon
build_unit('shake', 1e-8, 's')  # shake
build_unit('atu', DIRAC_CONST / (2 * PLANCK_CONST * SPEED_OF_LIGHT * RYDBERG_CONST), 's')  # a.u. of time
build_unit('mo', units.yr * (12 ** -1), 's')  # month (30 days)
build_unit('mo_sidereal', 2360590.0, 's')  # month (sidereal)
build_unit('mo_mean', 2628000.0, 's')  # month (solar mean)
build_unit('mo_synodic', 2551440.0, 's')  # month (synodic), lunar month
build_unit('d_sidereal', 86164.0, 's')  # day (sidereal)
build_unit('a_astr', 31557900.0, 's')  # year (astronomical), Bessel year
build_unit('a_sidereal', 31558200.0, 's')  # year (sidereal)
build_unit('a_mean', 31557600.0, 's')  # year (solar mean)
build_unit('a_tropical', 31556900.0, 's')  # year (tropical)
build_unit('planck_time', (DIRAC_CONST * NEWTONIAN_CONST_GRAVITATION / SPEED_OF_LIGHT ** 5) ** 0.5, 's')  # planck_time
build_unit('blink', 0.864, 's')  # blink
build_unit('wink', 3.33333e-10, 's')  # wink

# temperature
build_unit('°R', 1.0, 'K')
build_unit('°F', 1.0, 'K')
build_unit('atempu', (2 * PLANCK_CONST * SPEED_OF_LIGHT * RYDBERG_CONST) / BOLTZMANN_CONST, 'K')  # a.u. of temperature
build_unit('planck_temp', (DIRAC_CONST * SPEED_OF_LIGHT ** 5 / NEWTONIAN_CONST_GRAVITATION / BOLTZMANN_CONST ** 2) ** 0.5, 'K')  # planck_temp

# area
build_unit('are', 100, 'm²')  # are
build_unit('b', 1e-28, 'm²')  # barn
build_unit('D', 9.869232667160128e-13, 'm²')  # darcy
build_unit('ha', 100 * units.are, 'm²')  # hectare
build_unit('ac', 4046.8564224, 'm²')  # acre
build_unit('acre', 4046.8564224, 'm²')  # acre
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

# volume
build_unit('l', 0.001, 'm³')  # Liter
build_unit('L', 0.001, 'm³')  # Liter
build_unit('cc', 1.0e-6, 'm³')  # cubic centimeter (Mohr cubic centimeter)
build_unit('λ', 1.0e-3 * 1e-6, 'm³')  # lambda
build_unit('st', 1.0, 'm³')  # stere
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

# frequency
build_unit('rpm', 1.0, 'rev⋅min⁻¹')  # revolution per minute
build_unit('rps', 1.0, 'rev⋅s⁻¹')  # revolution per second
build_unit('cps', 1.0, 'Hz')  # cycles per second

# velocity
build_unit('avu', 2.18769126364e6, 'm⋅s⁻¹')  # a.u. of velocity
build_unit('kn', 0.514444, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
build_unit('knot', 1.0 * units.kn, 'm⋅s⁻¹')  # mile (naut.) per hour (knot, noeud)
build_unit('mph', 1.0, 'mi⋅h⁻¹')  # mile (stat.) per hour
build_unit('kph', 1.0, 'km⋅h⁻¹')  # mile (stat.) per hour
build_unit('kps', 1.0, 'km⋅s⁻¹')  # mile (stat.) per hour
build_unit('mps', 1.0, 'm⋅s⁻¹')  # mile (stat.) per hour
build_unit('fps', 1.0, 'ft⋅s⁻¹')  # foot per second
build_unit('fpm', 1.0, 'ft⋅min⁻¹')  # foot per minute
build_unit('fph', 1.0, 'ft⋅h⁻¹')  # foot per hour
build_unit('ips', 1.0, 'in⋅s⁻¹')  # inch per second
build_unit('Bz', 1.0, 'm⋅s⁻¹')  # benz
build_unit('mpy', 8.04327e-13, 'm⋅s⁻¹')  # mil per year
build_unit('c_light', 299792000.0, 'm⋅s⁻¹')  # speed of light

# acceleration
build_unit('Gal', 0.001, 'm⋅s⁻²')  # galileo
build_unit('G', 9.80665, 'm⋅s⁻²')  # g (gravitational acceleration)
build_unit('leo', 10, 'm⋅s⁻²')  # leo
build_unit('gn', 9.80665, 'm⋅s⁻²')  # normal acceleration

# force
build_unit('dyn', 1e-05, 'N')  # dyne
build_unit('kgf', GRAVITY_CONST * units.kg, 'N')  # kilogram force
build_unit('kgp', 1.0 * units.kgf, 'N')  # kilogram force
build_unit('gf', GRAVITY_CONST * units.g, 'N')  # gram force
build_unit('tf_metric', GRAVITY_CONST * units.t, 'N')  # ton force (metric)
build_unit('afu', (2 * PLANCK_CONST * SPEED_OF_LIGHT * RYDBERG_CONST) * units.a0(exponent=-1), 'N')  # a.u. of force
build_unit('crinal', 0.1, 'N')  # crinal
build_unit('grf', 0.6355, 'N')  # grain force
build_unit('kp', 9.80665, 'N')  # kilopond
build_unit('kipf', 4448.22, 'N')  # kilopound force (kip force)
build_unit('lbf', 4.4482216, 'N')  # Poundal force (US) (pound force)
build_unit('pdl', 0.138255, 'N')  # Poundal force (UK)
build_unit('slugf', 143.117, 'N')  # slug force
build_unit('tf_long', 9964.02, 'N')  # ton force (long)
build_unit('tf_short', 8896.44, 'N')  # ton force (short)
build_unit('ozf', 0.278014, 'N')  # ounce force

# energy
build_unit('erg', 1e-07, 'J')  # erg
build_unit('Wh', 1.0 * units.h, 'J')  # watt-hour
build_unit('eV', ELEMENTARY_CHARGE_CONST * units.V, 'J')  # electronvolt
build_unit('Ry', PLANCK_CONST * SPEED_OF_LIGHT * RYDBERG_CONST, 'J')  # rydberg
build_unit('Eh', 2 * units.Ry, 'J')  # hartree
build_unit('aeu', 4.3597447222071 * (10 ** -18), 'J')  # a. u. of energy
build_unit('cal_th', 4.184, 'J')  # calorie (thermochemical)
build_unit('cal_it', 4.18674, 'J')  # calorie (IT) (International Steam Table)
build_unit('cal_15', 4.1855, 'J')  # calorie (15°C)
build_unit('Btu_iso', 1055.056, 'J')  # British thermal unit (ISO)
build_unit('Btu_it', 1055.0558526, 'J')  # British thermal unit (IT)
build_unit('Btu_th', 1054.3499999744, 'J')  # British thermal unit (thermochemical)
build_unit('quad', 1e15 * units.Btu_iso, 'J')  # quadrillion_Btu
build_unit('thm', 1e5 * units.Btu_iso, 'J')  # therm
build_unit('thm_us', 1.054804e8, 'J')  # US therm
build_unit('tTNT', 1e9 * units.cal_th, 'J')  # ton TNT
build_unit('toe', 1e10 * units.cal_it, 'J')  # tonne of oil equivalent
build_unit('atm_l', ATMOSPHERE_CONST * units.l, 'J')  # atmosphere liter
build_unit('bboe', 6120000000.0, 'J')  # barrel oil equivalent
build_unit('BeV', 1.60218e-10, 'J')  # BeV (billion eV)
build_unit('Btu_mean', 1055.87, 'J')  # British thermal unit (mean)
build_unit('cal_4', 4.2045, 'J')  # calorie (4°C)
build_unit('Cal', 4180.0, 'J')  # Calorie (diet kilocalorie)
build_unit('kcal', 4180.0, 'J')  # Calorie (diet kilocalorie)
build_unit('cal_mean', 4.19002, 'J')  # calorie (mean)
build_unit('Chu', 1899.18, 'J')  # Celsius-heat unit

# power
build_unit('VA', 1.0 * units.V, 'W')  # volt ampere
build_unit('hp', 745.6998715823, 'W')  # horsepower (550 ft-lbf/s)
build_unit('bhp', 9809.5, 'W')  # horsepower (boiler)
build_unit('mhp', 735.49875, 'W')  # horsepower (metric)
build_unit('ehp', 746.0, 'W')  # horsepower (electric)
build_unit('slpm', ATMOSPHERE_CONST * units.l * units.min(exponent=2), 'W')  # standard liter per minute
build_unit('slm', 1.0 * units.slpm, 'W')  # standard liter per minute
build_unit('aW', 1e-07, 'W')  # abwatt (emu of power)
build_unit('whp', 746.043, 'W')  # horsepower (water)
build_unit('dbhp', 746.043, 'W')  # horsepower (Drawbar)
build_unit('hp_gb', 745.7, 'W')  # horsepower (British)
build_unit('cv', 1.0 * units.mhp, 'W')  # horsepower Italian (cavallo vapore), Spanish (caballo de vapor),Portuguese (cavalo-vapor)
build_unit('pk', 1.0 * units.mhp, 'W')  # horsepower (paardenkracht)
build_unit('ch', 1.0 * units.mhp, 'W')  # horsepower (cheval-vapeur)
build_unit('hk', 1.0 * units.mhp, 'W')  # horsepower Norwegian (hästkraft), Danish (hästkraft), Swedish (hästkraft)
build_unit('PS', 1.0 * units.mhp, 'W')  # horsepower  German (Pferdestärke)
build_unit('KM', 1.0 * units.mhp, 'W')  # horsepower Polish (koń mechaniczny), Slovenian (konjska moč)
build_unit('ks', 1.0 * units.mhp, 'W')  # horsepower Czech (koňská síla), Slovak (konská sila)
build_unit('hv', 1.0 * units.mhp, 'W')  # horsepower Finnish (hevosvoima)
build_unit('hj', 1.0 * units.mhp, 'W')  # horsepower Estonian (hobujõud)
build_unit('LE', 1.0 * units.mhp, 'W')  # horsepower Hungarian (lóerő)
build_unit('KS', 1.0 * units.mhp, 'W')  # horsepower Bosnian/Croatian/Serbian (konjska snaga)
build_unit('KC', 1.0 * units.mhp, 'W')  # horsepower Macedonian (коњска сила)
build_unit('лс', 1.0 * units.mhp, 'W')  # horsepower  Russian (лошадиная сила)
build_unit('кс', 1.0 * units.mhp, 'W')  # horsepower  Ukrainian (кінська сила)
build_unit('CP', 1.0 * units.mhp, 'W')  # horsepower  Romanian (calputere)
build_unit('prony', 98.0665, 'W')  # prony

# momentum

# density
build_unit('Hg', 13.5951 * units.kg * units.l(exponent=-1), 'Pa')  # Hg (mercury) (0°C)
build_unit('H2O', 1.0 * units.kg * units.l(exponent=-1), 'Pa')  # H₂O (water) (0°C)
build_unit('H₂O', 1.0 * units.H2O, 'Pa')  # H₂O (water) (0°C)
build_unit('Aq', 1.0 * units.H2O, 'Pa')  # H₂O (water) (0°C)
build_unit('O2', 12.677457000000462, 'Pa')  # O₂ (air) (0°C)
build_unit('O₂', 1.0 * units.O2, 'Pa')  # O₂ (air) (0°C)

# pressure
build_unit('apressu', 2.9421015697e13, 'Pa')  # a.u. for pressure
build_unit('Ba', 0.1, 'Pa')  # Bayre
build_unit('bar', 1e5 * units.Pa, 'Pa')  # bar
build_unit('at', 1.0 * GRAVITY_CONST * units.cm(exponent=-2), 'Pa')  # atmosphere (technical)
build_unit('torr', ATMOSPHERE_CONST / 760, 'Pa')  # Torr
build_unit('psi', 6894.7572932, 'Pa⋅m')  # pound force per square inch
build_unit('ksi', 6894757.293200044, 'Pa')  # kilopound force per square inch
build_unit('SPL', 20e-6 * units.Pa, 'Pa')  # sound pressure level
build_unit('atm', ATMOSPHERE_CONST, 'Pa')  # atmosphere (standard)
build_unit('pp', 4.63309e+113, 'Pa')  # Planck pressure
build_unit('cgs', 0.1, 'Pa')  # centimeter-gram-second
build_unit('pz', 1000.0, 'Pa')  # pieze
build_unit('psf', 47.88025897999996, 'Pa')  # pound force per square foot
build_unit('osi', 430.9223300000048, 'Pa')  # ounce force per square inch

# torque  N⋅m

# viscosity
build_unit('P', 0.1, 'Pa⋅s')  # Poise
build_unit('reyn', 6894.76, 'Pa⋅s')  # reynolds (reyns)
build_unit('Pl', 1.0, 'Pa⋅s')  # poiseuille

# kinematic viscosity
build_unit('St', 1e-05, 'm²⋅s⁻¹')  # stokes

# fluidity
build_unit('rhe', 1 * units.P(exponent=-1), 'Pa⋅s')  # rhe

# amount of substance
build_unit('particle', 1 / AVOGADRO_CONST, 'mol')  # molecule
build_unit('entities', 1.66054e-24, 'mol')  # entities
build_unit('SCF', 1.19531, 'mol')  # standard cubic foot
build_unit('SCM', 44.6159, 'mol')  # standard cubic meter

# concentration
build_unit('M', 1000, 'mol⋅m⁻³')  # molar

# catalytic activity

# entropy S  (J⋅K⁻¹)
build_unit('Cl', 4.184, 'J⋅K⁻¹')  # clausius

# molar entropy
build_unit('eu', 4.184, 'J⋅K⁻¹⋅mol⁻¹')  # entropy unit

# radiation
build_unit('rads', 0.01, 'Gy')  # radian (radioactive)
build_unit('Ci', 3.7e10, 'Bq')  # curie
build_unit('Rd', 1e6, 'Bq')  # rutherford
build_unit('roentgen', 2.58e-4, 'C⋅kg⁻¹')  # röntgen
build_unit('kerma', 1.0, 'Gy')  # kerma
build_unit('Mrd', 10000.0, 'Gy')  # megarad

# heat transimission
build_unit('PSH', 1e3 * units.Wh, 'J⋅m⁻²')  # peak sun hour
build_unit('Ly', 41840.0, 'J⋅m⁻²')  # langley

# radiant exitance Mc  (W⋅cm⁻²)
# luminous exitance Mv  (lm⋅cm⁻²)
# radiance Lc  (W⋅cm⁻²⋅sr⁻¹)
# luminance Lv  (lm⋅cm⁻²⋅sr⁻¹)
build_unit('nit', 1.0, 'cd⋅m⁻²')  # nit
build_unit('sb', 10000.0, 'cd⋅m⁻²')  # stilb
build_unit('lambert', 31831.0, 'cd⋅m⁻²')  # lambert
build_unit('asb', 0.31831, 'cd⋅m⁻²')  # apostilb

# luminous flux Φv  (lm)
build_unit('bd', 1.02, 'cd')  # bougie d&egrave;cimale
build_unit('bi', 1.0, 'cd')  # bougie international
build_unit('c_int', 1.01937, 'cd')  # candle (int.)
build_unit('c', 1.0, 'cd')  # candle (new unit)
build_unit('carcel', 10.0, 'cd')  # carcel
build_unit('HK', 0.903, 'cd')  # hefner unit (hefnerkerze)
build_unit('c_power', 12.56637, 'cd⋅sr')  # candlepower (spherical)

# radiant flux Φe  (W)

# illuminance Ev (lux)
build_unit('ph', 10000, 'lx')  # phot
build_unit('fc', 10.763910417, 'lx')  # foot-candle

# radiant intensity Ic (W⋅sr⁻¹)

# luminous intensity Iv (cd)
build_unit('violle', 20.4, 'cd')  # violle

# intensity (W⋅m⁻²)
build_unit('aiu', 0.5 * VACUUM_PERMITTIVITY * SPEED_OF_LIGHT * (ELEMENTARY_CHARGE_CONST * COULOMB_CONST * units.a0(exponent=-2)) ** 2, 'W⋅m⁻²')  # a. . intensity

# electric current I  (A)
build_unit('Bi', 10, 'A')  # biot
build_unit('abA', 1.0 * units.Bi, 'A')  # abampere
build_unit('aecu', ELEMENTARY_CHARGE_CONST * units.atu(exponent=-1), 'A')  # a.u. of electric current
build_unit('A_it', 1.00034 / 1.00049, 'A')  # mean international ampere
build_unit('A_us', 1.00033 / 1.000495, 'A')  # US international ampere
build_unit('planck_current', (SPEED_OF_LIGHT ** 6 / GRAVITY_CONST / COULOMB_CONST) ** 0.5, 'A')  # planck_current

build_unit('edison', 100.0, 'A')  # edison
build_unit('statA', 3.35564e-10, 'A')  # statampere
build_unit('gilbert', 0.79577, 'A')  # gilbert
build_unit('pragilbert', 11459.1, 'A')  # pragilbert

# electric charge q  (C)
build_unit('acu', 1.602176634e-19, 'C')  # a.u. of charge
build_unit('aC', 10, 'C')  # abcoulomb (emu of charge)
build_unit('abC', 1.0 * units.aC, 'C')  # abcoulomb (emu of charge)
build_unit('faraday', ELEMENTARY_CHARGE_CONST * AVOGADRO_CONST, 'mol')  # faraday
build_unit('esc', 1.6022e-19, 'C')  # electronic charge
build_unit('esu', 3.336e-06, 'C')  # electrostatic unit
build_unit('Fr', 3.33564e-10, 'C')  # franklin
build_unit('statC', 3.35564e-10, 'C')  # statcoulomb
build_unit('Ah', 3600, 'C')  # ampere-hour

# electric potential V  (V)  *
build_unit('aepu', 27.211386245988, 'V')  # a.u. of electric potential
build_unit('aV', 1e-8, 'V')  # abvolt (emu of electric potential)
build_unit('abV', 1.0 * units.aV, 'V')  # abvolt (emu of electric potential)
build_unit('V_it', 1.00034, 'V')  # volt (mean)
build_unit('V_us', 1.00033, 'V')  # volt (US)
build_unit('statV', 299.792, 'V')  # statvolt

# electric field E  (V⋅m⁻¹)  *
build_unit('aefu', 5.14220674763e11, 'V⋅m⁻¹')  # a.u. of electric field strength

# electric field gradient EFG  (V⋅m⁻²)
build_unit('aefgu', 9.7173624292e21, 'V⋅m⁻²')  # a.u. of electric field gradient

# electric displacement field D  (C⋅m⁻²)

# resistance Ω  (Ω)
build_unit('aΩ', 1e-9, 'Ω')  # abohm (emu of resistance)
build_unit('Ω_it', 1.00049, 'Ω')  # mean international ohm
build_unit('Ω_us', 1.000495, 'Ω')  # US international ohm
build_unit('SΩ', 0.96, 'Ω')  # siemens (resistance)
build_unit('statohm', 898755000000.0, 'Ω')  # statohm

# electrical resistivity and conductivity  Ω⋅m
build_unit('Ω_mechanical', 1.0, 'Pa⋅s⋅m⁻³')  # ohm (mechanical, SI)
build_unit('Ω_acoustic', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)
build_unit('Ω_SI', 1, 'Pa⋅s⋅m⁻³')  # ohm (acoustic, SI)

# conductance
build_unit('abS', 1e9, 'S')  # abmho (emu of conductance)
build_unit('aW-1', 1.0 * units.abS, 'S')  # abmho (emu of conductance)
build_unit('gemʊ', 1e-07, 'S')  # gemmho
build_unit('mho', 1.0, 'S')  # mho
build_unit('statmho', 1.11265e-12, 'S')  # statmho

# capacitance
build_unit('abF', 1e9, 'F')  # abfarad (emu of electric capacitance)
build_unit('jar', 1.11111e-09, 'F')  # jar
build_unit('statF', 1.11265e-12, 'F')  # statfarad

# inductance
build_unit('abH', 1e-9, 'H')  # abhenry (emu of inductance)
build_unit('statH', 898755000000.0, 'H')  # stathenry

# magnetic flux Φ  (Wb)
build_unit('Mx', 1e-9, 'Wb')  # maxwell

# magnetic flux density B  (T)
build_unit('γ', 1e-9, 'T')  # gamma
build_unit('amfu', 2.35051756758 * (10 ** 5), 'T')  # a.u. of magnetic field
build_unit('Gs', 1e-05, 'T')  # gauss

# magnetic field strength H  (A⋅m⁻¹)
build_unit('oe', 79.5775, 'A⋅m⁻¹')  # oersted
build_unit('praoersted', 11459.1, 'A⋅m⁻¹')  # praoersted

# magnetomotive force mmf  (A)
build_unit('At', 1.0, 'A')  # ampere_turn
build_unit('biot_turn', 1.0 * units.Bi, 'A')  # biot_turn
build_unit('gilbert ', 1 / (4 * PI) * units.biot_turn, 'A')  # gilbert

# electric dipole moment p  (C⋅m)
build_unit('debye', 1e-9 / ZETA_CONST * 1e-10, 'C⋅m')  # debye

build_unit('aedmu', 8.4783536255e-30, 'C⋅m')  # a.u. of electric dipole moment

# electric quadrupole moment Q  (C⋅m²)
build_unit('buckingham', 1e-9 / ZETA_CONST * (1e-10 ** 2), 'C⋅m²')  # buckingham
build_unit('aeqmu', 4.4865515246e-40, 'C⋅m²')  # a.u. of electric quadrupole moment

# magnetic moment µ (J⋅T⁻¹)
build_unit('bohr_magneton', ELEMENTARY_CHARGE_CONST * DIRAC_CONST / (2 * ELECTRON_MASS), 'J⋅T⁻¹')  # bohr_magneton
build_unit('nuclear_magneton', ELEMENTARY_CHARGE_CONST * DIRAC_CONST / (2 * PROTON_MASS), 'J⋅T⁻¹')  # nuclear_magneton
build_unit('amdmu', 1.85480201566e-23, 'J⋅T⁻¹')  # a.u. of magnetic dipole moment

# volume charge density ρ  (C⋅m⁻³)
build_unit('acdu', 1.08120238457 * (10 ** 12), 'C⋅m⁻³')  # a.u. of charge density

# surface charge density σ  (C⋅m⁻²)

build_unit('B_power', 10.0, 'dB')  # bel (power)
build_unit('B_voltage', 5.0, 'dB')  # bel (voltage)
build_unit('dB_power', 1.0, 'dB')  # decibel (power)
build_unit('dB_voltage', 0.5, 'dB')  # decibel (voltage)
build_unit('Nₚ', 4.34294, 'dB')  # neper


# build_unit('Kt', 0.0416667, '')  # carat (karat)
# build_unit('ppb', 1e-10, '')  # part per billion
# build_unit('pph', 0.001, '')  # part per hundred
# build_unit('pphm', 1e-09, '')  # part per hundred million
# build_unit('ppht', 1e-06, '')  # part per hundred thousand
# build_unit('ppm', 1e-07, '')  # part per million
# build_unit('ppq', 1e-15, '')  # part per quadrillion
# build_unit('ppt_tera', 1e-13, '')  # part per tera
# build_unit('ppt', 0.001, '')  # part per thousand

build_unit('gy', 1000, 'kg⋅m⁻³')  # specific gravity

build_unit('perm_0C', 5.72135e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (0°C)
build_unit('perm_23C', 5.74525e-11, 'kg⋅N⁻¹⋅s⁻¹')  # perm (23°C)
build_unit('permin_0C', 1.45322e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (0°C)
build_unit('permin_23C', 1.45929e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-inch (23°C)
build_unit('permmil_0C', 1.45322e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (0°C)
build_unit('permmil_23C', 1.45929e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')  # perm-mil (23°C)

build_unit('brewster', 1e-12, 'm²⋅N⁻¹')  # brewster

# build_unit('clo', 0.15482, 'K⋅m²⋅W⁻¹')  # clo
build_unit('°F⋅ft²⋅h⋅Btu_th⁻¹', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
build_unit('°F⋅ft²⋅h/Btu_th', 0.176228, 'K⋅m²⋅W⁻¹')  # R-value (imperial)
build_unit('RSI', 1.0, 'K⋅m²⋅W⁻¹')  # RSI (metric R-value)
build_unit('tog', 0.1, 'K⋅m²⋅W⁻¹')  # tog


build_unit('dioptre', 1.0, 'm⁻¹')  # dioptre
build_unit('mayer', 1000.0, 'J⋅kg⁻¹⋅K⁻¹')  # mayer


build_unit('mired', 1000000.0, 'K⁻¹')  # mired

# linear density  (kg⋅m⁻¹)
build_unit('den', 1.11111e-07, 'kg⋅m⁻¹')  # denier
build_unit('denier', 1.11111e-07, 'kg⋅m⁻¹')  # denier
build_unit('te', 1e-07, 'kg⋅m⁻¹')  # tex

# linear charge density λ  (C⋅m⁻¹)
build_unit('helmholtz', 3.336e-10, 'C⋅m⁻¹')  # helmholtz

# linear momentum (kg⋅m⋅s⁻¹)
build_unit('almu', 1.99285191410e-24, 'kg⋅m⋅s⁻¹')  # a.u. of linear momentum


# volumetric flow rate Q  (m³⋅s⁻¹)
build_unit('cumec', 1.0, 'm³⋅s⁻¹')  # cumec (musec)
build_unit('lusec', 0.001, 'm³⋅s⁻¹')  # lusec
build_unit('CO', 0.000707921, 'm³⋅s⁻¹')  # miner's inch
build_unit('gph_gb', 1.2627999999999998e-06, 'm³⋅s⁻¹')  # gallon (UK) per hour
build_unit('gpm_gb', 7.57682e-05, 'm³⋅s⁻¹')  # gallon (UK) per minute
build_unit('gps_gb', 0.004546090000000001, 'm³⋅s⁻¹')  # gallon (UK) per second
build_unit('gph', 1.0, 'gal⋅h⁻¹')  # gallon (US, liq.) per hour
build_unit('gpm', 1.0, 'gal⋅min⁻¹')  # gallon (US, liq.) per minute
build_unit('gps', 0.0037854100000000003, 'gal⋅s⁻¹')  # gallon (US, liq.) per second
build_unit('cfm', 1.0, 'ft³⋅min⁻¹')  # cubic foot per minute
build_unit('cfs', 1.0, 'ft³⋅s⁻¹')  # cubic foot per second

# angular momentum L  (kg⋅m²⋅s⁻¹)
build_unit('aamu', 1.054571817e-34, 'kg⋅m²⋅s⁻¹')  # a.u. of angular momentum
build_unit('aau', 1.0 * units.aamu, 'kg⋅m²⋅s⁻¹')  # a.u. of action

# acoustic impedeance Z  (rayl)
build_unit('rayl_cgs', 10, 'kg⋅m⁻²⋅s⁻¹')  # rayl (cgs)
build_unit('rayl', 1, 'kg⋅m⁻²⋅s⁻¹')  # rayl

build_unit('F_12C', 96485.3, 'C⋅mol⁻¹')  # faraday (based on ¹²C)
build_unit('F_chemical', 96495.7, 'C⋅mol⁻¹')  # faraday (chemical)
build_unit('F_physical', 96512.9, 'C⋅mol⁻¹')  # faraday (physical)

build_unit('roc', 100, 'S⋅m⁻¹')  # reciprocal ohm per centimeter
build_unit('rom', 1.0, 'S⋅m⁻¹')  # reciprocal ohm per meter

build_unit('Jy', 1e-27, 'W⋅m⁻²⋅Hz')  # jansky

build_unit('MGOe', 7957.75, 'J⋅m⁻³')  # megagauss-oersted (MGOe)
build_unit('ly_langley', 697.5, 'W⋅m⁻²')  # langley (flux)

build_unit('UI', 1.66667e-08, 'mol⋅s⁻¹')  # international unit
build_unit('IU', 1.66667e-08, 'mol⋅s⁻¹')  # international unit

build_unit('lbm', 0.45359237001003544, 'kg⋅m²')  # pound mass
