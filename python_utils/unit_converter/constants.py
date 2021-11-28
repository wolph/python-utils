"""
Constants used in SI units
==========================

.. py:data:: PI
    :type: decimal.Decimal

    Pi with a fractional precision of 49


.. py:data:: f_Cs
    :type: decimal.Decimal
    :value: 'Hz'

    hyperfine transition of 133Cs


.. py:data:: c
    :type: decimal.Decimal
    :value: 'm·s¹'

    speed of light


.. py:data:: h
    :type: decimal.Decimal
    :value: 'J·s'

    Planck constant


.. py:data:: e
    :type: decimal.Decimal
    :value: 'C'

    elementary charge


.. py:data:: k
    :type: decimal.Decimal
    :value: 'J·K⁻¹'

    Boltzmann constant


.. py:data:: N_A
    :type: decimal.Decimal
    :value: 'mol⁻¹'

    Avogadro constant


.. py:data:: K_cd
    :type: decimal.Decimal
    :value: 'lm·W⁻¹'

    luminous efficacy of monochromatic radiation


.. py:data:: atm
    :type: decimal.Decimal
    :value: 'Pa'

    standard atmosphere


.. py:data:: g_n
    :type: decimal.Decimal
    :value: 'm·s⁻²'

    acceleration of free fall


.. py:data:: F
    :type: decimal.Decimal
    :value: 'C·mol⁻¹'

    Faraday constant


.. py:data:: T_ice
    :type: decimal.Decimal
    :value: 'K'

    ice-point temperature


.. py:data:: R
    :type: decimal.Decimal
    :value: 'J·K⁻¹·mol⁻¹'

    molar gas constant


.. py:data:: V_m
    :type: decimal.Decimal
    :value: 'm³·mol⁻¹'

    molar volume of ideal gas (at 273.15 K and 101325 Pa)


.. py:data:: G_0
    :type: decimal.Decimal
    :value: 'S'

    Conductance quantum


.. py:data:: Phi_0
    :type: decimal.Decimal
    :value: 'Wb'

    (superconducting) Magnetic flux quantum


.. py:data:: K_j
    :type: decimal.Decimal
    :value: 'Hz·V⁻¹'

    Josephson constant


.. py:data:: Z_0
    :type: decimal.Decimal
    :value: 'Ω'

    Impedance of free space


.. py:data:: G
    :type: decimal.Decimal
    :value: 'm³·kg⁻¹·s⁻²'

    newtonian gravity constant


.. py:data:: m_u
    :type: decimal.Decimal
    :value: 'kg'

    atomic mass


.. py:data:: m_e
    :type: decimal.Decimal
    :value: 'kg'

    electron mass


.. py:data:: m_p
    :type: decimal.Decimal
    :value: 'kg'

    proton mass


.. py:data:: m_n
    :type: decimal.Decimal
    :value: 'kg'

    neutron mass


.. py:data:: electron_charge_to_mass_quotient
    :type: decimal.Decimal
    :value: 'C⋅kg⁻¹'
    


.. py:data:: h_bar
    :type: decimal.Decimal
    :value: 'J·s'

    h bar, reduced Planck constant, Dirac constant


.. py:data:: alpha
    :type: decimal.Decimal

    Sommerfeld's constant


.. py:data:: epsilon_0
    :type: decimal.Decimal
    :value: 'F·m⁻¹'

    electric constant, permitivitty of free space, vacuum permitivitty


.. py:data:: a_0
    :type: decimal.Decimal
    :value: 'm'

    Bohr radius


.. py:data:: E_h
    :type: decimal.Decimal
    :value: 'eV'

    Hartree energy


.. py:data:: mu_0
    :type: decimal.Decimal

    magnetic constant, permeability of free space, vacuum permeability


.. py:data:: R_K
    :type: decimal.Decimal

    von Klitzing constant


.. py:data:: k_e
    :type: decimal.Decimal
    :value: 'kg·m³·s⁻²·C⁻²'

    Coulomb constant


.. py:data:: R_inf
    :type: decimal.Decimal
    :value: 'm⁻¹'

    Rydberg constant


.. py:data:: sigma
    :type: decimal.Decimal
    :value: 'W m⁻² K⁻⁴'

    Stefan-Boltzmann constant



Atomic Units
============

.. py:data:: au_electric_polarizability
    :type: decimal.Decimal

    Atomic Unit of Electric Polarizability


.. py:data:: au_magnetizability
    :type: decimal.Decimal

    Atomic Unit of Magnetizability


.. py:data:: au_irradiance
    :type: decimal.Decimal

    Atomic Unit of Irradiance


.. py:data:: au_length
    :type: decimal.Decimal

    Atomic Unit of Length


.. py:data:: au_permittivity
    :type: decimal.Decimal

    Atomic Unit of Permittivity


.. py:data:: au_mass
    :type: decimal.Decimal

    Atomic Unit of Mass


.. py:data:: au_time
    :type: decimal.Decimal

    Atomic Unit of Time


.. py:data:: au_temperature
    :type: decimal.Decimal

    Atomic Unit of Temperature


.. py:data:: au_velocity
    :type: decimal.Decimal

    Atomic Unit of Velocity


.. py:data:: au_force
    :type: decimal.Decimal

    Atomic Unit of Force


.. py:data:: au_pressure
    :type: decimal.Decimal

    Atomic Unit of Pressure


.. py:data:: au_electric_field
    :type: decimal.Decimal

    Atomic Unit of Electric Field


.. py:data:: au_intensity
    :type: decimal.Decimal

    Atomic Unit of Intensity


.. py:data:: au_current
    :type: decimal.Decimal

    Atomic Unit of Current


.. py:data:: au_charge
    :type: decimal.Decimal

    Atomic Unit of Charge


.. py:data:: au_electric_potential
    :type: decimal.Decimal

    Atomic Unit of Electric Potential


.. py:data:: au_electric_field_gradient
    :type: decimal.Decimal

    Atomic Unit of Electric Field Gradient


.. py:data:: au_magnetic_flux_density
    :type: decimal.Decimal

    Atomic Unit of Magnetic Flux Density


.. py:data:: au_electric_dipole_moment
    :type: decimal.Decimal

    Atomic Unit of Electric Dipole Moment


.. py:data:: au_electric_quadrupole_moment
    :type: decimal.Decimal

    Atomic Unit of Electric Quadrupole Moment


.. py:data:: au_magnetic_dipole_moment
    :type: decimal.Decimal

    Atomic Unit of Magnetic Dipole Moment


.. py:data:: au_charge_density
    :type: decimal.Decimal

    Atomic Unit of Charge Density


.. py:data:: au_linear_momentum
    :type: decimal.Decimal

    Atomic Unit of Linear Momentum


.. py:data:: au_angular_momentum
    :type: decimal.Decimal

    Atomic Unit of Angular Momentum


.. py:data:: au_action
    :type: decimal.Decimal

    Atomic Unit of Action


.. py:data:: au_energy
    :type: decimal.Decimal

    Atomic Unit of Energy

|
|
"""
from decimal import Decimal


PI = Decimal('3.1415926535897932384626433832795028841971693993751')
TANSEC = Decimal('0.0000048481368111333441675396429478852851658848753880815')
LN_10 = Decimal('2.3025850929940456840179914546843642076011014886288')
WEIN_X = Decimal('4.9651142317442763036987591313228939440555849867973')
WEIN_U = Decimal('2.8214393721220788934031913302944851953458817440731')
EULERS = Decimal('2.71828182845904523536028747135266249775724709369995')

# Hz - hyperfine transition of 133Cs
f_Cs = Decimal('9192631770')

# m·s^1 - speed of light
c = Decimal('299792458')

# J·s - Planck constant
h = Decimal('6.62607015e-34')

# C elementary charge
e = Decimal('1.602176634e-19')

# J·K^–1 - Boltzmann constant
k = Decimal('1.380649e-23')

# mol^–1 - Avogadro constant
N_A = Decimal('6.02214076e23')

# lm·W^–1 luminous efficacy of monochromatic radiation
K_cd = Decimal('683')

# Pa - standard atmosphere
atm = Decimal('101325')

# m·s^-2 - acceleration of free fall
g_n = Decimal('9.80665')

# C·mol^-1 - Faraday constant
F = e * N_A

# K - ice-point temperature
T_ice = Decimal('273.15')

# J·K^-1·mol^-1 - molar gas constant
R = k * N_A

# m^3·mol^-1 - molar volume of ideal gas (at 273.15 K and 101325 Pa)
V_m = Decimal('22.41410e-3')

# S - Conductance quantum
G_0 = (Decimal('2') * (e ** Decimal('2'))) / h

# Wb - (superconducting) Magnetic flux quantum
Phi_0 = h / (Decimal('2') * e)

# Hz·V^-1 - Josephson constant
K_j = Decimal('1') / Phi_0

# Ω Impedance of free space
Z_0 = Decimal('376.730313668')

# m^3·kg^–1·s^–2 - newtonian gravity constant
G = Decimal('6.67430e-11')

# kg - atomic mass
m_u = Decimal('1.66053906660e-27')

# kg - electron mass
m_e = Decimal('9.1093837015e-31')

# kg - proton mass
m_p = Decimal('1.67262192369e-27')

# kg - neutron mass
m_n = Decimal('1.67492749804e-27')

# C⋅kg^−1
electron_charge_to_mass_quotient = -e/m_e

# J·s - h bar, reduced Planck constant, Dirac constant
h_bar = h / (Decimal('2') * PI)

# Sommerfeld's constant
alpha = ((e ** Decimal('2')) * Z_0) / (Decimal('4') * PI * h_bar)

# F·m^−1 - electric constant, permitivitty of free space, vacuum permitivitty
epsilon_0 = (e ** Decimal('2')) / (Decimal('2') * alpha * h * c)

# m - Bohr radius
a_0 = (
    (Decimal('4') * PI * epsilon_0 * (h_bar ** Decimal('2'))) /
    (m_e * (e ** Decimal('2')))
)

# eV - Hartree energy
E_h = (e ** Decimal('2')) / a_0

# magnetic constant, permeability of free space, vacuum permeability
mu_0 = Decimal('2') * alpha * h / (e ** Decimal('2') * c)

# von Klitzing constant
R_K = h / (e ** Decimal('2'))

# kg·m^3·s^−2·C^−2  - Coulomb constant
k_e = (Decimal('1') / (Decimal('4') * PI * epsilon_0))

# m^-1 - Rydberg constant
R_inf = (
    (m_e * (e ** Decimal('4'))) /
    (Decimal('8') * (epsilon_0 ** Decimal('2')) * (h ** Decimal('3')) * c)
)

# W m^-2 K^-4 - Stefan-Boltzmann constant
sigma = (
    (Decimal('2') * (PI ** Decimal('5')) * (k ** Decimal('4'))) /
    (Decimal('15') * (h ** Decimal('3')) * (c ** Decimal('3')))
)


au_electric_polarizability = (e ** Decimal('2')) * (a_0 ** Decimal('2')) / E_h
au_magnetizability = (e ** Decimal('2')) * (a_0 ** Decimal('2')) / m_e
au_irradiance = ((E_h ** Decimal('2')) / h_bar * a_0) ** Decimal('2')
au_length = a_0  # bohr
au_permittivity = (e ** Decimal('2')) / (a_0 * E_h)
au_mass = m_e
au_time = h_bar / E_h
au_temperature = (Decimal('2') * h * c * R_inf) / k
au_velocity = a_0 * E_h / h_bar
au_force = E_h / a_0
au_pressure = (E_h / a_0) ** Decimal('3')
au_electric_field = E_h / (e * a_0)
au_intensity = (
    Decimal('0.5') *
    epsilon_0 *
    c *
    (au_electric_field ** Decimal('2'))
)
au_current = e * E_h / h_bar
au_charge = e
au_electric_potential = E_h / e
au_electric_field_gradient = E_h / (e * (a_0 ** Decimal('2')))
au_magnetic_flux_density = h_bar / (e * (a_0 ** Decimal('2')))
au_electric_dipole_moment = e * a_0
au_electric_quadrupole_moment = e * (a_0 ** Decimal('2'))
au_magnetic_dipole_moment = e * h_bar / m_e
au_charge_density = e / (a_0 ** Decimal('3'))
au_linear_momentum = h_bar / a_0
au_angular_momentum = h_bar
au_action = h_bar
au_energy = E_h  # hartree
