from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import TextInput, Button, Div, PreText

import zscript as zs
from zgraph import np

# from program import zscript_code


# test = '''a := (1, 0)
# a_ = a * (3, 4)/5 + 0.1
# trace a
# next 0'''
# stuff = zs.compilerun(test, zs.Env())

env = zs.Env(repl=True)

def textstuff():
    global btn, inpt, output, env
    output.text += '>>>' + inpt.value + '<br/>'
    try:
        gen = zs.compilerun(inpt.value, env)
    except Exception as e:
        gen = [e.__class__.__name__ + ': ' + '\n'.join([a for a in e.args if type(a) is str])]
    envdiv.text = 'Env: \n'+repr(env)
    print(gen)
    for g in gen:
        print(g)
        if type(g) in (float, complex, str, bool, int, tuple):
            output.text += str(g) + '<br/>'
        elif type(g) is dict:
            length = len(list(g.values())[0])
            for i in range(length):
                output.text += str({var: val[i] for var, val in g.items()}) + '<br/>'

    return

envdiv = PreText(text='Env: \n'+repr(env))
inpt = TextInput(title='Equation: ', placeholder='a := 1')
output = Div(text='')
btn = Button(label="Update")
btn.on_click(textstuff)

mainLayout = column(output, inpt, btn, envdiv, name='thing')

curdoc().add_root(mainLayout)

def complexprotect(data):
    ndata = {}
    for var, val in data.items():
        if type(val) is list:
            if sum([num.imag**2 for num in val]) > 0:
                ndata[var+'#m'] = [abs(num) for num in val]
                ndata[var+'#d'] = [np.angle(num) for num in val]
                ndata[var+'#x'] = [num.real for num in val]
                ndata[var+'#y'] = [num.imag for num in val]
            else:
                ndata[var] = val
        else:
            if type(val) is complex:
                ndata[var+'#m'] = abs(val)
                ndata[var+'#d'] = np.angle(val)
                ndata[var+'#x'] = val.real
                ndata[var+'#y'] = val.imag
            else:
                ndata[var] = val
    return ndata


def rangetick(data):
    data = complexprotect(data)
    keys = list(data.keys())
    yield {key: [] for key in keys}
    i = 0
    mod = len(list(data.values())[0])
    print(mod)
    while True:
        yield {key: [data[key][i % mod]] for key in keys}
        i += 1


def infintick(data, first=None):
    if first is None:
        first = complexprotect(next(data))
    yield {var: [] for var in first.keys()}
    yield {var: [val] for var, val in first.items()}
    while True:
        yield {var: [val] for var, val in complexprotect(next(data)).items()}


# data = stuff[0]
# if type(data) is dict:
#     data = complexprotect(data)
#     bokehstaticgraph('am', 'ad', data)
# else:
#     tick = infintick(data)
#     bokehtickgraph('am', 'ad', tick)
#
#
# env = zs.Env(repl=True)
# zs.compilerun(zscript_code, env)
#
# zs.repl(env)
# zs.compilerun(zscript_code, env)
# zs.compilerun('next 10', env)