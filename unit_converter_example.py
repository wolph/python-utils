import decimal

from python_utils.unit_converter import Unit, units, convert
from python_utils.unit_converter.quantity import Quantities
from python_utils.unit_converter.quantity import ElectricCurrent

print()
print('There are 3 ways to use the unit converter')
print()
print('1st way')
print()

out_val = convert(52, '°F', '°C')
print("convert(52, '°F', '°C')")
print('>>>', out_val)
print()

out_val = convert(52, 'in³', 'mm³')
print("convert(52, 'in³', 'mm³')")
print('>>>', out_val)
print()

out_val = convert(52, 'g', 'lb')
print("convert(52, 'g', 'lb')")
print('>>>', out_val)
print()

out_val = convert(52, 'mi/h', 'km/h')
print("convert(52, 'mi/h', 'km/h')")
print('>>>', out_val)
print()

out_val = convert(52, 'P', 'Pa s')
print("convert(52, 'P', 'Pa s')")
print('>>>', out_val)
print()

out_val = convert(52, 'ftHg', 'psi')
print("convert(52, 'ftHg', 'psi')")
print('>>>', out_val)
print()


out_val = convert(52.0, '°F', '°C')
print("convert(52.0, '°F', '°C')")
print('>>>', out_val)
print()

out_val = convert(52.0, 'in³', 'mm³')
print("convert(52.0, 'in³', 'mm³')")
print('>>>', out_val)
print()

out_val = convert(52.0, 'g', 'lb')
print("convert(52, 'g', 'lb')")
print('>>>', out_val)
print()

out_val = convert(52.0, 'mi/h', 'km/h')
print("convert(52.0, 'mi/h', 'km/h')")
print('>>>', out_val)
print()

out_val = convert(52.0, 'P', 'Pa s')
print("convert(52.0, 'P', 'Pa s')")
print('>>>', out_val)
print()

out_val = convert(52.0, 'ftHg', 'psi')
print("convert(52.0, 'ftHg', 'psi')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), '°F', '°C')
print("convert(decimal.Decimal('52.00'), '°F', '°C')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), 'in³', 'mm³')
print("convert(decimal.Decimal('52.00'), 'in³', 'mm³')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), 'g', 'lb')
print("convert(decimal.Decimal('52.00'), 'g', 'lb')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), 'mi/h', 'km/h')
print("convert(52, 'mi/h', 'km/h')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), 'P', 'Pa s')
print("convert(52, 'P', 'Pa s')")
print('>>>', out_val)
print()

out_val = convert(decimal.Decimal('52.00'), 'ftHg', 'psi')
print("convert(decimal.Decimal('52.00'), 'ftHg', 'psi')")
print('>>>', out_val)
print()


print()
print('2nd way')
print()

f_unit = Unit('°F')
c_unit = Unit('°C')
out_val = 52 * (f_unit / c_unit)
print("""\
f_unit = Unit('°F')
c_unit = Unit('°C')
52 * (f_unit / c_unit)""")
print('>>>', out_val)
print()

inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
out_val = 52 * (inch_unit / mm_unit)
print("""\
inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
52 * (inch_unit / mm_unit)""")
print('>>>', out_val)
print()

g_unit = Unit('g')
lb_unit = Unit('lb')
out_val = 52 * (g_unit / lb_unit)
print("""\
g_unit = Unit('g')
lb_unit = Unit('lb')
52 * (g_unit / lb_unit)""")
print('>>>', out_val)
print()

mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
out_val = 52 * (mi_unit / km_unit)
print("""\
mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
52 * (mi_unit / km_unit)""")
print('>>>', out_val)
print()

P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
out_val = 52 * (P_unit / Pas_unit)
print("""\
P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
52 * (P_unit / Pas_unit)""")
print('>>>', out_val)
print()

ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
out_val = 52 * (ftHg_unit / psi_unit)
print("""\
ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
52 * (ftHg_unit / psi_unit)""")
print('>>>', out_val)
print()

f_unit = Unit('°F')
c_unit = Unit('°C')
out_val = 52.0 * (f_unit / c_unit)
print("""\
f_unit = Unit('°F')
c_unit = Unit('°C')
52.0 * (f_unit / c_unit)""")
print('>>>', out_val)
print()

inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
out_val = 52.0 * (inch_unit / mm_unit)
print("""\
inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
52.0 * (inch_unit / mm_unit)""")
print('>>>', out_val)
print()

g_unit = Unit('g')
lb_unit = Unit('lb')
out_val = 52.0 * (g_unit / lb_unit)
print("""\
g_unit = Unit('g')
lb_unit = Unit('lb')
52.0 * (g_unit / lb_unit)""")
print('>>>', out_val)
print()

mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
out_val = 52.0 * (mi_unit / km_unit)
print("""\
mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
52.0 * (mi_unit / km_unit)""")
print('>>>', out_val)
print()

P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
out_val = 52.0 * (P_unit / Pas_unit)
print("""\
P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
52.0 * (P_unit / Pas_unit)""")
print('>>>', out_val)
print()

ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
out_val = 52.0 * (ftHg_unit / psi_unit)
print("""\
ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
52.0 * (ftHg_unit / psi_unit)""")
print('>>>', out_val)
print()

f_unit = Unit('°F')
c_unit = Unit('°C')
out_val = decimal.Decimal('52.00') * (f_unit / c_unit)
print("""\
f_unit = Unit('°F')
c_unit = Unit('°C')
decimal.Decimal('52.00') * (f_unit / c_unit)""")
print('>>>', out_val)
print()

inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
out_val = decimal.Decimal('52.00') * (inch_unit / mm_unit)
print("""\
inch_unit = Unit('in', exponent=3)
mm_unit = Unit('mm', exponent=3)
decimal.Decimal('52.00') * (inch_unit / mm_unit)""")
print('>>>', out_val)
print()

g_unit = Unit('g')
lb_unit = Unit('lb')
out_val = decimal.Decimal('52.00') * (g_unit / lb_unit)
print("""\
g_unit = Unit('g')
lb_unit = Unit('lb')
decimal.Decimal('52.00') * (g_unit / lb_unit)""")
print('>>>', out_val)
print()

mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
out_val = decimal.Decimal('52.00') * (mi_unit / km_unit)
print("""\
mi_unit = Unit('mi')
h_unit = Unit('h')
km_unit = Unit('km')
mi_unit /= h_unit
km_unit /= h_unit
decimal.Decimal('52.00') * (mi_unit / km_unit)""")
print('>>>', out_val)
print()

P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
out_val = decimal.Decimal('52.00') * (P_unit / Pas_unit)
print("""\
P_unit = Unit('P')
Pa_unit = Unit('Pa')
s_unit = Unit('s')
Pas_unit = Pa_unit * s_unit
decimal.Decimal('52.00') * (P_unit / Pas_unit)""")
print('>>>', out_val)
print()

ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
out_val = decimal.Decimal('52.00') * (ftHg_unit / psi_unit)
print("""\
ftHg_unit = Unit('ftHg')
psi_unit = Unit('psi')
decimal.Decimal('52.00') * (ftHg_unit / psi_unit)""")
print('>>>', out_val)
print()

print()
print('3rd way')
print()

out_val = 52 * (units.deg_F / units.deg_C)
print("52 * (units.deg_F / units.deg_C)")
print('>>>', out_val)
print()

out_val = 52 * (units.inch(exponent=3) / units.mm(exponent=3))
print("52 * (units.inch(exponent=3) / units.mm(exponent=3))")
print('>>>', out_val)
print()

out_val = 52 * (units.g / units.lb)
print("52 * (units.g / units.lb)")
print('>>>', out_val)
print()

out_val = 52 * ((units.mi / units.h) / (units.km / units.h))
print("52 * ((units.mi / units.h) / (units.km / units.h))")
print('>>>', out_val)
print()

out_val = 52 * (units.P / (units.Pa * units.s))
print("52 * (units.P / (units.Pa * units.s))")
print('>>>', out_val)
print()

out_val = 52 * ((units.ft * units.Hg) / units.psi)
print("52 * ((units.ft * units.Hg) / units.psi)")
print('>>>', out_val)
print()

out_val = 52.0 * (units.deg_F / units.deg_C)
print("52.0 * (units.deg_F / units.deg_C)")
print('>>>', out_val)
print()

out_val = 52.0 * (units.inch(exponent=3) / units.mm(exponent=3))
print("52.0 * (units.inch(exponent=3) / units.mm(exponent=3))")
print('>>>', out_val)
print()

out_val = 52.0 * (units.g / units.lb)
print("52.0 * (units.g / units.lb)")
print('>>>', out_val)
print()

out_val = 52.0 * ((units.mi / units.h) / (units.km / units.h))
print("52.0 * ((units.mi / units.h) / (units.km / units.h))")
print('>>>', out_val)
print()

out_val = 52.0 * (units.P / (units.Pa * units.s))
print("52.0 * (units.P / (units.Pa * units.s))")
print('>>>', out_val)
print()

out_val = 52.0 * ((units.ft * units.Hg) / units.psi)
print("52.0 * ((units.ft * units.Hg) / units.psi)")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * (units.deg_F / units.deg_C)
print("decimal.Decimal('52.00') * (units.deg_F / units.deg_C)")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * (units.inch(exponent=3) / units.mm(exponent=3))
print("decimal.Decimal('52.00') * (units.inch(exponent=3) / units.mm(exponent=3))")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * (units.g / units.lb)
print("decimal.Decimal('52.00') * (units.g / units.lb)")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * ((units.mi / units.h) / (units.km / units.h))
print("decimal.Decimal('52.00') * ((units.mi / units.h) / (units.km / units.h))")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * (units.P / (units.Pa * units.s))
print("decimal.Decimal('52.00') * (units.P / (units.Pa * units.s))")
print('>>>', out_val)
print()

out_val = decimal.Decimal('52.00') * ((units.ft * units.Hg) / units.psi)
print("decimal.Decimal('52.00') * ((units.ft * units.Hg) / units.psi)")
print('>>>', out_val)
print()
print()

print('Alternate ways to do conversions')
print()
print('Creating a callable unit to do conversions over and over again.')
mph_to_kph = units.mph / units.kph
kph = mph_to_kph(60)
print("""\
mph_to_kph = units.mph / units.kph
mph_to_kph(60)""")
print('>>>', kph)
print()

print('Converting into more then one unit')
mph = units.mph(60) + 5
kph = mph / units.kph
fps = mph / units.fps
print("""\
mph = units.mph(60) + 5
mph / units.kph
mph / units.fps""")
print('>>>', kph)
print('>>>', fps)
print()

print('Accessing compatible units to convert to')
mph = units.mph(60)
kph = mph.kph
print("""\
mph = units.mph(60)
mph.kph""")
print('>>>', kph)
print()
print()

print('SI equivilent equation')
unit = Unit('are')
print(unit, '=', unit.base_unit_string)
print()
print()

print('Listing compatible quantities and units')
print()
print('unit:', unit)
print('    quantities:')
for quantity in unit.quantities:
    print('       ', quantity.name + ':', quantity.description)

print('    compatible units:')
for compat_unit in unit.compatible_units:
    print('       ', compat_unit)
    # print('       ', 60, unit, '=', 60 * (unit / compat_unit), compat_unit)

print()
print()

print('Listing compatible units with a quantity')
print()
print(ElectricCurrent.name + ':', ElectricCurrent.description)
for unit in ElectricCurrent.get_units():
    print('   ', unit)

print()
print()
print('The program may appear to be frozen, it is not.')
print('Please wait....')

core_quantities = [
    quantity for quantity in Quantities.get_quantities()
]
core_units = set([
    unit for quantity in Quantities.get_quantities() for unit in quantity
])
print()
print()
print(
    'The total number of available '
    '"core" units is {0}.\n'
    'The total number of available '
    '"core" quantities is {1}.'.format(len(core_units), len(core_quantities))
)
print('This does not include equations or units with a prefix.')
