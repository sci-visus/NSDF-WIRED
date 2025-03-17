# imports for data handling and utility functions
from data_handling import *
from util import *
from datetime import datetime, timedelta, timezone
import pandas as pd

# imports for visualization
from bokeh.layouts import layout
import xyzservices.providers as xyz
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from bokeh.models import (
    DatePicker,
    Slider,
    DateSlider,
    ColumnDataSource,
    Button,
    CustomJS,
)

##### Init ColumnDataSource #####
# Create a ColumnDataSource for the data
# for now, we use all latitudes and longitudes
default_res = 0
default_date = "2021-03-04"
default_hour = 0
latslons = get_latslons()
default_lats = latslons[:, 0]
default_lons = latslons[:, 1]
default_pm25_vals = get_pm25(default_date, default_hour, default_res)
source = ColumnDataSource(
    data=dict(
        date=[default_date],
        hour=[default_hour],
        res=[default_res],
        x=[default_lats],
        y=[default_lons],
        color=[default_pm25_vals],
    )
)

##### Init bokeh figure #####
# create a plot centering in north america
min_coords = latlon_to_mercator(32, -160)
max_coords = latlon_to_mercator(71, -51)
p = figure(
    x_range=(min_coords[0], max_coords[0]),
    y_range=(min_coords[1], max_coords[1]),
    x_axis_type="mercator",
    y_axis_type="mercator",
)
p.add_tile(xyz.OpenStreetMap.Mapnik)
p.scatter(x="x", y="y", source=source, color="color")

##### Widgets #####
### datepicker widget ###
date_picker = DatePicker(
    title="Select date",
    value=default_date,
    min_date="2021-03-04",  # earliest available forecast
    max_date="2024-06-27",  # last time we downloaded forecast
)


# callback function to update selected data on new date
def update_date(attr, old_date, new_date):
    # update data
    new_data = dict()

    # keep the same
    new_data["hour"] = source.data["hour"]
    new_data["res"] = source.data["res"]
    new_data["x"] = source.data["x"]
    new_data["y"] = source.data["y"]

    # new date and new pm2.5 values
    new_data["date"] = [new_date]
    new_data["color"] = [
        get_pm25(new_data["date"][0], new_data["hour"][0], new_data["res"][0])
    ]
    source.data = new_data


# when date selected changes, call update_date
date_picker.on_change("value", update_date)


### hour widget ###
# refs:
#   https://github.com/bokeh/bokeh/blob/branch-3.8/examples/server/app/gapminder/main.py
#   https://discourse.bokeh.org/t/a-simple-way-to-custom-a-slider-as-a-dateslider/10005

# hour slider shows hours for currently selected date
curr_date = source.data["date"][0]
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
    title=f"{curr_date} {t[0]}",
    show_value=False,
)


def animate_update():
    # get next hour
    hour = hour_slider.value + 1
    if hour > 23:
        hour = 0
    hour_slider.value = hour


def update_hour(attr, old_hour, new_hour):
    # update data
    new_data = dict()

    # keep the same
    new_data["date"] = source.data["date"]
    new_data["res"] = source.data["res"]
    new_data["x"] = source.data["x"]
    new_data["y"] = source.data["y"]

    # new date and new pm2.5 values
    new_data["hour"] = [new_hour]
    new_data["color"] = [
        get_pm25(new_data["date"][0], new_data["hour"][0], new_data["res"][0])
    ]
    source.data = new_data


hour_slider.js_on_change(
    "value",
    CustomJS(
        args=dict(sl=hour_slider, t=t, d=curr_date),
        code="""
    console.log('hour_slider: value=' + this.value, this.toString())
    sl.title = t[this.value];
""",
    ),
)
hour_slider.on_change("value", update_hour)

callback_id = None


def animate():
    global callback_id
    if button.label == "► Play":
        button.label = "❚❚ Pause"
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = "► Play"
        curdoc().remove_periodic_callback(callback_id)


button = Button(label="► Play", width=60)
button.on_event("button_click", animate)

### resolution widget ###
res_slider = Slider(start=-19, end=0, value=default_res, step=1, title="Resolution")


# callback function to update selected resolution
def update_res(attr, old_res, new_res):
    print("Selected resolution:", new_res)
    # update data
    new_data = dict()

    # keep the same
    new_data["date"] = source.data["date"]
    new_data["hour"] = source.data["hour"]
    new_data["x"] = source.data["x"]
    new_data["y"] = source.data["y"]

    # new res and new pm2.5 values
    new_data["res"] = [new_res]
    new_data["color"] = [
        get_pm25(new_data["date"][0], new_data["hour"][0], new_data["res"][0])
    ]
    source.data = new_data


res_slider.on_change("value", update_res)

# set up the layout and add to the current document
# sizing_mode="scale_width"
layout = layout([[date_picker, res_slider], [hour_slider, button], [p]])
curdoc().add_root(layout)
curdoc().title = "UBC FireSmoke Data Curation Dashboard"
