# try:
# import matplotlib.pyplot as plt
# import mpld3 as mpl
# import bokeh as bo
from bokeh.models import ColumnDataSource, Legend, PreText
from bokeh.plotting import Figure
# except:
#     pass
import numpy as np


def bokehtickgraph(x, y, nextdata, curdoc):
    source = ColumnDataSource(next(nextdata))
    fig = Figure()
    fig.line(source=source, x=x, y=y, line_width=2, alpha=0.85, color='red')

    def updategraph():
        new_data = next(nextdata)
        # div.text += str(new_data)
        source.stream(new_data, 100)
        curdoc().add_next_tick_callback(updategraph)

    return fig, updategraph

def bokehstaticgraph(x, y, data):
    source = ColumnDataSource(data)
    fig = Figure()
    fig.line(source=source, x=x, y=y, line_width=2, alpha=0.85, color='red')
    return fig


def complexprotect(data):
    ndata = {}
    for var, val in data.items():
        if type(val) is list:
            if sum([isinstance(num, complex) for num in val]) > 0:
                ndata[var+'#m'] = [abs(num) for num in val]
                ndata[var+'#d'] = [np.angle(num) for num in val]
                ndata[var+'#x'] = [num.real for num in val]
                ndata[var+'#y'] = [num.imag for num in val]
            else:
                ndata[var] = val
        else:
            if isinstance(val, complex):
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

if __name__ == '__main__':
    data = {'x': [-i for i in range(10)], 'y': range(10)}
    bokehstaticgraph('x', 'y', data)
