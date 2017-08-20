# try:
# import matplotlib.pyplot as plt
# import mpld3 as mpl
# import bokeh as bo
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.plotting import Figure
# except:
#     pass
import numpy as np


def graph(grph, nextdata):
    ndata = nextdata()
    source = ColumnDataSource(next(ndata))
    for x, y in grph:
        fig = Figure()
        fig.line(source=source, x=x, y=y, line_width=2, alpha=0.85, color='red')
        curdoc().add_root(fig)

    i = 0
    def updategraph():
        global i
        global ndata
        try:
            new_data = next(ndata)
            i += 1
        except StopIteration:
            ndata = nextdata()
            new_data = next(ndata)
            i = 0
        new_data['#'] = i

        source.stream(new_data, 100)
    curdoc().add_next_tick_callback(updategraph)



placeholder = ''' <style>

</style>

<div id="fig_el811644378604322271759321"></div>
<script>
function mpld3_load_lib(url, callback){
  var s = document.createElement('script');
  s.src = url;
  s.async = true;
  s.onreadystatechange = s.onload = callback;
  s.onerror = function(){console.warn("failed to load library " + url);};
  document.getElementsByTagName("head")[0].appendChild(s);
}

if(typeof(mpld3) !== "undefined" && mpld3._mpld3IsLoaded){
   // already loaded: just create the figure
   !function(mpld3){

       mpld3.draw_figure("fig_el811644378604322271759321", {"axes": [{"xlim": [20.5, 31.5], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [20.5, 31.5], "ylim": [20.5, 31.5], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#1F77B4", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.5, "data": "data01", "id": "el81164659969872"}], "markers": [], "id": "el81164601557904", "ydomain": [20.5, 31.5], "collections": [], "xscale": "linear", "bbox": [0.125, 0.10999999999999999, 0.775, 0.77]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[21.0, 21.0], [22.0, 22.0], [23.0, 23.0], [24.0, 24.0], [25.0, 25.0], [26.0, 26.0], [27.0, 27.0], [28.0, 28.0], [29.0, 29.0], [30.0, 30.0], [31.0, 31.0]]}, "id": "el81164437860432"});
   }(mpld3);
}else if(typeof define === "function" && define.amd){
   // require.js is available: use it to load d3/mpld3
   require.config({paths: {d3: "https://mpld3.github.io/js/d3.v3.min"}});
   require(["d3"], function(d3){
      window.d3 = d3;
      mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){

         mpld3.draw_figure("fig_el811644378604322271759321", {"axes": [{"xlim": [20.5, 31.5], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [20.5, 31.5], "ylim": [20.5, 31.5], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#1F77B4", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.5, "data": "data01", "id": "el81164659969872"}], "markers": [], "id": "el81164601557904", "ydomain": [20.5, 31.5], "collections": [], "xscale": "linear", "bbox": [0.125, 0.10999999999999999, 0.775, 0.77]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[21.0, 21.0], [22.0, 22.0], [23.0, 23.0], [24.0, 24.0], [25.0, 25.0], [26.0, 26.0], [27.0, 27.0], [28.0, 28.0], [29.0, 29.0], [30.0, 30.0], [31.0, 31.0]]}, "id": "el81164437860432"});
      });
    });
}else{
    // require.js not available: dynamically load d3 & mpld3
    mpld3_load_lib("https://mpld3.github.io/js/d3.v3.min.js", function(){
         mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){

                 mpld3.draw_figure("fig_el811644378604322271759321", {"axes": [{"xlim": [20.5, 31.5], "yscale": "linear", "axesbg": "#FFFFFF", "texts": [], "zoomable": true, "images": [], "xdomain": [20.5, 31.5], "ylim": [20.5, 31.5], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": null, "grid": {"gridOn": false}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [{"color": "#1F77B4", "yindex": 1, "coordinates": "data", "dasharray": "10,0", "zorder": 2, "alpha": 1, "xindex": 0, "linewidth": 1.5, "data": "data01", "id": "el81164659969872"}], "markers": [], "id": "el81164601557904", "ydomain": [20.5, 31.5], "collections": [], "xscale": "linear", "bbox": [0.125, 0.10999999999999999, 0.775, 0.77]}], "height": 480.0, "width": 640.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}], "data": {"data01": [[21.0, 21.0], [22.0, 22.0], [23.0, 23.0], [24.0, 24.0], [25.0, 25.0], [26.0, 26.0], [27.0, 27.0], [28.0, 28.0], [29.0, 29.0], [30.0, 30.0], [31.0, 31.0]]}, "id": "el81164437860432"});
            })
         });
}
</script>'''
if __name__ == '__main__':
    data = {'x': [i-(i*1j) for i in range(10)], 'y': range(10)}
    graph(data, 'x', None)
