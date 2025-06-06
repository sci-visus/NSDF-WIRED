### Here we rename all downloaded UBC Firesmoke NetCDF files to be `dispersion_{CDATE}_{CTIME}.nc`. ###

## Import libs
import xarray as xr
import os
# ref: https://docs.python.org/3/library/logging.html
import logging

## Set up logging
# ref: https://realpython.com/python-logging/
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("/home/collab/arleth/work/NSDF-WIRED/data_download/rename_all.log"),
        logging.StreamHandler()
    ]
)

## Directories from which to get files
parent_dir = "/usr/sci/cedmav/data/firesmoke"

# subdirs that contain netcdfs to copy and rename
# for now exclude the experimental Western Canada forecasts
subdirs = [
    "BSC00CA12-01",
    "BSC06CA12-01",
    "BSC12CA12-01",
    "BSC18CA12-01",
    # "BSC00WC04-01",
    "download_4-14-2025/BSC00CA12-01",
    "download_4-14-2025/BSC06CA12-01",
    "download_4-14-2025/BSC12CA12-01",
    "download_4-14-2025/BSC18CA12-01",
    # "download_4-14-2025/BSC00WC04-01",
    "download_5-19-2025/BSC00CA12-01",
    "download_5-19-2025/BSC06CA12-01",
    "download_5-19-2025/BSC12CA12-01",
    "download_5-19-2025/BSC18CA12-01",
    # "download_5-19-2025/BSC00WC04-01",
    # "daily_downloads/BSC00WC04-01"
]


# to store all renamed files
union_set_dir = f'{parent_dir}/union_set'

for subdir in subdirs:
    curr_dir = f'{parent_dir}/{subdir}'
    # get list of files in current directory
    file_names = sorted(os.listdir(curr_dir))

    # save each file in the union_set_dir
    for file_name in file_names:
        file = f'{curr_dir}/{file_name}'
        ds = xr.open_dataset(file)
        ds_CDATE = ds.CDATE
        ds_CTIME = ds.CTIME

        # save to union_set_dir
        ds.to_netcdf(f"{parent_dir}/union_set/dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")
        logging.info(f"Saved {file} to {union_set_dir} as dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")