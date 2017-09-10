import zscript as zs
from zgraph import *
from bokeh.io import curdoc

climatechange = '''
ts := 1
dt := ts*365*24*60*60
L := 1350
albedo := 0.3
epsilon := 1
sigma := 5.67 * 10^(-8)
waterdepth := 400
temp := 0
t := 0
heatcap := waterdepth * 4.2*1000^2
heatcont := temp*heatcap
in := L*(1 - albedo)/4

out = (temp^4)*sigma*epsilon

heatcont_+ = heatcont + (in - out)*dt
temp_+ = heatcont/heatcap + (index if index == 200 else 0)
t_+ = t + ts

trace t
trace temp
next 500
'''

# env = zs.Env()
#
# zs.compilerun(climatechange, env)
#
# zs.repl(env)
env = zs.Env()
data = zs.compilerun(climatechange, env)[-1]
fig = Figure(title='Temperature')
fig.line('t', 'temp', source=complexprotect(data))

curdoc().add_root(fig)
curdoc().add_root(PreText(text=repr(env)))