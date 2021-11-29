import decimal

from .unit import BASE_UNITS, NAMED_DERIVED_UNITS, UNITS, Unit  # NOQA
from .import units


# This meta is to save on typing, at the moment it only changes the
# parent_quantities attribute from a list to a _ParentQuantities instance
# which is a subclass of a list but has it's equality checking changed.
class _QuantityMeta(type):
    # only here to make IDE happy
    _quantities = []
    unit = None

    def __init__(cls, name, bases, dct):
        super(_QuantityMeta, cls).__init__(name, bases, dct)
        if cls.__name__ != 'Quantities':
            # this is here to ensure that each class has it's _units attribute.
            # This atribute is being accessed via a class method in the base
            # class and I didn't want to have to  declare this attribute for
            # each and every class. This is a shortcut to do that.
            cls._units = []

            cls.base_unit_string = cls.unit.base_unit_string
            instance = cls()

            if not cls.name:
                name = ''
                for char in cls.__name__:
                    if char.isupper():
                        name += ' '

                    name += char

                cls.name = name

            if not cls.description:
                description = cls.__doc__
                if description is None:
                    description = ''

                description = ' '.join(
                    line.strip() for line in description.split('\n')
                )

                cls.description = description

            cls._quantities.append(instance)


# The quantities are going to be responsible for the things listed below.
# Storing like units.
# Identifying compatable quantities to convert to/from.
# Generating the base SI equation
# Testing unit compatability for conversion
# Identifying the SI unit to convert to and from.

# There are SI conversions that can be done at the quantity level and
# need to be included into the unit converter. an exaple would be
# the mass to charge ratio "m/Q" where "m"  is the unit for the
# Mass quantity and "Q" is the unit for the Charge quantity.
# by  creating quantities  as if they are units will allow for such
# conversions to take place.
class Quantities(object, metaclass=_QuantityMeta):
    symbol = None
    unit = None
    _quantities = []
    exponent = 1
    base_unit_string = ''
    name = ''
    description = ''

    def __init__(self, exponent=1):
        self.exponent = decimal.Decimal(str(exponent))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.exponent == other.exponent

        if isinstance(other, Unit):
            return other.raw_unit == self.unit

        return False

    def __str__(self):
        return self.name

    @classmethod
    def get_units(cls):
        for quantity in cls._quantities:
            if isinstance(quantity, cls):
                return quantity.__iter__()

    def __iter__(self):
        if self.base_unit_string:
            all_units = [Unit(self.base_unit_string)]

            for u in BASE_UNITS.values():
                if (
                        u.base_unit_string == self.base_unit_string and
                        u not in all_units
                ):
                    all_units.append(u)

            for u in NAMED_DERIVED_UNITS.values():
                if (
                        u.base_unit_string == self.base_unit_string and
                        u not in all_units
                ):
                    all_units.append(u)

            for u in UNITS.values():
                if (
                        u.base_unit_string == self.base_unit_string and
                        u not in all_units
                ):
                    all_units.append(u)
        else:
            all_units = []

        return iter(all_units)

    def is_unit_compatible(self, unit):
        return unit.base_unit_string == self.base_unit_string

    @classmethod
    def get_quantities(cls):
        if cls != Quantities:
            raise TypeError(
                'This method is not available for the "{0}" class'.format(
                    cls.__name__
                )
            )

        return iter(cls._quantities)

    def __call__(self, exponent=1):
        return self.__class__(exponent)
        

class Length(Quantities):
    symbol = 'l'
    unit = units.m


class Mass(Quantities):
    symbol = 'm'
    unit = units.kg


class Time(Quantities):
    symbol = 't'
    unit = units.s


class ElectricCurrent(Quantities):
    symbol = 'I'
    unit = units.A


class ThermodynamicTemperature(Quantities):
    symbol = 'T'
    unit = units.K


class AmountOfSubstance(Quantities):
    symbol = 'n'
    unit = units.mol


subscript_v = chr(0x1D65)


class LuminiousIntensity(Quantities):
    symbol = 'Iᵥ'
    unit = units.cd


class PlaneAngle(Quantities):
    """
    Ratio of circular arc length to radius
    """
    symbol = 'θ'
    unit = units.rad


class SolidAngle(Quantities):
    """
    Ratio of area on a sphere to its radius squared
    """
    symbol = 'Ω'
    unit = units.sr


class Frequency(Quantities):
    """
    Number of (periodic) occurrences per unit time
    """
    symbol = 'f'
    unit = units.Hz


class Force(Quantities):
    """
    Transfer of momentum per unit time
    """
    symbol = 'F'
    unit = units.N


class Pressure(Quantities):
    """
    Force per unit area
    """
    symbol = 'P'
    unit = units.Pa


class Stress(Pressure):
    """
    Force per unit oriented surface area
    """
    symbol = 'σ'


class Energy(Quantities):
    """
    Energy
    """
    symbol = 'E'
    unit = units.J


class Work(Energy):
    """
    Transferred energy
    """
    symbol = 'W'


class QuantityOfHeat(Energy):
    """
    Thermal energy
    """
    symbol = 'Q'


class Power(Quantities):
    """
    Rate of transfer of energy per unit time
    """
    symbol = 'P'
    unit = units.W


class ElectricCharge(Quantities):
    """
    The force per unit electric field strength
    """
    symbol = 'Q'
    unit = units.C


class QuantityOfElectricity(ElectricCharge):
    pass


class ElectricPotential(Quantities):
    """
    Energy required to move a unit charge through an
    electric field from a reference point
    """
    symbol = 'φ'
    unit = units.V


class PotentialDifference(ElectricPotential):
    pass


class ElectromotiveForce(ElectricPotential):
    symbol = 'ℰ'


class SurfaceTension(Quantities):
    """
    Energy change per unit change in surface area
    """
    symbol = 'γ'
    unit = units.N / units.m


class ElectricCapacitance(Quantities):
    symbol = None
    unit = units.F


class ElectricResistance(Quantities):
    """
    Electric potential per unit electric current
    """
    symbol = 'R'
    unit = units.ohm


class ElectricConductance(Quantities):
    """
    Measure for how easily current flows through a material
    """
    symbol = 'G'
    unit = units.S


class MagneticFlux(Quantities):
    """
    Measure of magnetism, taking account of the strength and
    the extent of a magnetic field
    """
    symbol = 'Φ'
    unit = units.Wb


class FluxOfMagneticInductance(MagneticFlux):
    pass


class MagneticFluxDensity(Quantities):
    """
    Measure for the strength of the magnetic field
    """
    symbol = 'B'
    unit = units.T


class MagneticInductance(MagneticFluxDensity):
    pass


class MagneticFieldIntensity(Quantities):
    symbol = None
    unit = units.A / units.m


class Inductance(Quantities):
    """
    Magnetic flux generated per unit current through a circuit
    """
    symbol = 'L'
    unit = units.H


class CelsiusTemperature(Quantities):
    symbol = None
    unit = units.deg_C


class LuminousFlux(Quantities):
    """
    Perceived power of a light source
    """
    symbol = 'F'
    unit = units.lm


class Illuminance(Quantities):
    """
    Luminous flux per unit surface area
    """
    symbol = 'Ev'
    unit = units.lx


class RadioactiveActivity(Quantities):
    """
    Number of particles decaying per unit time
    """
    symbol = 'A'
    unit = units.Bq


class AbsorbedDoseOfRadiation(Quantities):
    """
    Ionizing radiation energy absorbed by biological tissue per unit mass
    """
    symbol = 'D'
    unit = units.Gy


class SpecificEnergy(AbsorbedDoseOfRadiation):
    """
    Energy density per unit mass
    """
    symbol = None


class RelativePermeability(Quantities):
    symbol = 'µr'
    unit = units.H / units.m


class AbsorbedDoseRate(Quantities):
    """Absorbed dose received per unit of time """
    symbol = None
    unit = units.Gy / units.s


class Acceleration(Quantities):
    """
    Rate of change of velocity per unit time:
    the second time derivative of position
    """
    symbol = 'a'
    unit = units.m / units.s(exponent=2)


class Admittance(Quantities):
    symbol = None
    unit = units.S


class AmountOfSubstanceConcentration(Quantities):
    """
    Amount of substance per unit volume
    """
    symbol = 'C'
    unit = units.mol / units.m(exponent=3)


class Molarity(AmountOfSubstanceConcentration):
    pass


SUB_A = chr(0x2090)  # ₐ
OMEGA_LOWER = chr(0x03C9)  # ω
PROPORTIONAL_TO = chr(0x221D)  # ∝


class AngularAcceleration(Quantities):
    """Change in angular velocity per unit time """
    symbol = '∝'
    unit = units.rad / units.s(exponent=2)


class AngularMomentum(Quantities):
    """
    Measure of the extent and direction of an object
    rotates about a reference point
    """
    symbol = 'L'
    unit = units.kg * units.m(exponent=2) / units.s


class AngularVelocity(Quantities):
    """
    The angle incremented in a plane by a segment
    connecting an object and a reference point per unit time
    """
    symbol = 'ω'
    unit = units.rad / units.s


class AngularJerk(Quantities):
    """
    The rate of change of the angular acceleration vector, or the third
    derivative of the angular displacement vector
    """
    symbol = 'ζ'
    unit = units.rad / units.s(exponent=3)


class AngularImpulse(Quantities):
    """
    The product of a torque and its time of duration being equal to the
    change in angular momentum of a body free to rotate.
    """
    symbol = 'ΔL'
    unit = units.kg * units.m(exponent=2) / units.s


class Area(Quantities):
    """Extent of a surface"""
    symbol = 'A'
    unit = units.m(exponent=2)


RHO_LOWER = chr(0x03C1)
GREEK_A = chr(0x0391)


class AreaDensity(Quantities):
    """Mass per unit area"""
    symbol = 'ρA'
    unit = units.kg / units.m(exponent=2)


class Capacitance(Quantities):
    """Stored charge per unit electric potential"""
    symbol = 'C'
    unit = units.F


class CatalyticConcentration(Quantities):
    """
    Change in reaction rate due to presence of a
    catalyst per unit volume of the system
    """
    symbol = None
    unit = units.kat / units.m(exponent=3)


class CatalyticActivity(Quantities):
    symbol = None
    unit = units.kat


class CatalyticEfficiency(Quantities):
    symbol = None
    unit = units.m(exponent=3) / (units.mol * units.s)


class CentrifugalForce(Quantities):
    """
    Inertial force that appears to act on all objects
    when viewed in a rotating frame of reference
    """
    symbol = 'Fc'
    unit = units.N * units.rad


class ChemicalPotential(Quantities):
    """
    Energy per unit change in amount of substance
    """
    symbol = 'μ'
    unit = units.J / units.mol


class Crackle(Quantities):
    """
    Change of jounce per unit time: the fifth time derivative of position
    """
    symbol = 'c'
    unit = units.m / units.s(exponent=5)


class ElectricCurrentDensity(Quantities):
    """
    Electric current per unit cross-section area
    """
    symbol = 'j'
    unit = units.A / units.m(exponent=2)


class DoseEquivalentOfRadiation(Quantities):
    """
    Received radiation adjusted for the effect on biological tissue
    """
    symbol = 'H'
    unit = units.Sv


class DynamicViscosity(Quantities):
    """
    Measure for the resistance of an incompressible fluid to stress
    """
    symbol = 'η'
    unit = units.Pa * units.s


class ElectricChargeDensity(Quantities):
    symbol = 'ρQ'
    unit = units.C / units.m(exponent=3)


class ElectricDisplacementField(Quantities):
    """
    Strength of the electric displacement
    """
    symbol = 'D'
    unit = units.C / units.m(exponent=2)


class ElectricFieldStrength(Quantities):
    """
    Strength of the electric field
    """
    symbol = 'E'
    unit = units.V / units.m


class ElectricConductivity(Quantities):
    """
    Measure of a material's ability to conduct an electric current
    """
    symbol = 'σ'
    unit = units.S / units.m


class ApparantPower(Quantities):
    symbol = None
    unit = units.VA


class Density(Quantities):
    """
    Mass per unit volume
    """
    symbol = 'ρ'
    unit = units.kg / units.m(exponent=3)


class ElectricFlux(Quantities):
    symbol = None
    unit = units.C


class ElectricFluxDensity(Quantities):
    symbol = 'D'
    unit = units.C / units.m(exponent=2)


class EnergyDensity(Quantities):
    """
    Energy per unit volume
    """
    symbol = 'ρE'
    unit = units.J / units.m(exponent=3)


class EnergyFluxDensity(Quantities):
    symbol = None
    unit = units.W / units.m(exponent=2)


class Entropy(Quantities):
    """
    Logarithmic measure of the number of available states of a system
    """
    symbol = 'S'
    unit = units.J / units.K


class HeatCapacity(Entropy):
    """
    Energy per unit temperature change
    """
    symbol = 'Cp'


class HeatFluxDensity(Quantities):
    """
    Heat flow per unit time per unit surface area
    """
    symbol = 'ϕQ'
    unit = units.W / units.m(exponent=2)


class Impedance(Quantities):
    """
    Resistance to an alternating current of a given frequency,
    including effect on phase
    """
    symbol = 'Z'
    unit = units.ohm


class Impulse(Quantities):
    """
    Transferred momentum
    """
    symbol = 'Imp'
    unit = units.N * units.s


class Rotatum(Quantities):
    """
    The derivative of torque with respect to time
    """
    symbol = 'P'
    unit = units.N * units.m / units.s


class MeanLifetime(Quantities):
    """
    Average time for a particle of a substance to decay
    """
    symbol = 'τ'
    unit = units.s


class Absement(Quantities):
    """
    Measure of sustained displacement:
    the first integral with respect to time of displacement
    """
    symbol = 'A'
    unit = units.m * units.s


class Jerk(Quantities):
    """
    Change of acceleration per unit time: the third
    time derivative of position
    """
    symbol = 'J'
    unit = units.m / units.s(exponent=3)


class Jolt(Jerk):
    pass


class Jounce(Quantities):
    """
    Change of jerk per unit time: the fourth time derivative of position
    """
    symbol = 's'
    unit = units.m / units.s(exponent=4)


class Snap(Jounce):
    pass


class LinearDensity(Quantities):
    """
    Mass per unit length
    """
    symbol = 'λ'
    unit = units.kg / units.m


class Luminance(Quantities):
    symbol = 'Lᵥ'
    unit = units.cd / units.m(exponent=2)


class LuminousEfficacy(Quantities):
    symbol = None
    unit = units.lm / units.W


class MagneticFieldStrength(Quantities):
    """
    Strength of a magnetic field
    """
    symbol = 'H'
    unit = units.A / units.m


class Magnetization(MagneticFieldStrength):
    pass


class MassConcentration(Quantities):
    symbol = 'γ'
    unit = units.kg / units.m(exponent=3)
    si_expression = ' kg⋅m⁻³'


class MolarEnergy(Quantities):
    """
    Amount of energy present in a system per unit amount of substance
    """
    symbol = None
    unit = units.J / units.mol


class MolarEntropy(Quantities):
    """
    Heat capacity of a material per unit amount of substance
    """
    symbol = None
    unit = units.J / (units.K * units.mol)


class MolarHeatCapacity(MolarEntropy):
    symbol = 'c'


class MolarVolume(Quantities):
    """
    Amount of substance per unit volume
    """
    symbol = ''
    unit = units.m(exponent=3) / units.mol
    si_expression = 'mol⁻¹⋅m³'


class MomentOfInertia(Quantities):
    """
    Inertia of an object with respect to angular acceleration
    """
    symbol = 'I'
    unit = units.kg * units.m(exponent=2)
    si_expression = 'kg⋅m²'


class Momentum(Quantities):
    """
    Product of an object's mass and velocity
    """
    symbol = 'p'
    unit = units.kg * units.m / units.s


class RadiantEnergy(Quantities):
    symbol = 'Qₑ'
    unit = units.J


class RadiantEnergyDensity(Quantities):
    symbol = 'Wₑ'
    unit = units.J / units.m(exponent=3)


SUB_V = chr(0x1D65)


class RadiantFlux(Quantities):
    symbol = 'ϕₑ'
    unit = units.W


class SpectralFlux(Quantities):
    symbol = 'ϕₑ,ᵥ'
    unit = units.W / units.Hz


SUB_E = chr(0x2091)


class RadiantIntensity(Quantities):
    """
    Power of emitted electromagnetic radiation per unit solid angle
    """
    symbol = 'I'
    unit = units.W / units.sr


class SpectralIntensity(Quantities):
    symbol = 'Iₑ,Ω,ᵥ'
    unit = units.W / (units.sr * units.Hz)


class Radiance(Quantities):
    """
    Power of emitted electromagnetic radiation per unit solid
    angle per emitting source area
    """
    symbol = 'L'
    unit = units.W / (units.m(exponent=2) * units.sr)


class SpectralRadiance(Quantities):
    symbol = 'Lₑ,Ω,ᵥ'
    unit = (
        units.W *
        units.sr(exponent=-1) *
        units.m(exponent=-2) *
        units.Hz(exponent=-1)
    )


class RadiantFluxDensity(Quantities):
    symbol = 'ϕ'
    unit = units.W / units.m(exponent=2)


class Irradiance(RadiantFluxDensity):
    """
    Electromagnetic radiation power per unit surface area
    """
    symbol = 'I'


class Intensity(Quantities):
    """
    Power per unit cross sectional area
    """
    symbol = 'I'
    unit = units.W / units.m(exponent=2)


class ElectricalResistivity(Quantities):
    """
    Bulk property equivalent of electrical resistance
    """
    symbol = 'ρe'
    unit = units.ohm * units.m


class SpecificVolume(Quantities):
    """
    Volume per unit mass (reciprocal of density)
    """
    symbol = 'v'
    unit = units.m(exponent=3) / units.kg


class Velocity(Quantities):
    """
    Moved distance per unit time
    """
    symbol = 'v'
    unit = units.m / units.s


class SurfaceDensity(Quantities):
    symbol = 'ρA'
    unit = units.kg / units.m(exponent=2)


class Volume(Quantities):
    """
    Three dimensional extent of an object
    """
    symbol = 'V'
    unit = units.m(exponent=3)


class VolumetricFlow(Quantities):
    """
    Rate of change of volume with respect to time
    """
    symbol = 'Q'
    unit = units.m(exponent=3) / units.s


class VolumetricEntropy(Quantities):
    symbol = None
    unit = units.S * units.arcsecond


class WaveLength(Quantities):
    """
    Perpendicular distance between repeating units of a wave
    """
    symbol = 'λ'
    unit = units.m


class WaveNumber(Quantities):
    """
    Repetency or spatial frequency: the number of cycles per unit distance
    """
    symbol = 'k'
    unit = units.m(exponent=-1)


class WaveVector(Quantities):
    """
    Repetency or spatial frequency vector: the number of cycles per
    unit distance
    """
    symbol = 'k'
    unit = units.m(exponent=-1)


class OpticalPower(Quantities):
    """
    Measure of the effective curvature of a lens or curved mirror;
    inverse of focal length
    """
    symbol = 'P'
    unit = units.dpt


class Permeability(Quantities):
    """
    Measure for how the magnetization of material is affected by the
    application of an external magnetic field
    """
    symbol = 'μs'
    unit = units.H / units.m


class Permittivity(Quantities):
    """
    Measure for how the polarization of a material is affected by the
    application of an external electric field
    """
    symbol = 'εs'
    unit = units.F / units.m


class Pop(Quantities):
    """
    Rate of change of crackle per unit time: the sixth time
    derivative of position
    """
    symbol = 'p'
    unit = units.m / units.s(exponent=6)


class ReactionRate(Quantities):
    """
    Rate of a chemical reaction for unit time
    """
    symbol = 'r'
    unit = units.mol / (units.m(exponent=3) * units.s)


class Reluctance(Quantities):
    """
    Rate of a chemical reaction for unit time
    """
    symbol = 'R'
    unit = units.H(exponent=-1)
    si_expression = 'kg⁻¹⋅m⁻²⋅s²⋅A²'


class Spin(Quantities):
    """
    Quantum-mechanically defined angular momentum of a particle
    """
    symbol = 'S'
    unit = units.kg * units.m(exponent=2) / units.s


class Weight(Quantities):
    """
    Gravitational force on an object
    """
    symbol = 'w'
    unit = units.N


class YoungsModulus(Quantities):
    """
    Ratio of stress to strain
    """
    symbol = 'E'
    unit = units.Pa


class Action(Quantities):
    """
    Numerical value describing how a physical system has changed over time
    """
    symbol = None
    unit = units.J * units.s


class Compressibility(Quantities):
    """
    The inverse or reciprocal of the bulk modulus of elasticity.
    """
    symbol = 'k'
    unit = units.m(exponent=2) / units.N


# Conductance
#
# conductance
# symbol = '['S']'
# unit = ''
# si_expression = 'A²⋅kg⁻¹⋅m⁻²⋅s³'
# parent_quantities = []


class DiffusionCoefficient(Quantities):
    """
    The diffusion coefficient is a physical constant dependent on
    molecule size and other properties of the diffusing substance
    as well as on temperature and pressure.
    """
    symbol = 'D'
    unit = units.m(exponent=2) / units.s


class Exposure(Quantities):
    """
    Measure of the ionization of air due to ionizing radiation from photons;
    that is, gamma rays and X-rays.
    """
    symbol = 'X'
    unit = units.C / units.kg


class FrequencyDrift(Quantities):
    """
    An unintended and generally arbitrary offset of an oscillator from
    its nominal frequency.
    """
    symbol = None
    unit = units.Hz / units.s


class FuelConsumption(Quantities):
    """
     Distance covered per unit volume.
    """
    symbol = None
    unit = units.m(exponent=-2)


class FuelEfficiency(FuelConsumption):
    pass


class Kerma(Quantities):
    """
    Amount of energy that is transferred from photons to electrons per
    unit mass at a certain position.
    """
    symbol = 'K'
    unit = units.Gy


class KinematicViscosity(Quantities):
    """
    The ratio of - absolute (or dynamic) viscosity to density - a quantity
    in which no force is involved.
    """
    symbol = 'ν'
    unit = units.St


class LinearChargeDensity(Quantities):
    """
    The amount of electric charge per unit length
    """
    symbol = 'λ'
    unit = units.C / units.m


class LuminousEmittance(Quantities):
    """
    Luminous flux emitted from a surface
    """
    symbol = 'Mv'
    unit = units.lm / units.m(exponent=2)


class LuminousEnergy(Quantities):
    """
    The perceived energy of light.
    """
    symbol = 'Qv'
    unit = units.lm * units.s


class LuminousEnergyDensity(Quantities):
    symbol = 'ωv'
    unit = units.lm * units.s / units.m(exponent=3)


class LuminousExitance(LuminousEmittance):
    pass


class LuminousExposure(Quantities):
    """
    Time-integrated illuminance
    """
    symbol = 'Hv'
    unit = units.lx / units.s


class LuminousPower(LuminousFlux):
    pass


class MagneticDipoleMoment(Quantities):
    """
    The torque that the object experiences in a given magnetic field.
    """
    symbol = 'μ'
    unit = units.Wb * units.m


class MagneticMoment(Quantities):
    """
    The magnetic strength and orientation of a magnet or other object
    that produces a magnetic field.
    """
    symbol = 'm'
    unit = units.A * units.m(exponent=2)
    si_expression = 'A⋅m²'


class MagneticPermeability(Quantities):
    """
    Relative increase or decrease in the resultant magnetic field inside
    a material compared with the magnetizing field in which the given
    material is located
    """
    symbol = 'μ'
    unit = units.H / units.m


class MagneticPermeance(Quantities):
    """
    Measure of the quantity of magnetic flux for a number of current-turns.
    """
    symbol = 'P'
    unit = units.H


class MagneticRigidity(Quantities):
    """
    The effect of particular magnetic fields on the motion of the
    charged particles.
    """
    symbol = 'R'
    unit = units.T * units.m
    si_expression = 'A⁻¹⋅kg⋅m⋅s⁻²'


class MagneticSusceptibility(Quantities):
    """
    How much a material will become magnetized in an applied magnetic field
    """
    symbol = 'M'
    unit = units.m / units.H


class MagneticVectorPotential(Quantities):
    """
    The vector quantity in classical electromagnetism defined so that its
    curl is equal to the magnetic field
    """
    symbol = 'B'
    unit = units.Wb / units.m


class MagnetomotiveForce(Quantities):
    """
    Quantity appearing in the equation for the magnetic flux in a
    magnetic circuit, often called Ohm's law for magnetic circuits
    """
    symbol = 'mmf'
    unit = units.A * units.rad


class MassFlowRate(Quantities):
    """
    The rate of flow of mass.
    """
    symbol = 'qm'
    unit = units.kg / units.s


class Molality(Quantities):
    symbol = 'b'
    unit = units.mol / units.kg


class MolarConductivity(Quantities):
    """
    The molar conductivity of an electrolyte solution is defined as
    its conductivity divided by its molar concentration.[
    """
    symbol = 'Λm'
    unit = units.S * units.m(exponent=2) / units.mol


class MolarMass(Quantities):
    """
    Mass of a sample of that compound divided by the amount of
    substance in that sample.
    """
    symbol = 'M'
    unit = units.kg / units.mol


class PolarizationDensity(Quantities):
    """
    The vector field that expresses the density of permanent or induced
    electric dipole moments in a dielectric material
    """
    symbol = 'P'
    unit = units.C / units.m(exponent=2)


class PowerDensity(Quantities):
    """
    The amount of power (time rate of energy transfer) per unit volume
    """
    symbol = None
    unit = units.W / units.m(exponent=3)
    si_expression = 'kg⋅m⁻¹⋅s⁻³'


class SpectralIrradiance(Quantities):
    """
    Irradiance of a surface per unit frequency or wavelength
    """
    symbol = 'Ee,ν'
    unit = units.W * units.m(exponent=-2) * units.Hz(exponent=-1)


class SpectralFluxDensity(SpectralIrradiance):
    symbol = 'Ee,λ'


class Radiosity(Quantities):
    """
    Radiant flux leaving (emitted, reflected and transmitted by) a
    surface per unit area
    """
    symbol = 'Je'
    unit = units.W / units.m(exponent=2)


class SpectralRadiosity(Quantities):
    """
    Radiosity of a surface per unit frequency or wavelength
    """
    symbol = 'Je,λ'
    unit = units.W / units.m(exponent=3)


class RadiantExitance(Quantities):
    """
    Radiant flux emitted by a surface per unit area
    """
    symbol = 'Me'
    unit = units.W / units.m(exponent=2)


class SpectralExitance(Quantities):
    """
    Radiant exitance of a surface per unit frequency or wavelength
    """
    symbol = 'Me,λ'
    unit = units.W / units.m(exponent=2)


class RadiantExposure(Quantities):
    """
    Radiant energy received by a surface per unit area, or equivalently
    irradiance of a surface integrated over time of irradiation
    """
    symbol = 'He'
    unit = units.J / units.m(exponent=2)


class SpectralExposure(Quantities):
    """
    Radiant exposure of a surface per unit frequency or wavelength
    """
    symbol = 'He,λ'
    unit = units.J / units.m(exponent=3)


class SpectralPower(SpectralFlux):
    pass


class Reactance(Quantities):
    """
    The opposition to the current flow of an element in the circuit
    because of its capacitance
    """
    symbol = 'X'
    unit = units.ohm


class SpecificAngularMomentum(Quantities):
    """
    The cross product of the relative position vector r
    and the relative velocity vector v.
    """
    symbol = 'h'
    unit = units.m(exponent=2) / units.s


class SpecificEntropy(Quantities):
    symbol = None
    unit = units.J / (units.K * units.kg)


class SpecificHeatCapacity(SpecificEntropy):
    """
    Heat capacity per unit mass
    """
    symbol = 'c'


class Stiffness(Quantities):
    """
    The extent to which an object resists deformation in response
    to an applied force.
    """
    symbol = 'k'
    unit = units.N / units.m


class Susceptance(Quantities):
    """
    The imaginary part of admittance, where the real part is conductance
    """
    symbol = 'B'
    unit = units.S


NABLA = chr(0x2207)


class TemperatureGradient(Quantities):
    """
    Steepest rate of temperature change at a particular location
    """
    symbol = '∇T'
    unit = units.K / units.m


class ThermalConductivity(Quantities):
    """
    Measure for the ease with which a material conducts heat
    """
    symbol = 'λ'
    unit = units.W / (units.m * units.K)


class ThermalConductance(Quantities):
    """
    Measure for the ease with which a material conducts heat
    """
    symbol = None
    unit = units.W / units.K


class ThermalDiffusivity(Quantities):
    """
    The thermal conductivity divided by density and specific
    heat capacity at constant pressure
    """
    symbol = '∝'
    unit = units.m(exponent=2) / units.s


class ThermalResistivity(Quantities):
    """
    Measure for the ease with which a material resists conduction of heat
    """
    symbol = 'Rλ'
    unit = units.K * units.m / units.W


class ThermalResistance(Quantities):
    """
    Measure for the ease with which an object resists conduction of heat
    """
    symbol = 'R'
    unit = units.K / units.W


class Torque(Quantities):
    """
    Product of a force and the perpendicular distance of the force
    from the point about which it is exerted
    """
    symbol = 'τ'
    unit = units.N * units.m


class Voltage(Quantities):
    """
    The pressure from an electrical circuit's power source that pushes
    charged electrons (current) through a conducting loop
    """
    symbol = 'V'
    unit = units.V


class Yank(Quantities):
    """
    Rate of change of force
    """
    symbol = 'Y'
    unit = units.N / units.s
