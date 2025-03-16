# imports for data handling
from data_handling import *

# imports for visualization
import xyzservices.providers as xyz
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from bokeh.models import CustomJS, DatePicker, Slider, ColumnDataSource

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

##### Init ColumnDataSource #####
# Create a ColumnDataSource for the data
# for now, we use all latitudes and longitudes
default_res = 0
default_date = "2021-03-04"
latslons = get_latslons()
default_lats = latslons[:, 0]
default_lons = latslons[:, 1]
default_pm25_vals = get_pm25(default_date, default_res)

source = ColumnDataSource(
    data=dict(
        date=[default_date],
        res=[default_res],
        lat=[default_lats],
        lon=[default_lons],
        pm25_vals=[default_pm25_vals],
    )
)

##### Widgets #####
### datepicker widget ###
date_picker = DatePicker(
    title="Select date",
    value="2021-03-03",
    min_date="2021-03-04",
    max_date="2024-06-27",
)


# callback function to update selected data on new date
def update_date(attr, old_date, new_date):
    print("Selected date:", new_date)
    # update data
    new_data = dict()

    # keep the same
    new_data["res"] = source.data["res"]
    new_data["lat"] = source.data["lat"]
    new_data["lon"] = source.data["lon"]

    # new date and new pm2.5 values
    new_data["date"] = [new_date]
    new_data["pm25_vals"] = [get_pm25(new_date, new_data["res"])]
    source.data = new_data


# when date selected changes, call update_date
date_picker.on_change("value", update_date)

### resolution widget ###
res_picker = Slider(start=-19, end=0, value=0, step=1, title="Resolution")


# callback function to update selected resolution
def update_res(attr, old_res, new_res):
    print("Selected resolution:", new_res)
    # update data
    new_data = source.data
    new_data["res"] = new_res
    new_data["pm25_vals"] = get_pm25(new_data["date"], new_res)


res_picker.on_change("value", update_res)

# set up the layout and add to the current document
layout = row(column(date_picker, res_picker), p)
curdoc().add_root(layout)
