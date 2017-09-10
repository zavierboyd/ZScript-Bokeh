import zscript as zs
from zgraph import *
from bokeh.io import curdoc


testsim = '''
;; Ocean ;;
layers := 30 ;; number of layers, its a test
layerdepth := 4000/layers ;; 4000 meters ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
k := 1e-4 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
dt := 365*24*60*60 ;; seconds -> 1 day
dyears := dt/(365*24*60*60)
tyears := 0
tyears_+ = tyears + dyears
density := 1e+3
heatcapacity := 4.2 * 1e+3
lambda := 1.25 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
oceanfraction := 0.71 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
ocean := 1..layers * 0
ocean_+ = ocean + totaldiff

surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
oceandiff = (diff2 ocean) * k * dt / layerdepth^2
totaldiff = oceandiff + surfacediff
surfacediff = (rfmap - surface0 * lambda) * layerdepth/(density * k * f * heatcapacity)
surface0 = oceandiff * surface
rfmap = surface * df * dt


;; Radiative Forcing ;;
Amass := 5.1e+6 ;; gigatons
molea := 28.97 ;; grams/AMU


;;; CO2 Calculations ;;;
co2mole := 44 ;; grams/AMU
co2mass-ppmv := (1.0e6/Amass) * (molea/co2mole)
alpha := co2mass-ppmv
co2amass := 0;;280/alpha;;400/alpha
co2in := 0;;450;;co2mass*co2g - co2mass ;;280/alpha - co2mass ;; gigatons
co2dmass = co2in - co2flow
co2amass_+ = co2amass + co2dmass - co2flow

tc := dyears/50
co2flow = (co2apres - co2opres)*tc ;;0.217+0.259*e^(-t/172.9) + 0.338*e^(-t/18.51) + 0.186*e^(-t/1.186)

co2ares := 0.458
co2apres = co2amass/co2ares

co2ores := 0.542
co2omass := 0
co2omass_+ = co2omass + co2flow - co2deep
co2opres = co2omass/co2ores

co2deep = 0.005*co2omass


;;; CH4 Calculations ;;;
ch4mole := 16.043 ;; grams/AMU
ch4mass-ppbv := (1e+9/Amass) * (molea/ch4mole)
beta := ch4mass-ppbv
ch4mass := 0;;1800/beta
ch4in = (0.26 + (0.2 if tyears >= 50 else 0) + (1 if tyears >= 100 and tyears <= 110 else 0))*dyears
ch4dmass = ch4in - ch4life ;;670/beta - ch4mass ;; gigatons
ch4mass_+ = ch4mass + ch4dmass
ch4life = dyears*ch4mass/12



;;; N2O Calculations ;;;
n2omole := 46.005
n2omass-ppbv := (1e+9/Amass) * (molea/n2omole)
gamma := n2omass-ppbv
n2omass := 320/gamma
n2oin := 0;;1*dyears
n2odmass = n2oin;; - n2olife ;;266/gamma - n2omass
n2omass_+ = n2omass + n2odmass
n2olife = dyears*n2omass/114

pco2 = co2amass * alpha ;; ppmv
pn2o = n2omass * gamma ;; ppbv
pch4 = ch4mass * beta ;; ppbv

pmch4 = pch4 + beta * ch4dmass
pmn2o = pn2o + gamma * n2odmass
pmco2 = pco2 + alpha * co2dmass

fpch4pn2o = 0.47*ln (1 + 2.01e-5*(pch4 * pn2o)^0.75 + 5.31e-15*pch4*(pch4 * pn2o)^1.52)
fpch4pmn2o = 0.47*ln (1 + 2.01e-5*(pch4 * pmn2o)^0.75 + 5.31e-15*pch4*(pch4 * pmn2o)^1.52)
fpmch4pn2o = 0.47*ln (1 + 2.01e-5*(pmch4 * pn2o)^0.75 + 5.31e-15*pmch4*(pmch4 * pn2o)^1.52)

gpmco2 = ln (1 + 1.2*pmco2 + 0.005*pmco2^2 + 1.4e-6*pmco2^3)
gpco2 = ln (1 + 1.2*pco2 + 0.005*pco2^2 + 1.4e-6*pco2^3)

dfco2 = 3.35(gpmco2 - gpco2)
dfch4 = 0.036(pmch4^0.5 - pch4^0.5) - fpmch4pn2o + fpch4pn2o
dfn2o = 0.12(pmn2o^0.5 - pn2o^0.5) - fpch4pmn2o + fpch4pn2o

df = dfn2o + dfch4 + dfco2
;;df :=
f := 100
tau := k*(density * heatcapacity/lambda)^2

fch4 := 0
fch4_+ 

t := 0
t_+ = dt + t

trace ocean
trace tyears
trace fpch4pn2o
trace ch4in
trace ch4life
trace ch4mass
trace pch4
trace dfch4
next 200
'''

env = zs.Env()
data = zs.compilerun(testsim, env)[-1]
data = complexprotect(data)
fig1 = Figure(title='Methane Budget')
fig1.line('index', 'ch4in', source=data)
fig1.line('index', 'ch4life', source=data)

fig2 = Figure(title='Methane Concentration')
fig2.line('index', 'pch4', source=data)
fig2.line('index', 'ch4mass', source=data)

fig3 = Figure(title='Methane Concentration')
fig3.line('index', 'dfch4', source=data)

curdoc().add_root(fig1)
curdoc().add_root(fig2)
curdoc().add_root(fig3)