import zscript as zs
from zgraph import *
from bokeh.io import curdoc


testsim = '''
;; Constants ;;
dt := 365*24*60*60 ;; seconds -> 1 day
dyears := dt/(365*24*60*60)
tyears := 0
tyears_+ = tyears + dyears
Amass := 5.1e6 ;; gigatons
molea := 28.97 ;; grams/AMU


;; CO2 Concentration Calculations ;;
co2mole := 44 ;; grams/AMU
co2mass-ppmv := (1.0e6/Amass) * (molea/co2mole)
alpha := co2mass-ppmv
co2amass := 0
co2in = 10 if index == 0 else 0 ;; gigatons
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

;; CO2 RF Calculation ;;

pco2 := 400 ;; ppmv
pmco2 = pco2 + alpha

gpmco2 = ln (1 + 1.2*pmco2 + 0.005*pmco2^2 + 1.4e-6*pmco2^3)
gpco2 = ln (1 + 1.2*pco2 + 0.005*pco2^2 + 1.4e-6*pco2^3)

dfco2 = 3.35(gpmco2 - gpco2)


;; Base Line ;;
co2-tmass = 10*(0.217 + 0.259*e^(-tyears/172.9) +0.338*e^(-tyears/18.51) + 0.186*e^(-tyears/1.186))
co2-tppmv = 400 + co2-tmass * alpha


t := 0
t_+ = dt + t

co2tppmv := 400
co2tppmv_+ = co2tppmv + co2dmass * alpha

CO2-dRF = -2.6222 * ( (ln (400)) - (ln (alpha + 400)) ) - 0.2960 * ( (ln (400))^2 - (ln (alpha + 400))^2 )

trace co2-tppmv
trace co2-drf
trace dfco2
trace co2tppmv
trace pco2
next 100
'''

env = zs.Env()
data = zs.compilerun(testsim, env)[-1]
# zs.repl(env)
data = complexprotect(data)
fig4 = Figure(title='CO2 Concentration')
fig4.line('index', 'co2tppmv', source=data)
fig4.line('index', 'co2-tppmv', source=data, color='green')
fig4.line('index', 'pco2', source=data, color='red')

fig6 = Figure(title='CO2 Change in Forcing')
fig6.line('index', 'dfco2', source=data)
fig6.line('index', 'co2-drf', source=data, color='green')

curdoc().add_root(fig4)
curdoc().add_root(fig6)