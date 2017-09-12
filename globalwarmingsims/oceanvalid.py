import zscript as zs
from zgraph import *
from bokeh.io import curdoc


testsim = '''
;; Ocean ;;
layers := 60 ;; number of layers, its a test
layerdepth := 2000/layers ;; 4000 meters ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
k := 1e-4 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
dt := 7*24*60*60 ;; seconds -> 1 day
tyears = t/(365*24*60*60)
density := 1e3
heatcapacity := 4.2 * 1e3
lambda := 1.25 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
oceanfraction := 0.71 ;; Myhrvold and Caldeira (2012) Supporting Information ... pg.13
ocean := 1..layers * 0
ocean_+ = ocean + totaldiff

heatcap := layerdepth * 4.2*1000^2
heatcont = surfacetemp*heatcap

surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
oceandiff = (diff2 ocean) * k * dt / layerdepth^2
totaldiff = oceandiff + surfacediff * surface
surfacediff = dt*(df - surfacetemp * lambda)/heatcap
surfacetemp = ocean . surface

Temp := 0
Temp-heatcap := layerdepth * 4.2 * 1e6
Temp-heatcont = T*T-heatcap

Temp-d = dt*(1.25 - 1.25*Temp)/Temp-heatcap
Temp_+ = Temp-d + Temp


tau := k*(density * heatcapacity/lambda)^2

t := 0
t_+ = dt + t
df := 1.25

ed = 1 - e^(-(t/tau))
3tau/dt

avgtemp = ocean . (1..layers * 0 + 1)/layers

trace ocean
trace surfacediff
trace surfacetemp
trace tyears
trace temp
trace ed
trace avgtemp
next 5201
'''

env = zs.Env()
data = zs.compilerun(testsim, env)[-1]
data = complexprotect(data)

fig1 = Figure(title='TCR vs ECS', toolbar_location='above', x_axis_label='year', y_axis_label='Temperature Change')
a = fig1.line('tyears', 'surfacetemp', source=data, line_width=5, alpha=.85, color='blue', line_dash='dashed', legend='Transient Climate Response (TCR)')
b = fig1.line('tyears', 'temp', source=data, line_width=5, alpha=.85, color='red', line_dash='dotted', legend='Equivalent Climate Sensitivity (ECS)')
# fig1.line('tyears', 'avgtemp', source=data, color='purple')
# fig1.line('tyears', 'ed', source=data, color='green')
fig1.legend.location = 'bottom_right'


curdoc().add_root(fig1)

