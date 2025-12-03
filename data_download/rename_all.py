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
        logging.FileHandler("/home/arleth/NSDF-WIRED/data_download/rename_all.log"),
        logging.StreamHandler()
    ]
)

## Directories from which to get files
parent_dir = "/opt/wired-data/firesmoke"

# subdirs that contain netcdfs to copy and rename
# for now exclude the experimental Western Canada forecasts
subdirs = [
    "stop_gapBSC00CA12-05",
    "stop_gapBSC06CA12-05",
    "stop_gapBSC12CA12-05",
    "stop_gapBSC18CA12-05",
]


# to store all renamed files
tmp_dir = f'{parent_dir}/tmp'

for subdir in subdirs:
    curr_dir = f'{parent_dir}/{subdir}'
    # get list of files in curr_dir
    file_names = sorted(os.listdir(curr_dir))

    # ensure subdir exists in tmp_dir
    target_subdir = f"{tmp_dir}/{subdir}"
    os.makedirs(target_subdir, exist_ok=True)

    # save each file in curr_dir
    for file_name in file_names:
        file = f'{curr_dir}/{file_name}'
        ds = xr.open_dataset(file)
        ds_CDATE = ds.CDATE
        ds_CTIME = ds.CTIME

        # save to tmp_dir/subdir
        target_path = f"{target_subdir}/dispersion_{ds_CDATE}_{ds_CTIME:06}.nc"
        ds.to_netcdf(target_path)
        logging.info(f"Saved {file} to {target_subdir} as dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")