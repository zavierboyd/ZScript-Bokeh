import zscript as zs
from zgraph import *
from bokeh.io import curdoc

program5 = '''
index := 1900
a := 0.0225
dt := 1
rf2015mask := -0.75
b := -0.3
tempresponsetime := 20
x := 1 / dt
climatesensitivity2x := 3
pco2 := 290
temptra := 0
tempeq := 0
rfscaledmask := 0
rfco2 := 0

rfmask = rfscaledmask * (rfscaledmask > rf2015mask) + rf2015mask * (rfscaledmask <= rf2015mask)
rftotal = rfmask + rfco2
climatesensitivity = climatesensitivity2x / 4
tempeq = climatesensitivity * rftotal
dtemptra = ((tempeq - temptra) / tempresponsetime) * x

rfscaledmask_+ = b * (pco2_+ - pco2) / 1
temptra_+ = dtemptra + temptra
pco2_+ = 280 + (pco2 - 280) * (1 + a * dt)
rfco2_+ = 4 * ln ( pco2 / 280 ) / ln ( 2 )

trace temptra
trace tempeq
trace pco2
trace rftotal
trace rfco2
trace rfmask
graph temptra
graph rftotal
graph pco2
'''

env = zs.Env()
zs.compilerun(program5, env)
data2015 = zs.compilerun('next 115', env)[0]
env2015 = repr(env).splitlines()  # snapshot of env
for line in range(len(env2015)):  # change code lines
    if 'rfmask =' in env2015[line]:
        env2015[line] = 'rfmask := rfscaledmask * (rfscaledmask > rf2015mask) + rf2015mask * (rfscaledmask <= rf2015mask); min := rfmask/10; rfmask_+ = (rfmask - min)*(rfmask > 0);'
    if 'pco2_+ =' in env2015[line]:
        env2015[line] = 'pco2_+ = pco2 + (340 - pco2) * (0.01 * dt)'
else:
    env2015 = '\n'.join(env2015)

datahuman2100 = zs.compilerun('next 85', env)[0]
env = zs.Env()
zs.compilerun(env2015, env)
dataplant2100 = zs.compilerun('next 85', env)[0]
data2015 = complexprotect(data2015)
dataplant2100 = complexprotect(dataplant2100)
datahuman2100 = complexprotect(datahuman2100)
fig1 = Figure(title='Temperature')
fig1.line('index', 'temptra', source=data2015)
fig1.line('index', 'temptra', source=datahuman2100)
fig1.line('index', 'temptra', source=dataplant2100, line_color='green')

fig2 = Figure(title='Radiative Forcings')
fig2.line('index', 'rftotal', source=datahuman2100)
fig2.line('index', 'rfmask', source=data2015)
fig2.line('index', 'rftotal', source=data2015)
fig2.line('index', 'rfmask', source=dataplant2100, line_color='green')
fig2.line('index', 'rftotal', source=dataplant2100, line_color='green')

fig3 = Figure(title='CO2 Concentration')
fig3.line('index', 'pco2', source=data2015)
fig3.line('index', 'pco2', source=datahuman2100)
fig3.line('index', 'pco2', source=dataplant2100, line_color='green')

curdoc().add_root(fig1)
curdoc().add_root(fig2)
curdoc().add_root(fig3)
curdoc().add_root(PreText(text=repr(env)))