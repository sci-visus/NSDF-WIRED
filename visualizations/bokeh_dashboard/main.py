##### Import Dependencies #####
from data_handling import *
from util import *
from datetime import timedelta
import pandas as pd
from pathlib import Path
from bokeh.layouts import layout, row, column, Spacer, gridplot
import xyzservices.providers as xyz
from bokeh.plotting import figure, curdoc
from bokeh.models import (
    DatePicker,
    Slider,
    Toggle,
    RadioButtonGroup,
    ColumnDataSource,
    LogColorMapper,
    Div,
    CustomJS,
    ResetTool,
    UndoTool,
    ZoomInTool,
    ZoomOutTool,
    BoxZoomTool,
    PanTool
)

##### Init ColumnDataSource #####
# Create a ColumnDataSource for the firesmoke data
default_res = 0
default_date = "2021-03-04"
default_hour = 0
latslons = get_latslons()
default_lats = latslons[:, 0]
default_lons = latslons[:, 1]
default_pm25_vals = get_pm25(default_date, default_hour, default_res)

rows, cols = np.shape(default_pm25_vals)
source = ColumnDataSource(
    data=dict(
        x=[default_lats],
        y=[default_lons],
        image=[default_pm25_vals],
    )
)

##### Init bokeh figure #####
# get coordinates centering on North America
canada_coords_min = latlon_to_mercator(32, -160)
canada_coords_max = latlon_to_mercator(71, -51)

# specify bokeh tools for user to use
# match_aspect is True to prevent stretching of map when zooming
tools = [BoxZoomTool(match_aspect=True), ResetTool(), UndoTool(), 
         ZoomInTool(), ZoomOutTool(), PanTool()]

p = figure(
    title="Ground level concentration of PM2.5 microns and smaller",
    tools=tools,
    x_range=(default_lats[0], default_lats[-1]),
    y_range=(default_lons[1], default_lons[-1]),
    x_axis_type="mercator",
    y_axis_type="mercator",
    sizing_mode="scale_both"
)
p.xaxis.axis_label = "Latitude"
p.yaxis.axis_label = "Longitude"
p.add_tile(xyz.OpenStreetMap.Mapnik)

# create log color map to colormap PM2.5 data
cmap = LogColorMapper(
    # using 'Oranges' from: https://observablehq.com/@d3/color-schemes
    palette=["#fff5eb00","#fdd8b3","#fdc28c","#fda762","#fb8d3d","#f2701d","#e25609","#c44103","#9f3303","#7f2704"],
    low=0.0001,
    high=np.nanmax(source.data["image"][0].flatten())
)
# color_bar = ColorBar(color_mapper=color_mapper, padding=5)

# print(f'canada_coords_min = {canada_coords_min}')
# print(f'canada_coords_max = {canada_coords_max}')

print(f'default_lats[0] = {default_lats[0]}, default_lats[-1] = {default_lats[-1]}')
print(f'default_lons[0] = {default_lons[0]}, default_lons[-1] = {default_lons[-1]}')

# draw PM2.5 data on figure
img = p.image(
    "image",
    source=source,
    x=default_lats[0],
    y=default_lons[0],
    dw=default_lats[-1] - default_lats[0],
    dh=default_lons[-1] - default_lons[0],
    color_mapper=cmap,
    alpha=.8 # so that the map tile is visible underneath
)
color_bar = img.construct_color_bar(padding=1, title="PM2.5 (µg/m3)", title_text_align="right", title_standoff=0)

p.add_layout(color_bar, "right")

##### Create and Init Buttons/Inputs #####
date_picker = DatePicker(
    title="Select date",
    value=default_date,
    min_date="2021-03-04",  # earliest available forecast
    max_date="2024-06-27",  # last time we downloaded forecast
)

# hour slider allows user to select hour 0-23 for currently selected date
# refs:
#   https://github.com/bokeh/bokeh/blob/branch-3.8/examples/server/app/gapminder/main.py
#   https://discourse.bokeh.org/t/a-simple-way-to-custom-a-slider-as-a-dateslider/10005
t = [f'{i:02}:00 UTC' for i in range(24)]
hour_slider = Slider(
    start=0,
    end=len(t) - 1,
    value=0,
    step=1,
    title=f"{date_picker.value} {t[0]}",
    show_value=False,
)

# IDX resolution slider
res_slider = Slider(start=-19, end=0, value=default_res, step=1, title="Resolution")

# select animation playback speed
callback_id = None # to enable or disable periodic callback to animation
ms_delay = 1000 # initialize animation playback to be 1x
dropdown_speeds = [2000, 1000, 500, 333]
dropdown_labels = ["0.5x", "1x", "2x", "3x"]
speed_radio_buttons = RadioButtonGroup(labels=dropdown_labels, active=1)

# toggle playing or pausing animation of hourly smoke data
toggle = Toggle(label="►/❚❚", button_type="default", width=60)

##### Callback Functions #####
# Update source on new date, hour, or resolution selection by user
def update_data(attr, old, new):
    new_data = {"x" : [default_lats], 
                "y" : [default_lons], 
                "image" : [get_pm25(date_picker.value, hour_slider.value, res_slider.value)]}

    source.data = new_data


## set or remove periodic callback based on play/pause toggle button
def animate(attr, old, new):
    global callback_id
    global ms_delay
    if toggle.active == True:
        callback_id = curdoc().add_periodic_callback(animate_update, ms_delay)
    else:
        curdoc().remove_periodic_callback(callback_id)

def animate_update():
    hour = hour_slider.value + 1
    if hour > 23:
        hour = 0
    # update plot with data of newly gotten hour
    update_data(None, None, None)
    hour_slider.value = hour

def change_playback(attr, old, new):
    global ms_delay
    ms_delay = dropdown_speeds[speed_radio_buttons.active]
    
    # if we change playback while toggle is playing, remove current callback and 
    # start a new one
    if toggle.active == True:
        curdoc().remove_periodic_callback(callback_id)
        animate(None, None, None)

##### Event Handling #####
## Upon any of these events, the corresponding callback is run

# Update hour slider UI
hour_slider.js_on_change(
    "value",
    CustomJS(
        args=dict(hs=hour_slider, t=t, dp=date_picker),
        code="""
        hs.title = `${dp.value} ${t[hs.value]}`;""",
    ),
)

speed_radio_buttons.on_change("active", change_playback)

toggle.on_change('active', animate)

# only update sliders user is done sliding the slider around
# ref: https://stackoverflow.com/questions/38375961/throttling-in-bokeh-application
hour_slider.on_change('value_throttled', update_data)
res_slider.on_change('value_throttled', update_data)

# # hour slider allows user to select hour 0-23 for currently selected date
# # refs:
# #   https://github.com/bokeh/bokeh/blob/branch-3.8/examples/server/app/gapminder/main.py
# #   https://discourse.bokeh.org/t/a-simple-way-to-custom-a-slider-as-a-dateslider/10005
# curr_date = date_picker.value
# year = int(curr_date[0:4])
# month = int(curr_date[5:7])
# day = int(curr_date[-2:])
# step = timedelta(hours=1)
# # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
# hr_start = get_datetime(year, month, day, 0)
# hr_end = get_datetime(year, month, day, 23)
# step_times = pd.date_range(start=hr_start, end=hr_end, freq=step, tz="utc")
# t = [str(t) for t in step_times]

date_picker.on_change('value', update_data)
date_picker.js_on_change('value', CustomJS(
        args=dict(hs=hour_slider, t=t, dp=date_picker),
        code="""
        hs.title = `${dp.value} ${t[hs.value]}`;""",
    ))

##### UI Layout #####
# description to display at top of page
desc = Div(text=(Path(__file__).parent / "description.html").read_text("utf8"), sizing_mode="stretch_width")
spacer0 = Spacer(width=15)
spacer1 = Spacer(width=10)
spacer2 = Spacer(width=25)
spacer3 = Spacer(width=10)
inputs = row([spacer0, date_picker, spacer1, res_slider, spacer2, hour_slider, spacer3, column(speed_radio_buttons, toggle)], sizing_mode="stretch_width")
layout = layout(column(desc, inputs, row(p, sizing_mode="scale_both")), sizing_mode="stretch_both")
# layout = gridplot([[p]], sizing_mode='stretch_both')
curdoc().add_root(layout)
curdoc().title = "UBC FireSmoke Data Curation Dashboard"