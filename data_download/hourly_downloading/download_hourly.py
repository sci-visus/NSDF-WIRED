# ref: https://realpython.com/python-download-file-from-url/
import requests
# ref: https://docs.python.org/3/library/logging.html
import logging
import os
import pandas as pd
import xarray as xr
from datetime import datetime, timedelta
import os
logger = logging.getLogger(__name__)

# Set up logging
# ref: https://realpython.com/python-logging/
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("/home/arleth/NSDF-WIRED/data_download/hourly_downloading/firesmoke_hourly_download.log"), ## TODO: Make more portable
        logging.StreamHandler()
    ]
)

## Define paths and URLs
# URL from which to download
url = "https://firesmoke.ca/forecasts/current/dispersion.nc"

# Directories for verifying and storing downloads
## TODO: Make more portable
tmp_dir = "/opt/wired-data/firesmoke/hourly_downloads/tmp"
final_dir = "/opt/wired-data/firesmoke/hourly_downloads/data"

## Gets latest file from final_dir
def get_latest_file():
    ret_name = ''
    file_names = sorted(os.listdir(final_dir))
    try:
        ret_name = file_names[-1]
    except:
        print('file_names[-1] in get_latest_file() failed')
    return ret_name

## Download from URL
# request from download URL
response = requests.get(url, stream=True)

# get response header
header = response.headers
# download file if we see 'save as' content type
# ref: https://stackoverflow.com/questions/20508788/do-i-need-content-type-application-octet-stream-for-file-download
if 'Content-Type' in header and header['Content-Type'] == 'application/octet-stream':
    with open(f'{tmp_dir}/dispersion.nc', mode="wb") as file:
        file.write(response.content)
        logging.info(f"Success: {url} -> {tmp_dir}")
else: #otherwise inspect header's Content-Type
    logging.error(f"Failed: {url} -> {tmp_dir} | Header Content-Type: {header['Content-Type']}")

## Verify we have a new file
# if get_latest_file fails i.e. we have nothing in our final_dir, save the netcdf
ds = xr.open_dataset(f'{tmp_dir}/dispersion.nc')
ds_CDATE = ds.CDATE
ds_CTIME = ds.CTIME
try:
    # open the NetCDF and check if we have already downloaded it 
    # by comparing creation timestamps to the most recently downloaded dispersion.nc in final_dir
    ds_last = xr.open_dataset(f'{final_dir}/{get_latest_file()}')
    ds_last_CDATE = ds_last.CDATE
    ds_last_CTIME = ds_last.CTIME

    # Convert to datetime objects, ensure it's zero-padded to be 6 digits
    dt_downloaded = datetime.strptime(f"{ds_CDATE}{ds_CTIME:06}", "%Y%j%H%M%S")
    dt_last = datetime.strptime(f"{ds_last_CDATE}{ds_last_CTIME:06}", "%Y%j%H%M%S")

    # If dt_last is younger save the dispersion.nc file as 'dispersion_{ds_CDATE}{ds_CTIME}.nc' in final_dir
    if dt_last < dt_downloaded:
        ds.to_netcdf(f"{final_dir}/dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")
        logging.info(f"Saved to {final_dir} as dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")
    else:
        logging.info(f"Already have file saved in {final_dir} as dispersion_{ds_CDATE}_{ds_CTIME}.nc")
except IndexError as e:
    ds.to_netcdf(f"{final_dir}/dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")
    logging.error(f"Exception {e}")
    logging.info(f"Saved to {final_dir} as dispersion_{ds_CDATE}_{ds_CTIME:06}.nc")