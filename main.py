from bokeh.io import curdoc, output_file
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import TextInput, Div, Button, PreText
from bokeh.layouts import widgetbox
from bokeh.plotting import Figure

import numpy as np

from zscript import *
from program import spring as p
env = Env(repl = True)
init = '''a := 1
a_ = a + 1
trace a'''
compilerun(p, env)

# env = Env()
# compilerun(init, env)
nxt = compiler('next 20')
nxt(env)
a = nxt.nextdata()


d = {'t': [], '#': []}
def textstuff():
    global output, text, env, envdiv
    output.text += '>>>' + text.value + '<br/>'
    compilerun(text.value, env)
    envdiv.text = 'Env: <br/>'+repr(env)

    return

source = ColumnDataSource(d)  # ColumnDataSource(dict(x=[], y=[], avg=[]))

text = TextInput(title='Equation: ', placeholder='a := 1')
# text.on_change ## make this work

update = Button(label="Update")
update.on_click(textstuff)

envdiv = PreText(text='Env: <br/>'+repr(env))
output = Div(text='hi this is test')

curdoc().add_root(widgetbox([envdiv, text, output, update]))


fig = Figure()
fig.line(source=source, x='#', y='t', line_width=2, alpha=.85, color='red')
curdoc().add_root(fig)
# fig = Figure()
# fig.line(source=source, x='x', y='y', line_width=2, alpha=.85, color='red')
# curdoc().add_root(fig)
# fig = Figure()
# fig.line(source=source, x='x', y='avg', line_width=2, alpha=.85, color='blue')
# curdoc().add_root(fig)

# ct = 0
# sine_sum = 0
#
# def i():
#     ct = 0
#     sine_sum = 0
#     for x in range(100):
#         ct += np.pi/100
#         sine = np.sin(ct)
#         sine_sum += sine
#         yield dict(x=[ct], y=[sine], avg=[sine_sum/ct])
# a = i()
i = 0
dt = (1/210)/10
def update_data():
    global a
    global i
    # global ct, sine_sum
    # ct += np.pi/100
    # sine = np.sin(ct)
    # sine_sum += sine
    try:
        [next(a) for x in range(10)]
        n = next(a)
        n['#'] = [i]
        new_data = {'t': [n['Xball'][0].imag*100], '#': [n['Xball'][0].real*100]}
    except StopIteration:
        a = nxt.nextdata()
        n = next(a)
        n['#'] = [i]
        new_data = n
    i += 1
    source.stream(new_data, 1000)


curdoc().add_periodic_callback(update_data, 10)
