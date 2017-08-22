# try:
# import matplotlib.pyplot as plt
# import mpld3 as mpl
# import bokeh as bo
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.plotting import Figure
from bokeh.models.widgets import Div
# except:
#     pass
import numpy as np


def bokehtickgraph(x, y, nextdata):
    source = ColumnDataSource(next(nextdata))
    fig = Figure()
    fig.line(source=source, x=x, y=y, line_width=2, alpha=0.85, color='red')
    curdoc().add_root(fig)
    # div = Div(text='hello world')
    # curdoc().add_root(div)

    def updategraph():
        new_data = next(nextdata)
        # div.text += str(new_data)
        source.stream(new_data, 100)
        curdoc().add_next_tick_callback(updategraph)

    curdoc().add_next_tick_callback(updategraph)
    # return updategraph

def bokehstaticgraph(x, y, data):
    source = ColumnDataSource(data)
    fig = Figure()
    fig.line(source=source, x=x, y=y, line_width=2, alpha=0.85, color='red')
    curdoc().add_root(fig)


# def replgraph(data, x, y):
#     x = np.array(data[x])
#     xtest = sum(x.imag ** 2)
#     fig = plt.figure()
#     if y is None:
#         if xtest != 0:
#             y = x.imag
#             x = x.real
#         else:
#             y = x
#             x = range(len(x))
#     else:
#         y = np.array(data[y])
#         ytest = sum(y.imag**2)
#         x = abs(x) if xtest != 0 else x
#         y = abs(y) if ytest != 0 else y
#     plt.plot(x, y)
#     plt.show()

if __name__ == '__main__':
    data = {'x': [-i for i in range(10)], 'y': range(10)}
    bokehstaticgraph('x', 'y', data)
