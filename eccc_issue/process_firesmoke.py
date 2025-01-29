# for numerical work
import numpy as np

# for accessing file system
import os

# for loading netcdf files, for metadata
import xarray as xr
# for connecting OpenVisus framework to xarray
# from https://github.com/sci-visus/openvisuspy, 
from openvisuspy.xarray_backend import OpenVisusBackendEntrypoint

# Used for processing netCDF time data
import time
import datetime

# Used for indexing via metadata
import pandas as pd

# Stores the OpenVisus cache in the local direcrtory 
import os
# os.environ["VISUS_CACHE"]="./visus_cache_can_be_erased"

from OpenVisus import *

def parse_tflag(tflag):
    """
    Return the tflag as a datetime object
    :param list tflag: a list of two int32, the 1st representing date and 2nd representing time
    """
    # obtain year and day of year from tflag[0] (date)
    date = int(tflag[0])
    year = date // 1000 # first 4 digits of tflag[0]
    day_of_year = date % 1000 # last 3 digits of tflag[0]

    # create datetime object representing date
    final_date = datetime.datetime(year, 1, 1) + datetime.timedelta(days=day_of_year - 1)

    # obtain hour, mins, and secs from tflag[1] (time)
    time = int(tflag[1])
    hours = time // 10000 # first 2 digits of tflag[1]
    minutes = (time % 10000) // 100 # 3rd and 4th digits of tflag[1] 
    seconds = time % 100  # last 2 digits of tflag[1]

    # create final datetime object
    full_datetime = datetime.datetime(year, final_date.month, final_date.day, hours, minutes, seconds)
    return full_datetime

def load_firesmoke_ds(path, use_chunks=False, chunk_size={'time': 1, 'resolution': 1}):
    # open tiny netcdf with xarray and OpenVisus backend
    ds = xr.open_dataset(path, engine=OpenVisusBackendEntrypoint)
    
    # Get metadata to compute lon and lat
    xorig = ds.XORIG
    yorig = ds.YORIG
    xcell = ds.XCELL
    ycell = ds.YCELL
    ncols = ds.NCOLS
    nrows = ds.NROWS

    longitude = np.linspace(xorig, xorig + xcell * (ncols - 1), ncols)
    latitude = np.linspace(yorig, yorig + ycell * (nrows - 1), nrows)
    
    # Create coordinates for lat and lon
    ds.coords['lat'] = ('ROW', latitude)
    ds.coords['lon'] = ('COL', longitude)

    # Replace col and row dimensions with newly calculated lon and lat arrays (credit: Aashish Panta)
    ds = ds.swap_dims({'COL': 'lon', 'ROW': 'lat'})
    
    # get all tflags
    tflag_values = ds['TFLAG'].values

    # to store pandas timestamps
    timestamps = []

    # convert all tflags to pandas timestamps, store in timestamps list
    for tflag in tflag_values:
        timestamps.append(pd.Timestamp(parse_tflag(tflag[0])))

    # set coordinates to each timestep with these pandas timestamps
    ds.coords['time'] = ('time', timestamps)
    
    return ds