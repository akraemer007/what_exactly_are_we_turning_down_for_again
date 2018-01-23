# Run with bokeh serve .

import pandas as pd
import numpy as np

from os.path import dirname, join
from datetime import datetime as dt
import time


from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Div, Span
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.layouts import row, column, layout, widgetbox # added layout not sure difference
from bokeh.models.ranges import Range1d


# import music data
song_data = pd.read_pickle('../data/df.pkl')
song_data = song_data.sort_values('chartDate').groupby('spotifyID').first().reset_index()
song_data['color'] = np.where(song_data['happy_index'] < .5, 'purple', 'grey')
song_data['chartDate'] = song_data['chartDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
# song_data['valence'] = song_data['valence'].apply(lambda x: round(x, 2))
# song_data['energy'] = song_data['energy'].apply(lambda x: round(x, 2))
# song_data['polarity'] = song_data['polarity'].apply(lambda x: round(x, 2))

month_data = pd.read_pickle('../data/month_df.pkl')
month_data = month_data.reset_index()


####### DROPDOWN
AXIS = ['valence', 'energy', 'polarity', 'happy_index']
# def nix(val, lst):
#     return [x for x in lst if x != val]

# instantiate scatter plot
source = ColumnDataSource(data = dict(title=[],
                                      chartDate=[],
                                      peakPos=[],
                                      valence=[],
                                      energy=[],
                                      polarity=[],
                                      happy_index=[],
                                      color=[]))

# instansiate time series plots
tools = 'pan,wheel_zoom,xbox_select,reset'
source_static = ColumnDataSource(data=dict(dates=[], cci_value=[], sad_hit_flag=[]))
source_static.data = source_static.from_df(month_data[['dates',
                                                     'cci_value',
                                                     'sad_hit_flag']])



####### WIGIT INITIATION
min_year = Slider(title="Year released", start=1958, end=2016, value=1970, step=1)
max_year = Slider(title="End Year released", start=1958, end=2016, value=2016, step=1)
pos_slider = Slider(title="Peak Position Max", start= 1, end = 10, value = 10, step=1)
x_axis = Select(title="x_axis", value='valence', options=AXIS)
y_axis = Select(title="y_axis", value='energy', options=AXIS)
title = TextInput(title="Song name :")
artist = TextInput(title="Artist name contains:")

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

corr = figure(plot_width=550, plot_height=550,
#               tools='pan,wheel_zoom,box_select,reset' # use for time series
              tools=[hover],
              title = 'Song Happiness',
              x_range = [0,1], y_range = [0,1])

corr.circle(x = 'x_axis', y = 'y_axis',
            size=7,
            source=source,
            color="color",
            alpha=0.3, nonselection_alpha=0.3, selection_color="blue", selection_alpha=0.7)
corr.xaxis.axis_label = 'Valence'
corr.yaxis.axis_label = 'Energy'


ts1 = figure(plot_width=1000, plot_height=300, tools=tools, title = 'Consumer Confidence with Sad Songs', x_axis_type='datetime', active_drag="xbox_select", y_range=Range1d(96, 103))
ts1.line('dates', 'cci_value', source=source_static, line_width=2)
ts1.vbar(x=month_data['dates'], width=1, bottom=95, top=105, line_width=2, line_alpha = month_data['sad_hit_flag']*.2, color="purple")
ts1.xaxis.axis_label = 'Date'
ts1.yaxis.axis_label = 'Consumer Confidence Index'




####### CREATE VERTICAL LINE LABELS
# TODO add labels
def create_vline(year_month_day):
    start_date = time.mktime(dt(year_month_day[0], year_month_day[1], year_month_day[2], 0, 0, 0).timetuple())*1000
    vertical_line1 = Span(location=start_date, dimension='height', line_color='blue',line_dash='dashed', line_width=1)
    ts1.add_layout(vertical_line1)
[create_vline(date) for date in [(1963,10,2, 'JFK Assassination'), (2001,9,1, '9/11'), (2008,9,15, "'08 Stock Crash")]]

####### HTML HEADER
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)

###### Dropdown update
# def x_axis_change(attrname, old, new):
#     x_axis.options = nix(new, AXIS)
#     update()
#
# def y_axis_change(attrname, old, new):
#     y_axis.options = nix(new, AXIS)
#     update()

###### DATA FILTERING
def select_data():
    title_val = title.value.strip()
    artist_val = artist.value.strip()

    selected_song = song_data[
        (song_data.year >= min_year.value) &
        (song_data.year <= max_year.value) &
        (song_data.peakPos <= pos_slider.value)
    ]

    # filter text boxes
    if (title_val != ""):
        selected_song = selected_song[selected_song.title.str.contains(title_val)==True]
    if (artist_val != ""):
        selected_song = selected_song[selected_song.artist.str.contains(artist_val) == True]

    selected_song['x_axis'] = selected_song[x_axis.value]
    selected_song['y_axis'] = selected_song[y_axis.value]


    selected_month = month_data#[]

    return selected_song, selected_month

####### UPDATING
def update(selected=None):
    song_df, month_df = select_data()
    source.data = source.from_df(song_df[['title',
                                          'artist',
                                          'chartDate',
                                          'peakPos',
                                          'valence',
                                          'energy',
                                          'polarity',
                                          'happy_index',
                                          'color',
                                          'x_axis',
                                          'y_axis']])
    corr.xaxis.axis_label = x_axis.value
    corr.yaxis.axis_label = y_axis.value

    source_static.data = source_static.from_df(month_df[['dates',
                                                         'cci_value',
                                                         'sad_hit_flag']])

controls = [x_axis, y_axis, min_year, max_year, pos_slider, title, artist]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)


####### LAYOUT
layout = layout([desc, [corr, inputs], ts1])

# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Energy - Polarity"