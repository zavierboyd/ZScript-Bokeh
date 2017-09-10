import zscript as zs
from zgraph import *
from bokeh.io import curdoc

program2 = '''
m1 := (75/(265 - 215) + 60/(255 - 215) + 45/(245 - 215) + 30/(235 - 215) + 15/(225 - 215))/5
b1 := 0 - m1 * 215
m2 := ((0.15 - 0.65)/(265 - 215) + (0.25 - 0.65)/(255 - 215) + (0.35 - 0.65)/(245 - 215) + (0.45 - 0.65)/(235 - 215) + (0.55 - 0.65)/(225 - 215)) / 5
b2 := 0.65 - m2 * 215
T := 215
L := 1200
sigma = 5.67e-8
epsilon = 1

ice-latitude = m1 * T + b1
a = m2 * T + b2
albedo = (a <= 0.65) * (a >= 0.15) * a + (a > 0.65) * 0.65 + (a < 0.15) * 0.15

T_+ = (L(1 - albedo)/(sigma(epsilon)4))^0.25

trace T
trace L
next 300
'''

env = zs.Env()
out = zs.compilerun(program2, env)[0]
out = complexprotect(out)
fig1 = Figure()
fig2 = Figure()
fig1.line('index', 't', source=out)
T = [out['t'][-1]]
l = [1200] + list(range(1210, 1601, 10)) + list(range(1590, 1199, -10))

for L in range(1210, 1601, 10):
    zs.compilerun('L := ' + str(L), env)
    out = zs.compilerun('index := 0 ;next 300', env)[0]
    out = complexprotect(out)
    T.append(out['t'][-1])
    fig1.line('index', 't', source=out)

for L in range(1590, 1199, -10):
    zs.compilerun('L := ' + str(L), env)
    out = zs.compilerun('index := 0 ;next 300', env)[0]
    out = complexprotect(out)
    T.append(out['t'][-1])
    fig1.line('index', 't', source=out)

fig2.line('l', 't', source=dict(t=T, l=l))
curdoc().add_root(fig1)
curdoc().add_root(fig2)
curdoc().add_root(PreText(text=repr(env)))