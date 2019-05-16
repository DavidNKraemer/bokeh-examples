import numpy as np

from bokeh.plotting import figure, output_file, show, curdoc, ColumnDataSource
from bokeh.layouts import gridplot 
from bokeh.driving import linear
from bokeh.palettes import viridis

max_to_display = 100
colors = viridis(int(max_to_display / 2)) + viridis(int(max_to_display / 2))[::-1]

def rvsample_generator(rv_generator):
    rv = rv_generator()
    mean = rv
    count = 1
    while True:
        yield (rv, mean, count)
        count += 1
        rv = rv_generator()
        mean = (count - 1) / count * mean + rv / count

source = ColumnDataSource({
    "rv_x": [],
    "rv_y": [],
    "mean_x": [],
    "mean_y": [],
    "colors": [],
})

rvp = figure(plot_width=400, plot_height=400, title="Random Variates")
rvp.circle(x='rv_x', y='rv_y', color="colors", source=source)


meanp = figure(plot_width=400, plot_height=400, title="Sample Means")
meanp.circle(x='mean_x', y='mean_y', color="colors", source=source)


rv_generator = rvsample_generator(lambda: np.random.randn(2))

@linear()
def update(step):
    rv, mean, count = next(rv_generator)

    count %= len(colors)

    new_data = {
        "rv_x": [rv[0]],
        "rv_y": [rv[1]],
        "mean_x": [mean[0]],
        "mean_y": [mean[1]],
        "colors": [colors[count]]
    }

    source.stream(new_data, max_to_display)

curdoc().add_root(gridplot([rvp, meanp], ncols=2))
curdoc().add_periodic_callback(update, 50)

