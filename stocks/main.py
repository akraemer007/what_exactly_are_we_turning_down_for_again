import pandas as pd
import numpy as np

from os.path import dirname, join

from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.layouts import row, column, layout, widgetbox # added layout not sure differentce

data = pd.read_pickle('../data/df.pkl')
data = data.sort_values('chartDate').groupby('spotifyID').first().reset_index()
data['color'] = np.where(data['polarity'] < .5, 'purple', 'grey')
data['chartDate'] = data['chartDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
# data['valence'] = data['valence'].apply(lambda x: round(x, 2))
# data['energy'] = data['energy'].apply(lambda x: round(x, 2))
# data['polarity'] = data['polarity'].apply(lambda x: round(x, 2))


source = ColumnDataSource(data = dict(title=[],
                                      chartDate=[],
                                      peakPos=[],
                                      valence=[],
                                      energy=[],
                                      polarity=[],
                                      happy_index=[],
                                      color=[]))

# set up widgets
min_year = Slider(title="Year released", start=1958, end=2016, value=1970, step=1)
max_year = Slider(title="End Year released", start=1958, end=2016, value=2016, step=1)
pos_slider = Slider(title="Peak Position Max", start= 1, end = 10, value = 10, step=1)
# happy_filter = Slider(title="Peak Position Max", start= 1, end = 10, value = 10, step=1)

hover = HoverTool(tooltips=[
    ("Title", "@title"),
    ("Artist", "@artist"),
    ("Chart Date", "@chartDate"),
    ("Peak Position", "@peakPos"),
    ("Valence", "@valence"),
    ("Energy", "@energy"),
    ("Polarity", "@polarity"),
    ("happy_index", "@happy_index")
])

corr = figure(plot_width=450, plot_height=450,
#               tools='pan,wheel_zoom,box_select,reset' # use for time series
              tools=[hover],
              title = 'dope title',
              x_range = [0,1], y_range = [0,1])

corr.circle(x = 'valence', y = 'energy',
            size=7,
            source=source,
            color="color",
            alpha=0.3, nonselection_alpha=0.3, selection_alpha=0.7)
corr.xaxis.axis_label = 'Valence'
corr.yaxis.axis_label = 'Energy'

# show(corr) # used to open graph in another tab.

# HTML header
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

def select_data():

    selected = data[
        (data.year >= min_year.value) &
        (data.year <= max_year.value) &
        (data.peakPos <= pos_slider.value)
    ]

    return selected

# def update_happiest_saddest():
#
#     return

def update(selected=None):
    df = select_data()
    source.data = source.from_df(df[['title',
                                     'artist',
                                     'chartDate',
                                     'peakPos',
                                     'valence',
                                     'energy',
                                     'polarity',
                                     'happy_index',
                                     'color']])


controls = [min_year, max_year, pos_slider]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)

# layout = column(main_row, series)
layout = layout([desc, [inputs, corr]])

# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Energy - Polarity"