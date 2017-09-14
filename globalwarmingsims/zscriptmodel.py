constants = '''
;; Time ;;
dt := 3*24*60*60
t := 0
t_+ = dt + t
dtyears = dt/(365*24*60*60) ;; years
tyears = t/(365*24*60*60) ;; years


;; Conversion Calculations ;; Values from: https://spacemath.gsfc.nasa.gov/books.html# -> Earth Math (2009) and Wikipedia
Ma := 5.1e6 ;; gigatons ;; total mass of atmosphere
Mola := 28.97 ;; grams/AMU ;; 1 mole of atmosphere

Molco2 := 44.009 ;; grams/AMU ;; mole
MtoCco2 := (1e6/Ma) * (Mola/Molco2) ;; gton -> ppmv

Molch4 := 16.043 ;; grams/AMU ;; mole
MtoCch4 := (1e9/Ma) * (Mola/Molch4) ;; gton -> ppbv

Moln2o := 46.005 ;; grams/AMU ;; mole
MtoCn2o := (1e9/Ma) * (Mola/Moln2o) ;; gton -> ppbv

;; Starting Concentrations ;; Values from: Recent Greenhouse Gas Concentrations, DOI: 10.3334/CDIAC/atg.032
Cco2 := 399.5 ;; ppmv
Cch4 := 1834 ;; ppbv
Cn2o := 328 ;; ppbv

;; Formula from: Myhrvold and Caldeira (2012) Supporting Information
Gbase = ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 = 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)

;; Ocean Calculations ;; Values from: Myhrvold and Caldeira (2012) Supporting Information ... pg.13 and Testing best values
layers := 60 ;; number of layers
layerdepth := 2000/layers ;; meters
k := 1e-4 ;; m^2/s
lambda := 1.25 ;; W/m^2 K
;; surface index
surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] ;; 60 layers

Srcco2 := 0 ;; gigatons
Srcch4 := 0 ;; gigatons ;; ch4 source
Srcn2o := 0 ;; gigatons ;; n2o source

;; Ocean Calculations ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
ocean := 1..layers * 0
ocean_+ = ocean + dTemp * dt

Cheat := layerdepth * 4.2*1000^2 ;; K m^2/J ;; Heat Capacity

dTempocean = (diff2 ocean) * k / layerdepth^2
dTemp = dTempocean + dTempsurfacerf * surface
dTempsurfacerf = (Frel - Tempsurface * lambda)/Cheat
Tempsurface = ocean . surface


Frel = Fco2rel + Fch4rel + Fn2orel


Mco2a := 0 ;; gigatons above current levels
Mco2a_+ = Mco2a + (dMco2a + dMco2-ch4)*dtyears
dMco2-ch4 = (Sinkch4 - Srcch4)*molco2/molch4
dMco2a = Srcco2 - dMa-oco2

tc := 1/50 ;; time constant for ocean uptake
dMa-oco2 = (Pco2a - Pco2o)*tc

Ra = 0.458 ;; atmosphere reservoir
Pco2a = Mco2a/Ra

;; ocean co2 content
Ro = 0.542 ;; ocean reservoir
Mco2o := 0
Mco2o_+ = Mco2o + (dMa-oco2 - Dco2) * dtyears
Pco2o = Mco2o/Ro
;; deep ocean sequestration
Dco2 = 0.005 * (Mco2o if Mco2o > 0 else 0)

Mch4 := 0 ;; gigatons above current levels
dMch4 = Srcch4 - Sinkch4
Mch4_+ = Mch4 + dMch4 * dtyears
Sinkch4 = Mch4/12.5 ;; gigatons ;; ch4 sink

Mn2o := 0 ;; gigatons above current levels
dMn2o = Srcn2o - Sinkn2o
Mn2o_+ = Mn2o + dMn2o * dtyears
Sinkn2o = Mn2o/114.1 ;; n2o sink

;; co2 Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cco2abs = Cco2 + Mco2a * MtoCco2
Gcurrent = ln (1 + 1.2*Cco2abs + 0.005*Cco2abs^2 + 1.4e-6*Cco2abs^3)
Fco2rel = 3.35(Gcurrent - Gbase)

;; ch4 Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cch4abs = Cch4 + Mch4 * MtoCch4
Fn2o0ch4 = 0.47*ln (1 + 2.01e-5*(Cch4abs * Cn2o)^0.75 + 5.31e-15*Cch4abs*(Cch4abs * Cn2o)^1.52)
Fch4rel = 0.036(Cch4abs^0.5 - Cch4^0.5) - Fn2o0ch4 + Fn2o0ch40

;; n2o Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cn2oabs = Cn2o + Mn2o * MtoCn2o
Fn2och40 = 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2oabs)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2oabs)^1.52)
Fn2orel = 0.12(Cn2oabs^0.5 - Cn2o^0.5) - Fn2och40 + Fn2o0ch40

trace Cch4abs
trace Cco2abs
trace Cn2oabs
trace Cch4
trace Cco2
trace Cn2o
trace Mch4
trace Mco2a
trace Mn2o
trace Srcco2
trace Srcch4
trace Srcn2o
trace Tempsurface
trace Fco2rel
trace Fch4rel
trace Fn2orel
trace Frel
trace tyears
'''

resets = '''
Cco2 := 399.5 ;; ppmv
Cch4 := 1834 ;; ppbv
Cn2o := 328 ;; ppbv
layers := 60 ;; number of layers
surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] ;; 60 layers
Srcco2 := 0 ;; gigatons
Srcch4 := 0 ;; gigatons ;; ch4 source
Srcn2o := 0 ;; gigatons ;; n2o source
ocean := 1..layers * 0
Mco2a := 0 ;; gigatons above current levels
Mco2o := 0
Mch4 := 0 ;; gigatons above current levels
Mn2o := 0 ;; gigatons above current levels
'''