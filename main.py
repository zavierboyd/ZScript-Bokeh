from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput, Div, Button, Select, Slider
from bokeh.io import curdoc

from globalwarmingsims.zscriptmodel import constants, resets
from zgraph import *
from copy import deepcopy
import zscript as zs

env = zs.Env(repl=True)
zs.compilerun(constants, env)

def textstuff():
    global output, text, env, envdiv
    output.text += '<br/> >>>' + text.value + '<br/>'
    out = zs.compilerun(text.value, env)
    output.text += '\n'.join([str(outbit) for outbit in out])
    output.text += '\n'.join(zs.ZWarning.currentwarnings)
    envdiv.text = 'Env: \n'+repr(env)

    return

text = TextInput(title='Equation: ', placeholder='a := 1')
# text.on_change ## make this work

def resetsim():
    global output, env, envdiv
    output.text += '<br/> >>> Concentrations and Temperature Reset! <br/>'
    zs.compilerun(resets, env)
    zs.ZWarning.clearwarnings()
    envdiv.text = 'Env: \n' + repr(env)

    return

def resetall():
    global output, env, envdiv, source, datainit
    output.text += '<br/> >>> Everything Reset! <br/>'
    zs.compilerun(constants, env)
    source.data = deepcopy(datainit)
    zs.ZWarning.clearwarnings()
    envdiv.text = 'Env: \n' + repr(env)

    return

def spike():
    global spikeamount, spikeduration, spikegas, env, output
    output.text += '<br/> >>> ' + spikegas.value + ' Spiked! <br/>'
    exc = ''
    if spikegas.value == 'Carbon Dioxide':
        exc = '''myyearco2 := tyears
        srcco2 = ''' + str(spikeamount.value) + ''' if tyears < myyearco2 + ''' + str(spikeduration.value) + ''' else 0'''
    elif spikegas.value == 'Agricultural Methane':
        exc = '''myyearch4 := tyears
                srcch4 = ''' + str(spikeamount.value) + ''' if tyears < myyearch4 + ''' + str(spikeduration.value) + '''else 0'''
    zs.compilerun(exc, env)

    return

speed = Slider(title='Simulation Speed (years per second)')
speed.start = 1.0
speed.end = 5.0
speed.step = 1.0
speed.value = 1.0

spikeduration = Slider(title='Duration of spike (years)')
spikeduration.start = 1.0
spikeduration.end = 10.0
spikeduration.step = 0.1
# spikeduration.value = 5.0

spikeamount = Slider(title='GTons of gas per year')
spikeamount.start = 0.5
spikeamount.end = 10.0
spikeamount.step = 0.1
# spikeamount.value = 1.0

spikegas = Select()
spikegas.value = 'Carbon Dioxide'
spikegas.options = ['Agricultural Methane', 'Carbon Dioxide']

spikebtn = Button(label='Spike!')
spikebtn.on_click(spike)

resetc = Button(label='Reset Concentrations and Temperature')
resetc.on_click(resetsim)

resety = Button(label='Reset Simulation')
resety.on_click(resetall)

update = Button(label="Update")
update.on_click(textstuff)

envdiv = PreText(text='Env: \n'+repr(env))
output = Div(text='hi this is test')


nxt = zs.compilerun('next 0', env)[-1]
gen = infintick(nxt)

datainit = deepcopy(next(gen))
source = ColumnDataSource(datainit)  # ColumnDataSource(dict(x=[], y=[], avg=[]))

fig = Figure(title='Temperature')
fig.line(source=source, x='tyears', y='tempsurface', line_width=2, alpha=.85)
curdoc().add_root(fig)

curdoc().add_root(widgetbox([output, text, update, resetc, resety, speed, spikeamount, spikeduration, spikegas, spikebtn]))

fig = Figure(title='GHG Mass relative to today (Gtons)')
fig.line(source=source, x='tyears', y='mco2a', line_width=2, alpha=.85, color='blue', legend='Carbon Dioxide')
fig.line(source=source, x='tyears', y='mch4', line_width=2, alpha=.85, color='green', legend='Methane')
fig.legend.location = 'top_left'
curdoc().add_root(fig)

curdoc().add_root(envdiv)

def update_data():
    global gen, speed
    [next(gen) for x in range(11*int(speed.value))]
    new_data = next(gen)
    source.stream(new_data, 1000)


curdoc().add_periodic_callback(update_data, 91)
