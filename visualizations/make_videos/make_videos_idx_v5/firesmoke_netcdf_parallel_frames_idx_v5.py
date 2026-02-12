#!/usr/bin/env python
# coding: utf-8

# # Create .PNG images of all timesteps from `idx_calls` loading from netCDF files
# 

# ## Import necessary libraries

# In[18]:


# to parallelize frame creation for timesteps
import multiprocessing

# for numerical work
import numpy as np

# for accessing file system
import os

# for loading netcdf files, for metadata
import xarray as xr

# Used for processing netCDF time data
import time
import datetime

# Used for indexing via metadata
import pandas as pd

# for plotting
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# for exporting the dictionary of issue files at the end of notebook
import pickle

# Accessory, used to generate progress bar for running for loops
# from tqdm.notebook import tqdm
# import ipywidgets
# import jupyterlab_widgets
from tqdm import tqdm


# ## Get path to original firesmoke data

# In[19]:


# ******* THIS IS WHEN RUNNING FROM canada1 **************
# directory to all netCDF firesmoke data
netcdf_dir =  "/opt/wired-data/firesmoke/final_union_set"


# ### In this section, we load metadata from 381x1041 and 381x1081 files using `xr.open_dataset`.

# In[20]:


# path to small and big files
file_s = f'{netcdf_dir}/dispersion_2021059_025055.nc'
file_b = f'{netcdf_dir}/dispersion_2025316_214651.nc'

# open check out metadata of each file
ds_s = xr.open_dataset(file_s)
ds_b = xr.open_dataset(file_b)


# In[21]:


ds_s


# In[22]:


ds_b


# ## Calculate derived metadata using original metadata above to create coordinates
# ### We'll use this for creating our visualizations

# #### Calculate latitude and longitude grid for each set of files' metadata

# In[23]:


# Get metadata to compute lon and lat
longitude_s = np.linspace(ds_s.XORIG, ds_s.XORIG + ds_s.XCELL * (ds_s.NCOLS - 1), ds_s.NCOLS)
latitude_s = np.linspace(ds_s.YORIG, ds_s.YORIG + ds_s.YCELL * (ds_s.NROWS - 1), ds_s.NROWS)

longitude_b = np.linspace(ds_b.XORIG, ds_b.XORIG + ds_b.XCELL * (ds_b.NCOLS - 1), ds_b.NCOLS)
latitude_b = np.linspace(ds_b.YORIG, ds_b.YORIG + ds_b.YCELL * (ds_b.NROWS - 1), ds_b.NROWS)


# #### The timestamps used in the files may not be intuitive. The following utility function returns the desired pandas timestamp based on your date and time of interest. 
# 
# ##### When you index the data at a desired time, use this function to get the timestamp you need to index.

# In[24]:


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


# In[25]:


def get_timestamp(year, month, day, hour):
    """
    return a pandas timestamp using the given date-time arguments
    :param int year: year
    :param int month: month
    :param int day: day
    :param int hour: hour
    """
    # Convert year, month, day, and hour to a datetime object
    full_datetime = datetime.datetime(year, month, day, hour)
    
    # Extract components from the datetime object
    year = full_datetime.year
    day_of_year = full_datetime.timetuple().tm_yday
    hours = full_datetime.hour
    minutes = full_datetime.minute
    seconds = full_datetime.second

    # Compute tflag[0] and tflag[1]
    tflag0 = year * 1000 + day_of_year
    tflag1 = hours * 10000 + minutes * 100 + seconds

    # Return the Pandas Timestamp object
    return pd.Timestamp(full_datetime)


# ## Import sequence of data slices to get at what time step

# In[26]:


# Load idx_calls from file
with open('idx_calls_v5.pkl', 'rb') as f:
    idx_calls = pickle.load(f)

print(f"there's {len(idx_calls)} frames to make")

for c in np.arange(len(idx_calls)):
    idx_calls[c].append(c)


# In[27]:


idx_calls[900]


# ## Create the frames

# In[28]:


# directory to save frames
folder = "/opt/wired-data/firesmoke_video_pngs/netcdf_frames"

# set parameters for creating visualization of each timestep with matplotlib
my_norm = "log"
my_extent_s = [np.min(longitude_s), np.max(longitude_s), np.min(latitude_s), np.max(latitude_s)]
my_extent_b = [np.min(longitude_b), np.max(longitude_b), np.min(latitude_b), np.max(latitude_b)]
my_aspect = 'auto'
my_origin = 'lower'
my_cmap = 'hot'

# to keep track of files that fail to visualized into .PNG
issue_files = {}


# In[ ]:


def create_frame_from_call(call):
    # get instructions from call:
    # [file name to open, timestamp, TSTEP index to select]
    file_name = call[0]
    timestamp = call[1]
    tstep_index = call[2]
    frame_num = call[3]

    # create visualization using matplotlib and cartopy geography lines, 
    # open the current file with xarray
    ds = xr.open_dataset(f'{netcdf_dir}/{file_name}')

    # Get the PM25 values, squeeze out empty axis
    ds_vals = np.squeeze(ds['PM25'].values)

    # get pm25 values at tstep_index and visualize them
    data_at_time = ds_vals[tstep_index]

    # catch exceptions accordingly
    try:
        my_fig, my_plt = plt.subplots(figsize=(15, 6), subplot_kw=dict(projection=ccrs.PlateCarree()))
        # extent is either with the 381x1041 lons/lats or 381x1081 lons/lats
        curr_extent = my_extent_s if ds['PM25'].shape[3] == 1041 else my_extent_b
        plot = my_plt.imshow(data_at_time, norm=my_norm, extent=curr_extent, aspect=my_aspect, origin=my_origin, cmap=my_cmap)
        my_fig.colorbar(plot,location='right', label='ug/m^3')
        my_plt.coastlines()
        my_plt.gridlines(draw_labels=True)
        # add a title with the time information
        my_fig.suptitle(f'Ground Level Concentration of PM2.5 Microns and Smaller\n{timestamp}')
        
        # add an additional caption for context
        my_plt.text(0.5, -0.1, 'Original NetCDF Data', ha='center', va='center', transform=my_plt.transAxes)
        
        # save the visualization as a frame
        save_path = f"{folder}/frames%06d.png" % frame_num
        plt.savefig(save_path, dpi=280)

        plt.close(my_fig);  # Close the figure after saving
        # plt.show()
        matplotlib.pyplot.close()
    except: # return key and value to add to our issues dictionary
        print(f"issue! {timestamp}")
        return timestamp, data_at_time


# In[ ]:


# create frames, capturing issues 
with multiprocessing.Pool() as pool:
   # Start a timer to measure how long the conversion takes
   start_time = time.time()
   print('starting')
   issues = pool.map(create_frame_from_call, idx_calls)
   print('done!')
   # End the timer and print the elapsed time
   end_time = time.time()
   print(f'Total elapsed time: {end_time - start_time}')


# In[ ]:


issues


# In[ ]:


# save 'issue_files' to review
with open('netcdf_issues_v5.pkl', 'wb') as f:
    pickle.dump(issue_files, f)


# In[ ]:


with open('netcdf_issues_v5.pkl', 'rb') as f:
    new_netcdf_issues = pickle.load(f)
print(f'len of new_netcdf_issues.pkl = {len(new_netcdf_issues)}')

