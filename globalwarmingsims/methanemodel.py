import zscript as zs
from zgraph import *
from bokeh.io import curdoc

methanemodel = '''
;; ZScript Methane.zs

;; initialization ;;
index := -100

spike-duration := 10
spike-duration := spike-duration if 1.1 < spike-duration else 1.1
spike-gton := 40
source-chronic := 0.2

time := -101
;; lifetime-0 := 7.5
gton-0 := 1.6
source-natural := 0.26  ;; gton-0 / lifetime-0
lifetime-0 := gton-0 / source-natural
age-exp := 0.26
CH4-RFK := 0.5 * 1.4

CH4-gton := gton-0
source-spike := spike-gton / spike-duration
pCO2 := 280.0
CO2-tau := 0.0065
CO2-RFK := 3.4
CH4-gton := 1.0e-3

;; definitions
CH4-src = source-natural + (source-chronic if time > -50 else 0) + (source-spike if time > 0 and time < spike-duration else 0)
lifetime = lifetime-0 * ( CH4-gton / gton-0 )^age-exp
CH4-sink = CH4-gton / lifetime
CH4-RF = -1.0569 * ( (ln (0.8)) - (ln (CH4-gton/2)) ) - 0.16019 * ( (ln (0.8))^2 - (ln (CH4-gton/2))^2 ) * 1.4
CO2-RF = -2.6222 * ( (ln (280.0)) - (ln (pCO2)) ) - 0.2960 * ( (ln (280.0))^2 - (ln (pCO2))^2 )
co2-rf0 := -2.6222 * ( (ln (280.0)) - (ln (pCO2)) ) - 0.2960 * ( (ln (280.0))^2 - (ln (pCO2))^2 )
dco2-rf = co2-rf - co2-rf0
CH4-gton2 = CH4-gton/2

;; loop
time_+ = time + 1.0
pCO2_+ = pCO2+(0.12909982174688056 if index > 0 else 0);;*(1 + (CO2-tau if time > -50 else 0))
CH4-gton_+ = CH4-gton + CH4-src - CH4-sink

trace CH4-gton2
trace CH4-RF
trace CH4-src
trace CO2-RF
trace pCO2
trace dco2-rf
trace CH4-sink
trace CH4-src
trace lifetime

next 200
'''

env = zs.Env()
data = zs.compilerun(methanemodel, env)[-1]
data = complexprotect(data)
fig1 = Figure(title='Methane Budget')
fig1.line('index', 'ch4-src', source=data)
fig1.line('index', 'ch4-sink', source=data)

fig2 = Figure(title='Radiative Forcings')
fig2.line('index', 'ch4-rf', source=data)
fig2.line('index', 'co2-rf', source=data)

fig3 = Figure(title='Methane Lifetime')
fig3.line('index', 'lifetime', source=data)

fig4 = Figure(title='Methane Concentration')
fig4.line('index', 'ch4-gton2', source=data)
fig4.line('index', 'pco2', source=data, color='red')

curdoc().add_root(fig1)
curdoc().add_root(fig2)
curdoc().add_root(fig3)
curdoc().add_root(fig4)
curdoc().add_root(PreText(text=repr(env)))