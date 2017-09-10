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
density := 1e3
heatcapacity := 4.2 * 1e3
lambda := 1.25 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
oceanfraction := 0.71 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
ocean := 1..layers * 0
ocean_+ = ocean + totaldiff

surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
oceandiff = (diff2 ocean) * k * dt / layerdepth^2
totaldiff = oceandiff + surfacediff * surface
surfacediff = (df - surfacetemp * lambda) * layerdepth/(density * k * f * heatcapacity)
surfacetemp = oceandiff . surface
rfmap = surface * df


;; Radiative Forcing ;;
Amass := 5.1e6 ;; gigatons
molea := 28.97 ;; grams/AMU


;;; CO2 Calculations ;;;
co2mole := 44 ;; grams/AMU
co2mass-ppmv := (1.0e6/Amass) * (molea/co2mole)
alpha := co2mass-ppmv
co2amass := 0
co2in = (278 - pco2)/alpha;;450;;co2mass*co2g - co2mass ;;280/alpha - co2mass ;; gigatons
co2dmass = co2in - co2flow
co2amass_+ = co2amass + co2dmass

tc := dyears/50
co2flow = (co2apres - co2opres)*tc ;;0.217+0.259*e^(-t/172.9) + 0.338*e^(-t/18.51) + 0.186*e^(-t/1.186)

co2ares := 0.458
co2apres = co2amass/co2ares

co2ores := 0.542
co2omass := 0
co2omass_+ = co2omass + co2flow - co2deep
co2opres = co2omass/co2ores

co2deep = 0.005*co2omass

;;releasetime := 10 ;; years
;;co2-tmass = 10*(e^(-0.903tyears)*((-0.221*e^(0.0598tyears) - 6.26*e^(0.894tyears) - 44.8*e^(0.897tyears) + e^(0.903tyears)*(51.3 + 0.217*tyears) + (0.222*e^(0.843*releasetime+0.0598*tyears) + 6.26*e^(0.054*releasetime+0.849*tyears) + 44.8*e^(0.00578tyears) + e^(0.903tyears)*(-51.3 + 0.217*releasetime - 0.217*tyears) if releasetime - tyears >= 0 else 0)))
;;co2-tmass = 10*(0.217 + 0.259*e^(-tyears/172.9) +0.338*e^(-tyears/18.51) + 0.186*e^(-tyears/1.186))
;;co2-tppmv = 400 + co2-tmass * alpha


;;; CH4 Calculations ;;;
ch4mole := 16.043 ;; grams/AMU
ch4mass-ppbv := (1e9/Amass) * (molea/ch4mole)
beta := ch4mass-ppbv
ch4mass := 0
ch4in = (650 - pch4) / beta
ch4dmass = ch4in - ch4life ;;670/beta - ch4mass ;; gigatons
ch4mass_+ = ch4mass + ch4dmass
ch4life = dyears*ch4mass/12
ch4life


;;; N2O Calculations ;;;
n2omole := 46.005
n2omass-ppbv := (1e9/Amass) * (molea/n2omole)
gamma := n2omass-ppbv
n2omass := 0
n2oin = (264 - pn2o)/gamma ;;1*dyears
n2odmass = n2oin - n2olife ;;266/gamma - n2omass
n2omass_+ = n2omass + n2odmass
n2olife = dyears*n2omass/114


;; Baseline Concentrations ;;
pco2 := 400 ;; ppmv
pn2o := 320 ;; ppbv
pch4 := 1800 ;; ppbv

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
co2mass-ppmv
f := 100
tau := k*(density * heatcapacity/lambda)^2

t := 0
t_+ = dt + t

ch4tppbv := 1800
ch4tppbv_+ = ch4tppbv + ch4dmass * beta
ch4trf := 0
ch4trf_+ = ch4trf + dfch4
co2tppmv := 400
co2tppmv_+ = co2tppmv + co2dmass * alpha
co2trf := 0
co2trf_+ = co2trf + dfco2

CO2-RF = -2.6222 * ( (ln (280)) - (ln (alpha * co2dmass + 280)) ) - 0.2960 * ( (ln (280.0))^2 - (ln (alpha * co2dmass + 280))^2 )
CO2-tRF := 0
co2-trf_+ = co2-trf + co2-rf


trace ocean
trace tyears
trace ch4in
trace ch4life
trace pch4
trace ch4trf
trace ch4tppbv

trace co2-trf
trace co2tppmv
trace co2trf
trace pco2
;;next 100
'''

env = zs.Env()
data = zs.compilerun(testsim, env)#[-1]
zs.repl(env)
data = complexprotect(data)
fig1 = Figure(title='Methane Budget')
fig1.line('index', 'ch4in', source=data)
fig1.line('index', 'ch4life', source=data, color='red')

fig2 = Figure(title='Methane Concentration')
fig2.line('index', 'ch4tppbv', source=data)
fig2.line('index', 'pch4', source=data, color='red')

fig3 = Figure(title='Methane Forcing from base')
fig3.line('index', 'ch4trf', source=data)

fig4 = Figure(title='CO2 Concentration')
fig4.line('index', 'co2tppmv', source=data)
# fig4.line('index', 'co2-tppmv', source=data, color='green')
fig4.line('index', 'pco2', source=data, color='red')

fig5 = Figure(title='CO2 Forcing from base')
fig5.line('index', 'co2trf', source=data)
fig5.line('index', 'co2-trf', source=data, color='red')

curdoc().add_root(fig1)
curdoc().add_root(fig2)
curdoc().add_root(fig3)
curdoc().add_root(fig4)
curdoc().add_root(fig5)