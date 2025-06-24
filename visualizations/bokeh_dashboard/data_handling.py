# for accessing file system
import os

# for numerical work
import numpy as np

# for loading netcdf files, for metadata
import xarray as xr

# for connecting OpenVisus framework to xarray
# from https://github.com/sci-visus/openvisuspy,
from openvisuspy.xarray_backend import OpenVisusBackendEntrypoint

# Used for processing netCDF time data
import requests

# Used for indexing via metadata
import pandas as pd

# local modules
from util import *

os.environ["VISUS_CACHE"] = "./visus_cache_can_be_erased"
os.environ["CURL_CA_BUNDLE"] = ""

# whether to download tiny netcdf or not
download = True

local_netcdf = "firesmoke_metadata.nc"

if download:
    # path to tiny NetCDF
    url = "https://github.com/sci-visus/NSDF-WIRED/raw/main/data/firesmoke_metadata.nc"

    # Download the file using requests
    response = requests.get(url)
    with open(local_netcdf, "wb") as f:
        f.write(response.content)

# open tiny netcdf with xarray and OpenVisus backend
ds = xr.open_dataset(local_netcdf, engine=OpenVisusBackendEntrypoint)

##### Process all metadata of file #####
### Lat/Lon ###
# get metadata to compute lon and lat
xorig = ds.XORIG
yorig = ds.YORIG
xcell = ds.XCELL
ycell = ds.YCELL
ncols = ds.NCOLS
nrows = ds.NROWS

longitude = np.linspace(xorig, xorig + xcell * (ncols - 1), ncols)
latitude = np.linspace(yorig, yorig + ycell * (nrows - 1), nrows)

# Create coordinates for lat and lon (credit: Aashish Panta)
ds.coords["lat"] = ("ROW", latitude)
ds.coords["lon"] = ("COL", longitude)

# Replace col and row dimensions with newly calculated lon and lat arrays (credit: Aashish Panta)
ds = ds.swap_dims({"COL": "lon", "ROW": "lat"})

### Timestamps ###
# get all tflags
tflag_values = ds["TFLAG"].values

# to store pandas timestamps
timestamps = []

# convert all tflags to pandas timestamps, store in timestamps list
for tflag in tflag_values:
    timestamps.append(pd.Timestamp(parse_tflag(tflag[0])))

# set coordinates to each timestep with these pandas timestamps
ds.coords["time"] = ("time", timestamps)


##### Functions for bokeh to access data #####
def get_latslons():
    """
    Return a numpy array of all lats and lons used in dataset in mercator coordinates
    """
    # get list of latitudes and longitudes
    data_stacked_index = ds["PM25"][0].stack(lat_lon=["lat", "lon"])

    # numpy array to return
    mercator_latlons = np.zeros((np.shape(data_stacked_index)[1], 2))
    for i, tup in enumerate(latlon_to_mercator_iter(data_stacked_index.lat_lon.data)):
        mercator_latlons[i][0] = tup[0]
        mercator_latlons[i][1] = tup[1]

    return mercator_latlons


def get_pm25(date, hour, res):
    """
    Return a numpy array of pm2.5 values for all hours of given date at specified resolution
    :param string date: Date to query data for, in format "YYYY-MM-DD"
    :param int hour: Hour to query data for, from hours 0-23
    :param int res: IDX resolution to use
    """
    # make timestamp
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[-2:])
    t = get_pd_timestamp(year, month, day, hour)

    # get slice, then flatten it
    # TODO: need to handle when a date that is unavailable is given, e.g. 2021-03-03
    data_array_at_time = ds["PM25"].loc[t, :, :, res].data[:, :, 0]
    
    print(f"np.max(data_array_at_time) = {np.max(data_array_at_time)}")
    # do not flatten bc we're visualizing with bokeh's figure.image
    return data_array_at_time
