# ref: https://realpython.com/python-download-file-from-url/
import requests
# ref: https://docs.python.org/3/library/logging.html
import logging
import os
import pandas as pd
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)

# Set up logging
# ref: https://realpython.com/python-logging/
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("/home/collab/arleth/work/NSDF-WIRED/data_download/daily_downloading/firesmoke_daily_download.log"),
        logging.StreamHandler()
    ]
)

# get metadata of datasets, had to be obtained manually
ids = ["BSC18CA12-01", "BSC00CA12-01", "BSC06CA12-01", "BSC12CA12-01", "BSC00WC04-01"]
init_times = ["02", "08", "14", "20", "08"]
parent_dir = "/usr/sci/cedmav/data/firesmoke/daily_downloads/"
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

for forecast_id, init_time in zip(ids, init_times):
    # create directory for forecast if it doesn't exist already
    os.makedirs(f"{parent_dir}{forecast_id}/", exist_ok=True)

    # build URL string to download from and directory & filename to download to
    # name the downloaded files starting the day after dataset's corresponding end date
    url = f"https://firesmoke.ca/forecasts/{forecast_id}/{yesterday}{init_time}/dispersion.nc"
    directory = f"{parent_dir}{forecast_id}/dispersion_{yesterday}.nc"
    
    # request from download URL
    response = requests.get(url, stream=True)
    # get response header
    header = response.headers
    # download file if we see 'save as' content type
    # ref: https://stackoverflow.com/questions/20508788/do-i-need-content-type-application-octet-stream-for-file-download
    if 'Content-Type' in header and header['Content-Type'] == 'application/octet-stream':
        with open(directory, mode="wb") as file:
            file.write(response.content)
            logging.info(f"Success: {url} -> {directory}")
    else: #otherwise inspect header's Content-Type
        logging.error(f"Failed: {url} -> {directory} | Header Content-Type: {header['Content-Type']}")
