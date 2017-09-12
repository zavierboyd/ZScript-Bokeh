import zscript as zs
from zgraph import *
from bokeh.io import curdoc



#################
#### Time Constants make stuff weird
#### Split the Models so that Delta Time does not affect each other
#################

spike = '''
;; spike constants ;;
spike-duration := 10
spike-duration := spike-duration if 1.1 < spike-duration else 1.1
spike-gton := 10
source-chronic := 0.2
source-spike := spike-gton / spike-duration

'''

testsim = '''
;; Constants ;;
dt := 365*24*60*60 ;; seconds -> 1 day
dyears = dt/(365*24*60*60)
tyears = t/(365*24*60*60)
Amass := 5.1e6 ;; gigatons
molea := 28.97 ;; grams/AMU


;;; CH4 Calculations ;;;
ch4mole := 16.043 ;; grams/AMU
ch4mass-ppbv := (1e9/Amass) * (molea/ch4mole)
beta := ch4mass-ppbv
ch4mass := 0
ch4in = (source-spike/dyears if tyears > 100 and tyears < spike-duration + 100 else 0)
ch4dmass = ch4in - ch4life ;;670/beta - ch4mass ;; gigatons
ch4mass_+ = ch4mass + ch4dmass
ch4life = dyears*ch4mass/12

t := 0
t_+ = dt + t

trace ch4life
trace ch4mass
trace tyears
next 200
'''

base1750 = '''

gton-0 := 1.6
source-natural := 0.26  ;; gton-0 / lifetime-0
lifetime-0 := gton-0 / source-natural
age-exp := 0.26

;;CH4-gton := gton-0
CH4-gton := 1.0e-3

;; Base Line Simulation 1750 ;;
CH4-src = source-natural + (source-chronic if index > 50 else 0) + (source-spike if index > 100 and index < spike-duration + 100 else 0)
lifetime = lifetime-0 * ( CH4-gton / gton-0 )^age-exp
CH4-sink = CH4-gton / lifetime
CH4-gton_+ = CH4-gton + CH4-src - CH4-sink

trace ch4-sink
trace CH4-gton
next 200
'''

env = zs.Env()
data = zs.compilerun(spike+testsim, env)[-1]
data1750 = zs.compilerun(spike+base1750, zs.Env())[-1]
data1750 = complexprotect(data1750)
data1750['ch4-sink'] = np.array(data1750['ch4-sink']) - 0.46
data1750['ch4-gton'] = np.array(data1750['ch4-gton']) - 3.459
data = complexprotect(data)
fig2 = Figure(title='Methane Concentration')
fig2.line('tyears', 'ch4mass', source=data, line_dash='dotted')
# fig2.line('index', 'pch4-base', source=data, color='green')
fig2.line('index', 'ch4-gton', source=data1750, color='black', line_dash='dashed')

fig4 = Figure(title='Methane sink')
fig4.line('tyears', 'ch4life', source=data)
fig4.line('index', 'ch4-sink', source=data1750, color='green')


curdoc().add_root(fig2)
curdoc().add_root(fig4)

