import zscript as zs
from zgraph import *
from bokeh.io import curdoc


constants = '''
;; Radiative Forcing ;;
dt := 365*24*60*60 ;; seconds -> 1 day
dyears = dt/(365*24*60*60)
tyears = t/(365*24*60*60)
Amass := 5.1e6 ;; gigatons
molea := 28.97 ;; grams/AMU
ch4mole := 16.043 ;; grams/AMU
ch4mass-ppbv := (1e9/Amass) * (molea/ch4mole)
beta := ch4mass-ppbv
gton-0 := 720/beta ;;1.6
CH4-gton = gton-0 + index*(5.083698308595099 - gton-0)/100
pn2o := 320 ;;270 ;; ppbv
pch4 := gton-0 * beta ;; ppbv
pmch4 = ch4-gton * beta

'''

testsim = '''
;; Baseline Concentrations ;;


fpch4pn2o = 0.47*ln (1 + 2.01e-5*(pch4 * pn2o)^0.75 + 5.31e-15*pch4*(pch4 * pn2o)^1.52)
fpmch4pn2o = 0.47*ln (1 + 2.01e-5*(pmch4 * pn2o)^0.75 + 5.31e-15*pmch4*(pmch4 * pn2o)^1.52)

dfch4 = 0.036(pmch4^0.5 - pch4^0.5) - fpmch4pn2o + fpch4pn2o

t := 0
t_+ = dt + t

trace tyears
trace pmch4
trace ch4-gton
trace dfch4
next 100
'''

baseline = '''
;; calculates the radiative forcing beyond gton-0
absrf = 1.0569 * ln (CH4-gton/2) + 0.16019 * (ln (CH4-gton/2))^2;; * 1.4
baserf := 1.0569 * ln (CH4-gton/2) + 0.16019 * (ln (CH4-gton/2))^2
df = absrf - baserf
;;CH4-RF = (-1.0569 * ( (ln (0.8)) - (ln (CH4-gton/2)) ) - 0.16019 * ( (ln (0.8))^2 - (ln (CH4-gton/2))^2 ));; * 1.4
;;CH4-RF = (-1.0569 * ( (ln (0.8)) - (ln (CH4-gton/2)) ) - 0.16019 * ( (ln (0.8))^2 - (ln (CH4-gton/2))^2 )) * 1.4

trace df
trace ch4-gton
trace pmch4
next 100
'''

data = zs.compilerun(constants+testsim, zs.Env())[-1]
data = complexprotect(data)
env1750 = zs.Env()
data1750 = zs.compilerun(constants+baseline, env1750)[-1]
data1750 = complexprotect(data1750)

fig = Figure(title='Radiative Forcing')
fig.line('tyears', 'dfch4', source=data)
# fig.line('index', 'ch4-rf', source=data1750, color='green')
fig.line('index', 'df', source=data1750, color='red')


curdoc().add_root(fig)

env = zs.Env()
zs.compilerun(constants, env)
zs.repl(env1750)