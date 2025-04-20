# ref: https://realpython.com/python-download-file-from-url/
import requests
# ref: https://docs.python.org/3/library/logging.html
import logging
import os
import pandas as pd
from datetime import datetime
logger = logging.getLogger(__name__)

# Set up logging
# ref: https://realpython.com/python-logging/
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("june_backfill_western_download.log"),
        logging.StreamHandler()
    ]
)

# get metadata of datasets, had to be obtained manually
forecast_id = "BSC00WC04-01"
start_date = "20240625"
end_date = "20250414"
init_time = "08"
parent_dir = "/usr/sci/cedmav/data/firesmoke/download_4-14-2025/"

# try downloading all files starting the day after dataset's corresponding end date
# create directory for forecast if it doesn't exist already
os.makedirs(f"{parent_dir}{forecast_id}/", exist_ok=True)

# generate dates of interest, which is all available data for each dataset
# ref: https://stackoverflow.com/questions/59882714/python-generating-a-list-of-dates-between-two-dates
dates = pd.date_range(start=start_date, end=end_date)
dates = dates.strftime('%Y%m%d').tolist()

# download datasets in specified dates
for date in dates:
    # build URL string to download from and directory & filename to download to
    url = f"https://firesmoke.ca/forecasts/{forecast_id}/{date}{init_time}/dispersion.nc"
    directory = f"{parent_dir}{forecast_id}/dispersion_{date}.nc"

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