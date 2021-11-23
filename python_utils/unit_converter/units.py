# noinspection PySingleQuotedDocstring
'''
SI Base Units
_____________
.. py:data:: SUP_2
    :type: str
    :value: '²'

.. py:data:: mol
    :type: Unit
    :value: 'mol'
    
    mole - amount of substance

.. py:data:: cd
    :type: Unit
    :value: 'cd'
    
    candela - luminous intensity

.. py:data:: kg
    :type: Unit
    :value: 'kg'
    
    kilogram - mass

.. py:data:: m
    :type: Unit
    :value: 'm'
    
    meter - length

.. py:data:: s
    :type: Unit
    :value: 's'
    
    second - time

.. py:data:: A
    :type: Unit
    :value: 'A'
    
    ampere - electric current

.. py:data:: K
    :type: Unit
    :value: 'K'
    
    kelvin - thermodynamic temperature


Non SI Base Units
________________

.. py:data:: bit
    :type: Unit
    :value: 'bit'
    
    binary bit - data

.. py:data:: dB
    :type: Unit
    :value: 'dB'
    
    decible - sound


 SI Derived units with special names
 ___________________________________

.. py:data:: Hz
    :type: Unit
    :value: 'Hz'
    
    hertz - frequency

.. py:data:: N
    :type: Unit
    :value: 'N'
    
    newton - force

.. py:data:: Pa
    :type: Unit
    :value: 'Pa'
    
    pascal - pressure, stress

.. py:data:: J
    :type: Unit
    :value: 'J'
    
    joule - energy, work, quantity of heat

.. py:data:: W
    :type: Unit
    :value: 'W'
    
    watt - power, radiant flux

.. py:data:: C
    :type: Unit
    :value: 'C'
    
    coulomb - electric charge, quantity of electricity

.. py:data:: V
    :type: Unit
    :value: 'V'
    
    volt - electric potential difference, electromotive force

.. py:data:: F
    :type: Unit
    :value: 'F'
    
    farad - capacitance

.. py:data:: ohm
    :type: Unit
    :value: 'Ω'
    
    ohm - electric resistance

.. py:data:: S
    :type: Unit
    :value: 'S'
    
    siemens - electric conductance

.. py:data:: Wb
    :type: Unit
    :value: 'Wb'
    
    weber - magnetic flux

.. py:data:: T
    :type: Unit
    :value: 'T'
    
    tesla - magnetic flux density

.. py:data:: H
    :type: Unit
    :value: 'H'
    
    henry - inductance

.. py:data:: deg_C
    :type: Unit
    :value: '°C'
    
    degree Celsius - Celsius temperature

.. py:data:: lm
    :type: Unit
    :value: 'lm'
    
    lumen - luminous flux

.. py:data:: lx
    :type: Unit
    :value: 'lx'
    
    lux - illuminance

.. py:data:: Bq
    :type: Unit
    :value: 'Bq'
    
    becquerel - activity (of a radionuclide)

.. py:data:: Gy
    :type: Unit
    :value: 'Gy'
    
    gray - absorbed dose, specific energy (imparted), kerma

.. py:data:: Sv
    :type: Unit
    :value: 'Sv'
    
    sievert - dose equivalent

.. py:data:: kat
    :type: Unit
    :value: 'kat'
    
    katal - catalytic activity

.. py:data:: r
    :type: Unit
    :value: 'r'
    
    radian - plane angle

.. py:data:: sr
    :type: Unit
    :value: 'sr'
    
    steradian - solid angle


Additional units
________________

.. py:data:: au_length
    :type: Unit
    :value: 'au_length'

.. py:data:: am
    :type: Unit
    :value: 'am'

.. py:data:: angstrom
    :type: Unit
    :value: 'Å'

.. py:data:: ft
    :type: Unit
    :value: 'ft'

.. py:data:: yd
    :type: Unit
    :value: 'yd'

.. py:data:: mi
    :type: Unit
    :value: 'mi'

.. py:data:: inch
    :type: Unit
    :value: 'in'

.. py:data:: micron
    :type: Unit
    :value: 'µ'

.. py:data:: arcmin
    :type: Unit
    :value: 'arcmin'

.. py:data:: AU
    :type: Unit
    :value: 'AU'

.. py:data:: UA
    :type: Unit
    :value: 'UA'

.. py:data:: au
    :type: Unit
    :value: 'au'

.. py:data:: agate
    :type: Unit
    :value: 'agate'

.. py:data:: aln
    :type: Unit
    :value: 'aln'

.. py:data:: bcorn
    :type: Unit
    :value: 'bcorn'

.. py:data:: a0
    :type: Unit
    :value: 'a0'

.. py:data:: rBohr
    :type: Unit
    :value: 'rBohr'

.. py:data:: bolt
    :type: Unit
    :value: 'bolt'

.. py:data:: bl
    :type: Unit
    :value: 'bl'

.. py:data:: line_UK
    :type: Unit
    :value: 'line_UK'

.. py:data:: line
    :type: Unit
    :value: 'line'

.. py:data:: cable_int
    :type: Unit
    :value: 'cable_int'

.. py:data:: cable_UK
    :type: Unit
    :value: 'cable_UK'

.. py:data:: cable
    :type: Unit
    :value: 'cable'

.. py:data:: caliber
    :type: Unit
    :value: 'caliber'

.. py:data:: ch_engineer
    :type: Unit
    :value: 'ch_engineer'

.. py:data:: ch_gunter
    :type: Unit
    :value: 'ch_gunter'

.. py:data:: ch_ramsden
    :type: Unit
    :value: 'ch_ramsden'

.. py:data:: ch_surveyor
    :type: Unit
    :value: 'ch_surveyor'

.. py:data:: cbt
    :type: Unit
    :value: 'cbt'

.. py:data:: didotpoint
    :type: Unit
    :value: 'didotpoint'

.. py:data:: digit
    :type: Unit
    :value: 'digit'

.. py:data:: re
    :type: Unit
    :value: 're'

.. py:data:: Ec
    :type: Unit
    :value: 'Ec'

.. py:data:: eel_scottish
    :type: Unit
    :value: 'eel_scottish'

.. py:data:: eel_flemish
    :type: Unit
    :value: 'eel_flemish'

.. py:data:: eel_french
    :type: Unit
    :value: 'eel_french'

.. py:data:: eel_polish
    :type: Unit
    :value: 'eel_polish'

.. py:data:: eel_danish
    :type: Unit
    :value: 'eel_danish'

.. py:data:: eel_swedish
    :type: Unit
    :value: 'eel_swedish'

.. py:data:: eel_german
    :type: Unit
    :value: 'eel_german'

.. py:data:: EM_pica
    :type: Unit
    :value: 'EM_pica'

.. py:data:: Em
    :type: Unit
    :value: 'Em'

.. py:data:: fath
    :type: Unit
    :value: 'fath'

.. py:data:: fm
    :type: Unit
    :value: 'fm'

.. py:data:: f
    :type: Unit
    :value: 'f'

.. py:data:: finer
    :type: Unit
    :value: 'finer'

.. py:data:: fb
    :type: Unit
    :value: 'fb'

.. py:data:: fod
    :type: Unit
    :value: 'fod'

.. py:data:: fbf
    :type: Unit
    :value: 'fbf'

.. py:data:: fur
    :type: Unit
    :value: 'fur'

.. py:data:: pleth
    :type: Unit
    :value: 'pleth'

.. py:data:: std
    :type: Unit
    :value: 'std'

.. py:data:: hand
    :type: Unit
    :value: 'hand'

.. py:data:: hiMetric
    :type: Unit
    :value: 'hiMetric'

.. py:data:: hl
    :type: Unit
    :value: 'hl'

.. py:data:: hvat
    :type: Unit
    :value: 'hvat'

.. py:data:: ly
    :type: Unit
    :value: 'ly'

.. py:data:: li
    :type: Unit
    :value: 'li'

.. py:data:: LD
    :type: Unit
    :value: 'LD'

.. py:data:: mil
    :type: Unit
    :value: 'mil'

.. py:data:: Mym
    :type: Unit
    :value: 'Mym'

.. py:data:: nail
    :type: Unit
    :value: 'nail'

.. py:data:: NL
    :type: Unit
    :value: 'NL'

.. py:data:: NM
    :type: Unit
    :value: 'NM'

.. py:data:: pace
    :type: Unit
    :value: 'pace'

.. py:data:: palm
    :type: Unit
    :value: 'palm'

.. py:data:: pc
    :type: Unit
    :value: 'pc'

.. py:data:: perch
    :type: Unit
    :value: 'perch'

.. py:data:: p
    :type: Unit
    :value: 'p'

.. py:data:: PX
    :type: Unit
    :value: 'PX'

.. py:data:: pl
    :type: Unit
    :value: 'pl'

.. py:data:: pole
    :type: Unit
    :value: 'pole'

.. py:data:: ru
    :type: Unit
    :value: 'ru'

.. py:data:: rem
    :type: Unit
    :value: 'rem'

.. py:data:: rd
    :type: Unit
    :value: 'rd'

.. py:data:: actus
    :type: Unit
    :value: 'actus'

.. py:data:: rope
    :type: Unit
    :value: 'rope'

.. py:data:: sir
    :type: Unit
    :value: 'sir'

.. py:data:: span
    :type: Unit
    :value: 'span'

.. py:data:: twip
    :type: Unit
    :value: 'twip'

.. py:data:: vr
    :type: Unit
    :value: 'vr'

.. py:data:: vst
    :type: Unit
    :value: 'vst'

.. py:data:: xu
    :type: Unit
    :value: 'xu'

.. py:data:: zoll
    :type: Unit
    :value: 'zoll'

.. py:data:: bicrons
    :type: Unit
    :value: 'µµ'

.. py:data:: D
    :type: Unit
    :value: 'D'

.. py:data:: ac
    :type: Unit
    :value: 'ac'

.. py:data:: acre
    :type: Unit
    :value: 'acre'

.. py:data:: are
    :type: Unit
    :value: 'are'

.. py:data:: b
    :type: Unit
    :value: 'b'

.. py:data:: cirin
    :type: Unit
    :value: 'cirin'

.. py:data:: cirmil
    :type: Unit
    :value: 'cirmil'

.. py:data:: Mg_dutch
    :type: Unit
    :value: 'Mg_dutch'

.. py:data:: Mg_prussian
    :type: Unit
    :value: 'Mg_prussian'

.. py:data:: Mg_southafrica
    :type: Unit
    :value: 'Mg_southafrica'

.. py:data:: quarter_sq_mi_stat
    :type: Unit
    :value: '¼mi²_stat'

.. py:data:: quarter_ac
    :type: Unit
    :value: '¼ac'

.. py:data:: rood
    :type: Unit
    :value: 'rood'

.. py:data:: sqmi
    :type: Unit
    :value: 'sqmi'

.. py:data:: sq_mi_stat
    :type: Unit
    :value: 'mi²_stat'

.. py:data:: outhouse
    :type: Unit
    :value: 'outhouse'

.. py:data:: shed
    :type: Unit
    :value: 'shed'

.. py:data:: sqch_engineer
    :type: Unit
    :value: 'sqch_engineer'

.. py:data:: sqch_gunter
    :type: Unit
    :value: 'sqch_gunter'

.. py:data:: acre_ft
    :type: Unit
    :value: 'acre⋅ft'

.. py:data:: bag
    :type: Unit
    :value: 'bag'

.. py:data:: bbl_UScranb
    :type: Unit
    :value: 'bbl_UScranb'

.. py:data:: bbl
    :type: Unit
    :value: 'bbl'

.. py:data:: bbl_USpetrol
    :type: Unit
    :value: 'bbl_USpetrol'

.. py:data:: bbl_UK
    :type: Unit
    :value: 'bbl_UK'

.. py:data:: FBM
    :type: Unit
    :value: 'FBM'

.. py:data:: bouteille
    :type: Unit
    :value: 'bouteille'

.. py:data:: bk_UK
    :type: Unit
    :value: 'bk_UK'

.. py:data:: bu_UK
    :type: Unit
    :value: 'bu_UK'

.. py:data:: bu_US
    :type: Unit
    :value: 'bu_US'

.. py:data:: bt_UK
    :type: Unit
    :value: 'bt_UK'

.. py:data:: chal_UK
    :type: Unit
    :value: 'chal_UK'

.. py:data:: cc
    :type: Unit
    :value: 'cc'

.. py:data:: l
    :type: Unit
    :value: 'l'

.. py:data:: L
    :type: Unit
    :value: 'L'

.. py:data:: gal
    :type: Unit
    :value: 'gal'

.. py:data:: gal_UK
    :type: Unit
    :value: 'gal_UK'

.. py:data:: qt
    :type: Unit
    :value: 'qt'

.. py:data:: qt_UK
    :type: Unit
    :value: 'qt_UK'

.. py:data:: pt
    :type: Unit
    :value: 'pt'

.. py:data:: pt_UK
    :type: Unit
    :value: 'pt_UK'

.. py:data:: floz
    :type: Unit
    :value: 'floz'

.. py:data:: floz_UK
    :type: Unit
    :value: 'floz_UK'

.. py:data:: cran
    :type: Unit
    :value: 'cran'

.. py:data:: dr
    :type: Unit
    :value: 'dr'

.. py:data:: st
    :type: Unit
    :value: 'st'

.. py:data:: gi
    :type: Unit
    :value: 'gi'

.. py:data:: gi_UK
    :type: Unit
    :value: 'gi_UK'

.. py:data:: cup
    :type: Unit
    :value: 'cup'

.. py:data:: cup_UK
    :type: Unit
    :value: 'cup_UK'

.. py:data:: dstspn
    :type: Unit
    :value: 'dstspn'

.. py:data:: dstspn_UK
    :type: Unit
    :value: 'dstspn_UK'

.. py:data:: tbsp
    :type: Unit
    :value: 'tbsp'

.. py:data:: tbsp_UK
    :type: Unit
    :value: 'tbsp_UK'

.. py:data:: tsp
    :type: Unit
    :value: 'tsp'

.. py:data:: tsp_UK
    :type: Unit
    :value: 'tsp_UK'

.. py:data:: M0
    :type: Unit
    :value: 'm₀'

.. py:data:: me
    :type: Unit
    :value: 'me'

.. py:data:: u_dalton
    :type: Unit
    :value: 'u_dalton'

.. py:data:: u
    :type: Unit
    :value: 'u'

.. py:data:: uma
    :type: Unit
    :value: 'uma'

.. py:data:: Da
    :type: Unit
    :value: 'Da'

.. py:data:: dr_troy
    :type: Unit
    :value: 'dr_troy'

.. py:data:: dr_apoth
    :type: Unit
    :value: 'dr_apoth'

.. py:data:: dr_avdp
    :type: Unit
    :value: 'dr_avdp'

.. py:data:: g
    :type: Unit
    :value: 'g'

.. py:data:: lb
    :type: Unit
    :value: 'lb'

.. py:data:: oz
    :type: Unit
    :value: 'oz'

.. py:data:: t_long
    :type: Unit
    :value: 't_long'

.. py:data:: t_short
    :type: Unit
    :value: 't_short'

.. py:data:: t
    :type: Unit
    :value: 't'

.. py:data:: dwt
    :type: Unit
    :value: 'dwt'

.. py:data:: kip
    :type: Unit
    :value: 'kip'

.. py:data:: gr
    :type: Unit
    :value: 'gr'

.. py:data:: slug
    :type: Unit
    :value: 'slug'

.. py:data:: t_assay
    :type: Unit
    :value: 't_assay'

.. py:data:: Da_12C
    :type: Unit
    :value: 'Da_12C'

.. py:data:: Da_16O
    :type: Unit
    :value: 'Da_16O'

.. py:data:: Da_1H
    :type: Unit
    :value: 'Da_1H'

.. py:data:: avogram
    :type: Unit
    :value: 'avogram'

.. py:data:: bag_UK
    :type: Unit
    :value: 'bag_UK'

.. py:data:: ct
    :type: Unit
    :value: 'ct'

.. py:data:: ct_troy
    :type: Unit
    :value: 'ct_troy'

.. py:data:: cH
    :type: Unit
    :value: 'cH'

.. py:data:: cwt
    :type: Unit
    :value: 'cwt'

.. py:data:: au_time
    :type: Unit
    :value: 'au_time'

.. py:data:: blink
    :type: Unit
    :value: 'blink'

.. py:data:: d
    :type: Unit
    :value: 'd'

.. py:data:: d_sidereal
    :type: Unit
    :value: 'd_sidereal'

.. py:data:: fortnight
    :type: Unit
    :value: 'fortnight'

.. py:data:: h
    :type: Unit
    :value: 'h'

.. py:data:: min
    :type: Unit
    :value: 'min'

.. py:data:: mo
    :type: Unit
    :value: 'mo'

.. py:data:: mo_sidereal
    :type: Unit
    :value: 'mo_sidereal'

.. py:data:: mo_mean
    :type: Unit
    :value: 'mo_mean'

.. py:data:: mo_synodic
    :type: Unit
    :value: 'mo_synodic'

.. py:data:: shake
    :type: Unit
    :value: 'shake'

.. py:data:: week
    :type: Unit
    :value: 'week'

.. py:data:: wink
    :type: Unit
    :value: 'wink'

.. py:data:: a_astr
    :type: Unit
    :value: 'a_astr'

.. py:data:: a
    :type: Unit
    :value: 'a'

.. py:data:: y
    :type: Unit
    :value: 'y'

.. py:data:: a_sidereal
    :type: Unit
    :value: 'a_sidereal'

.. py:data:: a_mean
    :type: Unit
    :value: 'a_mean'

.. py:data:: a_tropical
    :type: Unit
    :value: 'a_tropical'

.. py:data:: bd
    :type: Unit
    :value: 'bd'

.. py:data:: bi
    :type: Unit
    :value: 'bi'

.. py:data:: c_int
    :type: Unit
    :value: 'c_int'

.. py:data:: c
    :type: Unit
    :value: 'c'

.. py:data:: carcel
    :type: Unit
    :value: 'carcel'

.. py:data:: HK
    :type: Unit
    :value: 'HK'

.. py:data:: violle
    :type: Unit
    :value: 'violle'

.. py:data:: entities
    :type: Unit
    :value: 'entities'

.. py:data:: SCF
    :type: Unit
    :value: 'SCF'

.. py:data:: SCM
    :type: Unit
    :value: 'SCM'
    


.. py:data:: arcsecond
    :type: Unit
    :value: '\''

.. py:data:: arcminute
    :type: Unit
    :value: '"'

.. py:data:: pid
    :type: Unit
    :value: 'pid'

.. py:data:: degree
    :type: Unit
    :value: '°'

.. py:data:: gon
    :type: Unit
    :value: 'gon'

.. py:data:: grade
    :type: Unit
    :value: 'grade'

.. py:data:: ah
    :type: Unit
    :value: 'ah'

.. py:data:: percent
    :type: Unit
    :value: '%'

.. py:data:: rev
    :type: Unit
    :value: 'rev'

.. py:data:: sign
    :type: Unit
    :value: 'sign'

.. py:data:: B
    :type: Unit
    :value: 'B'

.. py:data:: Gib
    :type: Unit
    :value: 'Gib'

.. py:data:: GiB
    :type: Unit
    :value: 'GiB'

.. py:data:: Gb
    :type: Unit
    :value: 'Gb'

.. py:data:: GB
    :type: Unit
    :value: 'GB'

.. py:data:: Kib
    :type: Unit
    :value: 'Kib'

.. py:data:: KiB
    :type: Unit
    :value: 'KiB'

.. py:data:: Kb
    :type: Unit
    :value: 'Kb'

.. py:data:: KB
    :type: Unit
    :value: 'KB'

.. py:data:: Mib
    :type: Unit
    :value: 'Mib'

.. py:data:: MiB
    :type: Unit
    :value: 'MiB'

.. py:data:: Mb
    :type: Unit
    :value: 'Mb'

.. py:data:: MB
    :type: Unit
    :value: 'MB'

.. py:data:: Tib
    :type: Unit
    :value: 'Tib'

.. py:data:: TiB
    :type: Unit
    :value: 'TiB'

.. py:data:: Tb
    :type: Unit
    :value: 'Tb'

.. py:data:: TB
    :type: Unit
    :value: 'TB'

.. py:data:: aW
    :type: Unit
    :value: 'aW'

.. py:data:: hp
    :type: Unit
    :value: 'hp'

    horsepower (550 ft-lbf/s)

.. py:data:: mhp
    :type: Unit
    :value: 'mhp'

    horsepower (metric)

.. py:data:: bhp
    :type: Unit
    :value: 'bhp'

    horsepower (boiler)

.. py:data:: ehp
    :type: Unit
    :value: 'ehp'

    horsepower (electric)

.. py:data:: whp
    :type: Unit
    :value: 'whp'

    horsepower (water)

.. py:data:: dbhp
    :type: Unit
    :value: 'dbhp'

    horsepower (Drawbar)

.. py:data:: hp_gb
    :type: Unit
    :value: 'hp_gb'

    horsepower (British)

.. py:data:: cv
    :type: Unit
    :value: 'cv'

    horsepower Italian (cavallo vapore), Spanish (caballo de vapor),
    Portuguese (cavalo-vapor)

.. py:data:: pk
    :type: Unit
    :value: 'pk'

    horsepower (paardenkracht)

.. py:data:: ch
    :type: Unit
    :value: 'ch'

    horsepower (cheval-vapeur)

.. py:data:: hk
    :type: Unit
    :value: 'hk'

    horsepower Norwegian (hästkraft), Danish (hästkraft), Swedish (hästkraft)

.. py:data:: PS
    :type: Unit
    :value: 'PS'

    horsepower  German (Pferdestärke)

.. py:data:: KM
    :type: Unit
    :value: 'KM'

    horsepower Polish (koń mechaniczny), Slovenian (konjska moč)

.. py:data:: ks
    :type: Unit
    :value: 'ks'

    horsepower Czech (koňská síla), Slovak (konská sila)

.. py:data:: hv
    :type: Unit
    :value: 'hv'

    horsepower Finnish (hevosvoima)

.. py:data:: hj
    :type: Unit
    :value: 'hj'

    horsepower Estonian (hobujõud)

.. py:data:: LE
    :type: Unit
    :value: 'LE'

    horsepower Hungarian (lóerő)

.. py:data:: KS
    :type: Unit
    :value: 'KS'

    horsepower Bosnian/Croatian/Serbian (konjska snaga)

.. py:data:: KC
    :type: Unit
    :value: 'KC'

    horsepower Macedonian (коњска сила)

.. py:data:: Nc
    :type: Unit
    :value: 'лс'

    horsepower  Russian (лошадиная сила)

.. py:data:: Kc
    :type: Unit
    :value: 'кс'

    horsepower  Ukrainian (кінська сила)

.. py:data:: CP
    :type: Unit
    :value: 'CP'

    horsepower  Romanian (calputere)

.. py:data:: prony
    :type: Unit
    :value: 'prony'

    prony

.. py:data:: at
    :type: Unit
    :value: 'at'

.. py:data:: atm
    :type: Unit
    :value: 'atm'

.. py:data:: bar
    :type: Unit
    :value: 'bar'

.. py:data:: Ba
    :type: Unit
    :value: 'Ba'

.. py:data:: p_P
    :type: Unit
    :value: 'p_P'

.. py:data:: cgs
    :type: Unit
    :value: 'cgs'

.. py:data:: torr
    :type: Unit
    :value: 'torr'

.. py:data:: pz
    :type: Unit
    :value: 'pz'

.. py:data:: Hg
    :type: Unit
    :value: 'Hg'

.. py:data:: H2O
    :type: Unit
    :value: 'H2O'

.. py:data:: Aq
    :type: Unit
    :value: 'Aq'

.. py:data:: O2
    :type: Unit
    :value: 'O2'

.. py:data:: ksi
    :type: Unit
    :value: 'ksi'

.. py:data:: psi
    :type: Unit
    :value: 'psi'

.. py:data:: psf
    :type: Unit
    :value: 'psf'

.. py:data:: osi
    :type: Unit
    :value: 'osi'

.. py:data:: kerma
    :type: Unit
    :value: 'kerma'

.. py:data:: Mrd
    :type: Unit
    :value: 'Mrd'

.. py:data:: rad
    :type: Unit
    :value: 'rad'

.. py:data:: B_power
    :type: Unit
    :value: 'B_power'

.. py:data:: B_voltage
    :type: Unit
    :value: 'B_voltage'

.. py:data:: dB_power
    :type: Unit
    :value: 'dB_power'

.. py:data:: dB_voltage
    :type: Unit
    :value: 'dB_voltage'

.. py:data:: au_mf
    :type: Unit
    :value: 'au_mf'

.. py:data:: Gs
    :type: Unit
    :value: 'Gs'

.. py:data:: M
    :type: Unit
    :value: 'M'

.. py:data:: au_charge
    :type: Unit
    :value: 'au_charge'

.. py:data:: aC
    :type: Unit
    :value: 'aC'

.. py:data:: esc
    :type: Unit
    :value: 'esc'

.. py:data:: esu
    :type: Unit
    :value: 'esu'

.. py:data:: Fr
    :type: Unit
    :value: 'Fr'

.. py:data:: statC
    :type: Unit
    :value: 'statC'

.. py:data:: aS
    :type: Unit
    :value: 'aS'

.. py:data:: aW_1
    :type: Unit
    :value: 'aW-1'

.. py:data:: gemu
    :type: Unit
    :value: 'gemʊ'

.. py:data:: mho
    :type: Unit
    :value: 'mho'

.. py:data:: statmho
    :type: Unit
    :value: 'statmho'

.. py:data:: aH
    :type: Unit
    :value: 'aH'

.. py:data:: statH
    :type: Unit
    :value: 'statH'

.. py:data:: au_ep
    :type: Unit
    :value: 'au_ep'

.. py:data:: aV
    :type: Unit
    :value: 'aV'

.. py:data:: statV
    :type: Unit
    :value: 'statV'

.. py:data:: V_mean
    :type: Unit
    :value: 'V_mean'

.. py:data:: V_US
    :type: Unit
    :value: 'V_US'

.. py:data:: a_ohm
    :type: Unit
    :value: 'aΩ'

.. py:data:: S_ohm
    :type: Unit
    :value: 'SΩ'

.. py:data:: statohm
    :type: Unit
    :value: 'statohm'

.. py:data:: au_energy
    :type: Unit
    :value: 'au_energy'

.. py:data:: bboe
    :type: Unit
    :value: 'bboe'

.. py:data:: BeV
    :type: Unit
    :value: 'BeV'

.. py:data:: Btu_ISO
    :type: Unit
    :value: 'Btu_ISO'

.. py:data:: Btu_IT
    :type: Unit
    :value: 'Btu_IT'

.. py:data:: Btu_mean
    :type: Unit
    :value: 'Btu_mean'

.. py:data:: Btu_therm
    :type: Unit
    :value: 'Btu_therm'

.. py:data:: cal_15
    :type: Unit
    :value: 'cal_15'

.. py:data:: cal_4
    :type: Unit
    :value: 'cal_4'

.. py:data:: Cal
    :type: Unit
    :value: 'Cal'

.. py:data:: kcal
    :type: Unit
    :value: 'kcal'

.. py:data:: cal_IT
    :type: Unit
    :value: 'cal_IT'

.. py:data:: cal_mean
    :type: Unit
    :value: 'cal_mean'

.. py:data:: cal_therm
    :type: Unit
    :value: 'cal_therm'

.. py:data:: Chu
    :type: Unit
    :value: 'Chu'

.. py:data:: eV
    :type: Unit
    :value: 'eV'

.. py:data:: erg
    :type: Unit
    :value: 'erg'

.. py:data:: Eh
    :type: Unit
    :value: 'Eh'

.. py:data:: au_force
    :type: Unit
    :value: 'au_force'

.. py:data:: crinal
    :type: Unit
    :value: 'crinal'

.. py:data:: dyn
    :type: Unit
    :value: 'dyn'

.. py:data:: gf
    :type: Unit
    :value: 'gf'

.. py:data:: kgf
    :type: Unit
    :value: 'kgf'

.. py:data:: kgp
    :type: Unit
    :value: 'kgp'

.. py:data:: grf
    :type: Unit
    :value: 'grf'

.. py:data:: kp
    :type: Unit
    :value: 'kp'

.. py:data:: kipf
    :type: Unit
    :value: 'kipf'

.. py:data:: lbf
    :type: Unit
    :value: 'lbf'

.. py:data:: pdl
    :type: Unit
    :value: 'pdl'

.. py:data:: slugf
    :type: Unit
    :value: 'slugf'

.. py:data:: tf_long
    :type: Unit
    :value: 'tf_long'

.. py:data:: tf_metric
    :type: Unit
    :value: 'tf_metric'

.. py:data:: tf_short
    :type: Unit
    :value: 'tf_short'

.. py:data:: ozf
    :type: Unit
    :value: 'ozf'

.. py:data:: au_ec
    :type: Unit
    :value: 'au_ec'

.. py:data:: abA
    :type: Unit
    :value: 'abA'

.. py:data:: Bi
    :type: Unit
    :value: 'Bi'

.. py:data:: edison
    :type: Unit
    :value: 'edison'

.. py:data:: statA
    :type: Unit
    :value: 'statA'

.. py:data:: gilbert
    :type: Unit
    :value: 'gilbert'

.. py:data:: pragilbert
    :type: Unit
    :value: 'pragilbert'

.. py:data:: cps
    :type: Unit
    :value: 'cps'

.. py:data:: Kt
    :type: Unit
    :value: 'Kt'

.. py:data:: ppb
    :type: Unit
    :value: 'ppb'

.. py:data:: pph
    :type: Unit
    :value: 'pph'

.. py:data:: pphm
    :type: Unit
    :value: 'pphm'

.. py:data:: ppht
    :type: Unit
    :value: 'ppht'

.. py:data:: ppm
    :type: Unit
    :value: 'ppm'

.. py:data:: ppq
    :type: Unit
    :value: 'ppq'

.. py:data:: ppt_tera
    :type: Unit
    :value: 'ppt_tera'

.. py:data:: ppt
    :type: Unit
    :value: 'ppt'

.. py:data:: Ci
    :type: Unit
    :value: 'Ci'

.. py:data:: sp
    :type: Unit
    :value: 'sp'

.. py:data:: gy
    :type: Unit
    :value: 'gy'

.. py:data:: lbm
    :type: Unit
    :value: 'lbm'

.. py:data:: ohm_mechanical
    :type: Unit
    :value: 'Ω_mechanical'

.. py:data:: perm_0C
    :type: Unit
    :value: 'perm_0C'

.. py:data:: perm_23C
    :type: Unit
    :value: 'perm_23C'

.. py:data:: permin_0C
    :type: Unit
    :value: 'permin_0C'

.. py:data:: permin_23C
    :type: Unit
    :value: 'permin_23C'

.. py:data:: permmil_0C
    :type: Unit
    :value: 'permmil_0C'

.. py:data:: permmil_23C
    :type: Unit
    :value: 'permmil_23C'

.. py:data:: brewster
    :type: Unit
    :value: 'brewster'

.. py:data:: aF
    :type: Unit
    :value: 'aF'

.. py:data:: jar
    :type: Unit
    :value: 'jar'

.. py:data:: statF
    :type: Unit
    :value: 'statF'

.. py:data:: P
    :type: Unit
    :value: 'P'

.. py:data:: Pl
    :type: Unit
    :value: 'Pl'

.. py:data:: reyn
    :type: Unit
    :value: 'reyn'

.. py:data:: clo
    :type: Unit
    :value: 'clo'

.. py:data:: RSI
    :type: Unit
    :value: 'RSI'

.. py:data:: tog
    :type: Unit
    :value: 'tog'

.. py:data:: Bz
    :type: Unit
    :value: 'Bz'

.. py:data:: kn_noeud
    :type: Unit
    :value: 'kn_noeud'

.. py:data:: knot_noeud
    :type: Unit
    :value: 'knot_noeud'

.. py:data:: mpy
    :type: Unit
    :value: 'mpy'

.. py:data:: kn
    :type: Unit
    :value: 'kn'

.. py:data:: knot
    :type: Unit
    :value: 'knot'

.. py:data:: c_light
    :type: Unit
    :value: 'c_light'

.. py:data:: dioptre
    :type: Unit
    :value: 'dioptre'

.. py:data:: mayer
    :type: Unit
    :value: 'mayer'

.. py:data:: helmholtz
    :type: Unit
    :value: 'helmholtz'

.. py:data:: mired
    :type: Unit
    :value: 'mired'

.. py:data:: cumec
    :type: Unit
    :value: 'cumec'

.. py:data:: gph_UK
    :type: Unit
    :value: 'gph_UK'

.. py:data:: gpm_UK
    :type: Unit
    :value: 'gpm_UK'

.. py:data:: gps_UK
    :type: Unit
    :value: 'gps_UK'

.. py:data:: lusec
    :type: Unit
    :value: 'lusec'

.. py:data:: CO
    :type: Unit
    :value: 'CO'

.. py:data:: gph
    :type: Unit
    :value: 'gph'

.. py:data:: gpm
    :type: Unit
    :value: 'gpm'

.. py:data:: gps
    :type: Unit
    :value: 'gps'

.. py:data:: G
    :type: Unit
    :value: 'G'

.. py:data:: rps
    :type: Unit
    :value: 'rps'

.. py:data:: den
    :type: Unit
    :value: 'den'

.. py:data:: denier
    :type: Unit
    :value: 'denier'

.. py:data:: te
    :type: Unit
    :value: 'te'

.. py:data:: au_lm
    :type: Unit
    :value: 'au_lm'

.. py:data:: c_power
    :type: Unit
    :value: 'c_power'

.. py:data:: asb
    :type: Unit
    :value: 'asb'

.. py:data:: nit
    :type: Unit
    :value: 'nit'

.. py:data:: sb
    :type: Unit
    :value: 'sb'

.. py:data:: oe
    :type: Unit
    :value: 'oe'

.. py:data:: praoersted
    :type: Unit
    :value: 'praoersted'

.. py:data:: au_mdm
    :type: Unit
    :value: 'au_mdm'

.. py:data:: Gal
    :type: Unit
    :value: 'Gal'

.. py:data:: leo
    :type: Unit
    :value: 'leo'

.. py:data:: gn
    :type: Unit
    :value: 'gn'

.. py:data:: ohm_acoustic
    :type: Unit
    :value: 'Ω_acoustic'

.. py:data:: ohm_SI
    :type: Unit
    :value: 'Ω_SI'

.. py:data:: rayl_cgs
    :type: Unit
    :value: 'rayl_cgs'

.. py:data:: rayl_MKSA
    :type: Unit
    :value: 'rayl_MKSA'

.. py:data:: Na
    :type: Unit
    :value: 'Na'

.. py:data:: au_action
    :type: Unit
    :value: 'au_action'

.. py:data:: au_am
    :type: Unit
    :value: 'au_am'

.. py:data:: planck
    :type: Unit
    :value: 'planck'

.. py:data:: rpm
    :type: Unit
    :value: 'rpm'

.. py:data:: au_cd
    :type: Unit
    :value: 'au_cd'

.. py:data:: Ah
    :type: Unit
    :value: 'Ah'

.. py:data:: F_12C
    :type: Unit
    :value: 'F_12C'

.. py:data:: F_chemical
    :type: Unit
    :value: 'F_chemical'

.. py:data:: F_physical
    :type: Unit
    :value: 'F_physical'

.. py:data:: roc
    :type: Unit
    :value: 'roc'

.. py:data:: rom
    :type: Unit
    :value: 'rom'

.. py:data:: au_eqm
    :type: Unit
    :value: 'au_eqm'

.. py:data:: au_edm
    :type: Unit
    :value: 'au_edm'

.. py:data:: au_efs
    :type: Unit
    :value: 'au_efs'

.. py:data:: Jy
    :type: Unit
    :value: 'Jy'

.. py:data:: MGOe
    :type: Unit
    :value: 'MGOe'

.. py:data:: Ly
    :type: Unit
    :value: 'Ly'

.. py:data:: ly_langley
    :type: Unit
    :value: 'ly_langley'

.. py:data:: ue
    :type: Unit
    :value: 'ue'

.. py:data:: eu
    :type: Unit
    :value: 'eu'

.. py:data:: UI
    :type: Unit
    :value: 'UI'

.. py:data:: IU
    :type: Unit
    :value: 'IU'

.. py:data:: ph
    :type: Unit
    :value: 'ph'

.. py:data:: cSt
    :type: Unit
    :value: 'cSt'

.. py:data:: St
    :type: Unit
    :value: 'St'

.. py:data:: fps
    :type: Unit
    :value: 'fps'

.. py:data:: fpm
    :type: Unit
    :value: 'fpm'

.. py:data:: fph
    :type: Unit
    :value: 'fph'

.. py:data:: ips
    :type: Unit
    :value: 'ips'

.. py:data:: mph
    :type: Unit
    :value: 'mph'

.. py:data:: cfm
    :type: Unit
    :value: 'cfm'

.. py:data:: cfs
    :type: Unit
    :value: 'cfs'

.. py:data:: deg_R
    :type: Unit
    :value: '°R'

.. py:data:: deg_F
    :type: Unit
    :value: '°F'

.. py:data:: ft_survey
    :type: Unit
    :value: 'ft_survey'


Unit Prefixes
_____________

Units an all be prefixed  with the folling:

  * yotta: `'Y'`
  * zetta: `'Z'`
  * exa: `'E'`
  * peta: `'P'`
  * tera: `'T'`
  * giga: `'G'`
  * mega: `'M'`
  * kilo: `'k'`
  * hecto: `'h'`
  * deka: `'da'`
  * deci: `'d'`
  * centi: `'c'`
  * milli: `'m'`
  * micro: `'µ'`
  * nano: `'n'`
  * pico: `'p'`
  * femto: `'f'`
  * atto: `'a'`
  * zepto: `'z'`
  * yocto: `'y'`

For example. There is no definition for the unit centimeter,
however we have the SI base unit meter `'m'` and we have the prefix
centi `'c'`. Bring bring them together and you get `'cm'` centimeter.
'''

import sys


mol = None
cd = None
kg = None
m = None
s = None
A = None
K = None
bit = None
dB = None
Hz = None
N = None
Pa = None
J = None
W = None
C = None
V = None
F = None
ohm = None
S = None
Wb = None
T = None
H = None
lm = None
lx = None
Bq = None
Gy = None
Sv = None
kat = None
r = None
sr = None
au_length = None
am = None
angstrom = None
ft = None
yd = None
mi = None
inch = None
micron = None
arcmin = None
AU = None
UA = None
au = None
agate = None
aln = None
bcorn = None
a0 = None
rBohr = None
bolt = None
bl = None
line_UK = None
line = None
cable_int = None
cable_UK = None
cable = None
caliber = None
ch_engineer = None
ch_gunter = None
ch_ramsden = None
ch_surveyor = None
cbt = None
didotpoint = None
digit = None
re = None
Ec = None
eel_scottish = None
eel_flemish = None
eel_french = None
eel_polish = None
eel_danish = None
eel_swedish = None
eel_german = None
EM_pica = None
Em = None
fath = None
fm = None
f = None
finer = None
fb = None
fod = None
fbf = None
fur = None
pleth = None
std = None
hand = None
hiMetric = None
hl = None
hvat = None
ly = None
li = None
LD = None
mil = None
Mym = None
nail = None
NL = None
NM = None
pace = None
palm = None
pc = None
perch = None
p = None
PX = None
pl = None
pole = None
ru = None
rem = None
rd = None
actus = None
rope = None
sir = None
span = None
twip = None
vr = None
vst = None
xu = None
zoll = None
bicron = None
D = None
ac = None
acre = None
are = None
b = None
cirin = None
cirmil = None
Mg_dutch = None
Mg_prussian = None
Mg_southafrica = None
quarter_sq_mi_stat = None
quarter_ac = None
rood = None
sqmi = None
sq_mi_stat = None
outhouse = None
shed = None
sqch_engineer = None
sqch_gunter = None
acre_ft = None
bag = None
bbl_UScranb = None
bbl = None
bbl_USpetrol = None
bbl_UK = None
FBM = None
bouteille = None
bk_UK = None
bu_UK = None
bu_US = None
bt_UK = None
chal_UK = None
cc = None
# noinspection PyPep8
l = None  # NOQA
L = None
gal = None
gal_UK = None
qt = None
qt_UK = None
pt = None
pt_UK = None
floz = None
floz_UK = None
cran = None
dr = None
st = None
gi = None
gi_UK = None
cup = None
cup_UK = None
dstspn = None
dstspn_UK = None
tbsp = None
tbsp_UK = None
tsp = None
tsp_UK = None
M0 = None
me = None
u_dalton = None
u = None
uma = None
Da = None
dr_troy = None
dr_apoth = None
dr_avdp = None
g = None
lb = None
oz = None
t_long = None
t_short = None
t = None
dwt = None
kip = None
gr = None
slug = None
t_assay = None
Da_12C = None
Da_16O = None
Da_1H = None
avogram = None
bag_UK = None
ct = None
ct_troy = None
cH = None
cwt = None
au_time = None
blink = None
d = None
d_sidereal = None
fortnight = None
h = None
# noinspection PyShadowingBuiltins
min = None
mo = None
mo_sidereal = None
mo_mean = None
mo_synodic = None
shake = None
week = None
wink = None
a_astr = None
a = None
y = None
a_sidereal = None
a_mean = None
a_tropical = None
bd = None
bi = None
c_int = None
c = None
carcel = None
HK = None
violle = None
entities = None
SCF = None
SCM = None
arcsecond = None
arcminute = None
pid = None
degree = None
gon = None
grade = None
ah = None
percent = None
rev = None
sign = None
B = None
Gib = None
GiB = None
Gb = None
GB = None
Kib = None
KiB = None
Kb = None
KB = None
Mib = None
MiB = None
Mb = None
MB = None
Tib = None
TiB = None
Tb = None
TB = None
aW = None

hp = None
mhp = None
bhp = None
ehp = None
whp = None
dbhp = None
hp_gb = None
cv = None
pk = None
ch = None
hk = None
PS = None
KM = None
ks = None
hv = None
hj = None
LE = None
KS = None
KC = None
Nc = None
Kc = None
CP = None
prony = None

at = None
atm = None
bar = None
Ba = None
p_P = None
cgs = None
torr = None
pz = None
Hg = None
H2O = None
Aq = None
O2 = None
ksi = None
psi = None
psf = None
osi = None
kerma = None
Mrd = None
rad = None
B_power = None
B_voltage = None
dB_power = None
dB_voltage = None
au_mf = None
Gs = None
M = None
au_charge = None
aC = None
esc = None
esu = None
Fr = None
statC = None
aS = None
aW_1 = None
gemu = None
mho = None
statmho = None
aH = None
statH = None
au_ep = None
aV = None
statV = None
V_mean = None
V_US = None
a_ohm = None
S_ohm = None
statohm = None
au_energy = None
bboe = None
BeV = None
Btu_ISO = None
Btu_IT = None
Btu_mean = None
Btu_therm = None
cal_15 = None
cal_4 = None
Cal = None
kcal = None
cal_IT = None
cal_mean = None
cal_therm = None
Chu = None
eV = None
erg = None
Eh = None
au_force = None
crinal = None
dyn = None
gf = None
kgf = None
kgp = None
grf = None
kp = None
kipf = None
lbf = None
pdl = None
slugf = None
tf_long = None
tf_metric = None
tf_short = None
ozf = None
au_ec = None
abA = None
Bi = None
edison = None
statA = None
gilbert = None
pragilbert = None
cps = None
Kt = None
ppb = None
pph = None
pphm = None
ppht = None
ppm = None
ppq = None
ppt_tera = None
ppt = None
Ci = None
sp = None
gy = None
lbm = None
ohm_mechanical = None
perm_0C = None
perm_23C = None
permin_0C = None
permin_23C = None
permmil_0C = None
permmil_23C = None
brewster = None
aF = None
jar = None
statF = None
P = None
Pl = None
reyn = None
clo = None
RSI = None
tog = None
Bz = None
kn_noeud = None
knot_noeud = None
mpy = None
kn = None
knot = None
c_light = None
dioptre = None
mayer = None
helmholtz = None
mired = None
cumec = None
gph_UK = None
gpm_UK = None
gps_UK = None
lusec = None
CO = None
gph = None
gpm = None
gps = None
G = None
rps = None
den = None
denier = None
te = None
au_lm = None
c_power = None
asb = None
nit = None
sb = None
oe = None
praoersted = None
au_mdm = None
Gal = None
leo = None
gn = None
ohm_acoustic = None
ohm_SI = None
rayl_cgs = None
rayl_MKSA = None
Na = None
au_action = None
au_am = None
planck = None
rpm = None
au_cd = None
Ah = None
F_12C = None
F_chemical = None
F_physical = None
roc = None
rom = None
au_eqm = None
au_edm = None
au_efs = None
Jy = None
MGOe = None
Ly = None
ly_langley = None
ue = None
eu = None
UI = None
IU = None
ph = None
cSt = None
St = None
fps = None
fpm = None
fph = None
ips = None
mph = None
cfm = None
cfs = None
bicrons = None
ft_survey = None

deg_R = None
deg_C = None
deg_F = None


class __UnitsModule(object):

    def __init__(self):
        mod = sys.modules[__name__]

        self.__name__ = mod.__name__
        self.__doc__ = mod.__doc__
        self.__package__ = mod.__package__
        self.__loader__ = mod.__loader__
        self.__spec__ = mod.__spec__
        self.__file__ = mod.__file__
        self.__original_module__ = mod
        # noinspection PyTypeChecker
        sys.modules[__name__] = self

    def __getattr__(self, item):
        if hasattr(self.__original_module__, item):
            return getattr(self.__original_module__, item)()

        if item in self.__dict__:
            return self.__dict__[item]

        from .unit import Unit
        return Unit(item)

    def __setattr__(self, key, value):
        if key.startswith('__'):
            object.__setattr__(self, key, value)

        else:
            setattr(self.__original_module__, key, value)


__units_module = __UnitsModule()
