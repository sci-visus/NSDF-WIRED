# imports for data handling and utility functions
from data_handling import *
from util import *
from datetime import timedelta
import pandas as pd

# imports for visualization
from bokeh.layouts import layout
import xyzservices.providers as xyz
from bokeh.plotting import figure, curdoc
from bokeh.models import LogColorMapper
from bokeh.models import (
    DatePicker,
    Slider,
    ColumnDataSource,
    Button,
    Toggle,
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
# get shape of pm25 data, to reshape x and y in ColumnDataSource
rows, cols = np.shape(default_pm25_vals)
source = ColumnDataSource(
    data=dict(
        image=[default_pm25_vals],
    )
)

##### Init bokeh figure #####
# create a plot centering in north america
min_coords = latlon_to_mercator(32, -160)
max_coords = latlon_to_mercator(71, -51)

# create figure using lat/lon of dataset
p = figure(
    x_range=(min_coords[0], max_coords[0]),
    y_range=(min_coords[1], max_coords[1]),
    x_axis_type="mercator",
    y_axis_type="mercator",
)

# add map tiles
p.add_tile(xyz.OpenStreetMap.Mapnik)

# create log color map
cmap = LogColorMapper(
    # using 'Oranges' from: https://observablehq.com/@d3/color-schemes
    palette=["#fff5eb00","#fdd8b3","#fdc28c","#fda762","#fb8d3d","#f2701d","#e25609","#c44103","#9f3303","#7f2704"],
    low=0.0001,
    high=np.nanmax(source.data["image"][0].flatten())
)

# initialize image raster visualization on figure
p.image(
    "image",
    source=source,
    x=min_coords[0],
    y=min_coords[1],
    dw=max_coords[0] - min_coords[0],
    dh=max_coords[1] - min_coords[1],
    color_mapper=cmap,
    alpha=.8 # so the map tile is visible underneath
)

##### Widgets #####
### datepicker widget ###
date_picker = DatePicker(
    title="Select date",
    value=default_date,
    min_date="2021-03-04",  # earliest available forecast
    max_date="2024-06-27",  # last time we downloaded forecast
)
### hour widget ###
# refs:
#   https://github.com/bokeh/bokeh/blob/branch-3.8/examples/server/app/gapminder/main.py
#   https://discourse.bokeh.org/t/a-simple-way-to-custom-a-slider-as-a-dateslider/10005
# hour slider shows hours for currently selected date
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
### resolution widget ###
res_slider = Slider(start=-19, end=0, value=default_res, step=1, title="Resolution")

# callback function to update selected data on new date
def update_data(attrname, old, new):
    # create new dict to update source in 1 step
    new_data = dict()

    # new date and new pm2.5 values
    new_data["image"] = [get_pm25(date_picker.value, hour_slider.value, res_slider.value)]
    source.data = new_data

def animate_update():
    # get next hour
    hour = hour_slider.value + 1
    if hour > 23:
        hour = 0
    hour_slider.value = hour

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

callback_id = None

def animate():
    global callback_id
    if toggle.active == True:
        callback_id = curdoc().add_periodic_callback(animate_update, 600)
    else:
        curdoc().remove_periodic_callback(callback_id)


# button = Button(label="► Play", width=60)
# button.on_event("button_click", animate)
toggle = Toggle(label="►/❚❚", button_type="default", width=60)
toggle.on_event('button_click', animate)

# when date selected changes, call update_date
for w in [date_picker, hour_slider, res_slider]:
    w.on_change('value', update_data)

# set up the layout and add to the current document
# sizing_mode="scale_width"
layout = layout([[date_picker, res_slider], [hour_slider, toggle], [p]])
curdoc().add_root(layout)
curdoc().title = "UBC FireSmoke Data Curation Dashboard"
