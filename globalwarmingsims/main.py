from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput, Div, Button

from globalwarmingsims.finalsim import *
from zgraph import *
from zscript import *

env = Env(repl=True)
compilerun(simulation, env)

def textstuff():
    global output, text, env, envdiv
    print('HI I AM DOING STUFF :)')
    output.text += '>>>' + text.value + '<br/>'
    compilerun(text.value, env)
    envdiv.text = 'Env: \n'+repr(env)

    return

text = TextInput(title='Equation: ', placeholder='a := 1')
# text.on_change ## make this work

update = Button(label="Update")
update.on_click(textstuff)

envdiv = PreText(text='Env: <br/>'+repr(env))
output = Div(text='hi this is test')

curdoc().add_root(widgetbox([envdiv, text, output, update]))

nxt = zs.compilerun('next 0', env)[-1]
gen = infintick(nxt)

source = ColumnDataSource(next(gen))  # ColumnDataSource(dict(x=[], y=[], avg=[]))

fig = Figure(title='Temperature')
fig.line(source=source, x='tyears', y='tempsurface', line_width=2, alpha=.85)
curdoc().add_root(fig)

fig = Figure(title='GHG Concentrations')
fig.line(source=source, x='tyears', y='cco2abs', line_width=2, alpha=.85, color='blue')
fig.line(source=source, x='tyears', y='cch4abs', line_width=2, alpha=.85, color='green')
fig.line(source=source, x='tyears', y='cn2oabs', line_width=2, alpha=.85, color='red')
curdoc().add_root(fig)

fig = Figure(title='GHG Mass Reletive to 1750')
fig.line(source=source, x='tyears', y='mco2a', line_width=2, alpha=.85, color='blue')
fig.line(source=source, x='tyears', y='mch4', line_width=2, alpha=.85, color='green')
fig.line(source=source, x='tyears', y='mn2o', line_width=2, alpha=.85, color='red')
curdoc().add_root(fig)


# fig = Figure(title='Radiative Forcings')
# fig.line(source=source, x='tyears', y='tempsurface', line_width=2, alpha=.85)
# curdoc().add_root(fig)


def update_data():
    global gen
    [next(gen) for x in range(10)]
    new_data = next(gen)
    source.stream(new_data, 1000)
    # curdoc().add_next_tick_callback(update_data)


curdoc().add_periodic_callback(update_data, 100)
