from .units import units, UnitsModule

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
    c,
    h,
    e,
    k,
    g_n,
    h_bar,
    G,
    R_inf,
    m_u,
    m_e,
    atm,
    N_A,
    k_e,
    m_p,
    alpha,
    au_permittivity,
    au_length,
    au_mass,
    au_time,
    au_temperature,
    au_velocity,
    au_force,
    au_pressure,
    au_electric_field,
    au_intensity,
    au_current,
    au_charge,
    au_electric_potential,
    au_electric_field_gradient,
    au_magnetic_flux_density,
    au_electric_dipole_moment,
    au_electric_quadrupole_moment,
    au_magnetic_dipole_moment,
    au_charge_density,
    au_linear_momentum,
    au_angular_momentum,
    au_action,
    au_energy
)

from decimal import Decimal

_UNIT_TO_ATTRIBUTE = {
    'cd-ft': 'cd_ft',
    'float': 'float_',
    'int': 'int_',
    'Å': 'angstrom',
    'in': 'inch',
    'µ': 'micron',
    'µµ': 'bicrons',
    'sq¼mi_stat': 'quarter_sq_mi_stat',
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
            setattr(UnitsModule, attr_name, BASE_UNITS[symbol])

    else:
        setattr(UnitsModule, symbol, BASE_UNITS[symbol])


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
            setattr(UnitsModule, attr_name, NAMED_DERIVED_UNITS[symbol])

    else:
        setattr(UnitsModule, symbol, NAMED_DERIVED_UNITS[symbol])


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
            setattr(UnitsModule, attr_name, UNITS[symbol])

    else:
        setattr(UnitsModule, symbol, UNITS[symbol])


# mole
_build_base_unit('mol')

# candela
_build_base_unit('cd')

# kilogram
_build_base_unit('kg')

# meter
_build_base_unit('m')

# second
_build_base_unit('s')

# ampere
_build_base_unit('A')

# kelvin
_build_base_unit('K')

# these next 4 aren't really base units but they have a factor of 1.0
# bit
_build_base_unit('bit')

# decible
_build_base_unit('dB')

# radian (angle)
_build_base_unit('rad')

# steradian
_build_base_unit('sr')


# derived base units
# hertz
_build_derived_unit('Hz', 's⁻¹')

# newton
_build_derived_unit('N', 'kg⋅m⋅s⁻²')

# pascal
_build_derived_unit('Pa', 'kg⋅m⁻¹⋅s⁻²')

# joule
_build_derived_unit('J', 'kg⋅m²⋅s⁻²')

# watt
_build_derived_unit('W', 'kg⋅m²⋅s⁻³')

# coulomb
_build_derived_unit('C', 's⋅A')

# volt
_build_derived_unit('V', 'kg⋅m²⋅s⁻³⋅A⁻¹')

# farad
_build_derived_unit('F', 'kg⁻¹⋅m⁻²⋅s⁴⋅A²')

# ohm
_build_derived_unit('Ω', 'kg⋅m²⋅s⁻³⋅A⁻²')

# siemens
_build_derived_unit('S', 'kg⁻¹⋅m⁻²⋅s³⋅A²')

# weber
_build_derived_unit('Wb', 'kg⋅m²⋅s⁻²⋅A⁻¹')

# tesla
_build_derived_unit('T', 'kg⋅s⁻²⋅A⁻¹')

# henry
_build_derived_unit('H', 'kg⋅m²⋅s⁻²⋅A⁻²')

# lumen
_build_derived_unit('lm', 'cd')

# lux
_build_derived_unit('lx', 'cd⋅m⁻²')

# becquerel
_build_derived_unit('Bq', 's⁻¹')

# gray
_build_derived_unit('Gy', 'm²⋅s⁻²')

# sievert
_build_derived_unit('Sv', 'm²⋅s⁻²')

# katal
_build_derived_unit('kat', 's⁻¹⋅mol')

_build_derived_unit('°C', 'K')

# permittivity ε  (F·m⁻¹)
# a.u. of permittivity
build_unit('apu', au_permittivity, 'F⋅m⁻¹')


# angle
# revolution
build_unit('rev', Decimal('2') * PI * units.rad, 'rad')

# degree
build_unit('°', PI / Decimal('180') * units.rad, 'rad')

# arc minute (minute of arc)
build_unit('\'', (Decimal('60') ** Decimal('-1')) * units.degree, 'rad')

# arc second (second of arc)
build_unit('"', (Decimal('60') ** Decimal('-1')) * units.arcminute, 'rad')

# milliarcsecond
build_unit(
    'mas',
    Decimal('1e-3') * (Decimal('60') ** Decimal('-1')) * units.arcsecond,
    'rad'
)

# grade
build_unit('grad', PI / Decimal('200') * units.rad, 'rad')

# gon
build_unit('gon', 1.0 * units.grad, 'rad')

# milliradian
build_unit('mrad', PI / Decimal('32000') * units.rad, 'rad')

# circumference
build_unit('pid', 6.28319, 'rad')

# hour of arc
build_unit('ah', 0.261799, 'rad')

# percent
build_unit('%', 0.00999967, 'rad')

# sign
build_unit('sign', 0.523599, 'rad')


# solid angle
# spat
build_unit('sp', 12.5664, 'sr')

# data type sizes
build_unit('char', 8.0, 'bit')
build_unit('uchar', 8.0, 'bit')
build_unit('short', 16.0, 'bit')
build_unit('ushort', 16.0, 'bit')
build_unit('int', 32.0, 'bit')
build_unit('uint', 32.0, 'bit')
build_unit('long', 32.0, 'bit')
build_unit('longlong', 64.0, 'bit')
build_unit('ulong', 64.0, 'bit')
build_unit('ulonglong', 64.0, 'bit')
build_unit('word', 16.0, 'bit')
build_unit('dword', 32.0, 'bit')
build_unit('double', 64.0, 'bit')
build_unit('float', 32.0, 'bit')
build_unit('int8_t', 8.0, 'bit')
build_unit('int16_t', 16.0, 'bit')
build_unit('int32_t', 32.0, 'bit')
build_unit('int64_t', 64.0, 'bit')
build_unit('uint8_t', 8.0, 'bit')
build_unit('uint16_t', 16.0, 'bit')
build_unit('uint32_t', 32.0, 'bit')
build_unit('uint64_t', 64.0, 'bit')
build_unit('longdouble', 128.0, 'bit')


# data_speed
# circumference
build_unit('baud', 1.0, 'bit⋅s⁻¹')


# data size
# byte
build_unit('B', 8, 'bit')

# kilobinarybit (kibibit)
build_unit('Kib', 2 ** 10, 'bit')

# kilobinarybyte (kibibyte)
build_unit('KiB', 8 * units.Kib, 'bit')

# kilobit
build_unit('Kb', 10e3, 'bit')

# kilobyte
build_unit('KB', 1.0 * units.KiB, 'bit')

# megabinarybit (mebibit)
build_unit('Mib', 2 ** 20, 'bit')

# megabinarybyte (mebibyte)
build_unit('MiB', 8 * units.Mib, 'bit')

# megabit
build_unit('Mb', 10e6, 'bit')

# megabyte
build_unit('MB', 1.0 * units.MiB, 'bit')

# gigabinarybit (gibibit)
build_unit('Gib', 2 ** 30, 'bit')

# gigabinarybyte (gibibyte)
build_unit('GiB', 8 * units.Gib, 'bit')

# gigabit
build_unit('Gb', 10e9, 'bit')

# gigabyte
build_unit('GB', 1.0 * units.GiB, 'bit')

# terabinarybit (tebibit)
build_unit('Tib', 2 ** 40, 'bit')

# terabinarybyte (tebibyte)
build_unit('TiB', 8 * units.Tib, 'bit')

# terabit
build_unit('Tb', 10e12, 'bit')

# terabyte
build_unit('TB', 1.0 * units.TiB, 'bit')


# length
# ångström
build_unit('Å', 1e-10, 'm')

# micron
build_unit('µ', 0.000001, 'm')

# fermi
build_unit('f', 9.999999999E-16, 'm')

# light years
build_unit('ly', c, 'm')

# astronomical unit
build_unit('AU', 149597870700, 'm')

# astronomical unit
build_unit('UA', 149597870700, 'm')

# astronomical unit
build_unit('au', 149597870700, 'm')

# parsecs
build_unit('pc', Decimal('1') / TANSEC * units.au, 'm')

# Nautical Miles
build_unit('NM', 1852, 'm')

# a.u. of length
build_unit('alu', au_length, 'm')

# Bohr
build_unit('a0', h_bar / (alpha * m_e * c), 'm')

# first Bohr radius
build_unit('rBohr', 1.0 * units.a0, 'm')

# planck-length
build_unit('pl', (h_bar * G / c ** Decimal('3')) ** Decimal('0.5'), 'm')

# attometer
build_unit('am', 1e-18, 'm')

# US Survey foot
build_unit('ft_survey', 1200 / 3937, 'm')

# US statute mile, survey mile
build_unit('smi', 5280 * units.ft_survey, 'm')

# yard
build_unit('yd', 0.9144, 'm')

# inch
build_unit('in', (Decimal('36') ** Decimal('-1')) * units.yd, 'm')

# foot
build_unit('ft', (Decimal('3') ** Decimal('-1')) * units.yd, 'm')

# mile
build_unit('mi', 1760 * units.yd, 'm')

# arcmin
build_unit('arcmin', 0.000290888, 'm')

# agate
build_unit('agate', 0.00181428571429, 'm')

# alens
build_unit('aln', 0.593778, 'm')

# barleycorn (UK)
build_unit('bcorn', 0.0084666666666667, 'm')

# bolt (US cloth)
build_unit('bolt', 36.576, 'm')

# blocks
build_unit('bl', 80.4672, 'm')

# button (UK)
build_unit('line_UK', 0.00211667, 'm')

# button (US)
build_unit('line', 0.000635, 'm')

# caliber (centiinch)
build_unit('caliber', 2.54e-4, 'm')

# cubit (UK)
build_unit('cbt', 0.4572, 'm')

# didot point
build_unit('didotpoint', 0.000375972222, 'm')

# digits
build_unit('digit', 0.01905, 'm')

# electron classical radius
build_unit('re', 2.81794e-15, 'm')

# Earth circumfrence
build_unit('Ec', 40000000, 'm')

# ell (Scottish)
build_unit('eel_scottish', 0.94, 'm')

# ell (Flemish)
build_unit('eel_flemish', 0.686, 'm')

# ell (French)
build_unit('eel_french', 1.372, 'm')

# ell (Polish)
build_unit('eel_polish', 0.787, 'm')

# ell (Danish)
build_unit('eel_danish', 0.627708, 'm')

# ell (Swedish)
build_unit('eel_swedish', 0.59, 'm')

# ell (German)
build_unit('eel_german', 0.547, 'm')

# ems (pica)
build_unit('EM_pica', 0.0042175176, 'm')

# exameter
build_unit('Em', 1e+17, 'm')

# finger-cloth
build_unit('finer', 0.1143, 'm')

# fingerbreadth
build_unit('fb', 0.022225, 'm')

# fod
build_unit('fod', 0.3141, 'm')

# football-field
build_unit('fbf', 91.44, 'm')

# greek-plethron
build_unit('pleth', 30.8, 'm')

# greek-stadion
build_unit('std', 185.0, 'm')

# fathom
build_unit('fath', 6 * units.ft_survey, 'm')

# hands
build_unit('hand', 4 * units.inch, 'm')

# Nautical Leagues
build_unit('NL', 3 * units.smi, 'm')

# rods
build_unit('rd', 16.5 * units.ft_survey, 'm')

# perch
build_unit('perch', 1.0 * units.rd, 'm')

# poles
build_unit('pole', 1.0 * units.rd, 'm')

# furlong
build_unit('fur', 40 * units.rd, 'm')

# chain (Gunter's)
build_unit('ch_gunter', 20.1168, 'm')

# chain (engineer's)
build_unit('ch_engineer', 30.48, 'm')

# chain (Ramsden's)
build_unit('ch_ramsden', 30.48, 'm')

# chain (surveyor's)
build_unit('ch_surveyor', 4 * units.rd, 'm')

# cable length (int.)
build_unit('cable_int', 185.2, 'm')

# cable length (UK)
build_unit('cable_UK', 185.318, 'm')

# cable length (US)
build_unit('cable', 120 * units.fath, 'm')

# links
build_unit('li', 1e-2 * units.ch_surveyor, 'm')

# himetric
build_unit('hiMetric', 1e-05, 'm')

# horse-length
build_unit('hl', 2.4, 'm')

# hvat
build_unit('hvat', 1.89648384, 'm')

# lunar-distance
build_unit('LD', 384402000, 'm')

# mils
build_unit('mil', 2.54e-05, 'm')

# myriameters
build_unit('Mym', 10000, 'm')

# nails-cloth
build_unit('nail', 0.05715, 'm')

# paces
build_unit('pace', 0.762, 'm')

# palms
build_unit('palm', 0.0762, 'm')

# picas
build_unit('p', 0.00423333333, 'm')

# rems
build_unit('rem', 0.0042333328, 'm')

# pixels
build_unit('PX', 0.0002645833, 'm')

# rack-unit
build_unit('ru', 0.04445, 'm')

# roman-actus
build_unit('actus', 35.5, 'm')

# ropes
build_unit('rope', 6.096, 'm')

# siriometer
build_unit('sir', 1.496e+17, 'm')

# spans
build_unit('span', 0.2286, 'm')

# twips
build_unit('twip', 1.7639e-05, 'm')

# varas
build_unit('vr', 0.84667, 'm')

# versts
build_unit('vst', 1066.8, 'm')

# x-unit
build_unit('xu', 1.002004e-13, 'm')

# zolls
build_unit('zoll', 0.0254, 'm')

# bicrons
build_unit('µµ', 1e-12, 'm')


# mass
# gram
build_unit('g', 0.001, 'kg')

# electron rest mass (a.u. of mass)
build_unit('me', au_mass, 'kg')

# electron rest mass (a.u. of mass)
build_unit('m₀', 1.0 * units.me, 'kg')

# metric ton
build_unit('t', 1000.0, 'kg')

# dalton (atomic unit of mass)
build_unit('amu', m_u, 'kg')

# atomic mass unit
build_unit('u', m_u, 'kg')

# dalton (atomic unit of mass)
build_unit('Da', m_u, 'kg')

# grain
build_unit('gr', Decimal('64.79891') * Decimal('0.001'), 'kg')

# carat (metric)
build_unit('ct', 0.0002, 'kg')

# planck_mass
build_unit('pm', (h_bar * c / G) ** Decimal('0.5'), 'm')

# dram (troy)
build_unit('dr_troy', 0.00388793, 'kg')

# dram or drachm (apothecary)
build_unit('dr_apoth', 0.00388793, 'kg')

# dram or drachm (avoirdupois)
build_unit('dr_avdp', 0.001771845195312458, 'kg')

# pound
build_unit('lb', 0.45359237001003544, 'kg')

# ounce
build_unit('oz', 0.028349523124984257, 'kg')

# ton (long)
build_unit('t_long', 1016.0469088, 'kg')

# ton(short)
build_unit('t_short', 907.18474, 'kg')

# pennyweight
build_unit('dwt', 0.0015551738, 'kg')

# kip
build_unit('kip', 453.59237, 'kg')

# geepound (slug)
build_unit('slug', 14.5939029372, 'kg')

# assay ton
build_unit('t_assay', 0.029167, 'kg')

# atomic unit of mass (¹²C)
build_unit('Da_12C', 1.66054e-27, 'kg')

# atomic unit of mass (¹⁶O)
build_unit('Da_16O', 1.66001e-27, 'kg')

# atomic unit of mass (¹H)
build_unit('Da_1H', 1.67353e-27, 'kg')

# avogram
build_unit('avogram', 1.66036e-24, 'kg')

# bag (UK, cement)
build_unit('bag_UK', 42.6377, 'kg')

# carat (troy)
build_unit('ct_troy', 0.000205197, 'kg')

# cental
build_unit('cH', 45.3592, 'kg')

# quintal
build_unit('cwt', 100.0, 'kg')


# time
# minute
build_unit('min', 60.0, 's')

# hour
build_unit('h', 60.0 * units.min, 's')

# day
build_unit('d', 24 * units.h, 's')

# week
build_unit('week', 7 * units.d, 's')

# fortnight
build_unit('fortnight', 2 * units.week, 's')

# year (calendar)
build_unit('yr', 365.25 * units.d, 's')

# year (calendar)
build_unit('a', 1.0 * units.yr, 's')

# eon
build_unit('eon', 1e9 * units.yr, 's')

# shake
build_unit('shake', 1e-8, 's')

# a.u. of time
build_unit('atu', au_time, 's')

# month (30 days)
build_unit('mo', units.yr * (12 ** -1), 's')

# month (sidereal)
build_unit('mo_sidereal', 2360590.0, 's')

# month (solar mean)
build_unit('mo_mean', 2628000.0, 's')

# month (synodic), lunar month
build_unit('mo_synodic', 2551440.0, 's')

# day (sidereal)
build_unit('d_sidereal', 86164.0, 's')

# year (astronomical), Bessel year
build_unit('a_astr', 31557900.0, 's')

# year (sidereal)
build_unit('a_sidereal', 31558200.0, 's')

# year (solar mean)
build_unit('a_mean', 31557600.0, 's')

# year (tropical)
build_unit('a_tropical', 31556900.0, 's')

# planck_time
build_unit(
    'planck_time',
    (h_bar * G / c ** Decimal('5')) ** Decimal('0.5'),
    's'
)

# blink
build_unit('blink', 0.864, 's')

# wink
build_unit('wink', 3.33333e-10, 's')


# temperature
build_unit('°R', 1.0, 'K')
build_unit('°F', 1.0, 'K')
# a.u. of temperature
build_unit('atempu', au_temperature, 'K')

# planck_temp
build_unit(
    'planck_temp',
    (h_bar * c ** Decimal('5') / G / k ** Decimal('2')) ** Decimal('0.5'),
    'K'
)


# area
# are
build_unit('are', 100, 'm²')

# square = 100 ft^2
build_unit('square', 9.290304, 'm²')

# barn
build_unit('b', 1e-28, 'm²')

# darcy
build_unit('D', 9.869232667160128e-13, 'm²')

# hectare
build_unit('ha', 100 * units.are, 'm²')

# acre
build_unit('ac', 4046.8564224, 'm²')

# acre
build_unit('acre', 4046.8564224, 'm²')

# circular inch
build_unit('cirin', 0.0005067074790975, 'm²')

# circular mil
build_unit('cirmil', 5.067074790975e-10, 'm²')

# morgen (Dutch)
build_unit('Mg_dutch', 8244.35, 'm²')

# morgen (Prussian)
build_unit('Mg_prussian', 2532.24, 'm²')

# morgen (South Africa)
build_unit('Mg_southafrica', 8565.3, 'm²')

# quarter section
build_unit('sq¼mi_stat', 647497.0, 'm²')

# rood (UK)
build_unit('¼ac', 1011.71, 'm²')

# rood (UK)
build_unit('rood', 1011.71, 'm²')

# section (square statute mile)
build_unit('sqmi', 2589990.0, 'm²')

# section (square statute mile)
build_unit('sqmi_stat', 2589990.0, 'm²')

# outhouse
build_unit('outhouse', 1e-34, 'm²')

# shed
build_unit('shed', 1e-52, 'm²')

# square chain (engineer's)
build_unit('sqch_engineer', 929.03, 'm²')

# square chain (Gunter's)
build_unit('sqch_gunter', 404.686, 'm²')


# volume
# Liter
build_unit('l', 0.001, 'm³')

# Liter
build_unit('L', 0.001, 'm³')

# cubic centimeter (Mohr cubic centimeter)
build_unit('cc', 1.0e-6, 'm³')

# lambda
build_unit('λ', Decimal('1.0e-3') * Decimal('1e-6'), 'm³')

# stere
build_unit('st', 1.0, 'm³')

# acre foot
build_unit('acre⋅ft', 1233.48, 'm³')

# bag (UK)
build_unit('bag', 0.109106, 'm³')

# barrel (US, cranb.)
build_unit('bbl_UScranb', 0.095471, 'm³')

# barrel (US)
build_unit('bbl', 0.1192404712, 'm³')

# barrel (US petrol)
build_unit('bbl_USpetrol', 0.1589872949, 'm³')

# barrel (UK)
build_unit('bbl_UK', 0.16365924, 'm³')

# board foot measure
build_unit('FBM', 0.002359737, 'm³')

# cord foot
build_unit('cd-ft', 0.4525, 'm³')

# cord
build_unit('cord', 3.62, 'm³')

# Hoppus
build_unit('h_cu_ft', 0.0360, 'm³')

# bouteille
build_unit('bouteille', 0.000757682, 'm³')

# bucket (UK)
build_unit('bk_UK', 0.0181844, 'm³')

# bushel (UK)
build_unit('bu_UK', 0.036368700000000004, 'm³')

# bushel (US, dry)
build_unit('bu_US', 0.0352391, 'm³')

# butt (UK)
build_unit('bt_UK', 0.490978, 'm³')

# chaldron (UK)
build_unit('chal_UK', 1.30927, 'm³')

# Gallon (US)
build_unit('gal', 0.00378541178, 'm³')

# Gallon (UK)
build_unit('gal_UK', 4.54609e-3, 'm³')

# Quart (US)
build_unit('qt', 0.000946352946, 'm³')

# Quart (UK)
build_unit('qt_UK', 0.0011365225, 'm³')

# Pint (US)
build_unit('pt', 0.000473176473, 'm³')

# Pint (UK)
build_unit('pt_UK', 0.00056826125, 'm³')

# Fluid Ounce (US)
build_unit('floz', 2.95735296875e-05, 'm³')

# Fluid Ounce (UK)
build_unit('floz_UK', 2.84130625e-05, 'm³')

# cran
build_unit('cran', 0.170478, 'm³')

# dram
build_unit('dr', 3.6967e-06, 'm³')

# gill (US)
build_unit('gi', 0.0001182941, 'm³')

# gill (UK)
build_unit('gi_UK', 0.0001420653, 'm³')

# cup (US)
build_unit('cup', 0.00025, 'm³')

# cup (UK)
build_unit('cup_UK', 0.0002841306, 'm³')

# dessertspoon (US)
build_unit('dstspn', 9.8578e-06, 'm³')

# dessertspoon (UK)
build_unit('dstspn_UK', 1.18388e-05, 'm³')

# tablespoon (US)
build_unit('tbsp', 1.5e-05, 'm³')

# tablespoon (UK)
build_unit('tbsp_UK', 1.77582e-05, 'm³')

# teaspoon (US)
build_unit('tsp', 5e-06, 'm³')

# teaspoon (UK)
build_unit('tsp_UK', 5.9194e-06, 'm³')

# pinch (US)
build_unit('pinch', 6.25e-7, 'm³')

# dash (US)
build_unit('dash', 3.125e-7, 'm³')

# dash (US)
build_unit('smidgen', 1.5625e-7, 'm³')

# drop
build_unit('drop', 5e-8, 'm³')


# frequency
# revolution per minute
build_unit('rpm', 1.0, 'rev⋅min⁻¹')

# revolution per second
build_unit('rps', 1.0, 'rev⋅s⁻¹')

# cycles per second
build_unit('cps', 1.0, 'Hz')


# velocity
# a.u. of velocity
build_unit('avu', au_velocity, 'm⋅s⁻¹')

# mile (naut.) per hour (knot, noeud)
build_unit('kn', 0.514444, 'm⋅s⁻¹')

# mile (naut.) per hour (knot, noeud)
build_unit('knot', 1.0 * units.kn, 'm⋅s⁻¹')

# mile (stat.) per hour
build_unit('mph', 1.0, 'mi⋅h⁻¹')

# mile (stat.) per hour
build_unit('kph', 1.0, 'km⋅h⁻¹')

# mile (stat.) per hour
build_unit('kps', 1.0, 'km⋅s⁻¹')

# mile (stat.) per hour
build_unit('mps', 1.0, 'm⋅s⁻¹')

# foot per second
build_unit('fps', 1.0, 'ft⋅s⁻¹')

# foot per minute
build_unit('fpm', 1.0, 'ft⋅min⁻¹')

# foot per hour
build_unit('fph', 1.0, 'ft⋅h⁻¹')

# inch per second
build_unit('ips', 1.0, 'in⋅s⁻¹')

# benz
build_unit('Bz', 1.0, 'm⋅s⁻¹')

# mil per year
build_unit('mpy', 8.04327e-13, 'm⋅s⁻¹')

# speed of light
build_unit('c', c, 'm⋅s⁻¹')


# acceleration
# galileo
build_unit('Gal', 0.001, 'm⋅s⁻²')

# g (gravitational acceleration)
build_unit('g0', g_n, 'm⋅s⁻²')

# leo
build_unit('leo', 10, 'm⋅s⁻²')

# normal acceleration
build_unit('g0n', 9.80665, 'm⋅s⁻²')


# force
# dyne
build_unit('dyn', 1e-05, 'N')

# kilogram force
build_unit('kgf', g_n * units.kg, 'N')

# kilogram force
build_unit('kgp', 1.0 * units.kgf, 'N')

# gram force
build_unit('gf', g_n * units.g, 'N')

# ton force (metric)
build_unit('tf_metric', g_n * units.t, 'N')

# a.u. of force
build_unit('afu', au_force, 'N')

# crinal
build_unit('crinal', 0.1, 'N')

# grain force
build_unit('grf', 0.6355, 'N')

# kilopond
build_unit('kp', 9.80665, 'N')

# kilopound force (kip force)
build_unit('kipf', 4448.22, 'N')

# Poundal force (US) (pound force)
build_unit('lbf', 4.4482216, 'N')

# Poundal force (UK)
build_unit('pdl', 0.138255, 'N')

# slug force
build_unit('slugf', 143.117, 'N')

# ton force (long)
build_unit('tf_long', 9964.02, 'N')

# ton force (short)
build_unit('tf_short', 8896.44, 'N')

# ounce force
build_unit('ozf', 0.278014, 'N')


# energy
# erg
build_unit('erg', 1e-07, 'J')

# watt-hour
build_unit('Wh', 1.0 * units.h, 'J')

# electronvolt
build_unit('eV', e * units.V, 'J')

# rydberg
build_unit('Ry', h * c * R_inf, 'J')

# hartree
build_unit('Eh', 2 * units.Ry, 'J')


# a.u. of energy
build_unit('aeu', au_energy, 'J')

# calorie (thermochemical)
build_unit('cal_th', 4.184, 'J')

# calorie (IT) (International Steam Table)
build_unit('cal_it', 4.18674, 'J')

# calorie (15°C)
build_unit('cal_15', 4.1855, 'J')

# British thermal unit (ISO)
build_unit('Btu_iso', 1055.056, 'J')

# British thermal unit (IT)
build_unit('Btu_it', 1055.0558526, 'J')

# British thermal unit (thermochemical)
build_unit('Btu_th', 1054.3499999744, 'J')

# quadrillion_Btu
build_unit('quad', 1e15 * units.Btu_iso, 'J')

# therm
build_unit('thm', 1e5 * units.Btu_iso, 'J')

# US therm
build_unit('thm_us', 1.054804e8, 'J')

# ton TNT
build_unit('tTNT', 1e9 * units.cal_th, 'J')

# tonne of oil equivalent
build_unit('toe', 1e10 * units.cal_it, 'J')

# atmosphere liter
build_unit('atm_l', atm * units.l, 'J')

# barrel oil equivalent
build_unit('bboe', 6120000000.0, 'J')

# BeV (billion eV)
build_unit('BeV', 1.60218e-10, 'J')

# British thermal unit (mean)
build_unit('Btu_mean', 1055.87, 'J')

# calorie (4°C)
build_unit('cal_4', 4.2045, 'J')

# Calorie (diet kilocalorie)
build_unit('Cal', 4180.0, 'J')

# Calorie (diet kilocalorie)
build_unit('kcal', 4180.0, 'J')

# calorie (mean)
build_unit('cal_mean', 4.19002, 'J')

# Celsius-heat unit
build_unit('Chu', 1899.18, 'J')


# power
# volt ampere
build_unit('VA', 1.0 * units.V, 'W')

# manpower 1/10th horsepower
build_unit('manpower', 74.56998715823, 'W')

# horsepower (550 ft-lbf/s)
build_unit('hp', 745.6998715823, 'W')

# horsepower (boiler)
build_unit('bhp', 9809.5, 'W')

# horsepower (metric)
build_unit('mhp', 735.49875, 'W')

# horsepower (electric)
build_unit('ehp', 746.0, 'W')

# standard liter per minute
build_unit('slpm', atm * units.l * units.min(exponent=2), 'W')

# standard liter per minute
build_unit('slm', 1.0 * units.slpm, 'W')

# abwatt (emu of power)
build_unit('aW', 1e-07, 'W')

# horsepower (water)
build_unit('whp', 746.043, 'W')

# horsepower (Drawbar)
build_unit('dbhp', 746.043, 'W')

# horsepower (British)
build_unit('hp_gb', 745.7, 'W')

# horsepower
# Italian (cavallo vapore),
# Spanish (caballo de vapor),
# Portuguese (cavalo-vapor)
build_unit('cv', 1.0 * units.mhp, 'W')

# horsepower (paardenkracht)
build_unit('pk', 1.0 * units.mhp, 'W')

# horsepower (cheval-vapeur)
build_unit('ch', 1.0 * units.mhp, 'W')

# horsepower Norwegian (hästkraft), Danish (hästkraft), Swedish (hästkraft)
build_unit('hk', 1.0 * units.mhp, 'W')

# horsepower  German (Pferdestärke)
build_unit('PS', 1.0 * units.mhp, 'W')

# horsepower Polish (koń mechaniczny), Slovenian (konjska moč)
build_unit('KM', 1.0 * units.mhp, 'W')

# horsepower Czech (koňská síla), Slovak (konská sila)
build_unit('ks', 1.0 * units.mhp, 'W')

# horsepower Finnish (hevosvoima)
build_unit('hv', 1.0 * units.mhp, 'W')

# horsepower Estonian (hobujõud)
build_unit('hj', 1.0 * units.mhp, 'W')

# horsepower Hungarian (lóerő)
build_unit('LE', 1.0 * units.mhp, 'W')

# horsepower Bosnian/Croatian/Serbian (konjska snaga)
build_unit('KS', 1.0 * units.mhp, 'W')

# horsepower Macedonian (коњска сила)
build_unit('KC', 1.0 * units.mhp, 'W')

# horsepower  Russian (лошадиная сила)
build_unit('лс', 1.0 * units.mhp, 'W')

# horsepower  Ukrainian (кінська сила)
build_unit('кс', 1.0 * units.mhp, 'W')

# horsepower  Romanian (calputere)
build_unit('CP', 1.0 * units.mhp, 'W')

# prony
build_unit('prony', 98.0665, 'W')


# momentum

# density
# Hg (mercury) (0°C)
build_unit('Hg', 13.5951 * units.kg * units.l(exponent=-1), 'Pa')

# H₂O (water) (0°C)
build_unit('H2O', 1.0 * units.kg * units.l(exponent=-1), 'Pa')

# H₂O (water) (0°C)
build_unit('H₂O', 1.0 * units.H2O, 'Pa')

# H₂O (water) (0°C)
build_unit('Aq', 1.0 * units.H2O, 'Pa')

# O₂ (air) (0°C)
build_unit('O2', 12.677457000000462, 'Pa')

# O₂ (air) (0°C)
build_unit('O₂', 1.0 * units.O2, 'Pa')


# pressure
# a.u. for pressure
build_unit('apressu', au_pressure, 'Pa')

# Bayre
build_unit('Ba', 0.1, 'Pa')

# bar
build_unit('bar', 1e5 * units.Pa, 'Pa')

# atmosphere (technical)
build_unit('at', g_n * (Decimal('0.01') ** Decimal('-2')), 'Pa')

# Torr
build_unit('torr', atm / Decimal('760'), 'Pa')

# pound force per square inch
build_unit('psi', 6894.7572932, 'Pa⋅m')

# kilopound force per square inch
build_unit('ksi', 6894757.293200044, 'Pa')

# sound pressure level
build_unit('SPL', 20e-6 * units.Pa, 'Pa')

# atmosphere (standard)
build_unit('atm', atm, 'Pa')

# Planck pressure
build_unit('pp', 4.63309e+113, 'Pa')

# centimeter-gram-second
build_unit('cgs', 0.1, 'Pa')

# pieze
build_unit('pz', 1000.0, 'Pa')

# pound force per square foot
build_unit('psf', 47.88025897999996, 'Pa')

# ounce force per square inch
build_unit('osi', 430.9223300000048, 'Pa')


# torque  N⋅m

# viscosity
# Poise
build_unit('P', 0.1, 'Pa⋅s')

# reynolds (reyns)
build_unit('reyn', 6894.76, 'Pa⋅s')

# poiseuille
build_unit('Pl', 1.0, 'Pa⋅s')


# kinematic viscosity
# stokes
build_unit('St', 1e-05, 'm²⋅s⁻¹')


# fluidity
# rhe
build_unit('rhe', 1.0 * units.P(exponent=-1), 'Pa⋅s')


# amount of substance
# molecule
build_unit('particle', Decimal('1.0') / N_A, 'mol')

# entities
build_unit('entities', 1.66054e-24, 'mol')

# standard cubic foot
build_unit('SCF', 1.19531, 'mol')

# standard cubic meter
build_unit('SCM', 44.6159, 'mol')


# concentration
# molar
build_unit('M', 1000, 'mol⋅m⁻³')


# catalytic activity

# entropy S  (J⋅K⁻¹)
# clausius
build_unit('Cl', 4.184, 'J⋅K⁻¹')


# molar entropy
# entropy unit
build_unit('eu', 4.184, 'J⋅K⁻¹⋅mol⁻¹')


# radiation
# radian (radioactive)
build_unit('rads', 0.01, 'Gy')

# curie
build_unit('Ci', 3.7e10, 'Bq')

# rutherford
build_unit('Rd', 1e6, 'Bq')

# röntgen
build_unit('roentgen', 2.58e-4, 'C⋅kg⁻¹')

# kerma
build_unit('kerma', 1.0, 'Gy')

# megarad
build_unit('Mrd', 10000.0, 'Gy')


# heat transimission
# peak sun hour
build_unit('PSH', 1e3 * units.Wh, 'J⋅m⁻²')

# langley
build_unit('Ly', 41840.0, 'J⋅m⁻²')


# radiant exitance Mc  (W⋅cm⁻²)
# luminous exitance Mv  (lm⋅cm⁻²)
# radiance Lc  (W⋅cm⁻²⋅sr⁻¹)
# luminance Lv  (lm⋅cm⁻²⋅sr⁻¹)
# nit
build_unit('nit', 1.0, 'cd⋅m⁻²')

# stilb
build_unit('sb', 10000.0, 'cd⋅m⁻²')

# lambert
build_unit('lambert', 31831.0, 'cd⋅m⁻²')

# apostilb
build_unit('asb', 0.31831, 'cd⋅m⁻²')


# luminous flux Φv  (lm)
# bougie d&egrave;cimale
build_unit('bd', 1.02, 'cd')

# bougie international
build_unit('bi', 1.0, 'cd')

# candle (int.)
build_unit('c_int', 1.01937, 'cd')

# candle (new unit)
build_unit('candle', 1.0, 'cd')

# carcel
build_unit('carcel', 10.0, 'cd')

# hefner unit (hefnerkerze)
build_unit('HK', 0.903, 'cd')

# candlepower (spherical)
build_unit('c_power', 12.56637, 'cd⋅sr')


# radiant flux Φe  (W)

# illuminance Ev (lux)
# phot
build_unit('ph', 10000, 'lx')

# foot-candle
build_unit('fc', 10.763910417, 'lx')


# radiant intensity Ic (W⋅sr⁻¹)

# luminous intensity Iv (cd)
# violle
build_unit('violle', 20.4, 'cd')


# electric field E  (V⋅m⁻¹)  *

# 5.14220674763e11
# a.u. of electric field strength
build_unit('aefu', au_electric_field, 'V⋅m⁻¹')


# intensity (W⋅m⁻²)
# a.u. intensity
build_unit(
    'aiu',
    au_intensity,
    'W⋅m⁻²'
)


# electric current I  (A)
# biot
build_unit('Bi', 10, 'A')

# abampere
build_unit('abA', 1.0 * units.Bi, 'A')

# a.u. of electric current
build_unit('aecu', au_current, 'A')

# mean international ampere
build_unit('A_it', 1.00034 / 1.00049, 'A')

# US international ampere
build_unit('A_us', 1.00033 / 1.000495, 'A')

# planck_current
build_unit(
    'planck_current',
    (c ** Decimal('6') / g_n / k_e) ** Decimal('0.5'),
    'A'
)


# edison
build_unit('edison', 100.0, 'A')

# statampere
build_unit('statA', 3.35564e-10, 'A')

# gilbert
build_unit('gilbert', 0.79577, 'A')

# pragilbert
build_unit('pragilbert', 11459.1, 'A')


# electric charge q  (C)
# a.u. of charge
build_unit('acu', au_charge, 'C')

# abcoulomb (emu of charge)
build_unit('aC', 10, 'C')

# abcoulomb (emu of charge)
build_unit('abC', 1.0 * units.aC, 'C')

# faraday
build_unit('faraday', e * N_A, 'mol')

# electronic charge
build_unit('esc', 1.6022e-19, 'C')

# electrostatic unit
build_unit('esu', 3.336e-06, 'C')

# franklin
build_unit('Fr', 3.33564e-10, 'C')

# statcoulomb
build_unit('statC', 3.35564e-10, 'C')

# ampere-hour
build_unit('Ah', 3600, 'C')


# electric potential V  (V)  *
# a.u. of electric potential
build_unit('aepu', au_electric_potential, 'V')

# abvolt (emu of electric potential)
build_unit('aV', 1e-8, 'V')

# abvolt (emu of electric potential)
build_unit('abV', 1.0 * units.aV, 'V')

# volt (mean)
build_unit('V_it', 1.00034, 'V')

# volt (US)
build_unit('V_us', 1.00033, 'V')

# statvolt
build_unit('statV', 299.792, 'V')


# electric field gradient EFG  (V⋅m⁻²)
# a.u. of electric field gradient
build_unit('aefgu', au_electric_field_gradient, 'V⋅m⁻²')


# electric displacement field D  (C⋅m⁻²)

# resistance Ω  (Ω)
# abohm (emu of resistance)
build_unit('aΩ', 1e-9, 'Ω')

# mean international ohm
build_unit('Ω_it', 1.00049, 'Ω')

# US international ohm
build_unit('Ω_us', 1.000495, 'Ω')

# siemens (resistance)
build_unit('SΩ', 0.96, 'Ω')

# statohm
build_unit('statohm', 898755000000.0, 'Ω')


# electrical resistivity and conductivity  Ω⋅m
# ohm (mechanical, SI)
build_unit('Ω_mechanical', 1.0, 'Pa⋅s⋅m⁻³')

# ohm (acoustic, SI)
build_unit('Ω_acoustic', 1, 'Pa⋅s⋅m⁻³')

# ohm (acoustic, SI)
build_unit('Ω_SI', 1, 'Pa⋅s⋅m⁻³')


# conductance
# abmho (emu of conductance)
build_unit('abS', 1e9, 'S')

# abmho (emu of conductance)
build_unit('aW-1', 1.0 * units.abS, 'S')

# gemmho
build_unit('gemʊ', 1e-07, 'S')

# mho
build_unit('mho', 1.0, 'S')

# statmho
build_unit('statmho', 1.11265e-12, 'S')


# capacitance
# abfarad (emu of electric capacitance)
build_unit('abF', 1e9, 'F')

# jar
build_unit('jar', 1.11111e-09, 'F')

# statfarad
build_unit('statF', 1.11265e-12, 'F')


# inductance
# abhenry (emu of inductance)
build_unit('abH', 1e-9, 'H')

# stathenry
build_unit('statH', 898755000000.0, 'H')


# magnetic flux Φ  (Wb)
# maxwell
build_unit('Mx', 1e-9, 'Wb')


# magnetic flux density B  (T)
# gamma
build_unit('γ', 1e-9, 'T')

# a.u. of magnetic flux density
build_unit('amfdu', au_magnetic_flux_density, 'T')

# gauss
build_unit('Gs', 1e-05, 'T')


# magnetic field strength H  (A⋅m⁻¹)
# oersted
build_unit('oe', 79.5775, 'A⋅m⁻¹')

# praoersted
build_unit('praoersted', 11459.1, 'A⋅m⁻¹')


# magnetomotive force mmf  (A)
# ampere_turn
build_unit('At', 1.0, 'A')

# biot_turn
build_unit('biot_turn', 1.0 * units.Bi, 'A')

# gilbert
build_unit(
    'gilbert ',
    Decimal('1') / (Decimal('4') * PI) * units.biot_turn,
    'A'
)


# electric dipole moment p  (C⋅m)
# debye
build_unit('debye', Decimal('1e-9') / c * Decimal('1e-10'), 'C⋅m')


# a.u. of electric dipole moment
build_unit('aedmu', au_electric_dipole_moment, 'C⋅m')


# electric quadrupole moment Q  (C⋅m²)
# buckingham
build_unit(
    'buckingham',
    Decimal('1e-9') / c * (Decimal('1e-10') ** Decimal('2')),
    'C⋅m²'
)

# a.u. of electric quadrupole moment
build_unit('aeqmu', au_electric_quadrupole_moment, 'C⋅m²')


# magnetic moment µ (J⋅T⁻¹)
# bohr_magneton
build_unit('bohr_magneton', e * h_bar / (Decimal('2') * m_e), 'J⋅T⁻¹')

# nuclear_magneton
build_unit('nuclear_magneton', e * h_bar / (Decimal('2') * m_p), 'J⋅T⁻¹')

# a.u. of magnetic dipole moment
build_unit('amdmu', au_magnetic_dipole_moment, 'J⋅T⁻¹')


# volume charge density ρ  (C⋅m⁻³)
# a.u. of charge density
build_unit('acdu', au_charge_density, 'C⋅m⁻³')


# surface charge density σ  (C⋅m⁻²)

# bel (power)
build_unit('B_power', 10.0, 'dB')

# bel (voltage)
build_unit('B_voltage', 5.0, 'dB')

# decibel (power)
build_unit('dB_power', 1.0, 'dB')

# decibel (voltage)
build_unit('dB_voltage', 0.5, 'dB')

# neper
build_unit('Nₚ', 4.34294, 'dB')


# build_unit('Kt', 0.0416667, '')  # carat (karat)
# build_unit('ppb', 1e-10, '')  # part per billion
# build_unit('pph', 0.001, '')  # part per hundred
# build_unit('pphm', 1e-09, '')  # part per hundred million
# build_unit('ppht', 1e-06, '')  # part per hundred thousand
# build_unit('ppm', 1e-07, '')  # part per million
# build_unit('ppq', 1e-15, '')  # part per quadrillion
# build_unit('ppt_tera', 1e-13, '')  # part per tera
# build_unit('ppt', 0.001, '')  # part per thousand

# specific gravity
build_unit('gy', 1000, 'kg⋅m⁻³')


# perm (0°C)
build_unit('perm_0C', 5.72135e-11, 'kg⋅N⁻¹⋅s⁻¹')

# perm (23°C)
build_unit('perm_23C', 5.74525e-11, 'kg⋅N⁻¹⋅s⁻¹')

# perm-inch (0°C)
build_unit('permin_0C', 1.45322e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')

# perm-inch (23°C)
build_unit('permin_23C', 1.45929e-12, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')

# perm-mil (0°C)
build_unit('permmil_0C', 1.45322e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')

# perm-mil (23°C)
build_unit('permmil_23C', 1.45929e-15, 'kg⋅Pa⁻¹⋅m⁻¹⋅s⁻¹')


# brewster
build_unit('brewster', 1e-12, 'm²⋅N⁻¹')


# build_unit('clo', 0.15482, 'K⋅m²⋅W⁻¹')  # clo
# R-value (imperial)
build_unit('°F⋅ft²⋅h⋅Btu_th⁻¹', 0.176228, 'K⋅m²⋅W⁻¹')

# R-value (imperial)
build_unit('°F⋅ft²⋅h/Btu_th', 0.176228, 'K⋅m²⋅W⁻¹')

# RSI (metric R-value)
build_unit('RSI', 1.0, 'K⋅m²⋅W⁻¹')

# tog
build_unit('tog', 0.1, 'K⋅m²⋅W⁻¹')

# dioptre
build_unit('dioptre', 1.0, 'm⁻¹')

# mayer
build_unit('mayer', 1000.0, 'J⋅kg⁻¹⋅K⁻¹')

# mired
build_unit('mired', 1000000.0, 'K⁻¹')


# linear density  (kg⋅m⁻¹)
# denier
build_unit('den', 1.11111e-07, 'kg⋅m⁻¹')

# denier
build_unit('denier', 1.11111e-07, 'kg⋅m⁻¹')

# tex
build_unit('te', 1e-07, 'kg⋅m⁻¹')


# linear charge density λ  (C⋅m⁻¹)
# helmholtz
build_unit('helmholtz', 3.336e-10, 'C⋅m⁻¹')


# linear momentum (kg⋅m⋅s⁻¹)
# a.u. of linear momentum
build_unit('almu', au_linear_momentum, 'kg⋅m⋅s⁻¹')


# volumetric flow rate Q  (m³⋅s⁻¹)
# cumec (musec)
build_unit('cumec', 1.0, 'm³⋅s⁻¹')

# lusec
build_unit('lusec', 0.001, 'm³⋅s⁻¹')

# miner's inch
build_unit('CO', 0.000707921, 'm³⋅s⁻¹')

# gallon (UK) per hour
build_unit('gph_gb', 1.2627999999999998e-06, 'm³⋅s⁻¹')

# gallon (UK) per minute
build_unit('gpm_gb', 7.57682e-05, 'm³⋅s⁻¹')

# gallon (UK) per second
build_unit('gps_gb', 0.004546090000000001, 'm³⋅s⁻¹')

# gallon (US, liq.) per hour
build_unit('gph', 1.0, 'gal⋅h⁻¹')

# gallon (US, liq.) per minute
build_unit('gpm', 1.0, 'gal⋅min⁻¹')

# gallon (US, liq.) per second
build_unit('gps', 0.0037854100000000003, 'gal⋅s⁻¹')

# cubic foot per minute
build_unit('cfm', 1.0, 'ft³⋅min⁻¹')

# cubic foot per second
build_unit('cfs', 1.0, 'ft³⋅s⁻¹')


# angular momentum L  (kg⋅m²⋅s⁻¹)
# a.u. of angular momentum
build_unit('aamu', au_angular_momentum, 'kg⋅m²⋅s⁻¹')

# a.u. of action
build_unit('aau', au_action, 'kg⋅m²⋅s⁻¹')


# acoustic impedeance Z  (rayl)
# rayl (cgs)
build_unit('rayl_cgs', 10, 'kg⋅m⁻²⋅s⁻¹')

# rayl
build_unit('rayl', 1, 'kg⋅m⁻²⋅s⁻¹')

# faraday (based on ¹²C)
build_unit('F_12C', 96485.3, 'C⋅mol⁻¹')

# faraday (chemical)
build_unit('F_chemical', 96495.7, 'C⋅mol⁻¹')

# faraday (physical)
build_unit('F_physical', 96512.9, 'C⋅mol⁻¹')

# reciprocal ohm per centimeter
build_unit('roc', 100, 'S⋅m⁻¹')

# reciprocal ohm per meter
build_unit('rom', 1.0, 'S⋅m⁻¹')

# jansky
build_unit('Jy', 1e-27, 'W⋅m⁻²⋅Hz')

# megagauss-oersted (MGOe)
build_unit('MGOe', 7957.75, 'J⋅m⁻³')

# langley (flux)
build_unit('ly_langley', 697.5, 'W⋅m⁻²')

# international unit
build_unit('UI', 1.66667e-08, 'mol⋅s⁻¹')

# international unit
build_unit('IU', 1.66667e-08, 'mol⋅s⁻¹')

# pound mass
build_unit('lbm', 0.45359237001003544, 'kg⋅m²')

# diopter
build_unit('dpt', 1.0, 'm⁻¹')
