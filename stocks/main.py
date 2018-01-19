import pandas as pd
import numpy as np

from os.path import dirname, join
from datetime import datetime as dt
import time


from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Div, Span
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.layouts import row, column, layout, widgetbox # added layout not sure differentce
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

corr = figure(plot_width=550, plot_height=550,
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


ts1 = figure(plot_width=1000, plot_height=300, tools=tools, title = 'Consumer Confidence with Sad Songs', x_axis_type='datetime', active_drag="xbox_select", y_range=Range1d(96, 103))
ts1.line('dates', 'cci_value', source=source_static, line_width=2)
ts1.vbar(x=month_data['dates'], width=1, bottom=95, top=105, line_width=2, line_alpha = month_data['sad_hit_flag']*.2, color="purple")
ts1.xaxis.axis_label = 'Date'
ts1.yaxis.axis_label = 'Consumer Confidence Index'

# ts1.background_fill_color = "black"
# ts1.xgrid.grid_line_color = None
# ts1.ygrid.grid_line_color = None


# ts2 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
# ts2.line('dates', 'sad_hit_flag', fill= 'blue', source=source_static)



def create_vline(year_month_day):
    start_date = time.mktime(dt(year_month_day[0], year_month_day[1], year_month_day[2], 0, 0, 0).timetuple())*1000
    vertical_line1 = Span(location=start_date, dimension='height', line_color='blue',line_dash='dashed', line_width=1)
    vertical_line2 = Span(location=start_date, dimension='height', line_color='blue',line_dash='dashed', line_width=1)
    ts1.add_layout(vertical_line1)
    # ts2.add_layout(vertical_line2)

[create_vline(date) for date in [(1963,10,2), (2001,9,1), (2008,9,15)]]


# HTML header
desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)




def select_data():

    selected_song = song_data[
        (song_data.year >= min_year.value) &
        (song_data.year <= max_year.value) &
        (song_data.peakPos <= pos_slider.value)
    ]

    selected_month = month_data#[]

    return selected_song, selected_month

# def update_happiest_saddest():
#
#     return

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
                                          'color']])
    source_static.data = source_static.from_df(month_df[['dates',
                                                         'cci_value',
                                                         'sad_hit_flag']])


controls = [min_year, max_year, pos_slider]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(*controls, sizing_mode=sizing_mode)

# layout = column(main_row, series)
layout = layout([desc, [corr, inputs], ts1])

# initialize
update()

curdoc().add_root(layout)
curdoc().title = "Energy - Polarity"