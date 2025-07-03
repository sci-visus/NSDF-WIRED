##### Import Dependencies #####
from data_handling import *
from util import *
from datetime import timedelta
import pandas as pd
from pathlib import Path
from bokeh.layouts import layout, row, column, Spacer
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
        image=[default_pm25_vals],
    )
)

##### Init bokeh figure #####
# get coordinates centering on North America
min_coords = latlon_to_mercator(32, -160)
max_coords = latlon_to_mercator(71, -51)

# specify bokeh tools for user to use
# match_aspect is True to prevent stretching of map when zooming
tools = [BoxZoomTool(match_aspect=True), ResetTool(), UndoTool(), 
         ZoomInTool(), ZoomOutTool(), PanTool()]

p = figure(
    tools=tools,
    x_range=(min_coords[0], max_coords[0]),
    y_range=(min_coords[1], max_coords[1]),
    x_axis_type="mercator",
    y_axis_type="mercator",
    sizing_mode="scale_both"
)
p.add_tile(xyz.OpenStreetMap.Mapnik)

# create log color map to colormap PM2.5 data
cmap = LogColorMapper(
    # using 'Oranges' from: https://observablehq.com/@d3/color-schemes
    palette=["#fff5eb00","#fdd8b3","#fdc28c","#fda762","#fb8d3d","#f2701d","#e25609","#c44103","#9f3303","#7f2704"],
    low=0.0001,
    high=np.nanmax(source.data["image"][0].flatten())
)

# draw PM2.5 data on figure
p.image(
    "image",
    source=source,
    x=min_coords[0],
    y=min_coords[1],
    dw=max_coords[0] - min_coords[0],
    dh=max_coords[1] - min_coords[1],
    color_mapper=cmap,
    alpha=.8 # so that the map tile is visible underneath
)

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
curr_date = date_picker.value
year = int(curr_date[0:4])
month = int(curr_date[5:7])
day = int(curr_date[-2:])
step = timedelta(hours=1)
# https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
hr_start = get_datetime(year, month, day, 0)
hr_end = get_datetime(year, month, day, 23)
step_times = pd.date_range(start=hr_start, end=hr_end, freq=step, tz="utc")
t = [str(t) for t in step_times]
hour_slider = Slider(
    start=0,
    end=len(step_times) - 1,
    value=0,
    step=1,
    title=f"{t[0]}",
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
    # print(f"update_data: attr = {attr}, old = {old}, new = {new}")
    new_data = {"image" : [get_pm25(date_picker.value, hour_slider.value, res_slider.value)]}
    source.data = new_data

## set or remove periodic callback based on play/pause toggle button
def animate(attr, old, new):
    # print(f"animate: attr = {attr}, old = {old}, new = {new}")
    global callback_id
    global ms_delay
    if toggle.active == True:
        # immediately start playing, removes annoying delay of waiting for callback upon toggling play
        animate_update()
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
    print(f"change_playback: attr = {attr}, old = {old}, new = {new}\nplayback label is now {dropdown_labels[new]}")
    global ms_delay
    ms_delay = dropdown_speeds[speed_radio_buttons.active]
    print(f'curr ms_delay = {ms_delay}')
    
    # call animate if toggle is set to play
    if toggle.active == True:
        animate(None, None, None)

##### Event Handling #####
## Upon any of these events, the corresponding callback is run

# Update hour slider UI
hour_slider.js_on_change(
    "value",
    CustomJS(
        args=dict(sl=hour_slider, t=t, d=curr_date),
        code="""sl.title = t[this.value];""",
    ),
)

# dropdown.js_on_event("button_click", CustomJS(code="console.log('dropdown: click ' + this.toString())"))
# dropdown.on_event("menu_item_click", change_playback)
speed_radio_buttons.on_change("active", change_playback)

toggle.on_change('active', animate)

# only update sliders user is done sliding the slider around
# ref: https://stackoverflow.com/questions/38375961/throttling-in-bokeh-application
hour_slider.on_change('value_throttled', update_data)
res_slider.on_change('value_throttled', update_data)

date_picker.on_change('value', update_data)

##### UI Layout #####
# description to display at top of page
desc = Div(text=(Path(__file__).parent / "description.html").read_text("utf8"), sizing_mode="stretch_width")

inputs = column([date_picker, res_slider, hour_slider, speed_radio_buttons, toggle], width=320, height=800)
layout = layout(desc, row(inputs, column(p, width=800, height=700)), sizing_mode="scale_width")
curdoc().add_root(layout)
curdoc().title = "UBC FireSmoke Data Curation Dashboard"